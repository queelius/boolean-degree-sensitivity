import copy
import pytest
from matched_first_row_authorities import closed_batch_rows


def fixture():
    q=dict(path='quota',sha256='q')
    batch=dict(status='INDEPENDENTLY_VERIFIED_FIXED_FIRST_ROW_COMPONENT_SEARCH_BATCH',geometry_index=34,marked_pair=3,quotient_authority=q,
               records=[dict(first_row=7,search_status='UNSAT',conditional_case_excluded=True,unsearched_subtrees=0,necessary_component_witness=None,verified_nodes=9),
                        dict(first_row=8,search_status='UNKNOWN',conditional_case_excluded=False,unsearched_subtrees=2,necessary_component_witness=None,verified_nodes=10)])
    return batch,q


def test_only_exact_closed_cases_are_selected():
    batch,q=fixture()
    assert closed_batch_rows(batch,34,3,q)==[(0,7,9)]
    batch['records'][1].update(search_status='SAT',necessary_component_witness=[0]*6)
    assert closed_batch_rows(batch,34,3,q)==[(0,7,9)]


def test_wrong_scope_and_false_exclusions_rejected():
    batch,q=fixture()
    with pytest.raises(AssertionError):closed_batch_rows(batch,19,3,q)
    with pytest.raises(AssertionError):closed_batch_rows(batch,34,3,dict(path='wrong',sha256='q'))
    false=copy.deepcopy(batch);false['records'][0]['unsearched_subtrees']=1
    with pytest.raises(AssertionError):closed_batch_rows(false,34,3,q)
    false=copy.deepcopy(batch);false['records'][1]['conditional_case_excluded']=True
    with pytest.raises(AssertionError):closed_batch_rows(false,34,3,q)
