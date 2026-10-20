"""Exact cross-intersection support using packed positive-family signatures."""
import numpy as np


def family_masks(features):
    assert features.ndim==2 and 1<=features.shape[1]<=64 and np.all((features==0)|(features==1))
    weights=np.array([1<<i for i in range(features.shape[1])],dtype=np.uint64)
    return features.astype(np.uint64)@weights


def forbidden_masks(features,triples):
    assert features.shape[1]==len(triples)and len(set(triples))==len(triples)
    assert all(type(t)is int and t.bit_count()==3 for t in triples)
    assert np.all((features==0)|(features==1))
    disjoint=np.array([[int(not a&c)for c in triples]for a in triples],dtype=np.int16)
    forbidden=features.astype(np.int16)@disjoint>0
    return family_masks(forbidden)


def filter_pair(left_masks,right_forbidden,left_indices,right_indices,*,block_size=256):
    assert type(block_size)is int and block_size>0
    assert left_masks.ndim==right_forbidden.ndim==1 and left_masks.dtype==right_forbidden.dtype==np.uint64
    assert all(isinstance(i,(int,np.integer))and 0<=i<len(left_masks)for i in left_indices)
    assert all(isinstance(i,(int,np.integer))and 0<=i<len(right_forbidden)for i in right_indices)
    li=np.array(left_indices,dtype=np.int64);ri=np.array(right_indices,dtype=np.int64)
    assert len(set(map(int,li)))==len(li)and len(set(map(int,ri)))==len(ri)
    left,linverse=np.unique(left_masks[li],return_inverse=True)
    right,rinverse=np.unique(right_forbidden[ri],return_inverse=True)
    lkeep=np.zeros(len(left),dtype=bool);rkeep=np.zeros(len(right),dtype=bool)
    for start in range(0,len(left),block_size):
        compatible=(left[start:start+block_size,None]&right[None,:])==0
        lkeep[start:start+block_size]=np.any(compatible,axis=1)
        rkeep|=np.any(compatible,axis=0)
    return li[lkeep[linverse]],ri[rkeep[rinverse]]


def cover_features(mask,other_masks):
    mask=int(mask);assert 0<=mask<1<<64 and other_masks.ndim==1 and other_masks.dtype==np.uint64
    possible=np.unique(other_masks);points=[];options=[i for i in range(64)if mask>>i&1]
    while len(possible):
        score,point=max(((int(np.count_nonzero(possible&np.uint64(1<<i))),i)for i in options),default=(0,-1))
        assert score>0
        points.append(point);possible=possible[(possible&np.uint64(1<<point))==0]
    return points
