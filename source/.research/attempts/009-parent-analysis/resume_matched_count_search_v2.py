"""Continue a checked quotient search with the added linear-count restriction."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate, write_certificate
from resume_function_csp import PriorityPointCSP, resume_search
from matched_count_resume_authority import validate_previous

H = Path(__file__).resolve().parent


def run(refinement_path, previous_path, max_new_nodes, output):
    start = monotonic(); b = Bindings(); refinement = b.read(refinement_path); previous = b.read(previous_path)
    assert refinement['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT' and refinement['complete_actual_cover'] is True
    old = b.read(previous['source']['path'], previous['source']['sha256']); old_proof = read_certificate(b, old['proof'])
    validate_previous(previous, old, refinement, b.bind(refinement_path))
    quota = b.read(refinement['base_authority']['path'], refinement['base_authority']['sha256'])
    assert quota['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    instance = read_certificate(b, quota['instance']); extra = read_certificate(b, refinement['refinement'])
    tables = []
    for j, component in enumerate(instance['components']):
        values = np.load(component['values']['path'], allow_pickle=False)
        if j == quota['component_index']: values = values[quota['selected_row_indices']]
        counts = np.load(extra['columns'][j]['counts']['path'], allow_pickle=False)
        assert counts.shape == (len(values),)
        tables.append(np.column_stack((values, counts)))
    lookup = {(r['weight'], r['delta']): r['tuples'] for r in instance['relation_types']}
    relations = [lookup[x.bit_count(), 1-(x & 1)-((x >> 1) & 1)] for x in range(1024)]+[extra['allowed_count_tuples']]
    order = [1024]+sorted(range(1024), key=lambda x: (min(x.bit_count(), 10-x.bit_count()), x))
    solver = PriorityPointCSP(tables, relations, order, priority_point=1024)
    answer = resume_search(solver, old_proof['answer']['tree'], max_new_nodes=max_new_nodes, added_point=1024)
    assert answer['prior_certificate_nodes'] == previous['verified_search_nodes']
    proof_path = output.with_suffix('.json.gz'); assert not output.exists() and not proof_path.exists()
    proof = dict(instance_authority=b.bind(refinement_path), previous_search_authority=b.bind(previous_path), answer=answer)
    write_certificate(proof_path, proof)
    for name in ('resume_matched_count_search_v2.py', 'matched_count_resume_authority.py', 'test_matched_count_resume_authority.py', 'resume_function_csp.py', 'test_resume_function_csp.py', 'finite_function_csp.py'): b.bind(H/name)
    result = dict(status='PROPOSED_MATCHED_COMPONENT_COUNT_SEARCH_RESULT', global_status='UNRESOLVED',
                  instance_authority=b.bind(refinement_path), previous_search_authority=b.bind(previous_path),
                  geometry_index=refinement['geometry_index'], proof=b.bind(proof_path), search_status=answer['status'],
                  nodes=answer['nodes'], max_nodes=answer['max_nodes'], new_node_limit=max_new_nodes,
                  new_nodes_explored=answer['new_nodes_explored'], reused_closed_nodes=answer['reused_closed_nodes'],
                  added_relation_shortened_nodes=answer['added_relation_shortened_nodes'], witness=answer['witness'],
                  necessary_components_only=True, actual_boolean_function=False, independent_audit='PENDING',
                  seconds=monotonic()-start, files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('geometry_index', 'search_status', 'nodes', 'new_nodes_explored',
                                          'reused_closed_nodes', 'added_relation_shortened_nodes', 'witness', 'seconds')}), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--refinement', type=Path, required=True)
    p.add_argument('--previous', type=Path, required=True); p.add_argument('--max-new-nodes', type=int, default=20000)
    p.add_argument('--output', type=Path, required=True); a = p.parse_args(); run(a.refinement, a.previous, a.max_new_nodes, a.output)
