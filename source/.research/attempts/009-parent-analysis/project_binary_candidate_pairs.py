"""Project a complete selected-pair cover to bijectively reindexed row domains."""
import numpy as np


def project_pairs(parent_left,parent_right,indices,labels,kept,retained_left,retained_right):
    for rows in (parent_left,parent_right,retained_left,retained_right):
        assert len(rows)==len(set(rows)) and all(type(i) is int and i>=0 for i in rows)
    assert indices.ndim==labels.ndim==1 and len(indices)==len(labels)
    assert np.issubdtype(indices.dtype,np.integer) and np.issubdtype(labels.dtype,np.integer)
    assert np.all(indices>=0) and np.all(indices<len(parent_left)*len(parent_right))
    assert np.all(labels>=0) and all(type(k) is int and k>=0 for k in kept)
    left={row:i for i,row in enumerate(retained_left)};right={row:i for i,row in enumerate(retained_right)}
    result=[]
    for flat,label in zip(indices,labels):
        if int(label) not in kept:continue
        a,c=divmod(int(flat),len(parent_right));u,v=parent_left[a],parent_right[c]
        assert u in left and v in right
        result.append((left[u],right[v]))
    assert {u for u,v in result}==set(range(len(left))) and {v for u,v in result}==set(range(len(right)))
    return np.asarray(result,dtype=np.int64).reshape(-1,2)
