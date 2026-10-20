"""Catch lost original constraints, product signs/scales, and original row maps."""
import importlib
import numpy as np
import pytest
from append_product_value_relations import append_product_values
from finite_function_csp import FunctionCSP


def reader():
    return importlib.import_module('verify_cross_product_branch').verify_branch


@pytest.mark.parametrize('values,vector,normalization,want',[
    ((8,8,8,-8,0,0),1,8,'SAT'),
    ((8,8,8,-8,0,0),0,8,'UNSAT'),
    ((8,8,8,-8,0,0),-1,8,'UNSAT'),
    ((0,8,0,-8,0,0),0,8,'SAT'),
    ((127,127,127,-127,0,0),16129,1,'SAT'),
])
def test_literal_satisfiable_impossible_zero_and_wide_products(values,vector,normalization,want):
    tables=[np.array([[v]],dtype=np.int8) for v in values]
    relations=[[values]];pairs=[(0,1),(2,3)]
    new,allowed=append_product_values(tables,relations,[0],pairs,
                                     [[normalization**2*vector],[-normalization**2*vector]])
    answer=FunctionCSP(new,allowed).search(20)
    assert answer['status']==want
    assert reader()(tables,relations,[[0] for _ in tables],[0],pairs,[vector],answer['tree'],normalization)==want


def test_original_row_indices_select_the_certified_candidates():
    values=(8,8,8,-8,0,0)
    tables=[np.array([[0],[v]],dtype=np.int16) for v in values]
    tree=dict(kind='SAT',propagation=[],witness=[0]*6)
    assert reader()(tables,[[values]],[[1] for _ in tables],[0],[(0,1),(2,3)],[1],tree,8)=='SAT'
    with pytest.raises(AssertionError):
        reader()(tables,[[values]],[[0] for _ in tables],[0],[(0,1),(2,3)],[1],tree,8)


def test_old_relations_are_checked_even_when_appended_product_is_feasible():
    values=(8,8,8,-8,0,0)
    tables=[np.array([[v,1]],dtype=np.int16) for v in values]
    relations=[[values],[(0,)*6]]
    tree=dict(kind='UNSAT',propagation=[],contradiction_point=1)
    assert reader()(tables,relations,[[0] for _ in tables],[0],[(0,1),(2,3)],[1],tree,8)=='UNSAT'


def test_changed_product_rejects_a_previously_valid_sat_certificate():
    values=(8,8,8,-8,0,0);tables=[np.array([[v]],dtype=np.int16) for v in values]
    tree=dict(kind='SAT',propagation=[],witness=[0]*6)
    with pytest.raises(AssertionError):
        reader()(tables,[[values]],[[0] for _ in tables],[0],[(0,1),(2,3)],[0],tree,8)


def test_limit_tree_remains_unknown_and_invalid_domain_indices_are_rejected():
    values=(8,8,8,-8,0,0);tables=[np.array([[v]],dtype=np.int16) for v in values]
    good=[[0] for _ in tables]
    assert reader()(tables,[[values]],good,[0],[(0,1),(2,3)],[1],dict(kind='LIMIT'),8)=='UNKNOWN'
    for bad in (-1,1):
        domains=[list(d) for d in good];domains[0]=[bad]
        with pytest.raises(AssertionError):
            reader()(tables,[[values]],domains,[0],[(0,1),(2,3)],[1],dict(kind='LIMIT'),8)
