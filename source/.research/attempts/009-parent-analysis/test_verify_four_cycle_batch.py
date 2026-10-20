import pytest
from verify_four_cycle_batch import validate_rows


def test_complete_ordered_rows():
    validate_rows([0,7],[dict(second_row=0),dict(second_row=7)])


def test_missing_or_duplicated_case_rejected():
    with pytest.raises(AssertionError):validate_rows([0,7],[dict(second_row=0)])
    with pytest.raises(AssertionError):validate_rows([0,7],[dict(second_row=0),dict(second_row=0)])
