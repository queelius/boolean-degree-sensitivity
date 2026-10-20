"""Exact joint singleton identities and sizes of two actual component frontiers."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from verify_core_fourier_envelope_certificate import literal_words
from verify_four_cube_pair_domains import LiteralCubeChecker
from transport_stratified_catalog import catalog_map

H = Path(__file__).resolve().parent; b = Bindings()
pairs = [q for q in range(16) if q.bit_count() == 2]
records = literal_words((3, 12), 0); assert len(records) == 526
ordinary = set(); apex = set()
for word, delta, ts, value in records:
    coefficients = {q: sum((1-2*((word >> x) & 1))*(-1 if (q & x).bit_count() % 2 else 1) for x in range(16)) for q in range(16)}
    even = [coefficients[q] for q in [0]+pairs]
    if delta:
        assert all(abs(v) in (4, 12) for v in even)
        assert sum(abs(v) == 12 for v in even) <= 1
    else:
        assert all(v % 8 == 0 for v in even)
        assert sum(v*v for v in even) in (0, 128, 256)
    if any((1+x.bit_count() in (0, 12, 13) and (word >> x) & 1) or
           (1+x.bit_count() in (1, 2, 14) and not ((word >> x) & 1)) for x in range(16)): continue
    row = tuple(coefficients[q] for q in pairs)
    if delta == 1:
        assert all(v in (-4, 4) for v in row)
        ordinary.add(tuple(q for q, v in zip(pairs, row) if v == 4))
    if delta == 0: apex.add(row)
expected = set()
for size in range(7):
    for edges in combinations(pairs, size):
        degrees = sorted(sum(bool(e & (1 << v)) for e in edges) for v in range(4))
        if degrees in ([1, 1, 1, 1], [1, 1, 2, 2]): expected.add(edges)
assert ordinary == expected and len(ordinary) == 15
assert apex == {(0,)*6} | {tuple(8 if i == j else 0 for i in range(6)) for j in range(6)}
frontier_path = H/'two-positive-signed-geometry-frontier-cycle260.json'; frontier = b.read(frontier_path)
data = b.read(H/'two-positive-pair-embeddings.json', '0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')
scalar_path = H/'matched-core-scalar-catalog-independent-manifest-cycle263.json'; scalar = b.read(scalar_path)
assert scalar['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_CORE_CANONICAL_SCALAR_CATALOG_FILTER'
degree = b.read(scalar['catalog_authority']['path'], scalar['catalog_authority']['sha256'])
covers = {c['low_count']: c for c in degree['covers']}
catalogs = {(r['low_count'], r['index']): r for r in scalar['records']}
results = []
for index in (19, 34):
    assert index in frontier['remaining_geometries']; g = data['representatives'][index]
    core = g['positive_doubles'][0] & g['positive_doubles'][1]
    vertices = [v for v in range(14) if core >> v & 1]
    assert any(not (a & c) for a, c in combinations(g['eligible_pairs'], 2))
    _, outside = LiteralCubeChecker.coordinates(g); components = []
    for local_pair in pairs:
        pair = sum(1 << v for i, v in enumerate(vertices) if local_pair >> i & 1)
        if pair in g['eligible_pairs']: continue
        negative = sorted(sum(1 << i for i, v in enumerate(outside) if n >> v & 1) for n in g['negative_supports'] if n & core == pair)
        assert len(negative) == 1 and negative[0] & 3
        branches = []
        for low_count in range(7):
            for lows in combinations(range(2, 10), low_count):
                representative, image = catalog_map(negative, list(lows), covers[low_count])
                entry = catalogs[low_count, representative]
                assert sorted(sum(1 << image[i] for i in range(10) if q >> i & 1) for q in negative) == entry['negative']
                branches.append(dict(low_coordinates=list(lows), degree_index=representative,
                                     map=image, candidates=len(entry['retained_indices'])))
        components.append(dict(core_pair=pair, local_core_pair=local_pair, negative=negative,
                               complete_low_partitions=len(branches), candidates=sum(r['candidates'] for r in branches),
                               nonempty_partitions=sum(bool(r['candidates']) for r in branches), branches=branches))
    results.append(dict(geometry=index, outside=outside, components=components,
                        component_candidates=sum(r['candidates'] for r in components)))
for name in ('matched_core_joint_probe_cycle264.py', 'matching_core_word_lemma_cycle224.md',
             'matched_core_catalog_transfer_cycle229.md', 'singleton_linear_count_bound_cycle141.md',
             'transport_stratified_catalog.py', 'test_transport_stratified_catalog.py'): b.bind(H/name)
result = dict(status='EXACT_MATCHED_CORE_JOINT_IDENTITIES_AND_EXPLORATORY_COMPONENT_COUNTS', global_status='UNRESOLVED',
              core_words_checked=526, core_pair_order=pairs,
              ordinary_singleton_positive_graphs=[list(x) for x in sorted(ordinary)], apex_singleton_vectors=[list(x) for x in sorted(apex)],
              equal_apex_large_even_components_at_most=1, records=results,
              scalar_authority=b.bind(scalar_path), frontier=b.bind(frontier_path),
              actual_full_function_search=False, geometry_exclusions=0,
              files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
output = H/'matched-core-joint-probe-cycle264.json'; assert not output.exists(); output.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps([dict(geometry=r['geometry'], component_candidates=r['component_candidates'],
                      components=[{k: c[k] for k in ('local_core_pair', 'negative', 'candidates', 'nonempty_partitions')} for c in r['components']]) for r in results]), flush=True)
