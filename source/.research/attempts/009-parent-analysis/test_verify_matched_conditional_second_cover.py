import pytest
from verify_matched_conditional_second_cover import check_condition


def test_maps_preserve_both_marks_and_all_fixed_coefficients_including_zero():
    identity = list(range(14)); known = {1: 0, 2: 1, 4: -1, 8: -1}
    check_condition(identity, known, 3, 12)
    image = identity.copy(); image[2], image[3] = image[3], image[2]
    check_condition(image, known, 3, 12)
    image = identity.copy(); image[0], image[1] = image[1], image[0]
    with pytest.raises(AssertionError): check_condition(image, known, 3, 12)
    image = identity.copy(); image[0], image[2] = image[2], image[0]
    with pytest.raises(AssertionError): check_condition(image, {}, 3, 12)
    image = identity.copy(); image[0] = image[1]
    with pytest.raises(AssertionError): check_condition(image, {}, 3, 12)
