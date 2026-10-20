import pytest
from matched_component_coordinate_index import component_for_pair


def test_pair_index_is_derived_from_shared_local_coordinates():
    core=sum(1<<i for i in (1,3,5,7))
    geometry=dict(positive_doubles=[core|1,core|4])
    instance=dict(core_pair_order=[3,5,6,9,10,12],components=[dict(kind='safe_pair_row',local_core_pair=p)for p in [3,5,6,9,10,12]])
    assert component_for_pair(geometry,instance,(1<<1)|(1<<5))==1
    with pytest.raises(AssertionError):component_for_pair(geometry,instance,(1<<1)|1)
    with pytest.raises(AssertionError):component_for_pair(geometry,instance,1<<1)
