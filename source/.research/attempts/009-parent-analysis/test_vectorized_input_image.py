from itertools import permutations
import pytest
from vectorized_input_image import input_image
from compact_parent_scalar_catalogs import input_image as literal_image


def test_all_four_coordinate_maps_and_ten_coordinate_bit_positions():
    for image in permutations(range(4)):
        assert input_image(image)==tuple(literal_image(list(image)))
    for shift in range(10):
        image=tuple((i+shift)%10 for i in range(10))
        assert input_image(image)==tuple(literal_image(list(image)))
    assert input_image([])==(0,)
    with pytest.raises(AssertionError):input_image([0,0])
    with pytest.raises(AssertionError):input_image([1.0,0.0])
