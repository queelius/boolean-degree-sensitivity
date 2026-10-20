import pytest
from merge_first_row_exclusions import merge_rows


def test_scoped_union_preserves_residual_and_handles_redundancy():
    result=merge_rows([0,7,19],[7],[0,0])
    assert result==dict(excluded=[0,7],remaining=[19],newly_excluded=[0],whole_geometry_excluded=False)
    result=merge_rows([0,7,19],[7],[0,19])
    assert result['whole_geometry_excluded'] and not result['remaining']


def test_out_of_scope_or_ambiguous_row_ids_rejected():
    with pytest.raises(AssertionError):merge_rows([0,7],[7],[19])
    with pytest.raises(AssertionError):merge_rows([0,0],[0],[])
    with pytest.raises(AssertionError):merge_rows([0,7],[19],[])
