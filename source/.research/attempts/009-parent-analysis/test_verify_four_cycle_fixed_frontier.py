import pytest
from verify_four_cycle_fixed_frontier import check_choices


def test_complete_ordered_choices():
    choices=[dict(third_row=1,fourth_row=2),dict(third_row=1,fourth_row=3)]
    check_choices(choices,choices)


def test_missing_duplicate_or_wrong_choices_rejected():
    choices=[dict(third_row=1,fourth_row=2),dict(third_row=1,fourth_row=3)]
    for bad in (choices[:1],[choices[0],choices[0]],list(reversed(choices))):
        with pytest.raises(AssertionError):check_choices(choices,bad)
