"""Independent Cartesian enumeration of the new count relation."""
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
    assert source['status'] == 'PROPOSED_MATCHED_SAFE_COUNT_REFINEMENT'
    rule = b.read(source['exclusion_authority']['path'], source['exclusion_authority']['sha256'])
    base = b.read(source['base_refinement']['path'], source['base_refinement']['sha256'])
    assert rule['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_SAFE_LINEAR_COUNT_EXCLUSIONS'
    assert rule['actual_function_scope'] is True and rule['remaining_linear_counts'] == [2, 4]
    assert rule['excluded_linear_count'] == 8
    assert base['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT' and base['complete_actual_cover'] is True
    assert rule['base_refinement'] == source['base_refinement'] and rule['quotient_authority'] == base['base_authority']
    extra = read_certificate(b, base['refinement']); proof = read_certificate(b, source['proof'])
    assert proof['base_refinement'] == source['base_refinement'] and proof['exclusion_authority'] == source['exclusion_authority']
    assert proof['geometry_index'] == source['geometry_index'] == base['geometry_index'] == rule['geometry_index']
    assert proof['source_point'] == 1024 and proof['added_point'] == 1025 and proof['columns'] == extra['columns']
    choices = [sorted(set(map(int, np.load(c['counts']['path'], allow_pickle=False)))) for c in extra['columns']]
    restricted = rule['component_indices_restricted']; assert restricted and len(set(restricted)) == len(restricted)
    assert all(0 <= j < len(choices) and set(choices[j]) <= {2, 4, 8} for j in restricted)
    old_set = set(map(tuple, extra['allowed_count_tuples'])); expected = []; checked = 0
    for row in product(*choices):
        checked += 1
        ell = [10-sum(q for pair, q in zip(extra['core_pair_order'], row) if pair >> i & 1)//2 for i in range(4)]
        old_allowed = all(e >= (2 if n == 0 else 0) for e, n in zip(ell, extra['negative_singleton_core_counts']))
        assert old_allowed == (row in old_set)
        if old_allowed and not any(row[j] == 8 for j in restricted): expected.append(list(row))
    assert expected == proof['allowed_count_tuples'] and len(expected) == source['allowed_count_tuples']
    for name in ('verify_matched_safe_count_refinement.py', 'matched_safe_eight_exclusion_cycle323.md',
                 'test_verify_matched_safe_count_exclusion_v2.py', 'cycle324-test-fixture-note.md'): b.bind(H/name)
    result = dict(status='INDEPENDENTLY_VERIFIED_MATCHED_SAFE_COUNT_REFINEMENT', global_status='UNRESOLVED',
                  source=b.bind(source_path), base_refinement=source['base_refinement'],
                  exclusion_authority=source['exclusion_authority'], refinement=source['proof'],
                  geometry_index=source['geometry_index'], complete_actual_cover=True,
                  source_point=1024, added_point=1025, allowed_count_tuples=len(expected),
                  cartesian_tuples_checked=checked, old_point_semantics_unchanged=True,
                  producer_imported=False, whole_geometry_excluded=False, global_goal_complete=False,
                  files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(geometry=source['geometry_index'], allowed=len(expected), checked=checked)))


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True); a = p.parse_args(); run(a.source, a.output)
