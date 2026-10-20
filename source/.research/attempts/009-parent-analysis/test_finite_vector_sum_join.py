"""Catch omitted sums, lost duplicate row IDs, false matches, and overflow."""
import importlib
from itertools import product
import numpy as np
import pytest


def producer():return importlib.import_module('finite_vector_sum_join').join_sums
def checker():return importlib.import_module('verify_vector_sum_join').verify_sums


def test_positive_negative_and_duplicate_vectors_preserve_every_row_id():
    left=np.array([[1,0],[1,0],[-1,2]],dtype=np.int16)
    middle=np.array([[0,1],[0,1],[2,-1]],dtype=np.int16)
    right=np.array([[1,1],[1,1],[3,-1]],dtype=np.int16)
    want=[[0,0,0],[0,0,1],[0,1,0],[0,1,1],[0,2,2],
          [1,0,0],[1,0,1],[1,1,0],[1,1,1],[1,2,2],[2,2,0],[2,2,1]]
    actual=producer()(left,middle,right)
    assert actual.dtype==np.int64 and actual.tolist()==want
    assert checker()(left,middle,right,actual)==dict(cartesian_pairs_checked=9,matching_triples=12)


def test_empty_match_and_empty_domains_are_complete_covers():
    one=np.array([[1,2]],dtype=np.int16);zero=np.zeros_like(one)
    for left,middle,right in ((one,one,zero),(one[:0],one,one),(one,one[:0],one),(one,one,one[:0])):
        actual=producer()(left,middle,right)
        assert actual.shape==(0,3)
        assert checker()(left,middle,right,actual)==dict(cartesian_pairs_checked=len(left)*len(middle),matching_triples=0)


def test_exact_sums_match_independent_small_cartesian_exhaustion():
    rng=np.random.default_rng(467)
    for _ in range(20):
        left=rng.integers(-3,4,(4,3),dtype=np.int16)
        middle=rng.integers(-3,4,(5,3),dtype=np.int16)
        right=rng.integers(-4,5,(6,3),dtype=np.int16)
        right[0]=left[0].astype(np.int32)+middle[0].astype(np.int32)
        want=[[i,j,k] for i,j,k in product(range(4),range(5),range(6))
              if all(int(x)+int(y)==int(z) for x,y,z in zip(left[i],middle[j],right[k]))]
        actual=producer()(left,middle,right)
        assert actual.tolist()==want
        assert checker()(left,middle,right,actual)['matching_triples']==len(want)


def test_reader_rejects_missing_duplicate_and_false_match_indices():
    left=np.array([[1,0]],dtype=np.int16);middle=np.array([[0,1]],dtype=np.int16)
    right=np.array([[1,1],[2,2]],dtype=np.int16)
    for bad in (np.empty((0,3),dtype=np.int64),np.array([[0,0,0],[0,0,0]],dtype=np.int64),
                np.array([[0,0,1]],dtype=np.int64),np.array([[-1,0,0]],dtype=np.int64)):
        with pytest.raises(AssertionError):checker()(left,middle,right,bad)


def test_sums_use_wide_integers_and_reject_uncertified_ranges():
    a=np.array([[127]],dtype=np.int8);b=np.array([[127]],dtype=np.int8);c=np.array([[254]],dtype=np.int16)
    assert producer()(a,b,c).tolist()==[[0,0,0]]
    assert checker()(a,b,c,np.array([[0,0,0]],dtype=np.int64))['matching_triples']==1
    for left,middle,right in ((np.array([[2**62]],dtype=np.int64),np.array([[2**62]],dtype=np.int64),c),
                              (np.array([[-2**63]],dtype=np.int64),np.array([[-1]],dtype=np.int64),c),
                              (np.array([[2**64-1]],dtype=np.uint64),b,c),
                              (a.astype(float),b,c),(a,b,np.zeros((1,2),dtype=np.int16))):
        with pytest.raises(ValueError):producer()(left,middle,right)
