from itertools import combinations
import pytest
from parent00_cubic_cycles import gray_cycles
from small_link_high_cycles import bounded_high_codes,small_even_links


def test_link_counts_and_pair_parity():
    links=list(small_even_links(list(range(7)),5))
    assert len(links)==393 and len(set(links))==393
    assert all(all(sum(v in e for e in edges)%2==0 for v in range(7)) for edges in links)


def test_bounded_codes_match_complete_six_vertex_space():
    vertices=[0,2,3,5,7,8];faces=[sum(1<<v for v in t) for t in combinations(vertices,3)];lookup={q:i for i,q in enumerate(faces)}
    basis=[sum(1<<lookup[sum(1<<v for v in f)] for f in combinations((vertices[0],)+t,3)) for t in combinations(vertices[1:],3)]
    full=[]
    for code in gray_cycles(basis):
        degree=[sum(bool(code>>j&1) for j,q in enumerate(faces) if q>>v&1) for v in vertices]
        full.append((code,code.bit_count(),degree))
    for anchor in (vertices[0],vertices[-1]):
        for anchor_cap in (3,4,5):
            maxima=[7]*6;maxima[vertices.index(anchor)]=anchor_cap
            for cap in (0,4,8,14):
                expected={c for c,w,d in full if w<=cap and all(a<=b for a,b in zip(d,maxima))}
                actual=list(bounded_high_codes(vertices,anchor,maxima,cap))
                assert len(actual)==len({r[0] for r in actual}) and {r[0] for r in actual}==expected
                for code,count,degree in actual:
                    assert count==code.bit_count()
                    assert degree==[sum(bool(code>>j&1) for j,q in enumerate(faces) if q>>v&1) for v in vertices]
    with pytest.raises(AssertionError):list(bounded_high_codes(vertices,vertices[0],[6]*6,14))
