"""Necessary exact integer signatures and a complete equality join.

Moments can collide. A missing signature match excludes a pair; a match
establishes neither product equality nor a Boolean construction.
"""
from dataclasses import dataclass
import numpy as np


def product_signatures(left, right, weights, product_sign=1):
    left, right, weights = map(np.asarray, (left, right, weights))
    if (any(a.ndim != 2 or not np.issubdtype(a.dtype, np.integer) for a in (left,right,weights))
            or left.shape[1] != right.shape[1] or weights.shape[1] != left.shape[1]
            or not weights.shape[0] or product_sign not in (-1,1)
            or not np.all(np.isin(weights, [-1,1]))):
        raise ValueError('integer tables of matching width, +/-1 weights, and sign required')
    # Bound absolute sums before casting: every partial sum then fits too.
    maxima = [max(abs(int(a.min(initial=0))),abs(int(a.max(initial=0)))) for a in (left,right)]
    bound = maxima[0]*maxima[1]
    if max(maxima) > np.iinfo(np.int16).max or left.shape[1]*max(bound, bound*bound) > np.iinfo(np.int16).max:
        raise ValueError('signature exceeds certified int16 bound')
    left, right, weights = (a.astype(np.int32) for a in (left,right,weights))
    result = np.empty((len(left),len(right),len(weights)+1), dtype=np.int16)
    result[:,:,0] = (left*left) @ (right*right).T
    for k, weight in enumerate(weights):
        result[:,:,k+1] = product_sign*((left*weight) @ right.T)
    return result.reshape(len(left)*len(right),len(weights)+1)


@dataclass
class SignatureJoin:
    signatures: np.ndarray
    left_indices: np.ndarray
    right_indices: np.ndarray
    left_groups: np.ndarray
    right_groups: np.ndarray


def join_signatures(left, right):
    left, right = map(np.asarray, (left,right))
    if left.ndim != 2 or right.ndim != 2 or left.shape[1] != right.shape[1] or left.dtype != right.dtype:
        raise ValueError('signature arrays must have matching widths and dtypes')
    width = left.shape[1]
    def unique_rows(values):
        packed = np.ascontiguousarray(values).view(np.dtype((np.void,values.dtype.itemsize*width))).ravel()
        return np.unique(packed, return_inverse=True)
    lu, li = unique_rows(left); ru, ri = unique_rows(right)
    common, lk, rk = np.intersect1d(lu,ru,assume_unique=True,return_indices=True)
    lm = np.full(len(lu),-1,dtype=np.int64); rm = np.full(len(ru),-1,dtype=np.int64)
    lm[lk] = np.arange(len(common)); rm[rk] = np.arange(len(common))
    lg, rg = lm[li], rm[ri]; left_indices = np.flatnonzero(lg>=0); right_indices = np.flatnonzero(rg>=0)
    return SignatureJoin(common.view(left.dtype).reshape(len(common),width), left_indices, right_indices,
                         lg[left_indices], rg[right_indices])
