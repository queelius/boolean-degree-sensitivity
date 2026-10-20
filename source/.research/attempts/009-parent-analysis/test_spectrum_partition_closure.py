"""A partial, numerical, or differently scoped certificate must not close a case."""
from copy import deepcopy
import pytest
from spectrum_partition_closure import validate


def sample():
    names = ('groups', 'spectrum', 'inputs', 'base', 'zero', 'support')
    refs = {name: dict(path=name+'.json', sha256=name) for name in names}
    quotient = dict(path='quotient.json', sha256='quotient')
    scope = dict(geometry_index=34, first_row=58)
    group_scope = dict(scope, group_index=0)
    docs = dict(
        groups=dict(scope, quotient_authority=quotient,
            status='INDEPENDENTLY_VERIFIED_MATCHED_PRODUCT_GROUP_SEARCH',
            complete_exact_group_cover=True, group_count=2, necessary_component_witnesses=[],
            groups=[dict(group_index=0, search_status='UNKNOWN', unsearched_subtrees=1, zero_product=True, verified_search_nodes=3),
                    dict(group_index=1, search_status='UNSAT', unsearched_subtrees=0, zero_product=False, verified_search_nodes=5)]),
        spectrum=dict(group_scope, status='INDEPENDENTLY_VERIFIED_PRIMITIVE_FULL_OUTSIDE_SPECTRUM_LP_MODEL',
            input_authority=refs['inputs'], input_source=dict(path='input-source.json', sha256='input-source'),
            all_original_rows_and_divisors_rebuilt=True, result_status='EXACT_BOX_ROW_LP_CONTRADICTION',
            exact_certificate_verified=True, exact_integer_rhs=-7, conditional_product_group_excluded=True),
        inputs=dict(group_scope, status='INDEPENDENTLY_VERIFIED_MATCHED_FULL_OUTSIDE_INPUTS',
            source=dict(path='input-source.json', sha256='input-source'), base_authority=refs['base'],
            zero_product_authority=refs['zero'], quotient_authority=quotient,
            complete_original_pattern_cover=True, complete_word_pool_cover=True, complete_projected_coefficient_cover=True),
        base=dict(group_scope, status='INDEPENDENTLY_VERIFIED_MATCHED_BINARY_SUPPORT_SEARCH',
            product_group_authority=refs['groups'], support_sum_authority=refs['support'], quotient_authority=quotient),
        zero=dict(scope, status='INDEPENDENTLY_VERIFIED_FIRST_CASE_SELECTED_SLICE_ZERO_PRODUCTS',
            product_group_authority=refs['groups'], support_sum_authority=refs['support'], quotient_authority=quotient,
            complete_first_case_necessary_restriction=True, all_complementary_products_zero_on_selected_slice=True),
        support=dict(group_scope, status='INDEPENDENTLY_VERIFIED_MATCHED_SUPPORT_SUM_JOIN',
            group_authority=refs['groups'], quotient_authority=quotient, complete_sum_cover=True))
    return docs, refs


def test_exact_closure_extends_complete_partition():
    docs, refs = sample()
    answer = validate(docs, refs)
    assert answer['geometry_index'] == 34 and answer['first_row'] == 58
    assert answer['group_count'] == 2 and answer['spectrum_closed_group'] == 0
    assert answer['previously_excluded_groups'] == [1] and answer['exact_integer_rhs'] == -7


@pytest.mark.parametrize('section,key,value', [
    ('spectrum','result_status','INCONCLUSIVE_BOX_ROW_LP'),
    ('spectrum','exact_certificate_verified',False),
    ('spectrum','conditional_product_group_excluded',False),
    ('spectrum','exact_integer_rhs',0),
    ('spectrum','exact_integer_rhs',-0.5),
    ('spectrum','all_original_rows_and_divisors_rebuilt',False),
    ('spectrum','group_index',1),
    ('spectrum','first_row',59),
    ('spectrum','input_source',{}),
    ('inputs','complete_original_pattern_cover',False),
    ('inputs','complete_word_pool_cover',False),
    ('inputs','complete_projected_coefficient_cover',False),
    ('inputs','base_authority',{}),
    ('base','product_group_authority',{}),
    ('base','quotient_authority',{}),
    ('zero','complete_first_case_necessary_restriction',False),
    ('zero','all_complementary_products_zero_on_selected_slice',False),
    ('zero','support_sum_authority',{}),
    ('support','complete_sum_cover',False),
    ('groups','complete_exact_group_cover',False),
    ('groups','group_count',3),
    ('groups','necessary_component_witnesses',[[0]]),
])
def test_partial_or_mismatched_authority_rejected(section,key,value):
    docs, refs = sample()
    docs[section][key] = value
    with pytest.raises(AssertionError):
        validate(docs, refs)


@pytest.mark.parametrize('change', [
    lambda rows: rows.pop(),
    lambda rows: rows[1].update(search_status='UNKNOWN'),
    lambda rows: rows[1].update(unsearched_subtrees=1),
    lambda rows: rows[1].update(group_index=0),
    lambda rows: rows[0].update(zero_product=False),
])
def test_uncovered_product_group_rejected(change):
    docs, refs = deepcopy(sample())
    change(docs['groups']['groups'])
    with pytest.raises(AssertionError):
        validate(docs, refs)
