from itertools import combinations,product
from parent00_cubic_cycles import cycle_basis,gray_cycles
from multiple_low_cycles import bounded_low_cycles


def degrees(faces,vertices):return {v:sum(bool(q>>v&1) for q in faces) for v in vertices}


def test_low_link_classification_matches_every_six_vertex_cycle():
    vertices=list(range(6));triangles,basis=cycle_basis(vertices)
    for lows in ([0,1],[0,2,4]):
        high=[i for i in vertices if i not in lows]
        for critical in combinations(high,4-len(lows)):
            allowed={i:({0,4,5,6,7} if i in critical else {0,4,5}) for i in high};expected=set()
            for code in gray_cycles(basis):
                faces=tuple(sorted(q for j,q in enumerate(triangles) if code>>j&1));d=degrees(faces,vertices)
                if all(d[i]==3 for i in lows) and all(d[i] in allowed[i] for i in high):expected.add(faces)
            actual=list(bounded_low_cycles(high,lows,allowed,max_faces=20))
            assert len(actual)==len(set(actual)) and set(actual)==expected
            if len(lows)==2:assert expected


def test_full_tetrahedron_components_are_preserved_with_two_or_three_lows():
    high=list(range(6));octa={sum(1<<v for v in triple) for triple in product((0,1),(2,3),(4,5))}
    for lows in ([6,7],[6,7,8]):
        critical=list(range(4-len(lows)));tetra_vertices=lows+critical
        tetra={sum(1<<v for v in t) for t in combinations(tetra_vertices,3)};target=tuple(sorted(octa|tetra))
        allowed={i:({0,4,5,6,7} if i in critical else {0,4,5}) for i in high}
        assert target in set(bounded_low_cycles(high,lows,allowed,max_faces=12))
