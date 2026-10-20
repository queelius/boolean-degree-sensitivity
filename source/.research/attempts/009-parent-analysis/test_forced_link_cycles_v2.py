from itertools import combinations,product
import pytest
from forced_link_cycles_v2 import bounded_forced_cycles
from verify_forced_link_cycles import independent_forced_cycles
from verify_parent00_cubic_cycles import independent_cycles


def test_all_six_vertex_cycles_for_zero_through_four_forced_links():
    vertices=list(range(6));triangles=[sum(1<<v for v in t) for t in combinations(vertices,3)]
    incidence={v:sum(1<<j for j,q in enumerate(triangles) if q>>v&1) for v in vertices}
    ambient=independent_cycles(vertices,triangles)
    for k in range(5):
        lows=vertices[:k];high=vertices[k:];base=independent_cycles(high,triangles)
        for c in range(min(4-k,len(high))+1):
            for critical in combinations(high,c):
                allowed={v:({0,4,5,6,7} if v in critical else {0,4,5}) for v in high}
                degree_filtered=[code for code in ambient if all((code&incidence[v]).bit_count()==3 for v in lows) and all((code&incidence[v]).bit_count() in allowed[v] for v in high)]
                for cap in (0,4,8,20):
                    expected={code for code in degree_filtered if code.bit_count()<=cap}
                    expected_faces={tuple(sorted(q for j,q in enumerate(triangles) if code>>j&1)) for code in expected}
                    producer=list(bounded_forced_cycles(high,lows,allowed,cap))
                    reader=list(independent_forced_cycles(high,lows,allowed,cap,triangles,base))
                    assert len(producer)==len(set(producer)) and set(producer)==expected_faces
                    assert len(reader)==len(set(reader)) and set(reader)==expected


def test_tetrahedron_components_with_one_through_four_forced_vertices():
    high=list(range(6));octa={sum(1<<v for v in t) for t in product((0,1),(2,3),(4,5))}
    for k in range(1,5):
        lows=list(range(6,6+k));critical=high[:4-k]
        tetra={sum(1<<v for v in t) for t in combinations(lows+critical,3)}
        target=tuple(sorted(octa|tetra));allowed={v:({0,4,5,6,7} if v in critical else {0,4,5}) for v in high}
        assert target in set(bounded_forced_cycles(high,lows,allowed,12))


def test_unsupported_degree_regime_rejected():
    with pytest.raises(AssertionError):list(bounded_forced_cycles([0,1,2],[3,4],{v:{0,4,6} for v in [0,1,2]},12))
    with pytest.raises(AssertionError):list(bounded_forced_cycles([0,1,2],[],{v:{3} for v in [0,1,2]},12))
