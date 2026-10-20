"""Independent completeness, transport, value, and literal-relation instance audit."""
from argparse import ArgumentParser
from itertools import combinations
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_four_cube_pair_domains import LiteralCubeChecker
from verify_core_fourier_envelope_certificate import literal_words

H = Path(__file__).resolve().parent


def validate_catalog_map(image, negative, lows, canonical_negative):
    assert all(type(v) is int for v in image) and sorted(image) == list(range(10))
    assert {image[0], image[1]} == {0, 1}
    assert lows == sorted(set(lows)) and set(lows) <= set(range(2, 10))
    assert {image[v] for v in lows} == set(range(2, 2+len(lows)))
    moved = sorted(sum(1 << image[i] for i in range(10) if q >> i & 1) for q in negative)
    assert moved == canonical_negative


def run(source_path, output):
    assert not output.exists(); start = monotonic(); b = Bindings(); source = b.read(source_path)
    assert source['status'] == 'PROPOSED_COMPLETE_MATCHED_CORE_COMPONENT_INSTANCE'
    instance = read_certificate(b, source['proof'])
    scalar = b.read(source['scalar_authority']['path'], source['scalar_authority']['sha256'])
    assert scalar['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_CORE_CANONICAL_SCALAR_CATALOG_FILTER'
    cover_path = H/'two-positive-pair-embeddings-independent-manifest.json'
    cover = b.read(cover_path, '997d16b0bb5a88078ab2627692505250dc1bc144355a1230d5ab1157fcbf16e3')
    assert cover['status'] == 'INDEPENDENTLY_ACCEPTED_COMPLETE_TWO_POSITIVE_GEOMETRY_AND_PAIR_EMBEDDING_COVER'
    data = b.read(H/'two-positive-pair-embeddings.json', '0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')
    index = source['geometry_index']; geometry = data['representatives'][index]
    assert instance['geometry_index'] == index and instance['geometry'] == geometry
    core = geometry['positive_doubles'][0] & geometry['positive_doubles'][1]
    vertices = [v for v in range(14) if core >> v & 1]; assert len(vertices) == 4
    assert any(not (p & q) for p, q in combinations(geometry['eligible_pairs'], 2))
    assert all((n & core).bit_count() <= 2 for n in geometry['negative_supports'])
    pairs = sorted(sum(1 << i for i in c) for c in combinations(range(4), 2))
    assert instance['core_pair_order'] == pairs and [c['local_core_pair'] for c in instance['components']] == pairs
    _, outside = LiteralCubeChecker.coordinates(geometry); assert instance['outside'] == outside
    catalog = {(r['low_count'], r['index']): r for r in scalar['records']}
    supports = [q for q in range(1024) if q.bit_count() in (1, 3)]
    positions = {q: i for i, q in enumerate(supports)}
    characters = np.array([[(-1 if (q & x).bit_count() % 2 else 1) for x in range(1024)] for q in supports], dtype=np.int16)
    canonical_values = {}; original_cache = {}; safe_values = None; checked_values = 0; reports = []
    expected_lows = [list(c) for size in range(7) for c in combinations(range(2, 10), size)]
    # L>=7 forces Q<=12-2L<0, so no missing branch is discarded without a contradiction.
    assert all(12-2*size < 0 for size in (7, 8))
    for component in instance['components']:
        pair = sum(1 << v for i, v in enumerate(vertices) if component['local_core_pair'] >> i & 1)
        actual = np.load(component['values']['path'], allow_pickle=False)
        assert actual.dtype == np.int8 and actual.shape == (component['candidates'], 1024)
        negative = sorted(sum(1 << i for i, v in enumerate(outside) if n >> v & 1) for n in geometry['negative_supports'] if n & core == pair)
        if pair in geometry['eligible_pairs']:
            assert not negative and component['kind'] == 'safe_pair_row'
            assert component['row_count'] == component['candidates'] == len(data['domain']['rows'])
            if safe_values is None:
                checker = LiteralCubeChecker(data['domain']['rows'])
                safe_values = np.array([[-8*t-4*(1-(x & 1)-((x >> 1) & 1)) for t in checker.at(x)] for x in range(1024)], dtype=np.int16).T
            assert np.array_equal(actual, safe_values)
        else:
            assert component['kind'] == 'catalog_component' and component['core_pair'] == pair and component['negative'] == negative
            assert len(negative) in (1, 2) and all(q.bit_count() == 3 for q in negative)
            assert [r['low_coordinates'] for r in component['branches']] == expected_lows
            offset = 0
            for branch in component['branches']:
                key = len(branch['low_coordinates']), branch['degree_index']; entry = catalog[key]
                validate_catalog_map(branch['map'], negative, branch['low_coordinates'], entry['negative'])
                assert branch['canonical_indices'] == entry['retained_indices'] and branch['source'] == entry['source']
                count = len(entry['retained_indices'])
                assert branch['start'] == offset and branch['stop'] == offset+count
                if key not in canonical_values:
                    original = read_certificate(b, entry['source']); original_cache[key] = original
                    assert original['negative'] == entry['negative']
                    coefficients = np.zeros((count, len(supports)), dtype=np.int16)
                    coefficients[:, [positions[q] for q in original['negative']]] = -2
                    for i, candidate_index in enumerate(entry['retained_indices']):
                        candidate = original['candidates'][candidate_index]
                        coefficients[i, [positions[q] for q in candidate['positive']]] = 1
                        coefficients[i, [positions[q] for q in candidate['linear']]] = -1
                    assert np.max(np.sum(np.abs(coefficients), axis=1), initial=0) < 128
                    canonical_values[key] = coefficients @ characters
                points = [sum(1 << branch['map'][i] for i in range(10) if x >> i & 1) for x in range(1024)]
                assert sorted(points) == list(range(1024))
                assert np.array_equal(actual[offset:offset+count], canonical_values[key][:, points])
                offset += count
            assert offset == len(actual)
        assert len({row.tobytes() for row in actual}) == len(actual)
        checked_values += actual.size; reports.append(dict(pair=component['local_core_pair'], candidates=len(actual)))
    words = literal_words((3, 12), 0); assert len(words) == 526
    literal = []
    for word, delta, ts, empty in words:
        values = [sum((1-2*((word >> x) & 1))*(-1 if (q & x).bit_count() % 2 else 1) for x in range(16)) for q in pairs]
        literal.append((word, delta, values))
    relations = []
    for weight in range(11):
        for delta in (-1, 0, 1):
            tuples = set()
            for word, d, values in literal:
                if d != delta: continue
                if any((weight+x.bit_count() in (0, 12, 13) and (word >> x) & 1) or
                       (weight+x.bit_count() in (1, 2, 14) and not ((word >> x) & 1)) for x in range(16)): continue
                tuples.add(tuple(values))
            relations.append(dict(weight=weight, delta=delta, tuples=[list(r) for r in sorted(tuples)]))
    assert relations == instance['relation_types']
    assert source['domain_sizes'] == [r['candidates'] for r in reports]
    for name in ('verify_matched_component_instance.py', 'test_verify_matched_component_instance.py',
                 'matched_core_catalog_transfer_cycle229.md', 'singleton_linear_count_bound_cycle141.md',
                 'matching_core_word_lemma_cycle224.md'): b.bind(H/name)
    result = dict(status='INDEPENDENTLY_VERIFIED_COMPLETE_MATCHED_CORE_COMPONENT_INSTANCE', global_status='UNRESOLVED',
                  source=b.bind(source_path), instance=source['proof'], geometry_index=index, geometry=geometry,
                  scalar_authority=source['scalar_authority'], geometry_cover=b.bind(cover_path),
                  components=reports, table_entries_checked=checked_values, complete_component_domains=True,
                  producer_imported=False, producer_transform_used=False, necessary_components_only=True,
                  geometry_exclusions=0, seconds=monotonic()-start,
                  files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('geometry_index', 'components', 'table_entries_checked', 'seconds')}), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--source', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); run(a.source, a.output)
