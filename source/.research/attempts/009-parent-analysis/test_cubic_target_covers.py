import pytest
from cubic_target_covers import reanchor
from verify_cubic_target_covers import verify_maps


def fixture():
    reps=[(1,)];maps=[dict(pattern=[1],representative=0,map=[0,1,2]),dict(pattern=[2],representative=0,map=[2,0,1]),dict(pattern=[4],representative=0,map=[1,2,0])]
    return reps,maps


def test_reanchor_to_previously_excluded_member_with_noninvolutory_maps():
    reps,maps=fixture();out,changed=reanchor(reps,maps,{(2,)})
    assert out==[dict(index=0,pattern=[2],previously_excluded=True)]
    verify_maps(3,{(1,),(2,),(4,)},out,changed)


def test_unexcluded_orbit_and_damaged_map():
    reps,maps=fixture();out,changed=reanchor(reps,maps,set());assert not out[0]['previously_excluded']
    verify_maps(3,{(1,),(2,),(4,)},out,changed)
    changed[1]['map']=[0,1,2]
    with pytest.raises(AssertionError):verify_maps(3,{(1,),(2,),(4,)},out,changed)
