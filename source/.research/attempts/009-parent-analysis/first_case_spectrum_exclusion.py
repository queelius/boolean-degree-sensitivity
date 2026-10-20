"""Check scope and exact-result gates before a whole first case can be closed."""
from first_case_spectrum_scope import CaseScope


def validate(authority,frontier):
    if authority.get('status')!='INDEPENDENTLY_VERIFIED_FIRST_CASE_FULL_SPECTRUM_MODEL':
        raise ValueError('Require the independent whole-case model and certificate reader.')
    if frontier.get('status')!='VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER':
        raise ValueError('Require an accepted first-row frontier.')
    scope=CaseScope.from_data(authority.get('scope'))
    for key in ('exact_certificate_verified','whole_first_case_excluded','all_original_rows_and_divisors_rebuilt',
                'saved_primitive_matrix_equal_literal_rows','complete_distribution_partitions_rebuilt',
                'all_projected_coefficient_domains_rebuilt','all_value_moment_and_budget_rows_rebuilt',
                'input_cover_independent_authority_referenced'):
        if authority.get(key) is not True: raise ValueError('Missing exact whole-case verification: '+key)
    rhs=authority.get('exact_integer_rhs')
    if authority.get('result_status')!='EXACT_BOX_ROW_LP_CONTRADICTION' or type(rhs) is not int or rhs>=0:
        raise ValueError('Only a strict exact contradiction excludes this case.')
    if not isinstance(authority.get('run_source'),dict):
        raise ValueError('An executed certificate source is required.')
    parent=frontier['scope']
    if scope.geometry_index!=parent['geometry_index'] or scope.to_data()['quotient_authority']!=parent['quotient_authority']:
        raise ValueError('The certificate and frontier have different scopes.')
    if scope.first_row not in frontier['remaining_first_rows']:
        raise ValueError('The certified first case is not open in this frontier.')
    return scope.first_row
