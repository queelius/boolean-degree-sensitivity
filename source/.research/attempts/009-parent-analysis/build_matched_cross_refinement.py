"""Build a candidate-preserving ordinary-cubic cross-intersection refinement."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate, write_certificate
from load_matched_safe_count_instance import load
from ordinary_cross_intersection import ordinary_features, cross_relations

H = Path(__file__).resolve().parent


def run(base_path, output):
    start = monotonic(); directory = output.with_suffix(''); assert not directory.exists() and not output.exists()
    b = Bindings(); base, quota, tables, old_relations = load(b, base_path)
    instance = read_certificate(b, quota['instance']); features = []
    apex_mask = quota['geometry']['positive_doubles'][0] ^ quota['geometry']['positive_doubles'][1]
    assert sum(1 << v for v in instance['outside'][:2]) == apex_mask
    # This is a local structural assumption, checked again by the independent reader.
    assert all(n & 3 for c in instance['components'] for n in c.get('negative', []))
    for table in tables:
        triples, present = ordinary_features(table[:, :1024]); features.append(present)
    columns, relations, descriptions = cross_relations(features, instance['core_pair_order'], triples)
    directory.mkdir(); records = []
    for j, (f, col) in enumerate(zip(features, columns)):
        fp = directory/f'features-{j}.npy'; cp = directory/f'columns-{j}.npy'
        np.save(fp, f, allow_pickle=False); np.save(cp, col, allow_pickle=False)
        records.append(dict(component_index=j, features=b.bind(fp), columns=b.bind(cp), rows=len(f)))
    original = b.read(base['base_refinement']['path'], base['base_refinement']['sha256'])
    proof = dict(base_refinement=b.bind(base_path), quotient_authority=original['base_authority'],
                 geometry_index=base['geometry_index'], old_point_count=len(old_relations),
                 ordinary_triples=triples, core_pair_order=instance['core_pair_order'],
                 components=records, relations=relations, descriptions=descriptions)
    pp = directory/'refinement.json.gz'; write_certificate(pp, proof)
    for name in ('build_matched_cross_refinement.py', 'ordinary_cross_intersection.py', 'test_ordinary_cross_intersection.py',
                 'matched_ordinary_cross_intersection_cycle331.md', 'load_matched_safe_count_instance.py'): b.bind(H/name)
    result = dict(status='PROPOSED_MATCHED_ORDINARY_CROSS_REFINEMENT', global_status='UNRESOLVED',
                  base_refinement=b.bind(base_path), geometry_index=base['geometry_index'], proof=b.bind(pp),
                  added_points=len(relations), seconds=monotonic()-start,
                  files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(geometry=base['geometry_index'], added_points=len(relations), seconds=result['seconds'])), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--base', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True); a = p.parse_args(); run(a.base, a.output)
