"""Reject accidental import of a stronger or differently scoped refinement."""
from copy import deepcopy
import importlib
import pytest


def fixture():
    quota=dict(path='quotient.json',sha256='q')
    refinement=dict(path='cross.json',sha256='c')
    join=dict(status='INDEPENDENTLY_VERIFIED_MATCHED_VANISHING_SLICE_PRODUCT_JOIN',
              geometry_index=34,quotient_authority=quota,refinement_authority=refinement)
    cross=dict(status='INDEPENDENTLY_VERIFIED_MATCHED_ORDINARY_CROSS_REFINEMENT',
               geometry_index=34,complete_actual_cover=True)
    return join,cross,deepcopy(quota),deepcopy(refinement)


def test_exact_cross_scope_is_accepted():
    check=importlib.import_module('cross_product_scope').require_cross_source
    assert check(*fixture()) is None


@pytest.mark.parametrize('which,field,value',[
    (0,'status','PROPOSED_MATCHED_VANISHING_SLICE_PRODUCT_JOIN'),
    (0,'geometry_index',19),
    (1,'status','INDEPENDENTLY_VERIFIED_MATCHED_Q4_FRONTIER_REFINEMENT'),
    (1,'complete_actual_cover',False),
    (2,'sha256','different-quotient'),
    (3,'sha256','different-refinement'),
    (3,'path','stronger-unproved-refinement.json'),
])
def test_incomplete_or_mismatched_scopes_are_rejected(which,field,value):
    args=list(fixture());args[which][field]=value
    check=importlib.import_module('cross_product_scope').require_cross_source
    with pytest.raises(AssertionError):check(*args)
