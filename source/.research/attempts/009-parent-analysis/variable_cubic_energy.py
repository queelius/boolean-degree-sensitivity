"""Coefficient-consistent cubic interval and finite-value energy relaxation."""
from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from baseline_full_truth_model import Row


class CubicKind(Enum):
    LINEAR='negative_linear_flag'
    POSITIVE='positive_triangle_flag'
    NEGATIVE='negative_double_triangle_flag'
    VALUE='finite_value_weight'


@dataclass(frozen=True)
class CubicVariable:
    kind:CubicKind
    support:int=0
    point:int=-1
    value:int=0

    def metadata(self):return dict(kind=self.kind.value,support=self.support,point=self.point,value=self.value)


def build(n,negative_count,values,energy=True):
    assert negative_count in (1,2) and len(values)==1<<n and all(v and list(v)==sorted(set(v)) for v in values)
    assert all(list(values[x^((1<<n)-1)])==sorted(-v for v in values[x]) for x in range(1<<n))
    triples=[sum(1<<i for i in t) for t in combinations(range(n),3)]
    variables=[CubicVariable(CubicKind.LINEAR,1<<i) for i in range(n)]
    variables.extend(CubicVariable(CubicKind.POSITIVE,q) for q in triples);variables.extend(CubicVariable(CubicKind.NEGATIVE,q) for q in triples)
    base_count=len(variables);positive=list(range(n,n+len(triples)));negative=list(range(n+len(triples),base_count))
    rows=[Row(tuple((i,1) for i in negative),negative_count,negative_count,dict(kind='negative_triangle_count'))]
    for q,p,m in zip(triples,positive,negative):rows.append(Row(((p,1),(m,1)),0,1,dict(kind='exclusive_triangle_states',support=q)))
    signs={CubicKind.LINEAR:-1,CubicKind.POSITIVE:1,CubicKind.NEGATIVE:-2};expressions=[]
    for x,allowed in enumerate(values):
        terms=tuple((i,signs[v.kind]*(-1 if (v.support&x).bit_count()%2 else 1)) for i,v in enumerate(variables[:base_count]));expressions.append(terms)
        rows.append(Row(terms,allowed[0],allowed[-1],dict(kind='variable_cubic_interval',outside_point=x)))
    if energy:
        total=[];constant=0;half=1<<(n-1)
        for x in range(half):
            if len({v*v for v in values[x]})==1:constant+=values[x][0]**2;continue
            columns=[]
            for value in values[x]:
                columns.append(len(variables));variables.append(CubicVariable(CubicKind.VALUE,point=x,value=value));total.append((columns[-1],value*value))
            rows.append(Row(tuple((i,1) for i in columns),1,1,dict(kind='value_normalization',outside_point=x)))
            rows.append(Row(expressions[x]+tuple((i,-v) for i,v in zip(columns,values[x])),0,0,dict(kind='cubic_value_link',outside_point=x)))
        total.extend((i,-half) for i in list(range(n))+positive)
        target=half*4*negative_count-constant
        rows.append(Row(tuple(total),target,target,dict(kind='variable_cubic_parseval')))
    return variables,rows
