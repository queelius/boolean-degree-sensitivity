from copy import deepcopy
from itertools import product
import random
import numpy as np
import pytest
from finite_function_csp import FunctionCSP
from verify_finite_function_csp import verify_tree


def test_independent_tree_replay_against_literal_exhaustion():
    rng = random.Random(270)
    for _ in range(25):
        tables = [np.array(rng.sample(list(product(range(2), repeat=4)), 4)) for _ in range(3)]
        relations = [set(rng.sample(list(product(range(2), repeat=3)), rng.randrange(1, 9))) for _ in range(4)]
        feasible = [c for c in product(range(4), repeat=3)
                    if all(tuple(int(t[i, x]) for t, i in zip(tables, c)) in relations[x] for x in range(4))]
        result = FunctionCSP(tables, relations).search(1000)
        assert verify_tree(tables, relations, result['tree']) == result['status'] == ('SAT' if feasible else 'UNSAT')
        limited = FunctionCSP(tables, relations).search(1)
        assert verify_tree(tables, relations, limited['tree']) == limited['status']


def test_false_contradiction_and_false_witness_are_rejected():
    tables = [np.array([[0, 1], [1, 0]])]
    relations = [set(), {(0,), (1,)}]
    result = FunctionCSP(tables, relations).search(10)
    damaged = deepcopy(result['tree']); damaged['contradiction_point'] = 1
    with pytest.raises(AssertionError): verify_tree(tables, relations, damaged)
    relations = [{(0,)}, {(1,)}]
    result = FunctionCSP(tables, relations).search(10)
    damaged = deepcopy(result['tree']); damaged['witness'] = [1]
    with pytest.raises(AssertionError): verify_tree(tables, relations, damaged)
