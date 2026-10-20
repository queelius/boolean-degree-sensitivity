"""Independent Fourier-average counts and exhaustive added-relation verification."""
from argparse import ArgumentParser
from itertools import product
from pathlib import Path
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate

H = Path(__file__).resolve().parent


def run(source_path, output):
    assert not output.exists(); b = Bindings(); source = b.read(source_path)
    assert source['status'] == 'PROPOSED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT'
    authority = b.read(source['base_authority']['path'], source['base_authority']['sha256'])
    assert authority['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and authority['complete_actual_cover'] is True
    instance = read_certificate(b, authority['instance']); proof = read_certificate(b, source['proof'])
    assert proof['base_authority'] == source['base_authority'] and proof['geometry_index'] == authority['geometry_index'] == source['geometry_index']
    geometry = authority['geometry']; positives = [{i for i in range(14) if q >> i & 1} for q in geometry['positive_doubles']]
    core = sorted(positives[0] & positives[1]); negative = [{i for i in range(14) if q >> i & 1} for q in geometry['negative_supports']]
    one_core = [sum(n & set(core) == {v} for n in negative) for v in core]
    assert proof['negative_singleton_core_counts'] == one_core
    assert proof['incident_linear_count_caps'] == [16 if n == 0 else 20 for n in one_core]
    assert proof['core_pair_order'] == instance['core_pair_order']
    assert [r['component_index'] for r in proof['columns']] == list(range(6))
    weights = np.array([sum(1-2*((x >> i) & 1) for i in range(10)) for x in range(1024)], dtype=np.int32)
    choices = []; frequencies = []; checked = 0
    for j, (column, component) in enumerate(zip(proof['columns'], instance['components'])):
        values = np.load(component['values']['path'], allow_pickle=False)
        if j == authority['component_index']: values = np.stack([values[i] for i in authority['selected_row_indices']])
        numerator = -(values.astype(np.int32) @ weights)
        assert np.all(numerator % 1024 == 0)
        counts = numerator//1024
        claimed = np.load(column['counts']['path'], allow_pickle=False)
        assert claimed.dtype == np.int8 and claimed.shape == counts.shape and np.array_equal(claimed, counts)
        assert len(counts) == column['candidates'] and all(int(q) in range(0, 11, 2) for q in counts)
        values_q, multiplicities = np.unique(counts, return_counts=True)
        choice = list(map(int, values_q)); assert choice == column['values']; choices.append(choice)
        frequencies.append(dict(zip(choice, map(int, multiplicities)))); checked += len(counts)
    expected = []; total_mass = live_mass = 0; total_count = 0
    for row in product(*choices):
        total_count += 1; multiplicity = 1
        for j, q in enumerate(row): multiplicity *= frequencies[j][q]
        total_mass += multiplicity
        ell = [10-sum(row[j] for j, p in enumerate(instance['core_pair_order']) if p >> i & 1)//2 for i in range(4)]
        if all(e >= (2 if n == 0 else 0) for e, n in zip(ell, one_core)):
            expected.append(list(row)); live_mass += multiplicity
    assert expected == proof['allowed_count_tuples'] and len(expected) == source['allowed_count_tuples']
    assert total_count == proof['cartesian_count_tuples'] and total_mass == proof['cartesian_domain_mass'] and live_mass == proof['retained_domain_mass']
    controls = b.read(source['lemma_controls']['path'], source['lemma_controls']['sha256'])
    assert controls['status'] == 'EXACT_MATCHED_CORE_LINEAR_COUNT_LEMMA_CONTROLS' and controls['no_negative_quartic_minimum_ell'] == 2
    for name in ('verify_matched_count_refinement.py', 'matched_core_linear_count_bound_cycle283.md', 'matched_core_linear_count_checks_cycle283.py'): b.bind(H/name)
    result = dict(status='INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT', global_status='UNRESOLVED',
                  source=b.bind(source_path), base_authority=source['base_authority'], refinement=source['proof'],
                  geometry_index=authority['geometry_index'], complete_actual_cover=True,
                  candidates_checked=checked, count_tuples_checked=total_count, allowed_count_tuples=len(expected),
                  producer_imported=False, producer_singleton_evaluation_used=False, geometry_exclusions=0,
                  files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('geometry_index', 'candidates_checked', 'count_tuples_checked', 'allowed_count_tuples')}), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--source', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); run(a.source, a.output)
