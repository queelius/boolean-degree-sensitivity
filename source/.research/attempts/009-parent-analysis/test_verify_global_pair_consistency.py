from itertools import product
import copy
import numpy as np
import pytest
from finite_function_csp import FunctionCSP
from global_pair_consistency import GlobalPairConsistency
from verify_global_pair_consistency import replay_deletions, replay_steps, frontier_domains, incompatible


def test_independent_replay_and_false_incompatibility_rejection():
    tables = [np.array([[0, 0], [1, 1]]), np.array([[0, 1], [1, 0]])]
    relations = [[(0, 0), (1, 1)]]*2
    solver = FunctionCSP(tables, relations)
    proof = GlobalPairConsistency(solver).propagate(solver.initial)
    domains = [np.arange(len(t)) for t in tables]
    actual = replay_deletions(tables, relations, domains, proof['deletions'])
    assert any(not len(d) for d in actual)
    false = copy.deepcopy(proof['deletions']); false[0]['points'] = [0]
    with pytest.raises(AssertionError): replay_deletions(tables, relations, domains, false)


def test_random_reductions_have_independent_replays():
    rng = np.random.default_rng(303)
    for _ in range(20):
        tables = [np.unique(rng.integers(0, 3, (5, 3)), axis=0) for _ in range(3)]
        relations = [[r for r in product(range(3), repeat=3) if rng.random() < .5] for _ in range(3)]
        solver = FunctionCSP(tables, relations); proof = GlobalPairConsistency(solver).propagate(solver.initial)
        actual = replay_deletions(tables, relations, [np.arange(len(t)) for t in tables], proof['deletions'])
        assert [[int(i) for i in d] for d in actual] == [[i for i in range(len(t)) if bits >> i & 1] for t,bits in zip(tables,proof['domains'])]


def test_path_and_point_replay_controls():
    tables = [np.array([[0], [1]])]*2; relations = [[(0, 0), (1, 1)]]
    tree = FunctionCSP(tables, relations).search(1)['tree']
    for direction in (0, 1):
        domains = frontier_domains(tables, relations, tree, [direction])
        reduced = replay_steps(tables, relations, domains, [0])
        assert [d.tolist() for d in reduced] == [[direction], [direction]]
        assert not incompatible(tables, relations, reduced, 0)
    assert incompatible(tables, relations, [np.array([],dtype=int),np.array([0])], -1)
    with pytest.raises(AssertionError): frontier_domains(tables, relations, tree, [])
