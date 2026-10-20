import numpy as np
import pytest
from finite_pair_products import pair_products,opposite_zero_points


def test_selected_pair_order_sign_and_zero_slice():
    left=np.array([[1,2],[0,-1]],dtype=np.int8);right=np.array([[2,1],[-1,2]],dtype=np.int8)
    assert pair_products(left,right,np.array([3,0,2]),-1).tolist()==[[0,2],[-2,-2],[0,1]]
    assert opposite_zero_points(np.array([0,0,0,0,0,0,2,0])).tolist()==[2]
    assert opposite_zero_points(np.zeros(16,dtype=np.int8)).tolist()==[2,6,10,14]
    assert pair_products(left,right,np.array([],dtype=np.int64)).shape==(0,2)


def test_rejects_wrapping_indices_or_unsupported_values():
    v=np.ones((2,4),dtype=np.int8)
    for indices in (np.array([-1]),np.array([4]),np.array([1.5])):
        with pytest.raises(AssertionError):pair_products(v,v,indices)
    with pytest.raises(AssertionError):pair_products(v*3,v,np.array([0]))
    with pytest.raises(AssertionError):pair_products(v,v,np.array([0]),0)
    with pytest.raises(AssertionError):opposite_zero_points(np.zeros((2,4)))
    with pytest.raises(AssertionError):opposite_zero_points(np.zeros(6))
