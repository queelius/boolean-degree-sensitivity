"""Reject partial-group evidence and incomplete covers at the whole-case boundary."""
from copy import deepcopy
import pytest
from first_case_spectrum_scope import CaseScope, input_scope


def record():
    return dict(status='INDEPENDENTLY_VERIFIED_FIRST_CASE_FULL_SPECTRUM_INPUTS',
        scope=dict(kind='complete_first_case',geometry_index=34,first_row=163,
            quotient_authority=dict(path='/tmp/quota.json',sha256='a'*64)),
        complete_original_pattern_cover=True,complete_word_pool_cover=True,
        complete_projected_coefficient_cover=True,empty_points=[])


def test_complete_input_authority_preserves_the_exact_case_and_quota():
    r=record(); scope=input_scope(r)
    assert scope.geometry_index==34 and scope.first_row==163
    assert scope.to_data()==r['scope']


@pytest.mark.parametrize('key', ['complete_original_pattern_cover','complete_word_pool_cover','complete_projected_coefficient_cover'])
@pytest.mark.parametrize('bad', [False,None,1])
def test_any_missing_or_nonboolean_cover_is_rejected(key,bad):
    r=record();r[key]=bad
    with pytest.raises(ValueError):input_scope(r)


@pytest.mark.parametrize('change', [
    {'kind':'conditional_product_group'}, {'geometry_index':True}, {'first_row':-1},
    {'quotient_authority':{'path':'relative.json','sha256':'a'*64}},
    {'quotient_authority':{'path':'/tmp/quota.json','sha256':'z'*64}},
])
def test_invalid_or_narrower_scope_cannot_become_a_whole_first_case(change):
    r=record();r['scope'].update(change)
    with pytest.raises(ValueError):input_scope(r)


def test_wrong_authority_and_empty_word_domain_cannot_start_an_lp():
    r=record();r['status']='PROPOSED_FIRST_CASE_FULL_SPECTRUM_INPUTS'
    with pytest.raises(ValueError):input_scope(r)
    r=record();r['empty_points']=[0]
    with pytest.raises(ValueError):input_scope(r)


def test_missing_scope_field_and_extra_group_claim_are_rejected():
    r=record();del r['scope']['first_row']
    with pytest.raises(ValueError):input_scope(r)
    r=record();r['scope']['group_index']=0
    with pytest.raises(ValueError):input_scope(r)
