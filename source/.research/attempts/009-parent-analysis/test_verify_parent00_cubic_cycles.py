from itertools import combinations
import pytest
from verify_parent00_cubic_cycles import independent_cycles,check_value_witness


def test_independent_cycle_expansion_is_complete_on_five_vertices():
    vertices=list(range(5));triangles=[sum(1<<v for v in t) for t in combinations(vertices,3)]
    codes=independent_cycles(vertices,triangles);expected=set()
    for code in range(1<<len(triangles)):
        if all(sum(bool(code>>i&1) for i,t in enumerate(triangles) if t&p==p)%2==0 for p in [sum(1<<v for v in pair) for pair in combinations(vertices,2)]):expected.add(code)
    assert len(codes)==len(set(codes))==16 and set(codes)==expected


def test_value_failure_is_exact_and_a_true_value_cannot_be_rejected():
    spectrum=[(1,1)];values=[[1],[-1]]
    assert check_value_witness(spectrum,values,None)
    bad=dict(point=0,value=1,allowed=[1])
    with pytest.raises(AssertionError):check_value_witness(spectrum,values,bad)
    excluded=[[0],[-1]];assert not check_value_witness(spectrum,excluded,dict(point=0,value=1,allowed=[0]))
    with pytest.raises(AssertionError):check_value_witness(spectrum,excluded,dict(point=0,value=2,allowed=[0]))
