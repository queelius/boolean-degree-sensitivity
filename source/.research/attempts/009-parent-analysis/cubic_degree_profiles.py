"""Necessary triangle-degree profiles from scalar singleton values and pair parity."""
from itertools import product
from math import comb


def degree_options(n,negative,singletons):
    assert len(singletons)==n and negative==sorted(set(negative)) and all(q.bit_count()==3 and 0<q<1<<n for q in negative)
    result=[]
    for i,values in enumerate(singletons):
        assert values and values==sorted(set(values)) and all((4-v)%2==0 for v in values)
        incident=sum(bool(q>>i&1) for q in negative);choices=set()
        for value in values:
            for linear in (0,1):
                degree=(4-value)//2+2*incident+linear
                if 0<=degree<=comb(n-1,2) and degree not in (1,2):choices.add((degree,linear))
        assert choices;result.append(sorted(choices))
    return result


def degree_profiles(n,negative,singletons):
    result=[]
    for chosen in product(*degree_options(n,negative,singletons)):
        degrees=[d for d,u in chosen];linear=[u for d,u in chosen];Q=sum(linear);P=Q+4+2*len(negative)
        if Q%2 or sum(degrees)!=3*P:continue
        result.append(dict(degrees=degrees,linear=linear,linear_count=Q,positive_count=P))
    return result


def low_degree_cycle_bound(degrees):
    """A necessary bound for an even-pair triangle family, not arbitrary graphs."""
    assert all(type(d) is int and (d==0 or d>=3) for d in degrees) and sum(degrees)%3==0
    faces=sum(degrees)//3;vertices=sum(d>0 for d in degrees)
    if max(degrees,default=0)>5:return None
    assert faces%2==0;chi=vertices-faces//2;assert chi>=0 and (chi>0 or faces==0)
    minimum=4*(chi//2)+10*(chi%2)
    return dict(vertices=vertices,faces=faces,euler_characteristic=chi,minimum_faces=minimum,excluded=faces<minimum)
