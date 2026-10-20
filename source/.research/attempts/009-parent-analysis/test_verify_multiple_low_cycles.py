from itertools import combinations
from verify_parent00_cubic_cycles import independent_cycles
from verify_multiple_low_cycles import independent_low_families


def test_independent_restoration_matches_complete_six_vertex_space():
    vertices=list(range(6));high=[0,2,4,5];lows=[1,3]
    triangles=[sum(1<<v for v in t) for t in combinations(vertices,3)];allowed={i:({0,4,5,6,7} if i in (0,2) else {0,4,5}) for i in high}
    masks={v:sum(1<<j for j,q in enumerate(triangles) if q>>v&1) for v in vertices}
    expected={c for c in independent_cycles(vertices,triangles) if all((c&masks[v]).bit_count()==3 for v in lows) and all((c&masks[v]).bit_count() in allowed[v] for v in high)}
    actual=list(independent_low_families(high,lows,allowed,20,triangles,independent_cycles(high,triangles)))
    assert expected and len(actual)==len(set(actual)) and set(actual)==expected
