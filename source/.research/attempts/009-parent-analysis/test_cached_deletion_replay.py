import numpy as np
import pytest
from finite_function_csp import FunctionCSP
from global_pair_consistency import GlobalPairConsistency
from verify_global_pair_consistency import replay_deletions
from cached_deletion_replay import replay_cached


def test_cache_reuses_only_equal_values_and_same_partner_domain():
    tables=[np.array([[0,0],[0,1],[1,0]]),np.array([[1,0],[1,1]])]
    relations=[[(0,0),(1,1)],[(0,0),(0,1),(1,0),(1,1)]]
    domains=[np.arange(3),np.arange(2)]
    deletions=[dict(variable=0,candidate=i,partner=1,points=[0])for i in (0,1)]
    stats={};actual=replay_cached(tables,relations,domains,deletions,stats=stats)
    expected=replay_deletions(tables,relations,domains,deletions)
    assert all(np.array_equal(a,c)for a,c in zip(actual,expected))
    assert stats=={'cover_replays':1,'cached_covers':1}
    bad=deletions+[dict(variable=0,candidate=2,partner=1,points=[0])]
    with pytest.raises(AssertionError):replay_cached(tables,relations,domains,bad)
    with pytest.raises(AssertionError):replay_cached(tables,relations,domains,deletions+[deletions[0]])


def test_matches_literal_reader_on_random_valid_deletion_certificates():
    rng=np.random.default_rng(346);nonempty=0
    from itertools import product
    for _ in range(40):
        tables=[np.unique(rng.integers(0,3,(5,4)),axis=0)for _ in range(3)]
        relations=[[r for r in product(range(3),repeat=3)if rng.random()<.3]for _ in range(4)]
        solver=FunctionCSP(tables,relations);result=GlobalPairConsistency(solver).propagate(solver.initial)
        domains=[np.arange(len(t))for t in tables]
        want=replay_deletions(tables,relations,domains,result['deletions'])
        actual=replay_cached(tables,relations,domains,result['deletions'])
        assert all(np.array_equal(a,c)for a,c in zip(actual,want))
        nonempty+=bool(result['deletions'])
    assert nonempty>10
