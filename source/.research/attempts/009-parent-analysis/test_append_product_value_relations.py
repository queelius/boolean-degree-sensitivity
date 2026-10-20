"""Exact controls for fixed, possibly nonzero, complementary products."""
from itertools import product
import numpy as np
import pytest
from append_product_value_relations import append_product_values
from finite_function_csp import FunctionCSP
from verify_finite_function_csp import verify_tree


@pytest.mark.parametrize('values,target,expected', [
    ((1, 1, 1, -1), 1, 'SAT'),
    ((1, 1, 1, -1), 2, 'UNSAT'),
    ((0, 1, 0, -1), 0, 'SAT'),
    ((1, 1, 1, -1), 0, 'UNSAT'),
    ((127, 127, 127, -127), 16129, 'SAT'),
])
def test_literal_positive_negative_zero_and_overflow_controls(values, target, expected):
    tables = [np.array([[v]], dtype=np.int8) for v in values]
    relations = [[tuple(np.int8(v) for v in values)]]
    transformed, allowed = append_product_values(tables, relations, [0], [(0, 1), (2, 3)], [[target], [-target]])
    answer = FunctionCSP(transformed, allowed).search(20)
    assert answer['status'] == expected
    assert verify_tree(transformed, allowed, answer['tree']) == expected
    assert allowed[:1] == relations
    assert all(np.array_equal(t, new[:, :1]) for t, new in zip(tables, transformed))
    assert all(np.array_equal(t, new[:, 1:]) for t, new in zip(tables, transformed))


def test_seeded_encodings_match_literal_exhaustion():
    rng = np.random.default_rng(401)
    for _ in range(20):
        tables = [rng.integers(-2, 3, (2, 3), dtype=np.int16) for _ in range(4)]
        relations = [list(product(range(-2, 3), repeat=4)) for _ in range(3)]
        targets = rng.integers(-2, 3, (2, 2)).tolist()
        points, pairs = [2, 0], [(0, 1), (2, 3)]
        transformed, allowed = append_product_values(tables, relations, points, pairs, targets)
        for assignment in product(range(2), repeat=4):
            expected = all(int(tables[i][assignment[i], x]) * int(tables[j][assignment[j], x]) == targets[k][p]
                           for p, x in enumerate(points) for k, (i, j) in enumerate(pairs))
            actual = all(tuple(int(t[assignment[j], x]) for j, t in enumerate(transformed)) in allowed[x]
                         for x in range(len(allowed)))
            assert actual == expected


def test_invalid_dimensions_and_empty_slice():
    tables = [np.array([[1]], dtype=np.int16) for _ in range(2)]
    relations = [[(1, 1)]]
    transformed, allowed = append_product_values(tables, relations, [], [(0, 1)], [[]])
    assert all(np.array_equal(a, b) for a, b in zip(tables, transformed)) and allowed == relations
    for points, pairs, targets in [([1], [(0, 1)], [[1]]), ([0, 0], [(0, 1)], [[1, 1]]),
                                  ([0], [(0, 2)], [[1]]), ([0], [(0, 0)], [[1]]),
                                  ([0], [(0, 1)], [[]]), ([0], [(0, 1)], [[1.5]])]:
        with pytest.raises(AssertionError):
            append_product_values(tables, relations, points, pairs, targets)
