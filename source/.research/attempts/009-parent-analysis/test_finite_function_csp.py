from itertools import product
import random
import numpy as np
from finite_function_csp import FunctionCSP


def brute(tables, relations):
    return [choice for choice in product(*(range(len(t)) for t in tables))
            if all(tuple(int(t[i, x]) for t, i in zip(tables, choice)) in relations[x]
                   for x in range(tables[0].shape[1]))]


def test_search_agrees_with_exhaustive_small_instances():
    rng = random.Random(265)
    for _ in range(40):
        tables = [np.array(rng.sample(list(product(range(3), repeat=3)), 3)) for _ in range(3)]
        relations = [set(rng.sample(list(product(range(3), repeat=3)), rng.randrange(1, 28))) for _ in range(3)]
        expected = brute(tables, relations)
        solver = FunctionCSP(tables, relations)
        result = solver.search(max_nodes=1000)
        assert result['status'] == ('SAT' if expected else 'UNSAT')
        if expected: assert tuple(result['witness']) in expected
        assert result['nodes'] <= 53  # At most all nodes of the 3^3 assignment tree.


def test_planted_witness_empty_relation_and_unknown_are_distinct():
    tables = [np.array([[0, 1], [1, 0]]), np.array([[0, 0], [1, 1]])]
    relation = [{(0, 1)}, {(1, 1)}]
    assert FunctionCSP(tables, relation).search(max_nodes=10)['witness'] == [0, 1]
    assert FunctionCSP(tables, [set(), relation[1]]).search(max_nodes=10)['status'] == 'UNSAT'
    assert FunctionCSP(tables, relation).search(max_nodes=0)['status'] == 'UNKNOWN'


def test_empty_domain_repeated_relations_and_unbalanced_value_splits():
    assert FunctionCSP([np.zeros((0, 2), dtype=int)], [{(0,)}, {(0,)}]).search()['status'] == 'UNSAT'
    tables = [np.eye(7, dtype=np.int8)]
    assert FunctionCSP(tables, [{(0,), (1,)}]*7).search(max_nodes=3)['status'] == 'UNKNOWN'
    result = FunctionCSP(tables, [{(0,), (1,)}]*7).search(max_nodes=20)
    assert result['status'] == 'SAT' and result['witness'] in [[i] for i in range(7)]
