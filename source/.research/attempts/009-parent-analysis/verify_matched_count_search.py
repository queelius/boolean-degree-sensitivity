"""Independent full-tree replay after the proved linear-count refinement."""
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
    assert source['status'] == 'PROPOSED_MATCHED_COMPONENT_COUNT_SEARCH_RESULT'
    refinement = b.read(source['instance_authority']['path'], source['instance_authority']['sha256'])
    assert refinement['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT' and refinement['complete_actual_cover'] is True
    prior = b.read(source['previous_search_authority']['path'], source['previous_search_authority']['sha256'])
    assert prior['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_SEARCH' and prior['search_status'] == 'UNKNOWN'
    prior_source = b.read(prior['source']['path'], prior['source']['sha256'])
    assert prior_source['instance_authority'] == refinement['base_authority']
    quota = b.read(refinement['base_authority']['path'], refinement['base_authority']['sha256'])
    assert quota['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    assert source['geometry_index'] == refinement['geometry_index'] == prior['geometry_index'] == quota['geometry_index']
    instance = read_certificate(b, quota['instance']); extra = read_certificate(b, refinement['refinement'])
    proof = read_certificate(b, source['proof'])
    assert proof['instance_authority'] == source['instance_authority'] and proof['previous_search_authority'] == source['previous_search_authority']
    tables = []
    for j, component in enumerate(instance['components']):
        base = np.load(component['values']['path'], allow_pickle=False)
        if j == quota['component_index']: base = np.stack([base[i] for i in quota['selected_row_indices']])
        counts = np.load(extra['columns'][j]['counts']['path'], allow_pickle=False)
        assert counts.shape == (len(base),)
        tables.append(np.concatenate((base, counts[:, None]), axis=1))
    lookup = {(r['weight'], r['delta']): r['tuples'] for r in instance['relation_types']}
    relations = [lookup[x.bit_count(), 1-(x & 1)-((x >> 1) & 1)] for x in range(1024)]
    relations.append(extra['allowed_count_tuples'])
    answer = proof['answer']; status = verify_tree(tables, relations, answer['tree'])
    assert status == answer['status'] == source['search_status']
    visited = pending = 0; witnesses = []; stack = [answer['tree']]
    while stack:
        node = stack.pop()
        if node['kind'] == 'LIMIT': pending += 1
        else:
            visited += 1; stack.extend(node.get('children', []))
            if 'witness' in node: witnesses.append(node['witness'])
    assert visited == answer['nodes'] == source['nodes'] <= answer['max_nodes'] == source['max_nodes']
    assert source['max_nodes'] == prior['verified_search_nodes']+source['new_node_limit']
    assert answer['new_nodes_explored'] == source['new_nodes_explored'] <= source['new_node_limit']
    assert answer['witness'] == source['witness']
    if status == 'SAT': assert witnesses == [source['witness']]
    else: assert not witnesses and source['witness'] is None
    if status == 'UNSAT': assert pending == 0
    for name in ('verify_matched_count_search.py', 'verify_finite_function_csp.py', 'test_verify_finite_function_csp.py',
                 'matched_core_linear_count_bound_cycle283.md'): b.bind(H/name)
    result = dict(status='INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_COUNT_SEARCH', global_status='UNRESOLVED',
                  source=b.bind(source_path), instance_authority=source['instance_authority'], previous_search_authority=source['previous_search_authority'],
                  geometry_index=source['geometry_index'], search_status=status, verified_search_nodes=visited,
                  unsearched_subtrees=pending, component_problem_excluded=status == 'UNSAT',
                  necessary_component_witness=source['witness'], actual_boolean_function=False, global_goal_complete=False,
                  producer_imported=False, bitset_kernel_imported=False, previous_tree_nodes_replayed=True,
                  seconds=monotonic()-start, files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('geometry_index', 'search_status', 'verified_search_nodes', 'unsearched_subtrees', 'seconds')}), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--source', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); run(a.source, a.output)
