"""Bounded exact component search after a proved actual-geometry row quotient."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate, write_certificate
from finite_function_csp import FunctionCSP

H = Path(__file__).resolve().parent


def run(authority_path, max_nodes, output):
    start = monotonic(); b = Bindings(); authority = b.read(authority_path)
    assert authority['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT'
    assert authority['complete_actual_cover'] is True and authority['complete_component_domains'] is False
    base = b.read(authority['base_instance_authority']['path'], authority['base_instance_authority']['sha256'])
    assert base['status'] == 'INDEPENDENTLY_VERIFIED_COMPLETE_MATCHED_CORE_COMPONENT_INSTANCE'
    assert base['complete_component_domains'] is True and base['instance'] == authority['instance']
    instance = read_certificate(b, authority['instance'])
    tables = [np.load(c['values']['path'], allow_pickle=False) for c in instance['components']]
    j = authority['component_index']; selected = authority['selected_row_indices']
    assert selected == sorted(set(selected)) and set(selected) <= set(range(len(tables[j])))
    tables[j] = tables[j][selected]
    lookup = {(r['weight'], r['delta']): r['tuples'] for r in instance['relation_types']}
    relations = [lookup[x.bit_count(), 1-(x & 1)-((x >> 1) & 1)] for x in range(1024)]
    order = sorted(range(1024), key=lambda x: (min(x.bit_count(), 10-x.bit_count()), x))
    solver = FunctionCSP(tables, relations, order)
    root, steps, bad = solver.propagate(solver.initial)
    print(json.dumps(dict(geometry=authority['geometry_index'], root_sizes=[d.bit_count() for d in root],
                          root_contradiction=bad, seconds=monotonic()-start)), flush=True)
    answer = solver.search(max_nodes)
    proof = dict(instance_authority=b.bind(authority_path), root_sizes=[d.bit_count() for d in root],
                 root_propagation=steps, root_contradiction=bad, answer=answer)
    proof_path = output.with_suffix('.json.gz'); assert not output.exists() and not proof_path.exists()
    write_certificate(proof_path, proof)
    for name in ('run_matched_component_search_v2.py', 'finite_function_csp.py', 'test_finite_function_csp.py'): b.bind(H/name)
    result = dict(status='PROPOSED_MATCHED_COMPONENT_SEARCH_RESULT', global_status='UNRESOLVED',
                  instance_authority=b.bind(authority_path), geometry_index=authority['geometry_index'], proof=b.bind(proof_path),
                  search_status=answer['status'], nodes=answer['nodes'], max_nodes=max_nodes,
                  witness=answer['witness'], necessary_components_only=True, actual_boolean_function=False,
                  independent_audit='PENDING', seconds=monotonic()-start,
                  files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('geometry_index', 'search_status', 'nodes', 'max_nodes', 'witness', 'seconds')}), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--authority', type=Path, required=True)
    p.add_argument('--max-nodes', type=int, default=1000); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); run(a.authority, a.max_nodes, a.output)
