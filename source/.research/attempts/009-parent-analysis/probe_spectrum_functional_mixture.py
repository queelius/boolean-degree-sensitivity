"""Diagnostic exact mixtures on common, independently propagated case domains.

This producer never accepts an exclusion. Source certificates are checked
again against rebuilt rows; extending their scores requires a separate audit.
"""
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from time import monotonic
import gc
import json
import resource
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate, write_certificate
from first_case_spectrum_scope import CaseScope, input_scope
from core_slice_degree_lp import PatternBlock
from selfdual_core_projection import ProjectedCoefficient
from bounded_core_spectrum_lp import CoefficientTotal, prepare
from primitive_box_rows import primitive_row
from spectrum_dual_functional import compile_functional, lift_multipliers, simplex_bound
from simplex_functional_mixture import SimplexScores, mixture_grid
from matched_component_frontier import guarded_words
from read_matched_cross_arrays import load

H = Path(__file__).resolve().parent


@dataclass
class Source:
    functional: object
    flags: tuple
    flag_keys: tuple
    coordinates: dict
    report: dict


def source_functional(b, path):
    authority = b.read(path)
    assert authority['exact_certificate_verified']
    assert authority['result_status'] == 'EXACT_BOX_ROW_LP_CONTRADICTION'
    assert authority['exact_integer_rhs'] < 0
    kind = authority['status']
    if kind == 'INDEPENDENTLY_VERIFIED_FIRST_CASE_FULL_SPECTRUM_MODEL':
        scope = CaseScope.from_data(authority['scope'])
        assert authority['whole_first_case_excluded']
        ref = authority['input_authority']
        assert input_scope(b.read(ref['path'], ref['sha256'])) == scope
        ref = authority['model_source']; model_source = b.read(ref['path'], ref['sha256'])
        model_proof = read_certificate(b, model_source['proof'])
        ref = authority['run_source']; run_source = b.read(ref['path'], ref['sha256'])
        run_proof = read_certificate(b, run_source['proof'])
        assert run_source['model_source'] == authority['model_source']
        assert run_source['scope'] == model_source['scope'] == scope.to_data()
        divisors = model_proof['divisors']
        geometry_index, quotient = scope.geometry_index, scope.to_data()['quotient_authority']
        source_scope = scope.to_data()
    elif kind == 'INDEPENDENTLY_VERIFIED_PRIMITIVE_FULL_OUTSIDE_SPECTRUM_LP_MODEL':
        assert authority['conditional_product_group_excluded']
        ref = authority['source']; run_source = b.read(ref['path'], ref['sha256'])
        run_proof = read_certificate(b, run_source['proof'])
        ref = run_source['original_model']; model_source = b.read(ref['path'], ref['sha256'])
        model_proof = read_certificate(b, model_source['proof'])
        divisors = run_proof['divisors']
        geometry_index = authority['geometry_index']
        source_scope = dict(kind='conditional_product_group', geometry_index=geometry_index,
                            first_row=authority['first_row'], group_index=authority['group_index'])
        quotient = None
    else:
        raise ValueError('Unsupported exact source authority.')
    assert model_proof['include_moments'] is True
    ref = authority['input_source']; inputs = b.read(ref['path'], ref['sha256'])
    p = read_certificate(b, inputs['proof'])
    assert model_source['input_source'] == authority['input_source']
    if quotient is None:
        quotient = inputs['quotient_authority']
    blocks = []
    for record in p['blocks']:
        ref = record['values']; b.bind(ref['path'], ref['sha256'])
        values = np.load(ref['path'], allow_pickle=False)
        assert list(values.shape) == ref['shape'] and str(values.dtype) == ref['dtype']
        blocks.append(PatternBlock(tuple(record['features']), values))
    coefficients = [ProjectedCoefficient(c['feature'], c['character'], c['support'], tuple(c['values']))
                    for c in p['projected_coefficients']]
    totals = [CoefficientTotal(tuple(t['supports']), t['target']) for t in model_proof['totals']]
    model = prepare(p['word_pools'], blocks, coefficients, totals=totals, include_moments=True)
    rows = list(model.rows())
    assert model.coefficient_records() == model_proof['coefficients']
    assert model.base.partition_records() == model_proof['partitions']
    assert len(rows) == len(divisors)
    saved_matrix = (read_certificate(b, model_proof['primitive_matrix'])
                    if 'primitive_matrix' in model_proof else None)
    if saved_matrix is not None:
        assert len(saved_matrix) == len(rows)
    for i, (row, divisor) in enumerate(zip(rows, divisors)):
        normalized, actual = primitive_row(row)
        assert actual == divisor
        if saved_matrix is not None:
            assert saved_matrix[i] == [normalized.lower, normalized.upper,
                                      [[j, a] for j, a in sorted(normalized.terms)]]
    del saved_matrix
    certificate = run_proof['result']['certificate']
    assert certificate['integer_rhs'] == authority['exact_integer_rhs']
    scale, weights = lift_multipliers(divisors, certificate['terms'])
    functional = compile_functional(rows, model.variable_count, weights)
    residual = list(functional.coefficients); rhs = functional.rhs
    for j, sign, multiplier in certificate['box_terms']:
        assert type(j) is int and 0 <= j < len(residual)
        assert sign in (-1, 1) and type(multiplier) is int and multiplier > 0
        residual[j] += scale * sign * multiplier
        if sign == 1:
            rhs += scale * multiplier
    assert not any(residual) and rhs == scale * certificate['integer_rhs'] < 0
    base = model.base.basis.base; word_costs = [[] for _ in p['word_pools']]
    for i, variable in enumerate(model.variables[:base.word_variable_count]):
        cost = functional.word_score(variable['outside_point'], variable['features'])
        assert cost == functional.coefficients[i]
        word_costs[variable['outside_point']].append(cost)
    pattern_costs = []
    for block, (record, offset) in enumerate(zip(blocks, base.block_offsets)):
        costs = functional.pattern_scores(block, record.values, record.features)
        assert list(map(int, costs)) == list(functional.coefficients[offset:offset+len(costs)])
        pattern_costs.append(costs)
    flag_pairs = [(variable, functional.coefficients[i]) for i, variable in enumerate(model.variables)
                  if variable['kind'] == 'full_spectral_flag']
    flags = tuple(cost for _, cost in flag_pairs)
    flag_keys = tuple((v['feature'], v['character'], v['support'], tuple(v['values'])) for v, _ in flag_pairs)
    original = simplex_bound(word_costs + pattern_costs, flags, functional.rhs)
    assert original['contradiction'] and original['gap'] >= -scale * authority['exact_integer_rhs']
    coordinates = dict(geometry_index=geometry_index, quotient=quotient, geometry=p['geometry'],
                       outside=p['outside'], points=len(p['word_pools']),
                       coefficient_domains=sorted((c.feature, c.character, c.support, c.values) for c in coefficients),
                       totals=model_proof['totals'])
    report = dict(authority=b.bind(path), source_scope=source_scope, scale=scale,
                  rows=len(rows), columns=model.variable_count, original_bound=original,
                  exact_integer_rhs=certificate['integer_rhs'], original_rows_divisors_and_columns_rechecked=True,
                  original_certificate_rechecked=True, row_weights=list(weights))
    return Source(functional, flags, flag_keys, coordinates, report)


def score_case(sources, tables, domains, features, pools):
    values = [table[domain, :len(pools)] for table, domain in zip(tables, domains)]
    for table, domain in zip(tables, domains):
        assert domain and len(domain) == len(set(domain))
        assert all(type(i) is int and 0 <= i < len(table) for i in domain)
    word_indices = []; selected_words = []
    for point, words in enumerate(pools):
        allowed = [set(map(int, v[:, point])) for v in values]
        indices = [i for i, word in enumerate(words)
                   if all(word[f] in unary for f, unary in zip(features, allowed))]
        assert indices, 'Empty pool needs its own independently checked domain contradiction.'
        word_indices.append(indices)
        selected_words.append([words[i] for i in indices])
    systems = []
    for source in sources:
        f = source.functional
        groups = [tuple(f.word_score(x, word) for word in words) for x, words in enumerate(selected_words)]
        groups.extend(tuple(map(int, f.pattern_scores(j, v[:, :, None], (feature,))))
                      for j, (v, feature) in enumerate(zip(values, features)))
        systems.append(SimplexScores(tuple(groups), source.flags, f.rhs))
    return systems, word_indices


def run(args):
    start = monotonic(); assert not args.output.exists()
    resource.setrlimit(resource.RLIMIT_AS, (args.memory_mib << 20, args.memory_mib << 20))
    b = Bindings(); sources = []
    for path in args.authorities:
        source = source_functional(b, path); sources.append(source); gc.collect()
        print(json.dumps(dict(stage='source_rechecked',authority=source.report['authority'],
                              original_gap=source.report['original_bound']['gap'],seconds=monotonic()-start)),flush=True)
    assert len(sources) == 2 and sources[0].coordinates == sources[1].coordinates
    assert sources[0].flag_keys == sources[1].flag_keys
    assert sources[0].report['scale'] == sources[1].report['scale']
    coordinates = sources[0].coordinates
    frontier = b.read(args.frontier)
    assert frontier['status'] == 'VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER'
    assert frontier['scope']['geometry_index'] == coordinates['geometry_index']
    assert frontier['scope']['quotient_authority'] == coordinates['quotient']
    assert args.first_rows and len(args.first_rows) == len(set(args.first_rows))
    assert set(args.first_rows) <= set(frontier['remaining_first_rows'])
    selected = {}; refinement = None
    for path in args.propagation_authorities:
        prop = b.read(path)
        assert prop['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_WHOLE_FAMILY_DELETIONS'
        assert prop['geometry_index'] == coordinates['geometry_index']
        assert prop['quotient_authority'] == coordinates['quotient']
        if refinement is None:
            refinement = prop['refinement_authority']
        assert prop['refinement_authority'] == refinement
        ref = prop['source']; produced = b.read(ref['path'], ref['sha256'])
        assert produced['refinement_authority'] == refinement
        assert [r['first_row'] for r in prop['records']] == [r['first_row'] for r in produced['records']]
        for accepted, record in zip(prop['records'], produced['records']):
            first = record['first_row']
            if first not in args.first_rows:
                continue
            assert first not in selected and not accepted['conditional_case_excluded']
            proof = read_certificate(b, record['proof'])
            assert proof['first_row'] == first
            assert list(map(len, proof['final_domains'])) == accepted['final_domain_sizes']
            selected[first] = (b.bind(path), record['proof'], proof)
    assert set(selected) == set(args.first_rows)
    data = load(b, refinement['path']); assert b.bind(refinement['path']) == refinement
    assert data.quotient_reference == coordinates['quotient']
    instance = read_certificate(b, data.quota['instance'])
    assert instance['geometry'] == coordinates['geometry'] and instance['outside'] == coordinates['outside']
    points = coordinates['points']; assert points == 512
    pools = [guarded_words(x.bit_count(), 1-(x&1)-((x>>1)&1)) for x in range(points)]
    endpoints = {}
    for path in args.endpoint_diagnostics:
        diagnostic = b.read(path)
        assert diagnostic['status'] in ('PROPOSED_PROPAGATED_SPECTRUM_DUAL_EXTENSION',
                                         'PROPOSED_COMPLETE_FIRST_CASE_SPECTRUM_TRANSFER')
        authority = diagnostic.get('dual_authority', diagnostic.get('exact_authority'))
        for record in diagnostic['records']:
            endpoints[(authority['path'], record['first_row'])] = record['after_gap']
    records = []
    for first in args.first_rows:
        prop_ref, proof_ref, proof = selected[first]
        candidate = data.quota['selected_row_indices'].index(first)
        assert proof['parent_candidate_index'] == candidate
        domains = proof['final_domains']
        assert domains[data.quota['component_index']] == [candidate]
        systems, word_indices = score_case(sources, data.tables, domains, instance['core_pair_order'], pools)
        grid = mixture_grid(*systems, args.denominator)
        for source, record in zip(sources, (grid[0], grid[-1])):
            assert record['bound']['gap'] == args.denominator * endpoints[(source.report['authority']['path'], first)]
        best = max(grid, key=lambda r: r['bound']['gap'])
        records.append(dict(first_row=first, propagation_authority=prop_ref, domain_proof=proof_ref,
                            retained_domains=domains, retained_word_indices=word_indices,
                            score_systems=[dict(groups=s.groups, flags=s.flags, rhs=s.rhs) for s in systems],
                            grid=grid, best=best))
        print(json.dumps(dict(stage='mixture_grid',first_row=first,best_right_weight=best['right_weight'],
                              denominator=args.denominator,best_gap_numerator=best['bound']['gap'],
                              candidate_contradiction=best['bound']['contradiction'],seconds=monotonic()-start)),flush=True)
    proof_path = args.output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(sources=[s.report for s in sources],coordinates=coordinates,
                                     flag_keys=sources[0].flag_keys,records=records))
    for name in ('probe_spectrum_functional_mixture.py','simplex_functional_mixture.py',
                 'test_simplex_functional_mixture.py','spectrum_dual_functional.py',
                 'propagated_spectrum_minimum.py','matched_component_frontier.py'):
        b.bind(H/name)
    result = dict(schema_version=1,status='PROPOSED_SPECTRUM_FUNCTIONAL_MIXTURE',global_status='UNRESOLVED',
                  proof=b.bind(proof_path),authorities=[s.report['authority'] for s in sources],
                  frontier_authority=b.bind(args.frontier),source_case_word_filters_transferred=False,
                  extended_score_independent_audit='PENDING',endpoint_diagnostics_reproduced=True,
                  records=[dict(first_row=r['first_row'],best_right_weight=r['best']['right_weight'],
                                denominator=args.denominator,best_gap_numerator=r['best']['bound']['gap'],
                                candidate_contradiction=r['best']['bound']['contradiction']) for r in records],
                  candidate_excluded_first_rows=[r['first_row'] for r in records if r['best']['bound']['contradiction']],
                  whole_geometry_excluded=False,global_goal_complete=False,
                  parameters=dict(denominator=args.denominator,memory_mib=args.memory_mib),
                  seconds=monotonic()-start,process_peak_resident_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with args.output.open('x') as stream:
        json.dump(result,stream,indent=2); stream.write('\n')
    print(json.dumps(dict(status=result['status'],records=result['records'],seconds=result['seconds'])),flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__)
    p.add_argument('--authorities',type=Path,nargs=2,required=True)
    p.add_argument('--frontier',type=Path,required=True)
    p.add_argument('--propagation-authorities',type=Path,nargs='+',required=True)
    p.add_argument('--endpoint-diagnostics',type=Path,nargs='+',required=True)
    p.add_argument('--first-rows',type=int,nargs='+',required=True)
    p.add_argument('--denominator',type=int,default=64)
    p.add_argument('--memory-mib',type=int,default=4096)
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
