"""Controls for exact bounds across every marked component pattern."""
import importlib.util
import itertools
import numpy as np
import pytest
from spectrum_dual_functional import Category, Functional
from propagated_spectrum_minimum import minimum


def build(*args, **kwargs):
    assert importlib.util.find_spec("conditioned_spectrum_bounds") is not None, "Conditioned bound builder is missing"
    from conditioned_spectrum_bounds import build as build_bounds
    return build_bounds(*args, **kwargs)


def functional(rhs=0, **changes):
    fields = dict(coefficients=(), rhs=rhs, word_normalizations={},
                  pattern_normalizations={}, value_weights={}, moment_weights={},
                  categories_by_point={}, categories_by_block={})
    fields.update(changes)
    return Functional(**fields)


@pytest.mark.parametrize("target", [0, 1, 2])
def test_fixed_scalar_equation_has_feasible_and_infeasible_controls(target):
    # B=target; each marked pattern fixes B to 0 or 1.
    f = functional(-target, value_weights={0: [(0, 1)]})
    result = build(f, [np.array([[0], [1]])], [0], [[(0,), (1,)]], [], 0)
    assert [r.candidate_index for r in result.bounds] == [0, 1]
    assert [r.gap for r in result.bounds] == [target, target-1]
    assert [r.candidate_contradiction for r in result.bounds] == [target > 0, target > 1]


def test_component_order_and_flags_contribute_to_each_conditioned_bound():
    cat = Category(1, 0, (0,), (5,), 3)
    f = functional(20, word_normalizations={0: 17}, pattern_normalizations={0: 11, 1: 13},
                   value_weights={0: [(1, 2)]}, categories_by_point={0: [cat]}, categories_by_block={1: [cat]})
    result = build(f, [np.array([[7], [0]]), np.array([[5], [1]])],
                   [1, 0], [[(5, 7), (1, 0)]], [-8, 2], 1)
    assert [r.lower_bound for r in result.bounds] == [19, 33]
    assert [r.gap for r in result.bounds] == [-1, 13]


def test_unmarked_pattern_minimum_preserves_correlation_across_points():
    cats = [Category(1, x, (0,), (0,), 10) for x in range(2)]
    f = functional(categories_by_point={x: [c] for x, c in enumerate(cats)},
                   categories_by_block={1: cats})
    result = build(f, [np.array([[0, 0]]), np.array([[0, 1], [1, 0]])],
                   [1, 0], [[(0, 0), (1, 0)], [(0, 0), (1, 0)]], [], 0)
    assert result.bounds[0].gap == -10
    assert result.pattern_costs[1] == (-10, -10)


def test_empty_pool_is_reported_separately_from_a_finite_score():
    result = build(functional(), [np.array([[0], [2]])], [0], [[(0,), (1,)]], [], 0)
    assert result.bounds[0].gap == 0 and not result.bounds[0].candidate_contradiction
    bad = result.bounds[1]
    assert bad.empty_points == (0,) and bad.lower_bound is None and bad.gap is None
    assert bad.candidate_contradiction


def test_large_integer_scores_and_duplicate_patterns_keep_exact_indices():
    huge = 10**30
    f = functional(huge-1, pattern_normalizations={0: huge})
    result = build(f, [np.array([[0], [0]])], [0], [[(0,)]], [], 0)
    assert [(r.candidate_index, r.gap) for r in result.bounds] == [(0, 1), (1, 1)]
    assert all(type(r.gap) is int for r in result.bounds)


@pytest.mark.parametrize("marked", [0, 1])
def test_precomputed_bounds_agree_with_direct_per_case_minima(marked):
    rng = np.random.default_rng(649)
    words = list(itertools.product(range(2), repeat=2))
    tables = [np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) for _ in range(2)]
    features = [1, 0]
    for _ in range(8):
        categories = [Category(j, x, (feature,), (int(rng.integers(2)),), int(rng.integers(-9, 10)))
                      for j, feature in enumerate(features) for x in range(2)]
        f = functional(int(rng.integers(-20, 21)),
                       word_normalizations={x: int(rng.integers(-5, 6)) for x in range(2)},
                       pattern_normalizations={j: int(rng.integers(-5, 6)) for j in range(2)},
                       value_weights={x: [(f, int(rng.integers(-5, 6))) for f in features] for x in range(2)},
                       moment_weights={0: int(rng.integers(-3, 4))},
                       categories_by_point={x: [c for c in categories if c.point == x] for x in range(2)},
                       categories_by_block={j: [c for c in categories if c.block == j] for j in range(2)})
        flags = [-7, 3]
        result = build(f, tables, features, [words, words], flags, marked)
        for row in result.bounds:
            domains = [list(range(len(t))) for t in tables]
            domains[marked] = [row.candidate_index]
            direct = minimum(f, tables, domains, features, [words, words], flags)
            assert row.gap == direct["bound"]["gap"]
            assert row.lower_bound == direct["bound"]["lower_bound"]
            assert row.candidate_contradiction == direct["candidate_contradiction"]


@pytest.mark.parametrize("change", [
    {"tables": []}, {"pools": []}, {"marked": -1}, {"marked": 1}, {"marked": True},
    {"features": [True]}, {"features": [0, 0]}, {"features": [1]},
    {"tables": [np.array([[0.]])]}, {"tables": [np.array([])]},
    {"tables": [np.array([[0]])], "pools": [[(0,)], [(0,)]]},
    {"pools": [[(0.5,)]]}, {"flags": [0.5]}, {"flags": [True]},
])
def test_malformed_domains_and_noninteger_inputs_are_rejected(change):
    args = dict(functional=functional(), tables=[np.array([[0]])],
                features=[0], pools=[[(0,)]], flags=[], marked=0)
    args.update(change)
    with pytest.raises(ValueError):
        build(**args)
