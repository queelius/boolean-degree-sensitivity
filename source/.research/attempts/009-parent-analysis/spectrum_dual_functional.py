"""Exact row functionals on full-spectrum words, patterns, and bounded flags."""
from collections import defaultdict
from dataclasses import dataclass
from math import lcm
from numbers import Integral
import numpy as np


@dataclass(frozen=True)
class Category:
    block: int
    point: int
    features: tuple
    values: tuple
    weight: int


@dataclass(frozen=True)
class Functional:
    coefficients: tuple
    rhs: int
    word_normalizations: dict
    pattern_normalizations: dict
    value_weights: dict
    moment_weights: dict
    categories_by_point: dict
    categories_by_block: dict

    def word_score(self,point,features):
        score=self.word_normalizations.get(point,0)
        for feature,weight in self.value_weights.get(point,()):
            score-=weight*int(features[feature])
        for feature,weight in self.moment_weights.items():
            score+=weight*int(features[feature])**2
        for category in self.categories_by_point.get(point,()):
            if tuple(int(features[f]) for f in category.features)==category.values:
                score+=category.weight
        return score

    def pattern_scores(self,block,values,features):
        values=np.asarray(values)
        if values.ndim!=3 or values.shape[2]!=len(features) or not np.issubdtype(values.dtype,np.integer):
            raise ValueError('Require integer pattern x point x feature values.')
        positions={feature:i for i,feature in enumerate(features)}
        categories=self.categories_by_block.get(block,())
        constant=self.pattern_normalizations.get(block,0)
        bound=abs(constant)+sum(abs(c.weight) for c in categories)
        dtype=np.int64 if bound<=np.iinfo(np.int64).max else object
        scores=np.full(len(values),constant,dtype=dtype)
        for category in categories:
            if category.point>=values.shape[1] or not set(category.features)<=positions.keys():
                raise ValueError('Pattern values omit a required coordinate.')
            mask=np.ones(len(values),dtype=bool)
            for feature,value in zip(category.features,category.values):
                mask &= values[:,category.point,positions[feature]]==value
            scores[mask]-=category.weight
        return scores


def lift_multipliers(divisors, terms):
    if any(not isinstance(d,Integral) or d<=0 for d in divisors):
        raise ValueError('Require positive integer row divisors.')
    scale=lcm(*(int(d) for d in divisors))
    weights=[0]*len(divisors)
    for index,sign,multiplier in terms:
        if not isinstance(index,Integral) or not 0<=index<len(divisors) or sign not in (-1,1) or not isinstance(multiplier,Integral) or multiplier<=0:
            raise ValueError('Invalid signed row multiplier.')
        weights[index]+=int(sign)*int(multiplier)*(scale//int(divisors[index]))
    return scale,tuple(weights)


def compile_functional(rows, variable_count, weights):
    rows=tuple(rows);weights=tuple(weights)
    if len(rows)!=len(weights) or any(not isinstance(w,Integral) for w in weights):
        raise ValueError('Require one integer weight per row.')
    columns=[0]*variable_count;rhs=0;wn=defaultdict(int);pn=defaultdict(int)
    values=defaultdict(list);moments=defaultdict(int);by_point=defaultdict(list);by_block=defaultdict(list)
    for row,weight in zip(rows,weights):
        weight=int(weight)
        if row.lower!=row.upper or not isinstance(row.upper,Integral):
            raise ValueError('Only exact integer equalities define this extension.')
        rhs+=weight*int(row.upper)
        for j,a in row.terms:
            if not isinstance(j,Integral) or not 0<=j<variable_count or not isinstance(a,Integral):
                raise ValueError('Invalid integer matrix column.')
            columns[int(j)]+=weight*int(a)
        reason=row.reason;kind=reason['kind']
        if kind=='joint_word_normalization':wn[reason['outside_point']]+=weight
        elif kind=='slice_pattern_normalization':pn[reason['block']]+=weight
        elif kind=='slice_tuple_distribution':
            category=Category(reason['block'],reason['point'],tuple(reason['features']),tuple(reason['value']),weight)
            if len(category.features)!=len(category.values):raise ValueError('Mismatched categorical tuple.')
            if weight:
                by_point[category.point].append(category);by_block[category.block].append(category)
        elif kind=='bounded_spectrum_value':values[reason['point']].append((reason['feature'],weight))
        elif kind=='bounded_spectrum_parseval':moments[reason['feature']]+=weight
        elif kind=='bounded_spectrum_total':pass
        else:raise ValueError('Unsupported row kind: '+str(kind))
    return Functional(tuple(columns),rhs,dict(wn),dict(pn),dict(values),dict(moments),dict(by_point),dict(by_block))


def simplex_bound(groups, flag_costs, rhs):
    if not isinstance(rhs,Integral):raise ValueError('Require an integer right-hand side.')
    minimums=[];minimizers=[]
    for group in groups:
        if len(group)==0 or any(not isinstance(c,Integral) for c in group):
            raise ValueError('Require nonempty complete integer cost groups.')
        index=min(range(len(group)),key=lambda i:int(group[i]))
        minimums.append(int(group[index]));minimizers.append(index)
    if any(not isinstance(c,Integral) for c in flag_costs):raise ValueError('Require integer flag costs.')
    flag_minimum=sum(min(0,int(c)) for c in flag_costs)
    bound=sum(minimums)+flag_minimum
    return dict(minimums=minimums,minimizers=minimizers,flag_minimum=flag_minimum,
        lower_bound=bound,rhs=int(rhs),gap=bound-int(rhs),contradiction=bound>rhs)
