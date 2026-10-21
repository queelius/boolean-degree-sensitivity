"""Independent literal replay of the normalized codegree-eleven obstruction."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip
import json

from small_valence_catalog import records, inspect
from negative_free_endpoint_strips import strip_roots, cycle_components, vertices

HERE = Path(__file__).resolve().parent
EIGHT = HERE.parent / '008-sparse-spectrum-proof'


def eligible(facets):
    pairs = Counter(e for t in facets for e in combinations(t, 2))
    active = sorted({v for t in facets for v in t})
    if len(active) != 14 or min(pairs.values()) < 4:
        return None
    neighbors = {v: {w for edge in pairs if v in edge for w in edge if w != v}
                 for v in active}
    result = []
    for a, b in combinations(active, 2):
        if (a, b) in pairs or sorted((len(neighbors[a]), len(neighbors[b]))) != [6, 7]:
            continue
        shared = neighbors[a] & neighbors[b]
        if len(shared) != 1:
            continue
        if len(neighbors[a]) == 7:
            a, b = b, a
        independent = [t for t in combinations([v for v in active if v not in (a, b)], 3)
                       if all(len(set(t) & set(facet)) <= 1 for facet in facets)]
        assert independent
        # Check identification directly against facets, without neighbor lookups.
        triple = independent[0]
        identified = {tuple(sorted(a if v == b else v for v in facet)) for facet in facets}
        assert len(identified) == len(facets)
        assert all(len(set(t)) == 4 for t in identified)
        vector = [len({face for facet in identified for face in combinations(facet, size)
                       if set(face) <= set(triple)}) for size in range(1, 5)]
        assert vector == [3, 0, 0, 0]
        result.append(dict(split_endpoints=[a, b], common_neighbor=next(iter(shared)),
                           independent_triple=list(triple), induced_f_vector=vector,
                           derivative_value=1-vector[0]+vector[1]-vector[2]+vector[3]))
    return result


def normalized_strips():
    answer = []
    for form in ('rim', 'apex'):
        data = json.loads((EIGHT / f'codegree11-no-negative-{form}.json').read_text())
        triangles = {sum(1 << v for v in row['support']) for row in data['fourier_coefficients']
                     if len(row['support']) == 3 and row['numerator'] == 1}
        assert len(triangles) == 18
        w = data['special_positive_triple_vertex']
        boundary = {t ^ (1 << w) for t in triangles if t >> w & 1}
        components = cycle_components(boundary)
        assert components is not None
        lengths = sorted(map(len, components))
        if form == 'apex':
            assert lengths == [4, 5]
            answer.append(dict(form=form, boundary_lengths=lengths, excluded=True))
            continue
        assert lengths == [4, 4]
        octahedron = {v for pair in data['octahedron_opposite_pairs'] for v in pair}
        bipyramid = set(data['bipyramid_apices'] + data['bipyramid_rim_cycle'])
        assert octahedron & bipyramid == {w}
        roots = strip_roots(boundary)
        assert len(roots) == 8
        for root in roots:
            link = set(root['faces'])
            for triangle in triangles:
                if not triangle >> w & 1:
                    continue
                copy = 12 if set(vertices(triangle)) <= octahedron else 13
                assert copy == 12 or set(vertices(triangle)) <= bipyramid
                link.add((triangle ^ (1 << w)) | (1 << copy))
            edge_counts = Counter(sum(1 << v for v in e) for face in link
                                  for e in combinations(vertices(face), 2))
            active = {v for face in link for v in vertices(face)}
            assert [len(active), len(edge_counts), len(link)] == [10, 24, 16]
            assert set(edge_counts.values()) == {2}
            for v in active:
                local = {face ^ (1 << v) for face in link if face >> v & 1}
                local_cycles = cycle_components(local)
                assert local_cycles is not None and len(local_cycles) == 1
                assert len(local_cycles[0]) in (4, 5)
            reached = {min(active)}
            while True:
                expanded = reached | {v for edge in edge_counts
                                      if set(vertices(edge)) & reached for v in vertices(edge)}
                if expanded == reached:
                    break
                reached = expanded
            assert reached == active
        answer.append(dict(form=form, boundary_lengths=lengths,
                           normalized_sphere_links=len(roots), f_vector=[10, 24, 16]))
    return answer


def evaluate():
    source = HERE / 'manifolds_lex_d3_deg5.txt.gz'
    assert sha256(source.read_bytes()).hexdigest() == '41071b36a731396d5273c60748aea7937c876136684ac479971e87e27e2fbb59'
    counts, selected, witnesses = Counter(), [], []
    for index, facets in records(gzip.decompress(source.read_bytes()).decode('ascii')):
        row = inspect(index, facets)
        counts['all_records'] += 1
        if row['f_vector'][0] != 14:
            continue
        counts['order14'] += 1
        found = eligible(facets)
        if found is None:
            continue
        counts['minimum_valence4'] += 1
        assert row['f_vector'][1] <= 57
        selected.append(index)
        witnesses.extend(dict(index=index, **witness) for witness in found)
    assert counts == dict(all_records=4787, order14=111, minimum_valence4=19)
    assert len(witnesses) == 4 and all(w['derivative_value'] == -2 for w in witnesses)
    producer = json.loads((EIGHT / 'negative-free-endpoint-d11-catalog-verification.json').read_text())
    assert selected == [row['index'] for row in producer['retained_manifolds']]
    for actual, expected in zip(witnesses, producer['obstructions']):
        assert all(actual[key] == expected[key] for key in actual)
    return dict(status='INDEPENDENT_PASS', global_status='UNRESOLVED', counts=dict(counts),
                selected_records=selected, witnesses=witnesses, strip_controls=normalized_strips(),
                external_dependency='Frick2015 Theorem3.10 completeness; enumeration not regenerated.',
                sources=[dict(path=str(p), sha256=sha256(p.read_bytes()).hexdigest()) for p in
                         [source, Path(__file__), HERE / 'small_valence_catalog.py',
                          HERE / 'negative_free_endpoint_strips.py',
                          EIGHT / 'negative-free-endpoint-d11-manifest.json']])


if __name__ == '__main__':
    output = HERE / 'endpoint-d11-independent-verification.json'
    assert not output.exists()
    report = evaluate()
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'counts', 'witnesses')}))
