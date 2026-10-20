"""Whole-case frontier updates require exact evidence in the identical scope."""
from copy import deepcopy
import pytest
from first_case_spectrum_exclusion import validate


def fixture():
    quota=dict(path='/tmp/quota.json',sha256='a'*64)
    proof=dict(status='INDEPENDENTLY_VERIFIED_FIRST_CASE_FULL_SPECTRUM_MODEL',
        scope=dict(kind='complete_first_case',geometry_index=34,first_row=163,quotient_authority=quota),
        result_status='EXACT_BOX_ROW_LP_CONTRADICTION',exact_integer_rhs=-3,
        exact_certificate_verified=True,whole_first_case_excluded=True,
        all_original_rows_and_divisors_rebuilt=True,saved_primitive_matrix_equal_literal_rows=True,
        complete_distribution_partitions_rebuilt=True,all_projected_coefficient_domains_rebuilt=True,
        all_value_moment_and_budget_rows_rebuilt=True,input_cover_independent_authority_referenced=True,
        run_source=dict(path='/tmp/run.json',sha256='b'*64))
    frontier=dict(status='VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER',
        scope=dict(geometry_index=34,marked_pair=4097,quotient_authority=quota),remaining_first_rows=[163,596])
    return proof,frontier


def test_exact_same_scope_certificate_identifies_one_complete_case():
    assert validate(*fixture())==163


@pytest.mark.parametrize('key', ['exact_certificate_verified','whole_first_case_excluded',
    'all_original_rows_and_divisors_rebuilt','saved_primitive_matrix_equal_literal_rows',
    'complete_distribution_partitions_rebuilt','all_projected_coefficient_domains_rebuilt',
    'all_value_moment_and_budget_rows_rebuilt','input_cover_independent_authority_referenced'])
def test_missing_mathematical_check_prevents_an_exclusion(key):
    p,f=fixture();p[key]=False
    with pytest.raises(ValueError):validate(p,f)


@pytest.mark.parametrize('rhs', [0,3,-0.5,None])
def test_only_strict_negative_integer_rhs_is_a_certificate(rhs):
    p,f=fixture();p['exact_integer_rhs']=rhs
    with pytest.raises(ValueError):validate(p,f)


def test_inconclusive_and_model_only_results_never_close_a_case():
    for status in ('INCONCLUSIVE_BOX_ROW_LP','MODEL_ONLY','NUMERICALLY_FEASIBLE_BOX_RELAXATION'):
        p,f=fixture();p['result_status']=status
        with pytest.raises(ValueError):validate(p,f)


@pytest.mark.parametrize('change', [{'geometry_index':19},{'first_row':58},{'kind':'conditional_product_group'},
    {'quotient_authority':dict(path='/tmp/quota.json',sha256='c'*64)}])
def test_different_geometry_case_quota_or_group_scope_is_rejected(change):
    p,f=fixture();p['scope'].update(change)
    with pytest.raises(ValueError):validate(p,f)


def test_proposals_missing_runs_and_unverified_frontiers_are_rejected():
    p,f=fixture();p['status']='PROPOSED_FIRST_CASE_FULL_SPECTRUM_LP_RUN'
    with pytest.raises(ValueError):validate(p,f)
    p,f=fixture();p['run_source']=None
    with pytest.raises(ValueError):validate(p,f)
    p,f=fixture();f['status']='PROPOSED_FRONTIER'
    with pytest.raises(ValueError):validate(p,f)
