import numpy as np
import pytest
from ordinary_cross_intersection import cross_relations
from finite_function_csp import FunctionCSP
from verify_global_pair_consistency import replay_deletions
from whole_family_cross import family_masks,forbidden_masks,filter_pair,cover_features


def test_one_companion_must_meet_every_face_and_deletion_replays():
    triples=[7,56,73]
    features=[np.array([[1,1,0],[0,0,1]],dtype=np.int8),np.array([[1,0,0],[0,1,0]],dtype=np.int8)]
    tables,relations,_=cross_relations(features,[3,12],triples)
    solver=FunctionCSP(tables,relations)
    assert solver.propagate(solver.initial)[0]==solver.initial
    left=family_masks(features[0]);right=forbidden_masks(features[1],triples)
    keep_left,keep_right=filter_pair(left,right,[0,1],[0,1],block_size=1)
    assert keep_left.tolist()==[1]and keep_right.tolist()==[0,1]
    points=cover_features(left[0],right)
    reduced=replay_deletions(tables,relations,[np.array([0,1]),np.array([0,1])],
                            [dict(variable=0,candidate=0,partner=1,points=points)])
    assert reduced[0].tolist()==[1]


def test_signature_filter_agrees_with_exhaustive_pairs():
    rng=np.random.default_rng(344)
    for _ in range(40):
        left=rng.integers(0,256,19,dtype=np.uint64);right=rng.integers(0,256,23,dtype=np.uint64)
        li=np.sort(rng.choice(len(left),13,replace=False));ri=np.sort(rng.choice(len(right),17,replace=False))
        a,c=filter_pair(left,right,li,ri,block_size=3)
        assert a.tolist()==[int(i)for i in li if any(int(left[i])&int(right[j])==0 for j in ri)]
        assert c.tolist()==[int(j)for j in ri if any(int(left[i])&int(right[j])==0 for i in li)]
        for i in set(map(int,li))-set(map(int,a)):
            covered=cover_features(left[i],right[ri]);remaining=list(map(int,right[ri]))
            for bit in covered:
                smaller=[r for r in remaining if not r>>bit&1]
                assert len(smaller)<len(remaining);remaining=smaller
            assert not remaining


def test_empty_domains_and_invalid_encoding():
    a,c=filter_pair(np.array([1,2],dtype=np.uint64),np.array([3],dtype=np.uint64),[0,1],[])
    assert not len(a)and not len(c)
    with pytest.raises(AssertionError):family_masks(np.array([[2]],dtype=np.int8))
    with pytest.raises(AssertionError):family_masks(np.ones((1,65),dtype=np.int8))
    with pytest.raises(AssertionError):filter_pair(np.array([1],dtype=np.uint64),np.array([1],dtype=np.uint64),[0],[0],block_size=0)
    with pytest.raises(AssertionError):cover_features(np.uint64(1),np.array([2],dtype=np.uint64))
