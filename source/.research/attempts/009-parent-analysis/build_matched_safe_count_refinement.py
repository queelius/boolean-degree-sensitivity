"""Append the accepted exclusion of Q=8; keep the old count relation intact."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate, write_certificate

H = Path(__file__).resolve().parent


def run(rule_path, output):
    assert not output.exists() and not output.with_suffix('.json.gz').exists()
    b = Bindings(); rule = b.read(rule_path)
    assert rule['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_SAFE_LINEAR_COUNT_EXCLUSIONS'
    assert rule['actual_function_scope'] is True
    base = b.read(rule['base_refinement']['path'], rule['base_refinement']['sha256'])
    assert base['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT'
    assert base['complete_actual_cover'] is True and base['base_authority'] == rule['quotient_authority']
    assert base['geometry_index'] == rule['geometry_index']
    extra = read_certificate(b, base['refinement'])
    allowed = [row for row in extra['allowed_count_tuples']
               if all(row[j] in rule['remaining_linear_counts'] for j in rule['component_indices_restricted'])]
    proof = dict(base_refinement=rule['base_refinement'], exclusion_authority=b.bind(rule_path),
                 geometry_index=rule['geometry_index'], columns=extra['columns'],
                 source_point=1024, added_point=1025, allowed_count_tuples=allowed)
    proof_path = output.with_suffix('.json.gz'); write_certificate(proof_path, proof)
    b.bind(H/'build_matched_safe_count_refinement.py')
    result = dict(status='PROPOSED_MATCHED_SAFE_COUNT_REFINEMENT', geometry_index=rule['geometry_index'],
                  base_refinement=rule['base_refinement'], exclusion_authority=b.bind(rule_path),
                  proof=b.bind(proof_path), allowed_count_tuples=len(allowed),
                  files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(geometry=rule['geometry_index'], before=len(extra['allowed_count_tuples']), after=len(allowed))))


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--rule', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True); a = p.parse_args(); run(a.rule, a.output)
