import numpy as np
import pytest
from finite_function_csp import FunctionCSP
from conditioned_function_search import search_from
from verify_conditioned_function_tree import verify_from


def test_conditioned_search_has_positive_negative_and_partial_controls():
    tables=[np.array([[0,0],[0,1],[1,0],[1,1]])]*2
    relations=[[(0,0),(1,1)]]*2;solver=FunctionCSP(tables,relations);original=solver.initial
    for domains,cap,expected in [((4,15),20,'SAT'),((1,8),20,'UNSAT'),((15,15),1,'UNKNOWN'),((0,15),20,'UNSAT')]:
        answer=search_from(solver,domains,max_nodes=cap)
        indices=[[i for i in range(4)if bits>>i&1]for bits in domains]
        assert verify_from(tables,relations,answer['tree'],indices)==answer['status']==expected
        assert solver.initial==original
    with pytest.raises(AssertionError):search_from(solver,(16,15),max_nodes=20)
    with pytest.raises(AssertionError):search_from(solver,(1,15),max_nodes=-1)
    assert solver.initial==original


def test_false_parent_witness_is_rejected():
    tables=[np.array([[0],[1]])];relations=[[(0,),(1,)]]
    with pytest.raises(AssertionError):verify_from(tables,relations,dict(kind='SAT',propagation=[],witness=[0]),[[1]])
