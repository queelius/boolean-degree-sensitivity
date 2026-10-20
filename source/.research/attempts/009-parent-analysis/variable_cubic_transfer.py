"""Reuse a verified interval Farkas identity when only scalar bounds change."""
from dataclasses import dataclass,asdict
from collections import Counter
from math import comb
from verify_variable_cubic_certificate import rebuild,verify


@dataclass(frozen=True)
class IntervalIdentity:
    constant:int
    negative_count_weight:int
    lower_weights:tuple
    upper_weights:tuple

    def metadata(self):return asdict(self)

    def evaluate(self,values,N):
        return self.constant+self.negative_count_weight*N+sum(w*values[x][0] for x,w in self.lower_weights)+sum(w*values[x][-1] for x,w in self.upper_weights)

    def points(self):return sorted({x for x,w in self.lower_weights+self.upper_weights})


def extract(record,n=10):
    assert record['energy'] is False and record['result']['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
    variables,rows=rebuild(n,record['negative_count'],record['values'],False);assert variables==record['variables']
    certificate=record['result']['certificate'];verify(variables,rows,certificate)
    constant=0;Nweight=0;lower=Counter();upper=Counter();offset=1+comb(n,3)
    for index,side,multiplier in certificate['terms']:
        if index==0:Nweight+=side*multiplier
        elif index<offset:
            if side==1:constant+=multiplier
        elif side==1:upper[index-offset]+=multiplier
        else:lower[index-offset]-=multiplier
    constant+=sum(multiplier for i,side,multiplier in certificate['box_terms'] if side==1)
    result=IntervalIdentity(constant,Nweight,tuple(sorted(lower.items())),tuple(sorted(upper.items())))
    assert result.evaluate(record['values'],record['negative_count'])==certificate['integer_rhs'];return result
