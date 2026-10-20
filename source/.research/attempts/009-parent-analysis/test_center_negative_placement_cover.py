import pytest
from center_negative_placement_cover import orbit_cover,move


def test_complete_cover_with_explicit_maps():
    patterns=[(3,),(5,),(6,),(9,),(10,),(12,)]
    reps,maps=orbit_cover(patterns,[(1,2,0,3)],4)
    assert len(reps)==2 and len(maps)==6
    for row in maps:
        assert sorted(row['map'])==list(range(4))
        assert tuple(sorted(move(q,row['map']) for q in row['pattern']))==reps[row['representative']]


def test_nonclosed_domain_or_invalid_permutation_rejected():
    with pytest.raises(AssertionError):orbit_cover([(3,)],[(1,2,0,3)],4)
    with pytest.raises(AssertionError):orbit_cover([(3,)],[(0,0,2,3)],4)
