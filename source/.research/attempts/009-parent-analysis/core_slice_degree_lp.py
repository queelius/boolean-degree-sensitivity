"""Shared word and whole-pattern weights with exact outside-degree equations."""
from dataclasses import dataclass
from collections import Counter
import numpy as np
from baseline_full_truth_model import Row
from joint_core_moments import joint_hull


@dataclass(frozen=True)
class PatternBlock:
    features: tuple
    values: np.ndarray  # pattern x outside input x feature


@dataclass(frozen=True)
class DegreeCap:
    feature: int
    degree: int


@dataclass(frozen=True)
class SliceModel:
    variables: tuple
    word_rows: tuple
    word_features: tuple
    blocks: tuple
    block_offsets: tuple
    caps: tuple
    word_variable_count: int

    @property
    def variable_count(self):return len(self.variables)

    def rows(self):
        yield from self.word_rows
        points=len(self.word_features)
        for ordinal,(block,offset) in enumerate(zip(self.blocks,self.block_offsets)):
            yield Row(tuple((offset+k,1) for k in range(len(block.values))),1,1,
                      dict(kind='slice_pattern_normalization',block=ordinal))
            for j,feature in enumerate(block.features):
                for point in range(points):
                    terms=tuple(self.word_features[point][feature])+tuple(
                        (offset+k,-int(value)) for k,value in enumerate(block.values[:,point,j]) if value)
                    yield Row(terms,0,0,dict(kind='slice_component_link',block=ordinal,feature=feature,point=point))
        for cap in self.caps:
            for character in range(points):
                if character.bit_count()<=cap.degree:continue
                terms=tuple((i,(-1 if (point&character).bit_count()%2 else 1)*value)
                    for point in range(points) for i,value in self.word_features[point][cap.feature])
                yield Row(terms,0,0,dict(kind='slice_degree',feature=cap.feature,
                                       degree=cap.degree,character=character))

    def inventory(self):
        counts=Counter();nonzeros=rows=0
        for row in self.rows():
            counts[row.reason['kind']]+=1;rows+=1;nonzeros+=len(row.terms)
        # Conservative preflight allowance for Python tuples and the phase-I sparse copies.
        estimate=(512<<20)+512*nonzeros+4096*(self.variable_count+rows)+sum(b.values.nbytes for b in self.blocks)
        return dict(variables=self.variable_count,word_variables=self.word_variable_count,
                    pattern_variables=self.variable_count-self.word_variable_count,rows=rows,nonzeros=nonzeros,
                    degree_rows=counts['slice_degree'],rows_by_kind=dict(counts),estimated_peak_bytes=estimate,
                    estimate_is_a_budget_guard_not_measured_memory=True)


def prepare(pools,blocks,caps):
    points=len(pools);assert points>0 and points&(points-1)==0 and all(pools)
    width=len(pools[0][0]);assert width>0 and width&(width-1)==0
    assert all(len(row)==width and all(isinstance(v,(int,np.integer)) for v in row) for pool in pools for row in pool)
    used=set()
    for block in blocks:
        assert block.features and len(set(block.features))==len(block.features)
        assert all(type(f) is int and 0<=f<width and f not in used for f in block.features)
        used.update(block.features)
        assert block.values.ndim==3 and block.values.shape[0]>0
        assert block.values.shape[1:]==(points,len(block.features)) and np.issubdtype(block.values.dtype,np.integer)
    assert len({cap.feature for cap in caps})==len(caps)
    assert all(type(cap.feature) is int and 0<=cap.feature<width and type(cap.degree) is int and cap.degree>=0 for cap in caps)
    integer_pools=[[tuple(map(int,row)) for row in pool] for pool in pools]
    variables,word_rows,features=joint_hull(integer_pools);word_count=len(variables);offsets=[]
    for ordinal,block in enumerate(blocks):
        offsets.append(len(variables))
        variables.extend(dict(kind='slice_pattern_weight',block=ordinal,pattern=k) for k in range(len(block.values)))
    return SliceModel(tuple(variables),tuple(word_rows),tuple(features),tuple(blocks),tuple(offsets),
                      tuple(sorted(caps,key=lambda cap:cap.feature)),word_count)
