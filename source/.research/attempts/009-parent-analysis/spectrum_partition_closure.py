"""Validate a complete product cover extended by an exact spectrum certificate."""


def validate(authorities, references):
    groups = authorities['groups']
    spectrum = authorities['spectrum']
    inputs = authorities['inputs']
    base = authorities['base']
    zero = authorities['zero']
    support = authorities['support']
    assert groups['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_PRODUCT_GROUP_SEARCH'
    assert spectrum['status'] == 'INDEPENDENTLY_VERIFIED_PRIMITIVE_FULL_OUTSIDE_SPECTRUM_LP_MODEL'
    assert inputs['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FULL_OUTSIDE_INPUTS'
    assert base['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_BINARY_SUPPORT_SEARCH'
    assert zero['status'] == 'INDEPENDENTLY_VERIFIED_FIRST_CASE_SELECTED_SLICE_ZERO_PRODUCTS'
    assert support['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_SUPPORT_SUM_JOIN'
    assert spectrum['input_authority'] == references['inputs']
    assert spectrum['input_source'] == inputs['source']
    assert inputs['base_authority'] == references['base']
    assert inputs['zero_product_authority'] == references['zero']
    assert base['product_group_authority'] == zero['product_group_authority'] == support['group_authority'] == references['groups']
    assert base['support_sum_authority'] == zero['support_sum_authority'] == references['support']
    for document in authorities.values():
        assert document['geometry_index'] == groups['geometry_index']
        assert document['first_row'] == groups['first_row']
    for document in (inputs, base, zero, support):
        assert document['quotient_authority'] == groups['quotient_authority']
    group = spectrum['group_index']
    assert type(group) is int and group == inputs['group_index'] == base['group_index'] == support['group_index']
    assert spectrum['all_original_rows_and_divisors_rebuilt'] is True
    assert spectrum['result_status'] == 'EXACT_BOX_ROW_LP_CONTRADICTION'
    assert spectrum['exact_certificate_verified'] is True and spectrum['conditional_product_group_excluded'] is True
    rhs = spectrum['exact_integer_rhs']
    assert type(rhs) is int and rhs < 0
    assert inputs['complete_original_pattern_cover'] is True
    assert inputs['complete_word_pool_cover'] is True
    assert inputs['complete_projected_coefficient_cover'] is True
    assert zero['complete_first_case_necessary_restriction'] is True
    assert zero['all_complementary_products_zero_on_selected_slice'] is True
    assert support['complete_sum_cover'] is True
    assert groups['complete_exact_group_cover'] is True and groups['necessary_component_witnesses'] == []
    count = groups['group_count']
    assert type(count) is int and count > 0 and 0 <= group < count
    assert [row['group_index'] for row in groups['groups']] == list(range(count))
    assert groups['groups'][group]['zero_product'] is True
    excluded = []
    for row in groups['groups']:
        if row['group_index'] != group:
            assert row['search_status'] == 'UNSAT' and row['unsearched_subtrees'] == 0
            excluded.append(row['group_index'])
    return dict(geometry_index=groups['geometry_index'], first_row=groups['first_row'],
        quotient_authority=groups['quotient_authority'], group_count=count,
        spectrum_closed_group=group, previously_excluded_groups=excluded, exact_integer_rhs=rhs)
