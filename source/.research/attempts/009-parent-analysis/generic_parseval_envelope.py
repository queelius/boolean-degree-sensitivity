"""Necessary exact Parseval lifts for arbitrary core Fourier characters."""
from dataclasses import dataclass
import numpy as np
from baseline_full_truth_model import Row
from unspecified_negative_envelope import Role
from energy_pattern_envelope import LiftKind,LiftVariable,value_hull_rows
from core_fourier_envelope import core_words
from two_positive_four_cube_domains import setup


@dataclass(frozen=True)
class ValueState:
    core_mask:int
    outside_point:int
    value:int
    kind:str='generic_fourier_value_state'

    def metadata(self):return dict(kind=self.kind,core_mask=self.core_mask,outside_point=self.outside_point,value=self.value)


def norm_affine(variables,known,core,selected):
    constant=sum(k*k for q,k in known.items() if q&core==selected);terms=[]
    for i,v in enumerate(variables):
        assert v.support&core==selected
        if v.role==Role.SINGLETON_EXTRA:constant+=1;weight=3
        elif v.role in (Role.CUBIC_NEGATIVE,Role.QUINTIC_POSITIVE):weight=1
        else:assert v.role==Role.QUINTIC_NEGATIVE;weight=4
        terms.append((i,weight))
    return constant,terms


def lift_block(variables,base_rows,values,known,core,selected,core_mask):
    assert len(values)==1024
    lifted=[LiftVariable(LiftKind.COEFFICIENT,coefficient=v) for v in variables];rows=list(base_rows)
    point_rows={r.reason['outside_point']:r for r in base_rows if r.reason['kind']=='core_fourier_envelope'}
    parity=1 if core_mask.bit_count()%2 else -1;energy=[];fixed=0
    for point in range(512):
        assert values[point]==sorted(set(values[point])) and values[point]
        assert sorted(parity*v for v in values[point])==values[point^1023]
        squares={v*v for v in values[point]}
        if len(squares)==1:fixed+=next(iter(squares));continue
        columns=[]
        for value in values[point]:columns.append(len(lifted));lifted.append(ValueState(core_mask,point,value))
        row=point_rows[point];extra,terms=value_hull_rows(row.terms,values[point][0]-row.lower,values[point],columns,point)
        rows.extend(extra);energy.extend(terms)
    constant,terms=norm_affine(variables,known,core,selected)
    energy.extend((i,-512*k) for i,k in terms);target=512*constant-fixed
    rows.append(Row(tuple(energy),target,target,dict(kind='generic_core_parseval',core_mask=core_mask)))
    return lifted,rows


def permitted(g,domains,cubes,masks):
    pairs,_=setup(g);words,truth,delta,ts,sums=core_words(pairs)
    row_sets=[sum(1<<i for i in d['rows']) for d in domains];cache={};result={m:[] for m in masks}
    for point in range(1024):
        available=tuple(tuple(k-2 for k,part in enumerate(cubes.partitions(point)) if rows&part) for rows in row_sets)
        signature=point.bit_count(),(1,0,0,-1)[point&3],available
        if signature not in cache:
            weight,d,possibilities=signature;live=delta==d
            for i,p in enumerate(possibilities):live&=np.isin(ts[:,i],p)
            for y in range(16):
                if weight+y.bit_count() in (0,12,13):live&=truth[:,y]==0
                elif weight+y.bit_count() in (1,2,14):live&=truth[:,y]==1
            assert np.any(live);cache[signature]={m:sorted(set(map(int,sums[live,m]))) for m in masks}
        for m in masks:result[m].append(cache[signature][m])
    return result


def global_budgets(variables,known):
    limits={Role.SINGLETON_EXTRA:2-sum(k-1 for q,k in known.items() if q.bit_count()==1),
            Role.CUBIC_NEGATIVE:104-sum(k==-1 for q,k in known.items() if q.bit_count()==3),
            Role.QUINTIC_POSITIVE:108-sum(k==1 for q,k in known.items() if q.bit_count()==5),
            Role.QUINTIC_NEGATIVE:4-sum(k==-2 for q,k in known.items() if q.bit_count()==5)}
    rows=[]
    for role,limit in limits.items():
        assert limit>=0
        terms=tuple((i,1) for i,v in enumerate(variables) if v.kind==LiftKind.COEFFICIENT and v.coefficient.role==role)
        rows.append(Row(terms,0,limit,dict(kind='global_coefficient_budget',role=role.value)))
    return rows
