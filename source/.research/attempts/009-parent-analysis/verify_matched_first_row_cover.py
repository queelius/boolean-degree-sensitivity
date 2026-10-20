"""Check every first-row coordinate map and expose a proved search quotient."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_coupled_two_positive import literal_embedding
from verify_parent_coordinate_cover import check_map
from verify_two_positive_conditional_orbits import relabel

H = Path(__file__).resolve().parent


def row_map_coverage(maps, representatives, count):
    assert [r['index'] for r in representatives] == list(range(len(representatives)))
    rows = [r['row'] for r in representatives]
    assert rows == sorted(set(rows)) and set(rows) <= set(range(count))
    assert len(maps) == count and {r['source_row'] for r in maps} == set(range(count))
    assert {r['representative'] for r in maps} == set(range(len(representatives)))
    return rows


def run(source_path, output):
    assert not output.exists(); start = monotonic(); b = Bindings(); source = b.read(source_path)
    assert source['status'] == 'PROPOSED_COMPLETE_MATCHED_GEOMETRY_FIRST_ROW_COVER'
    authority = b.read(source['instance_authority']['path'], source['instance_authority']['sha256'])
    assert authority['status'] == 'INDEPENDENTLY_VERIFIED_COMPLETE_MATCHED_CORE_COMPONENT_INSTANCE'
    assert authority['complete_component_domains'] is True
    instance = read_certificate(b, authority['instance']); proof = read_certificate(b, source['proof'])
    assert proof['instance_authority'] == source['instance_authority']
    assert proof['geometry_index'] == source['geometry_index'] == authority['geometry_index']
    geometry = dict(authority['geometry']); pair = proof['marked_pair']
    assert pair == source['marked_pair'] and pair in geometry['eligible_pairs']
    geometry['selected_pair'] = pair; assert geometry == proof['geometry']
    known = {q: -2 for q in geometry['negative_supports']} | {q: 2 for q in geometry['positive_doubles']}
    assert proof['known'] == [list(r) for r in sorted(known.items())]
    data = b.read(H/'two-positive-pair-embeddings.json', '0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')
    rows = data['domain']['rows']; selected = row_map_coverage(proof['maps'], proof['representatives'], len(rows))
    assert len(rows) == proof['raw_rows'] == source['input_rows']
    assert len(selected) == proof['representative_count'] == source['representatives']
    targets = {r['index']: literal_embedding(rows[r['row']], geometry, pair) for r in proof['representatives']}
    seen = set()
    for record in proof['maps']:
        image = tuple(record['map'])
        if image not in seen:
            assert sorted(image) == list(range(14)) and relabel(pair, image) == pair
            assert {relabel(q, image): k for q, k in known.items()} == known
            seen.add(image)
        embedded = literal_embedding(rows[record['source_row']], geometry, pair)
        check_map(record['map'], embedded, targets[record['representative']], geometry)
    core = geometry['positive_doubles'][0] & geometry['positive_doubles'][1]
    vertices = [v for v in range(14) if core >> v & 1]
    local_pair = sum(1 << i for i, v in enumerate(vertices) if pair >> v & 1)
    component_index = instance['core_pair_order'].index(local_pair)
    component = instance['components'][component_index]
    assert component['kind'] == 'safe_pair_row' and component['row_count'] == component['candidates'] == len(rows)
    for name in ('verify_matched_first_row_cover.py', 'test_verify_matched_first_row_cover.py',
                 'matched_first_row_quotient_soundness_cycle278.md', 'verify_parent_coordinate_cover.py'): b.bind(H/name)
    result = dict(status='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT', global_status='UNRESOLVED',
                  source=b.bind(source_path), base_instance_authority=source['instance_authority'], instance=authority['instance'],
                  geometry_index=authority['geometry_index'], geometry=authority['geometry'],
                  marked_pair=pair, component_index=component_index, selected_row_indices=selected,
                  full_row_count=len(rows), coordinate_maps_checked=len(proof['maps']), distinct_maps=len(seen),
                  complete_actual_cover=True, complete_component_domains=False,
                  no_symmetry_imposed_on_function=True, canonicalizer_imported=False,
                  necessary_components_only=True, geometry_exclusions=0, seconds=monotonic()-start,
                  files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(geometry=authority['geometry_index'], component_index=component_index,
                         representatives=len(selected), maps_checked=len(proof['maps']), seconds=result['seconds'])), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--source', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); run(a.source, a.output)
