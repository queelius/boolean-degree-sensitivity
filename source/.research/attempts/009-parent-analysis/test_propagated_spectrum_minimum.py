"""Controls catch wrong domain indices, lost correlations, and false contradictions."""
import numpy as np
import pytest
from spectrum_dual_functional import Category, Functional
from propagated_spectrum_minimum import minimum


def functional(rhs=0, **changes):
    fields = dict(coefficients=(), rhs=rhs, word_normalizations={},
                  pattern_normalizations={}, value_weights={}, moment_weights={},
                  categories_by_point={}, categories_by_block={})
    fields.update(changes)
    return Functional(**fields)


@pytest.mark.parametrize('target,gap,contradiction', [(0,-1,False),(1,0,False),(2,1,True)])
def test_exact_scalar_equation_has_feasible_and_infeasible_controls(target,gap,contradiction):
    # B = target, B in {0,1}; the functional is -B = -target.
    f = functional(-target, value_weights={0: [(0,1)]})
    result = minimum(f, [np.array([[0],[1]])], [[0,1]], [0], [[(0,),(1,)]], [])
    assert result['bound']['gap'] == gap
    assert result['candidate_contradiction'] is contradiction


def test_domain_indices_change_the_bound_and_are_not_rebased():
    f = functional(-1, value_weights={0: [(0,1)]})
    result = minimum(f, [np.array([[0],[1]])], [[0]], [0], [[(0,),(1,)]], [])
    assert result['bound']['gap'] == 1
    assert result['pattern_minimizing_rows'] == [0]
    assert result['retained_word_counts'] == [1]


def test_feature_order_pattern_costs_and_flag_costs_are_all_counted():
    cat = Category(1,0,(0,),(5,),3)
    f = functional(20, word_normalizations={0:17}, pattern_normalizations={0:11,1:13},
                   value_weights={0:[(1,2)]}, categories_by_point={0:[cat]}, categories_by_block={1:[cat]})
    result = minimum(f, [np.array([[7],[0]]),np.array([[5],[1]])],
                     [[0],[0]], [1,0], [[(5,7),(1,0)]], [-8,2])
    assert result['bound']['lower_bound'] == 19
    assert result['bound']['gap'] == -1
    assert result['pattern_minimizing_rows'] == [0,0]


def test_pattern_minimum_keeps_correlation_between_points():
    cats = [Category(0,x,(0,),(0,),10) for x in range(2)]
    f = functional(categories_by_point={x:[c] for x,c in enumerate(cats)}, categories_by_block={0:cats})
    result = minimum(f,[np.array([[0,1],[1,0]])],[[0,1]],[0],[[(0,),(1,)],[(0,),(1,)]],[])
    assert result['bound']['minimums'] == [0,0,-10]
    assert result['bound']['lower_bound'] == -10
    assert not result['candidate_contradiction']


def test_empty_filtered_word_pool_is_explicit_and_has_no_numeric_bound():
    result = minimum(functional(),[np.array([[2]])],[[0]],[0],[[(0,),(1,)]],[])
    assert result['empty_points'] == [0]
    assert result['bound'] is None
    assert result['candidate_contradiction']


def test_large_integer_scores_remain_exact():
    huge = 10**30
    f = functional(huge-1,pattern_normalizations={0:huge})
    result = minimum(f,[np.array([[0]])],[[0]],[0],[[(0,)]],[])
    assert result['bound']['gap'] == 1


@pytest.mark.parametrize('tables,domains,features,pools', [
    ([np.array([[0]])],[[]],[0],[[(0,)]]),
    ([np.array([[0]])],[[1]],[0],[[(0,)]]),
    ([np.array([[0]])],[[0,0]],[0],[[(0,)]]),
    ([np.array([[0.]])],[[0]],[0],[[(0,)]]),
    ([np.array([[0]])],[[0]],[0],[[(0,)],[(0,)]]),
    ([np.array([[0]])],[[0]],[0,1],[[(0,)]]),
    ([np.array([[0]])],[[0]],[1],[[(0,)]]),
    ([np.array([[0]])],[[0]],[0],[[(0.5,)]]),
])
def test_invalid_domain_or_feature_data_is_rejected(tables,domains,features,pools):
    with pytest.raises(ValueError):
        minimum(functional(),tables,domains,features,pools,[])
