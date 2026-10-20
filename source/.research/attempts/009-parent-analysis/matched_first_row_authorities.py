"""Normalize accepted batch records into explicitly scoped first-row exclusions."""


def closed_batch_rows(batch,geometry,marked_pair,quota_reference):
    assert batch['status']=='INDEPENDENTLY_VERIFIED_FIXED_FIRST_ROW_COMPONENT_SEARCH_BATCH'
    assert batch['geometry_index']==geometry and batch['marked_pair']==marked_pair
    assert batch['quotient_authority']==quota_reference
    result=[]
    for i,record in enumerate(batch['records']):
        if record['search_status']=='UNSAT':
            assert record['conditional_case_excluded']is True and record['unsearched_subtrees']==0
            assert record['necessary_component_witness']is None
            result.append((i,record['first_row'],record['verified_nodes']))
        else:
            assert record['search_status']in('UNKNOWN','SAT') and record['conditional_case_excluded']is False
    return result
