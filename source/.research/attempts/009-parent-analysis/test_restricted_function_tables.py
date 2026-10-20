import numpy as np
import pytest
from finite_function_csp import FunctionCSP
from verify_finite_function_csp import verify_tree
from restricted_function_tables import restrict_tables


def test_positive_and_negative_restrictions_with_exact_parent_lift():
    parent=[np.array([[0,0],[0,1],[1,0],[1,1]])]*2
    relations=[[(0,0),(1,1)]]*2
    indices=[[1,3],[0,1,3]]
    tables=restrict_tables(parent,indices);answer=FunctionCSP(tables,relations).search(100)
    assert verify_tree(tables,relations,answer['tree'])==answer['status']=='SAT'
    lifted=[indices[j][i]for j,i in enumerate(answer['witness'])]
    assert np.array_equal(parent[0][lifted[0]],parent[1][lifted[1]])
    tables=restrict_tables(parent,[[0],[3]]);answer=FunctionCSP(tables,relations).search(100)
    assert verify_tree(tables,relations,answer['tree'])==answer['status']=='UNSAT'


def test_invalid_restriction_maps_rejected():
    tables=[np.array([[0],[1]])]
    for indices in ([[0,0]],[[]],[[2]],[[-1]],[[0.5]]):
        with pytest.raises(AssertionError):restrict_tables(tables,indices)
