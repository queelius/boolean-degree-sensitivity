"""Exact functional bounds on retained full patterns and compatible core words."""
from numbers import Integral
import numpy as np
from spectrum_dual_functional import simplex_bound


def minimum(functional, tables, domains, features, pools, flags):
    points = len(pools)
    if not points or not tables or not len(tables) == len(domains) == len(features):
        raise ValueError('Require matching nonempty tables, domains, features, and points.')
    if any(not isinstance(f,Integral) or f < 0 for f in features) or len(set(features)) != len(features):
        raise ValueError('Require distinct nonnegative integer features.')
    selected = []; pattern_costs = []; minimizing_rows = []
    for block,(table,domain,feature) in enumerate(zip(tables,domains,features)):
        table = np.asarray(table)
        if table.ndim != 2 or table.shape[1] < points or not np.issubdtype(table.dtype,np.integer):
            raise ValueError('Require integer pattern tables covering every point.')
        if not len(domain) or any(not isinstance(i,Integral) or not 0 <= i < len(table) for i in domain) or len(set(domain)) != len(domain):
            raise ValueError('Require nonempty distinct original domain indices.')
        values = table[list(domain),:points]; selected.append(values)
        costs = functional.pattern_scores(block,values[:,:,None],(feature,))
        pattern_costs.append(costs)
        minimizing_rows.append(int(domain[min(range(len(costs)),key=lambda i:int(costs[i]))]))
    word_costs = []; word_counts = []; word_indices = []; empty = []
    for point,words in enumerate(pools):
        if any(len(word) <= max(features) or any(not isinstance(v,Integral) for v in word) for word in words):
            raise ValueError('Require integer words covering every feature.')
        unary = [set(map(int,values[:,point])) for values in selected]
        kept = [(i,functional.word_score(point,word)) for i,word in enumerate(words)
                if all(word[f] in allowed for f,allowed in zip(features,unary))]
        word_counts.append(len(kept)); word_costs.append([cost for _,cost in kept])
        if kept:
            word_indices.append(min(kept,key=lambda item:item[1])[0])
        else:
            empty.append(point); word_indices.append(None)
    bound = None if empty else simplex_bound(word_costs+pattern_costs,flags,functional.rhs)
    return dict(bound=bound,empty_points=empty,candidate_contradiction=bool(empty) or bound['contradiction'],
                retained_word_counts=word_counts,word_minimizing_indices=word_indices,
                pattern_minimizing_rows=minimizing_rows)
