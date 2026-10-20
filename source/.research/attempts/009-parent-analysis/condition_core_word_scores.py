"""Exact word-cost minima under complete unary domains and one fixed feature."""
from numbers import Integral


def minima_by_feature(words,costs,unary,marked):
    if len(words)!=len(costs) or not isinstance(marked,Integral) or marked<0:
        raise ValueError('Mismatched words, costs, or marked feature.')
    minima={}
    for word,cost in zip(words,costs):
        if not isinstance(cost,Integral) or marked>=len(word) or any(not isinstance(f,Integral) or not 0<=f<len(word) for f in unary):
            raise ValueError('Require integer costs and valid feature indices.')
        if all(word[feature] in allowed for feature,allowed in unary.items()):
            value=int(word[marked]);minima[value]=min(minima.get(value,int(cost)),int(cost))
    return minima
