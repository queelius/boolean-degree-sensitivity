"""Exact controls for whole-row compatibility alongside pointwise constraints."""
from copy import deepcopy
from itertools import product
import importlib
import numpy as np
import pytest


def relation(left,right,pairs):
    cls=importlib.import_module('binary_row_relation').BinaryRelation
    return cls(left,right,np.asarray(pairs,dtype=np.int64).reshape(-1,2))


def solve(tables,allowed,binary,limit=100):
    cls=importlib.import_module('binary_function_csp').BinaryFunctionCSP
    return cls(tables,allowed,binary,priority_point=0).search(limit)


def replay(tables,allowed,binary,tree):
    return importlib.import_module('verify_binary_function_csp').verify_tree(tables,allowed,binary,tree)


@pytest.mark.parametrize('pairs,want', [([(1,0)],'SAT'),([], 'UNSAT'),([(0,1),(1,0)],'SAT')])
def test_allowed_pair_is_enforced_at_a_witness_and_empty_relation_is_impossible(pairs,want):
    tables=[np.array([[0],[1]],dtype=np.int16) for _ in range(2)]
    allowed=[list(product((0,1),repeat=2))];binary=[relation(0,1,pairs)]
    result=solve(tables,allowed,binary)
    assert result['status']==want and replay(tables,allowed,binary,result['tree'])==want
    if want=='SAT':assert tuple(result['witness']) in pairs


def test_inconsistent_binary_cycle_is_excluded_despite_unrestricted_pointwise_relation():
    tables=[np.array([[0],[1]],dtype=np.int16) for _ in range(3)]
    allowed=[list(product((0,1),repeat=3))]
    binary=[relation(0,1,[(0,0),(1,1)]),relation(1,2,[(0,0),(1,1)]),relation(0,2,[(0,1),(1,0)])]
    result=solve(tables,allowed,binary)
    assert result['status']=='UNSAT' and result['nodes']>1
    assert replay(tables,allowed,binary,result['tree'])=='UNSAT'


def test_original_pointwise_contradiction_is_not_lost():
    tables=[np.array([[0],[1]],dtype=np.int16) for _ in range(2)]
    allowed=[[(0,0)]];binary=[relation(0,1,[(1,1)])]
    result=solve(tables,allowed,binary)
    assert result['status']=='UNSAT' and replay(tables,allowed,binary,result['tree'])=='UNSAT'


def test_small_seeded_models_agree_with_complete_cartesian_enumeration():
    rng=np.random.default_rng(481)
    for _ in range(25):
        tables=[np.unique(rng.integers(-1,2,(3,2),dtype=np.int16),axis=0) for _ in range(3)]
        allowed=[[row for row in product((-1,0,1),repeat=3) if rng.integers(2)] for _ in range(2)]
        binary=[relation(i,j,[(a,c) for a in range(len(tables[i])) for c in range(len(tables[j])) if rng.integers(2)])
                for i,j in ((0,1),(1,2),(0,2))]
        possible=[]
        for choice in product(*(range(len(t)) for t in tables)):
            point_ok=all(tuple(int(t[choice[j],x]) for j,t in enumerate(tables)) in allowed[x] for x in range(2))
            pair_ok=all([choice[r.left],choice[r.right]] in r.allowed.tolist() for r in binary)
            if point_ok and pair_ok:possible.append(list(choice))
        result=solve(tables,allowed,binary)
        want='SAT' if possible else 'UNSAT'
        assert result['status']==want and replay(tables,allowed,binary,result['tree'])==want
        if possible:assert result['witness'] in possible


def test_limit_and_empty_component_domain_keep_their_correct_meanings():
    tables=[np.array([[0],[1]],dtype=np.int16) for _ in range(2)]
    allowed=[list(product((0,1),repeat=2))];binary=[relation(0,1,[(0,0),(1,1)])]
    result=solve(tables,allowed,binary,0)
    assert result['status']=='UNKNOWN' and replay(tables,allowed,binary,result['tree'])=='UNKNOWN'
    empty=[tables[0][:0],tables[1]];none=[relation(0,1,[])]
    result=solve(empty,allowed,none)
    assert result['status']=='UNSAT' and replay(empty,allowed,none,result['tree'])=='UNSAT'


def test_missing_binary_propagation_or_changed_compatibility_rejects_a_sat_proof():
    tables=[np.array([[0],[1]],dtype=np.int16) for _ in range(2)]
    allowed=[list(product((0,1),repeat=2))];binary=[relation(0,1,[(1,0)])]
    tree=solve(tables,allowed,binary)['tree'];assert tree['kind']=='SAT'
    damaged=deepcopy(tree);damaged['propagation']=[]
    with pytest.raises(AssertionError):replay(tables,allowed,binary,damaged)
    with pytest.raises(AssertionError):replay(tables,allowed,[relation(0,1,[(0,1)])],tree)


@pytest.mark.parametrize('left,right,pairs',[(0,0,[(0,0)]),(-1,1,[(0,0)]),(0,2,[(0,0)]),
                                          (0,1,[(-1,0)]),(0,1,[(2,0)])])
def test_invalid_component_or_candidate_indices_are_rejected(left,right,pairs):
    tables=[np.array([[0],[1]],dtype=np.int16) for _ in range(2)]
    allowed=[list(product((0,1),repeat=2))];binary=[relation(left,right,pairs)]
    with pytest.raises(AssertionError):solve(tables,allowed,binary)
    with pytest.raises(AssertionError):replay(tables,allowed,binary,dict(kind='LIMIT'))
