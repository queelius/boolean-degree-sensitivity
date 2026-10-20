from copy import deepcopy
import pytest
from verify_incremental_cubic_transfers import validate_input_cover


def test_incremental_cover_rejects_omitted_pair_or_negative_count():
    prior=dict(remaining_pairs=1,remaining=[dict(pair_index=7,row_pair=[20,30],negative_counts=[1,2])])
    detail=dict(records=[dict(pair_index=7,row_pair=[20,30],counts=[dict(negative_count=1),dict(negative_count=2)])])
    assert validate_input_cover(prior,detail)=={7:prior['remaining'][0]}
    missing=deepcopy(detail);missing['records'][0]['counts'].pop()
    with pytest.raises(AssertionError):validate_input_cover(prior,missing)
    with pytest.raises(AssertionError):validate_input_cover(prior,dict(records=[]))
    duplicate=deepcopy(detail);duplicate['records'].append(duplicate['records'][0])
    with pytest.raises(AssertionError):validate_input_cover(prior,duplicate)
