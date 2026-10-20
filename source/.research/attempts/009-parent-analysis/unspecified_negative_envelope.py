"""Necessary Fourier envelope with unknown positions of four negative doubles."""
from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from baseline_full_truth_model import Row


class Role(Enum):
    SINGLETON_EXTRA='singleton_extra'
    CUBIC_NEGATIVE='cubic_negative'
    QUINTIC_POSITIVE='quintic_positive'
    QUINTIC_NEGATIVE='quintic_negative'


@dataclass(frozen=True)
class Variable:
    support:int
    role:Role


def build_projection(g,known,envelope,core_mask):
    assert 0<=core_mask<16
    core=g['positive_doubles'][0]&g['positive_doubles'][1]
    core_vertices=[v for v in range(14) if core>>v&1]
    selected=sum(1<<v for i,v in enumerate(core_vertices) if core_mask>>i&1)
    outside=envelope['outside'];assert len(outside)==len(set(outside))==10
    assert set(outside)==set(range(14))-set(core_vertices)
    assert all(known[q]==2 for q in g['positive_doubles'])
    supports=[]
    for size in range(6-selected.bit_count()):
        if (size+selected.bit_count())%2==0:continue
        for vs in combinations(range(10),size):
            supports.append((selected|sum(1<<outside[v] for v in vs),sum(1<<v for v in vs)))
    variables=[];expansion={};negative=[];extra=[];rows=[]
    for q,local in supports:
        if q in known:expansion[q]=(known[q],());continue
        degree=q.bit_count();column=len(variables)
        if degree==1:
            variables.append(Variable(q,Role.SINGLETON_EXTRA));extra.append(column);expansion[q]=(1,((column,1),))
        elif degree==3:
            variables.append(Variable(q,Role.CUBIC_NEGATIVE));expansion[q]=(0,((column,-1),))
        else:
            assert degree==5 and q not in g['positive_doubles']
            variables.extend((Variable(q,Role.QUINTIC_POSITIVE),Variable(q,Role.QUINTIC_NEGATIVE)))
            negative.append(column+1);expansion[q]=(0,((column,1),(column+1,-2)))
            rows.append(Row(((column,1),(column+1,1)),0,1,dict(kind='exclusive_quintic_states',support=q)))
    fixed_negative=sum(q.bit_count()==5 and k==-2 for q,k in known.items())
    fixed_extra=sum(k-1 for q,k in known.items() if q.bit_count()==1)
    assert 0<=fixed_negative<=4 and 0<=fixed_extra<=2
    rows.append(Row(tuple((column,1) for column in negative),0,4-fixed_negative,dict(kind='negative_quintic_budget')))
    rows.append(Row(tuple((column,1) for column in extra),0,2-fixed_extra,dict(kind='singleton_extra_budget')))
    for point in range(1024):
        constant=0;terms=[]
        for q,local in supports:
            character=-1 if (local&point).bit_count()%2 else 1
            offset,columns=expansion[q];constant+=character*offset
            terms.extend((column,character*value) for column,value in columns)
        rows.append(Row(tuple(terms),envelope['lower'][point][core_mask]-constant,
                        envelope['upper'][point][core_mask]-constant,
                        dict(kind='core_fourier_envelope',core_mask=core_mask,outside_point=point)))
    return variables,rows
