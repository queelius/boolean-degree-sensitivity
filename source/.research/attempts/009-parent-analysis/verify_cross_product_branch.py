"""Rebuild one product branch literally, without the producer's append helper."""
import numpy as np
from verify_finite_function_csp import verify_tree


def verify_branch(tables, relations, domains, points, pairs, vector, tree, normalization):
    assert len(tables)==len(domains) and tables
    assert type(normalization) is int and normalization>0
    assert len(points)==len(vector) and len(set(points))==len(points)
    assert all(type(x) is int and 0<=x<len(relations) for x in points)
    assert all(type(v) is int for v in vector)
    assert len(pairs)==2 and all(len(p)==2 for p in pairs)
    indices=[i for pair in pairs for i in pair]
    assert len(set(indices))==4 and all(type(i) is int and 0<=i<len(tables) for i in indices)
    reconstructed=[]
    for table,domain in zip(tables,domains):
        assert table.ndim==2 and table.shape[1]==len(relations)
        assert domain==sorted(set(domain)) and all(type(i) is int and 0<=i<len(table) for i in domain)
        subset=table[np.asarray(domain,dtype=np.int64)]
        reconstructed.append(np.hstack((subset,subset[:,np.asarray(points,dtype=np.int64)])))
    allowed=list(relations);scale=normalization*normalization
    for x,v in zip(points,vector):
        keep=[]
        for row in relations[x]:
            first=int(row[pairs[0][0]])*int(row[pairs[0][1]])
            second=int(row[pairs[1][0]])*int(row[pairs[1][1]])
            if first==scale*v and second==-scale*v:keep.append(tuple(row))
        allowed.append(keep)
    return verify_tree(reconstructed,allowed,tree)
