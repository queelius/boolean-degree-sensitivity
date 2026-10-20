"""An enlarged-domain score must reproduce every original integer column."""
from dataclasses import replace
import numpy as np
import pytest
from baseline_full_truth_model import Row
from bounded_core_spectrum_lp import CoefficientTotal,prepare
from core_slice_degree_lp import PatternBlock
from selfdual_core_projection import ProjectedCoefficient
from spectrum_dual_functional import lift_multipliers,compile_functional,simplex_bound


def test_lifting_uses_every_nonuniform_row_divisor_and_combines_signs():
    scale,weights=lift_multipliers([4,6,1],[[0,1,2],[1,-1,3],[0,-1,1]])
    assert scale==12 and weights==(3,-6,0)


@pytest.mark.parametrize('divisors,terms', [([0],[]),([.5],[]),([1],[[1,1,2]]),
    ([1],[[0,0,2]]),([1],[[0,1,-1]])])
def test_invalid_primitive_lift_is_rejected(divisors,terms):
    with pytest.raises(ValueError):lift_multipliers(divisors,terms)


def fixture():
    pools=[[(-1,0),(0,2)],[(0,0),(1,2)]]
    blocks=[PatternBlock((0,),np.array([[[-1],[0]],[[0],[1]]],dtype=np.int8)),
            PatternBlock((1,),np.array([[[0],[0]],[[2],[2]]],dtype=np.int8))]
    coeffs=[ProjectedCoefficient(0,0,0,(-1,0)),ProjectedCoefficient(0,1,2,(0,1)),ProjectedCoefficient(1,0,1,(0,2))]
    return prepare(pools,blocks,coeffs,totals=[CoefficientTotal((0,1),1)])


def test_all_original_columns_and_rhs_match_literal_integer_row_combination():
    model=fixture();rows=list(model.rows());weights=[(i%7)-3 for i in range(len(rows))]
    functional=compile_functional(rows,model.variable_count,weights)
    expected=[0]*model.variable_count
    for row,w in zip(rows,weights):
        for j,a in row.terms:expected[j]+=w*a
    assert functional.coefficients==tuple(expected)
    assert functional.rhs==sum(w*row.upper for row,w in zip(rows,weights))
    base=model.base.basis.base
    for i,variable in enumerate(model.variables):
        if variable['kind']=='joint_core_value_state':
            assert functional.word_score(variable['outside_point'],variable['features'])==expected[i]
        elif variable['kind']=='slice_pattern_weight':
            block=base.blocks[variable['block']]
            costs=functional.pattern_scores(variable['block'],block.values,block.features)
            assert int(costs[variable['pattern']])==expected[i]
    assert simplex_bound([[1,2],[-2,0]],[-3,4,0],-4)['gap']==0


def test_simplex_normalization_is_stronger_than_separate_box_minima():
    answer=simplex_bound([[1,2]],[],0)
    assert answer['lower_bound']==1 and answer['gap']==1 and answer['contradiction']
    assert answer['minimizers']==[0]
    assert sum(min(0,c) for c in (1,2))==0


def test_enlarging_a_domain_can_destroy_an_exact_contradiction():
    assert simplex_bound([[1,2]],[],0)['contradiction']
    enlarged=simplex_bound([[1,2,-1]],[],0)
    assert enlarged['lower_bound']==-1 and not enlarged['contradiction']
    assert enlarged['minimizers']==[2]


def test_unseen_tuple_has_zero_categorical_multiplier():
    rows=[Row(((0,1),),0,0,dict(kind='slice_tuple_distribution',block=0,point=0,features=[0],value=[1]))]
    f=compile_functional(rows,1,[7])
    assert f.word_score(0,[1])==7 and f.word_score(0,[2])==0
    assert list(f.pattern_scores(0,np.array([[[1]],[[2]]]),(0,)))==[-7,0]


def test_large_integer_pattern_costs_do_not_overflow_int64():
    huge=10**30
    rows=[Row(((0,1),),1,1,dict(kind='slice_pattern_normalization',block=0))]
    f=compile_functional(rows,1,[huge])
    assert list(f.pattern_scores(0,np.array([[[0]],[[1]]]),(0,)))==[huge,huge]


@pytest.mark.parametrize('rows,weights', [
    ([Row((),0,1,dict(kind='bounded_spectrum_total'))],[1]),
    ([Row((),0,0,dict(kind='unrecognized'))],[1]),
    ([Row((),0,0,dict(kind='bounded_spectrum_total'))],[.5]),
    ([Row((),0,0,dict(kind='bounded_spectrum_total'))],[])])
def test_unsupported_rows_or_weights_cannot_define_an_extension(rows,weights):
    with pytest.raises(ValueError):compile_functional(rows,0,weights)


def test_empty_domain_or_noninteger_cost_is_rejected():
    with pytest.raises(ValueError):simplex_bound([[]],[],0)
    with pytest.raises(ValueError):simplex_bound([[.5]],[],0)
