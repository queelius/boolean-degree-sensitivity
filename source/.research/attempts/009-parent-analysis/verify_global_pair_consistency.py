"""Independent array-domain checking of scoped global-companion deletions.

The reader accepts deletions and contradictions only. It does not accept a
producer's fixed-point claim without checking all positive companion pairs.
"""
from argparse import ArgumentParser
from pathlib import Path
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate

H = Path(__file__).resolve().parent


def live_rows(tables, relations, domains, point):
    assert type(point) is int and 0 <= point < len(relations)
    choices = [set(map(int, t[d, point])) for t, d in zip(tables, domains)]
    return [r for r in relations[point] if all(v in c for v, c in zip(r, choices))]


def replay_steps(tables, relations, domains, steps):
    for x in steps:
        live = live_rows(tables, relations, domains, x); assert live
        reduced = [d[np.isin(t[d, x], sorted({r[j] for r in live}))] for j, (t, d) in enumerate(zip(tables, domains))]
        assert all(len(d) for d in reduced) and any(len(a) < len(c) for a, c in zip(reduced, domains))
        domains = reduced
    return domains


def incompatible(tables, relations, domains, point):
    return any(not len(d) for d in domains) if point == -1 else not live_rows(tables, relations, domains, point)


def frontier_domains(tables, relations, tree, path):
    domains = [np.arange(len(t), dtype=np.int64) for t in tables]; node = tree
    for direction in path:
        assert direction in (0, 1) and node['kind'] == 'UNKNOWN'
        domains = replay_steps(tables, relations, domains, node['propagation'])
        s = node['split']; j, x, value = s['variable'], s['point'], s['value']
        assert type(j) is int and 0 <= j < len(tables) and type(x) is int and 0 <= x < len(relations)
        chosen = tables[j][domains[j], x] == value
        assert np.any(chosen) and not np.all(chosen)
        domains[j] = domains[j][chosen if direction == 0 else ~chosen]
        node = node['children'][direction]
    assert node['kind'] == 'LIMIT'
    return domains


def replay_deletions(tables, relations, domains, deletions):
    domains = list(domains)
    for deletion in deletions:
        a, i, b = deletion['variable'], deletion['candidate'], deletion['partner']
        assert all(type(v) is int for v in (a, i, b)) and 0 <= a < len(tables) and 0 <= b < len(tables) and a != b
        assert i in domains[a] and len(domains[b])
        possible = domains[b]
        for x in deletion['points']:
            assert type(x) is int and 0 <= x < len(relations)
            value = int(tables[a][i, x]); allowed = sorted({r[b] for r in relations[x] if r[a] == value})
            reduced = possible[np.isin(tables[b][possible, x], allowed)]
            assert len(reduced) < len(possible)
            possible = reduced
        assert not len(possible)
        domains[a] = domains[a][domains[a] != i]
    return domains


def run(source_path, output):
    assert not output.exists(); b = Bindings(); source = b.read(source_path)
    assert source['status'] == 'PROPOSED_MATCHED_FRONTIER_GLOBAL_PAIR_PROBE'
    authority = b.read(source['search_authority']['path'], source['search_authority']['sha256'])
    assert authority['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_COUNT_SEARCH' and authority['search_status'] == 'UNKNOWN'
    search = b.read(authority['source']['path'], authority['source']['sha256']); search_proof = read_certificate(b, search['proof'])
    refinement = b.read(search['instance_authority']['path'], search['instance_authority']['sha256'])
    assert refinement['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT'
    quota = b.read(refinement['base_authority']['path'], refinement['base_authority']['sha256'])
    assert quota['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    instance = read_certificate(b, quota['instance']); extra = read_certificate(b, refinement['refinement'])
    tables = []
    for j, component in enumerate(instance['components']):
        values = np.load(component['values']['path'], allow_pickle=False)
        if j == quota['component_index']: values = np.stack([values[i] for i in quota['selected_row_indices']])
        counts = np.load(extra['columns'][j]['counts']['path'], allow_pickle=False)
        tables.append(np.concatenate((values, counts[:, None]), axis=1))
    lookup = {(r['weight'], r['delta']): r['tuples'] for r in instance['relation_types']}
    relations = [lookup[x.bit_count(), 1-(x & 1)-((x >> 1) & 1)] for x in range(1024)]
    relations.append(extra['allowed_count_tuples'])
    proof = read_certificate(b, source['proof']); assert proof['search_authority'] == source['search_authority']
    assert source['geometry_index'] == authority['geometry_index'] == quota['geometry_index']
    paths = set(); deletions = 0; checked = []; local_count = 0
    for record in proof['local_contradictions']:
        path = tuple(record['path']); assert path not in paths; paths.add(path)
        domains = frontier_domains(tables, relations, search_proof['answer']['tree'], path)
        domains = replay_steps(tables, relations, domains, record['propagation'])
        assert incompatible(tables, relations, domains, record['contradiction_point']); local_count += 1
    for record in proof['records']:
        path = tuple(record['path']); assert path not in paths; paths.add(path)
        domains = frontier_domains(tables, relations, search_proof['answer']['tree'], path)
        domains = replay_steps(tables, relations, domains, record['initial_propagation'])
        assert list(map(len, domains)) == record['initial_domain_sizes']
        contradiction = False
        for stage in record['stages']:
            assert not contradiction
            pair = stage['pair_propagation']; domains = replay_deletions(tables, relations, domains, pair['deletions'])
            deletions += len(pair['deletions'])
            if pair['status'] == 'CONTRADICTION':
                assert any(not len(d) for d in domains) and 'point_propagation' not in stage
                contradiction = True
            else:
                assert pair['status'] in ('FIXED_POINT', 'LIMIT') and all(len(d) for d in domains)
                point = stage['point_propagation']; domains = replay_steps(tables, relations, domains, point['steps'])
                if point['contradiction_point'] is not None:
                    assert incompatible(tables, relations, domains, point['contradiction_point']); contradiction = True
        assert [d.tolist() for d in domains] == record['final_domains']
        assert (record['status'] == 'FRONTIER_STATE_CONTRADICTION') == contradiction
        checked.append(dict(path=list(path), exact_deletions_verified=True, contradiction=contradiction,
                            final_domain_sizes=list(map(len, domains))))
    assert len(checked) == source['tested_states'] and local_count == source['local_contradictions']
    assert sum(r['contradiction'] for r in checked) == source['new_contradictions']
    for name in ('verify_global_pair_consistency.py', 'test_verify_global_pair_consistency.py'): b.bind(H/name)
    result = dict(status='INDEPENDENTLY_VERIFIED_SCOPED_GLOBAL_COMPANION_REDUCTIONS', global_status='UNRESOLVED',
                  source=b.bind(source_path), search_authority=source['search_authority'], geometry_index=source['geometry_index'],
                  verified_pair_deletions=deletions, local_contradictions=local_count, records=checked,
                  producer_imported=False, bitset_kernel_imported=False, producer_fixed_point_claims_verified=False,
                  geometry_exclusions=0, global_goal_complete=False,
                  files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(geometry=source['geometry_index'], verified_pair_deletions=deletions,
                         checked_states=len(checked), new_contradictions=source['new_contradictions'])))


if __name__ == '__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
