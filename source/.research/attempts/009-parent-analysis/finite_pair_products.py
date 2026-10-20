"""Exact selected Cartesian product rows and a literal opposite-apex zero slice."""
import numpy as np


def pair_products(left,right,indices,sign=1):
    left,right,indices=map(np.asarray,(left,right,indices))
    assert left.ndim==right.ndim==2 and left.shape[1]==right.shape[1]
    assert indices.ndim==1 and all(np.issubdtype(a.dtype,np.integer)for a in(left,right,indices))
    assert sign in(-1,1)and all(np.all((a>=-2)&(a<=2))for a in(left,right))
    assert np.all((indices>=0)&(indices<len(left)*len(right)))
    if not len(indices):return np.empty((0,left.shape[1]),dtype=np.int16)
    return sign*left[indices//len(right)].astype(np.int16)*right[indices%len(right)]


def opposite_zero_points(values):
    values=np.asarray(values)
    assert values.ndim==1 and np.issubdtype(values.dtype,np.integer)
    assert len(values)>=4 and len(values)&(len(values)-1)==0
    points=np.arange(2,len(values),4,dtype=np.int64)
    return points[values[points]==0]
