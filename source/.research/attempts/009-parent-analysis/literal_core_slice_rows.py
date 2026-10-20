"""Scalar equation reconstruction for slice-degree LP certificates; no solver."""
from collections import Counter
from enum import Enum,auto
import numpy as np


class EquationKind(Enum):
    WORD_NORMALIZATION=auto()
    PATTERN_NORMALIZATION=auto()
    LINK=auto()
    DEGREE=auto()
    BASIS_VALUE=auto()


class DegreeEncoding(Enum):
    VANISHING_CHARACTERS=auto()
    LOW_DEGREE_BASIS=auto()


class LiteralRows:
    def __init__(self,pools,blocks,caps,*,encoding=DegreeEncoding.VANISHING_CHARACTERS):
        self.points=len(pools);assert self.points>0 and self.points&(self.points-1)==0 and all(pools)
        self.pools=[sorted(set(tuple(map(int,row)) for row in pool)) for pool in pools]
        width=len(self.pools[0][0]);assert all(len(row)==width for pool in self.pools for row in pool)
        self.word_offsets=[];count=0
        for pool in self.pools:self.word_offsets.append(count);count+=len(pool)
        self.word_count=count;self.blocks=blocks;self.block_offsets=[];used=set()
        for features,values in blocks:
            assert features and len(set(features))==len(features) and not used & set(features)
            assert all(type(f) is int and 0<=f<width for f in features);used.update(features)
            assert values.ndim==3 and values.shape[0]>0 and values.shape[1:]==(self.points,len(features))
            assert np.issubdtype(values.dtype,np.integer)
            self.block_offsets.append(count);count+=len(values)
        self.pattern_count=count-self.word_count;self.variable_count=count;self.caps=sorted(caps)
        self.encoding=encoding;self.coefficient_blocks=[]
        assert len({f for f,d in caps})==len(caps) and all(type(f) is int and 0<=f<width and type(d) is int and d>=0 for f,d in caps)
        self.requests=[(EquationKind.WORD_NORMALIZATION,(x,)) for x in range(self.points)]
        for k,(features,_) in enumerate(blocks):
            self.requests.append((EquationKind.PATTERN_NORMALIZATION,(k,)))
            self.requests.extend((EquationKind.LINK,(k,j,x)) for j in range(len(features)) for x in range(self.points))
        if encoding is DegreeEncoding.VANISHING_CHARACTERS:
            self.requests.extend((EquationKind.DEGREE,(feature,character)) for feature,degree in self.caps
                                 for character in range(self.points) if character.bit_count()>degree)
        else:
            assert encoding is DegreeEncoding.LOW_DEGREE_BASIS
            for ordinal,(feature,degree) in enumerate(self.caps):
                bound=max(abs(state[feature]) for pool in self.pools for state in pool)
                characters=[s for s in range(self.points) if s.bit_count()<=degree] if bound else []
                self.coefficient_blocks.append(dict(feature=feature,degree=degree,bound=bound,
                    characters=characters,offset=self.variable_count))
                self.variable_count+=len(characters)
                if bound:self.requests.extend((EquationKind.BASIS_VALUE,(ordinal,x)) for x in range(self.points))
        self.row_count=len(self.requests)

    def row(self,index):
        assert type(index) is int and 0<=index<self.row_count
        kind,args=self.requests[index]
        if kind is EquationKind.WORD_NORMALIZATION:
            x,=args;return {self.word_offsets[x]+k:1 for k in range(len(self.pools[x]))},1,1
        if kind is EquationKind.PATTERN_NORMALIZATION:
            block,=args;return {self.block_offsets[block]+k:1 for k in range(len(self.blocks[block][1]))},1,1
        terms={}
        if kind is EquationKind.LINK:
            block,j,x=args;features,values=self.blocks[block];feature=features[j]
            for k,state in enumerate(self.pools[x]):
                if state[feature]:terms[self.word_offsets[x]+k]=state[feature]
            for k in range(len(values)):
                value=-int(values[k,x,j])
                if value:terms[self.block_offsets[block]+k]=value
        elif kind is EquationKind.DEGREE:
            feature,character=args
            for x,pool in enumerate(self.pools):
                sign=-1 if (x&character).bit_count()%2 else 1
                for k,state in enumerate(pool):
                    if state[feature]:terms[self.word_offsets[x]+k]=sign*state[feature]
        else:
            assert kind is EquationKind.BASIS_VALUE;ordinal,x=args
            block=self.coefficient_blocks[ordinal];feature=block['feature'];target=0
            for k,s in enumerate(block['characters']):
                signed=block['bound']*(-1 if (x&s).bit_count()%2 else 1)
                target+=signed;terms[block['offset']+k]=2*signed
            for k,state in enumerate(self.pools[x]):
                if state[feature]:terms[self.word_offsets[x]+k]=-state[feature]
            return terms,target,target
        return terms,0,0

    def inventory(self):
        return dict(variables=self.variable_count,word_variables=self.word_count,
            pattern_variables=self.pattern_count,coefficient_variables=self.variable_count-self.word_count-self.pattern_count,
            rows=self.row_count,
            nonzeros=sum(len(self.row(i)[0]) for i in range(self.row_count)),
            degree_rows=sum(kind is EquationKind.DEGREE for kind,_ in self.requests),
            degree_value_rows=sum(kind is EquationKind.BASIS_VALUE for kind,_ in self.requests))

    def verify(self,certificate):
        residual=Counter();rhs=0
        for index,side,multiplier in certificate['terms']:
            assert side in (-1,1) and type(multiplier) is int and multiplier>0
            terms,low,high=self.row(index);rhs+=multiplier*(high if side==1 else -low)
            for column,value in terms.items():residual[column]+=side*multiplier*value
        for column,side,multiplier in certificate['box_terms']:
            assert type(column) is int and 0<=column<self.variable_count and side in (-1,1)
            assert type(multiplier) is int and multiplier>0
            residual[column]+=side*multiplier
            if side==1:rhs+=multiplier
        assert all(value==0 for value in residual.values()) and rhs<0 and rhs==certificate['integer_rhs']
        return rhs
