"""Small necessary interval model for fixed negative cubic supports."""
from itertools import combinations
from baseline_full_truth_model import Row


def build(n,negative,values):
    assert negative==sorted(set(negative)) and all(type(q) is int and 0<q<1<<n and q.bit_count()==3 for q in negative)
    assert len(values)==1<<n and all(v==sorted(set(v)) and v for v in values)
    triples=[sum(1<<i for i in t) for t in combinations(range(n),3)]
    variables=[(1<<i,-1) for i in range(n)]+[(q,1) for q in triples if q not in negative];rows=[]
    for x,allowed in enumerate(values):
        constant=-2*sum((-1)**((q&x).bit_count()) for q in negative)
        terms=tuple((i,sign*(-1)**((q&x).bit_count())) for i,(q,sign) in enumerate(variables))
        rows.append(Row(terms,allowed[0]-constant,allowed[-1]-constant,dict(kind='fixed_cubic_envelope',outside_point=x)))
    return variables,rows
