"""Complete finite vector-sum joins, preserving all input row identities."""
import numpy as np


def join_sums(left,middle,right):
    arrays=list(map(np.asarray,(left,middle,right)))
    if any(a.ndim!=2 or not np.issubdtype(a.dtype,np.integer) for a in arrays):
        raise ValueError('two-dimensional integer vectors required')
    if len({a.shape[1] for a in arrays})!=1:raise ValueError('vector widths differ')
    bounds=[(int(a.min(initial=0)),int(a.max(initial=0))) for a in arrays]
    limit=np.iinfo(np.int64)
    if any(lo<limit.min or hi>limit.max for lo,hi in bounds):raise ValueError('input exceeds int64')
    if bounds[0][0]+bounds[1][0]<limit.min or bounds[0][1]+bounds[1][1]>limit.max:
        raise ValueError('sum exceeds certified int64 range')
    left,middle,right=(a.astype(np.int64) for a in arrays)
    lookup={}
    for k,row in enumerate(right):lookup.setdefault(row.tobytes(),[]).append(k)
    matches=[]
    for i,row in enumerate(left):
        targets=middle+row
        for j,target in enumerate(targets):
            for k in lookup.get(target.tobytes(),()):matches.append((i,j,k))
    return np.asarray(matches,dtype=np.int64).reshape(-1,3)
