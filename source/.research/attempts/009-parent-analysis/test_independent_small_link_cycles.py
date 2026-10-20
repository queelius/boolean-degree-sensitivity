from itertools import combinations
from parent00_cubic_cycles import gray_cycles
from independent_small_link_cycles import literal_bounded_high_cycles


def test_independent_links_match_complete_six_vertex_space():
    high=list(range(6));triangles=[sum(1<<i for i in t) for t in combinations(range(8),3)];indices={q:j for j,q in enumerate(triangles)}
    basis=[sum(1<<indices[sum(1<<i for i in f)] for f in combinations((0,)+t,3)) for t in combinations(high[1:],3)]
    for maximum in ([5]*6,[4,5,3,5,5,5]):
        for cap in (4,8,14):
            expected={code for code in gray_cycles(basis) if code.bit_count()<=cap and all(sum(bool(code>>j&1) for j,q in enumerate(triangles) if q>>v&1)<=maximum[v] for v in high)}
            actual=list(literal_bounded_high_cycles(high,5,maximum,cap,triangles))
            assert len(actual)==len(set(actual)) and set(actual)==expected
