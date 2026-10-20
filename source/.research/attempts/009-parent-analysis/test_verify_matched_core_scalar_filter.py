from itertools import product
import numpy as np
import pytest
from verify_matched_core_scalar_filter import walsh, check_filter


def test_walsh_against_all_small_signed_coefficient_vectors():
    coefficients = np.array(list(product((-1, 0, 1), repeat=4)), dtype=np.int64)
    expected = [[sum(int(c)*(-1 if (q & x).bit_count() % 2 else 1) for q, c in enumerate(row))
                 for x in range(4)] for row in coefficients]
    assert np.array_equal(walsh(coefficients), expected)
    assert walsh(np.zeros((0, 4), dtype=np.int64)).shape == (0, 4)
    with pytest.raises(AssertionError): walsh(np.zeros((2, 3)))


def test_exact_membership_has_positive_and_negative_controls():
    values = np.array([[1, -1, 1, -1], [1, 1, 1, -1]])
    allowed = [{1}, {-1}, {1}, {-1}]
    assert check_filter(values, allowed) == ([None, 1], [0])
    # A plausible-looking modular survivor with an inadmissible exact value.
    assert check_filter(np.array([[1, -1, 18, -1]]), allowed) == ([2], [])
