"""Original Cartesian indices must survive grouping and local row reindexing."""
import importlib
import numpy as np
import pytest


def project(*args):return importlib.import_module('project_binary_candidate_pairs').project_pairs(*args)


def fixture():
    return ([7,1,3],[8,2],np.array([0,1,3,4,5],dtype=np.int64),
            np.array([1,0,0,1,1],dtype=np.int64),{1},[3,7],[2,8])


def test_permuted_original_rows_and_cartesian_width_map_to_exact_local_pairs():
    assert project(*fixture()).tolist()==[[1,1],[0,1],[0,0]]


def test_empty_projection_has_an_explicit_two_column_shape():
    args=list(fixture());args[4]=set();args[5]=[];args[6]=[]
    assert project(*args).shape==(0,2)


@pytest.mark.parametrize('position,replacement',[
    (0,[7,7,3]),(2,np.array([-1,1,3,4,5],dtype=np.int64)),
    (2,np.array([0,1,3,4,6],dtype=np.int64)),(3,np.array([1,0],dtype=np.int64)),
    (5,[3]),(5,[1,3,7]),(6,[8,8]),
])
def test_lost_extra_duplicate_or_out_of_range_candidate_rows_are_rejected(position,replacement):
    args=list(fixture());args[position]=replacement
    with pytest.raises(AssertionError):project(*args)
