import pytest
from verify_matched_safe_count_exclusion import check_family,check_transport


def test_family_requires_every_representative():
    rows=[dict(unit_faces=list(range(n)))for n in (12,6,12)]
    assert check_family([0,1,2],[0,2],rows)==[0,2]
    with pytest.raises(AssertionError):check_family([0,1,2],[0],rows)


def test_literal_transport_preserves_signed_data():
    known={1:-2,4:-2,2:2,8:2};image=list(range(14));image[:4]=[2,3,0,1]
    check_transport(known,3,12,image)
    with pytest.raises(AssertionError):check_transport(known,3,3,image)
    with pytest.raises(AssertionError):check_transport(dict(known,1:2),3,12,image)
    image[0]=image[1]
    with pytest.raises(AssertionError):check_transport(known,3,12,image)
