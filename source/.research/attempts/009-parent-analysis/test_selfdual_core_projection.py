"""A face character must map bijectively to its odd full-cube coefficient."""
from importlib.util import find_spec
from itertools import combinations
import pytest


def project(*args,**kwargs):
    assert find_spec('selfdual_core_projection') is not None, 'self-dual coefficient projection is missing'
    from selfdual_core_projection import projected_coefficients
    return projected_coefficients(*args,**kwargs)


@pytest.mark.parametrize('core,outside,degree',[
    ([0,2],[1,3,4],3),([0,9,11,12],[10,13,1,2,3,4,5,6,7,8],5)])
def test_exact_bijection_covers_every_relevant_odd_support(core,outside,degree):
    defaults={d:(-1,1) for d in range(1,degree+1,2)}
    records=project(core,outside,degree,{},defaults);n=len(core)+len(outside);mask=sum(1<<v for v in core)
    expected={s for s in range(1<<n) if s.bit_count()%2 and s.bit_count()<=degree and (s&mask).bit_count()<=1}
    assert {r.support for r in records}==expected and len(records)==len(expected)
    for r in records:
        assert sum(1<<core[i] for i in range(len(core)) if r.feature>>i&1)==r.support&mask
        for x in range(1<<(len(outside)-1)):
            full=sum(1<<v for i,v in enumerate(outside[:-1]) if x>>i&1)
            assert (r.support&full).bit_count()%2==(r.character&x).bit_count()%2
        outside_support=r.support&~mask
        assert outside_support.bit_count()%2==(1-r.feature.bit_count())%2


def test_current_geometry_has_one_fixed_negative_in_the_five_unknown_blocks():
    core=[0,9,11,12];outside=[10,13,1,2,3,4,5,6,7,8]
    fixed={7216:-2,9731:-2,10764:-2,12736:-2,7681:2,14849:2}
    records=project(core,outside,5,fixed,{1:(1,2),3:(-1,0),5:(0,1)})
    assert len(records)==1406 and sum(len(r.values)==2 for r in records)==1405
    exceptions=[r for r in records if len(r.values)==1]
    assert len(exceptions)==1 and exceptions[0].support==12736 and exceptions[0].feature==8 and exceptions[0].values==(-2,)
    assert sum(r.support.bit_count()==1 for r in records)==14


@pytest.mark.parametrize('fault',['overlap','missing_coordinate','even_degree','missing_domain','noninteger_fixed'])
def test_bad_projection_hypotheses_are_rejected(fault):
    core=[0,1];outside=[2,3];degree=3;fixed={};defaults={1:(1,2),3:(-1,0)}
    if fault=='overlap':outside=[1,3]
    elif fault=='missing_coordinate':outside=[2,4]
    elif fault=='even_degree':degree=2
    elif fault=='missing_domain':defaults.pop(3)
    else:fixed={1:0.5}
    with pytest.raises(ValueError):project(core,outside,degree,fixed,defaults)
