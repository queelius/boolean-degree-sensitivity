"""Replay a complete or partial component search without importing its solver."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_finite_function_csp import verify_tree

H = Path(__file__).resolve().parent


def run(source_path, output):
    assert not output.exists(); start = monotonic(); b = Bindings(); source = b.read(source_path)
    assert source['status'] == 'PROPOSED_MATCHED_COMPONENT_SEARCH_RESULT'
    authority = b.read(source['instance_authority']['path'], source['instance_authority']['sha256'])
    assert authority['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT'
    assert authority['complete_actual_cover'] is True and authority['complete_component_domains'] is False
    assert source['geometry_index'] == authority['geometry_index']
    original = b.read(authority['base_instance_authority']['path'], authority['base_instance_authority']['sha256'])
    assert original['status'] == 'INDEPENDENTLY_VERIFIED_COMPLETE_MATCHED_CORE_COMPONENT_INSTANCE'
    assert original['complete_component_domains'] is True and original['instance'] == authority['instance']
    instance = read_certificate(b, authority['instance']); proof = read_certificate(b, source['proof'])
    assert proof['instance_authority'] == source['instance_authority']
    tables = [np.load(c['values']['path'], allow_pickle=False) for c in instance['components']]
    position = authority['component_index']; choices = authority['selected_row_indices']
    assert 0 <= position < len(tables) and len(set(choices)) == len(choices)
    assert all(type(i) is int and 0 <= i < len(tables[position]) for i in choices)
    tables[position] = np.stack([tables[position][i] for i in choices])
    lookup = {(r['weight'], r['delta']): r['tuples'] for r in instance['relation_types']}
    relations = [lookup[x.bit_count(), 1-(x & 1)-((x >> 1) & 1)] for x in range(1024)]
    answer = proof['answer']; status = verify_tree(tables, relations, answer['tree'])
    assert status == answer['status'] == source['search_status']
    pending = 0; visited = 0; witnesses = []; stack = [answer['tree']]
    while stack:
        node = stack.pop()
        if node['kind'] == 'LIMIT': pending += 1
        else:
            visited += 1; stack.extend(node.get('children', []))
            if 'witness' in node: witnesses.append(node['witness'])
    assert visited == answer['nodes'] == source['nodes'] <= source['max_nodes'] == answer['max_nodes']
    assert answer['witness'] == source['witness']
    if status == 'SAT': assert witnesses == [source['witness']]
    else: assert not witnesses and source['witness'] is None
    if status == 'UNSAT': assert pending == 0
    for name in ('verify_matched_component_search_v2.py', 'verify_finite_function_csp.py', 'test_verify_finite_function_csp.py'): b.bind(H/name)
    result = dict(status='INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_SEARCH', global_status='UNRESOLVED',
                  source=b.bind(source_path), instance_authority=source['instance_authority'],
                  geometry_index=authority['geometry_index'], search_status=status, verified_search_nodes=visited,
                  unsearched_subtrees=pending, component_problem_excluded=status == 'UNSAT',
                  necessary_component_witness=source['witness'], actual_boolean_function=False,
                  global_goal_complete=False, producer_imported=False, bitset_kernel_imported=False,
                  diagnostic_root_counts_verified=False, seconds=monotonic()-start,
                  files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('geometry_index', 'search_status', 'verified_search_nodes', 'unsearched_subtrees', 'seconds')}), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--source', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); run(a.source, a.output)
