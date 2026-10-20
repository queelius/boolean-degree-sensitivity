"""Normalization may strengthen a dual, but must be an actual model equation."""
import importlib
import importlib.util
import pytest
from baseline_full_truth_model import Row
from exact_box_row_lp import verify_certificate


def reconstruct():
    assert importlib.util.find_spec('simplex_row_reconstruction') is not None
    return importlib.import_module('simplex_row_reconstruction').reconstruct


def test_normalization_finds_contradiction_missed_by_separate_box_minima():
    rows = [Row(((0,1),(1,1)),1,1,{}), Row(((0,1),(1,2)),0,0,{})]
    result = reconstruct()(rows,2,[0,1],[[0,1]])
    assert result['original_box_rhs'] == 0
    assert result['integer_rhs'] == -1
    assert result['status'] == 'EXACT_BOX_ROW_LP_CONTRADICTION'
    assert verify_certificate(rows,2,result['certificate']) == -1


def test_feasible_normalized_system_has_no_strict_contradiction():
    rows = [Row(((0,1),(1,1)),1,1,{}), Row(((0,1),(1,2)),1,1,{})]
    result = reconstruct()(rows,2,[0,1],[[0,1]])
    assert result['integer_rhs'] == 0
    assert result['status'] == 'INCONCLUSIVE_BOX_ROW_LP'
    assert 'certificate' not in result


def test_ungrouped_flags_keep_their_individual_box_bounds():
    rows = [Row(((0,1),(1,1)),1,1,{}), Row(((0,1),(1,2),(2,-5)),-5,-5,{})]
    result = reconstruct()(rows,3,[0,1],[[0,1]])
    assert result['original_box_rhs'] == 0
    assert result['integer_rhs'] == -1
    assert verify_certificate(rows,3,result['certificate']) == -1


def test_large_signed_weights_and_permuted_group_columns_are_exact():
    h = 10**40
    rows = [Row(((1,1),(0,1)),1,1,{}), Row(((0,-1),(1,-2)),0,0,{})]
    result = reconstruct()(rows,2,[7,-h],[[1,0]])
    assert result['integer_rhs'] == -h
    assert verify_certificate(rows,2,result['certificate']) == -h


def test_constant_contradiction_does_not_require_a_simplex():
    rows = [Row((),-1,-1,{})]
    result = reconstruct()(rows,0,[1],[])
    assert result['integer_rhs'] == -1
    assert verify_certificate(rows,0,result['certificate']) == -1


@pytest.mark.parametrize('groups', [[[0]],[[0,1],[1]],[[0,0]],[[0,2]],[[]],[[True,1]]])
def test_unproved_or_invalid_normalization_is_rejected(groups):
    rows = [Row(((0,1),(1,1)),1,1,{})]
    with pytest.raises(ValueError):
        reconstruct()(rows,2,[1],groups)


@pytest.mark.parametrize('rows,weights', [
    ([Row(((0,1),),0,1,{})],[1]),
    ([Row(((0,1),),1,1,{})],[]),
    ([Row(((0,1),),1,1,{})],[.5]),
    ([Row(((1,1),),1,1,{})],[1]),
    ([Row(((0,1),(0,1)),1,1,{})],[1]),
])
def test_unsupported_or_malformed_rows_are_rejected(rows,weights):
    with pytest.raises(ValueError):
        reconstruct()(rows,1,weights,[])
