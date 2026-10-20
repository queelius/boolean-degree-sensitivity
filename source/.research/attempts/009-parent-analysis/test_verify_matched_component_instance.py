import pytest
from verify_matched_component_instance import validate_catalog_map


def test_catalog_transport_preserves_the_required_structure():
    image = [1, 0, 4, 2, 3, 5, 6, 7, 8, 9]
    # Actual low set {3,4} maps to canonical {2,3}; negative {0,2,3} to {1,4,2}.
    validate_catalog_map(image, [13], [3, 4], [22])
    for damaged in ([0, 0]+image[2:], [2, 0, 4, 1, 3, 5, 6, 7, 8, 9], list(range(10))):
        with pytest.raises(AssertionError): validate_catalog_map(damaged, [13], [3, 4], [22])
