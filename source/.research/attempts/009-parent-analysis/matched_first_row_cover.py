"""Explicit first-row coordinate covers preserving each actual signed geometry."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from two_positive_conditional_orbits import cover
from gzip_certificate_io import write_certificate

H = Path(__file__).resolve().parent


def run(authority_path, output):
    start = monotonic(); b = Bindings(); authority = b.read(authority_path)
    assert authority['status'] == 'INDEPENDENTLY_VERIFIED_COMPLETE_MATCHED_CORE_COMPONENT_INSTANCE'
    data = b.read(H/'two-positive-pair-embeddings.json', '0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')
    g = dict(authority['geometry']); rows = data['domain']['rows']
    degrees = {v: sum(bool(p & (1 << v)) for p in g['eligible_pairs']) for v in range(14)}
    pair = min(g['eligible_pairs'], key=lambda p: (-sum(degrees[v] for v in range(14) if p >> v & 1), p))
    g['selected_pair'] = pair
    known = {q: -2 for q in g['negative_supports']} | {q: 2 for q in g['positive_doubles']}
    details = cover(g, rows, known, pair, list(range(len(rows))))
    proof = dict(geometry_index=authority['geometry_index'], geometry=g, marked_pair=pair,
                 known=sorted(known.items()), instance_authority=b.bind(authority_path), **details)
    proof_path = output.with_suffix('.json.gz'); assert not output.exists() and not proof_path.exists(); write_certificate(proof_path, proof)
    for name in ('matched_first_row_cover.py', 'two_positive_conditional_orbits.py', 'test_two_positive_conditional_orbits.py'): b.bind(H/name)
    result = dict(status='PROPOSED_COMPLETE_MATCHED_GEOMETRY_FIRST_ROW_COVER', global_status='UNRESOLVED',
                  instance_authority=b.bind(authority_path), proof=b.bind(proof_path), geometry_index=authority['geometry_index'],
                  marked_pair=pair, input_rows=len(rows), representatives=details['representative_count'],
                  no_symmetry_imposed_on_function=True, seconds=monotonic()-start,
                  files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('geometry_index', 'marked_pair', 'input_rows', 'representatives', 'seconds')}), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--authority', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); run(a.authority, a.output)
