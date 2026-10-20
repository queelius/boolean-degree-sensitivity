from copy import deepcopy
import pytest
from verify_cubic_parent_energy import remaining_patterns


def test_partial_pilot_cannot_exclude_untested_patterns_or_counts():
    pending=[dict(index=0,negative=[7]),dict(index=1,negative=[13])]
    records=[dict(index=0,negative=[7],linear_count=q,excluded=True) for q in range(0,11,2)]
    assert remaining_patterns(pending,pending[:1],records)==pending[1:]
    bad=deepcopy(records);bad[-1]['excluded']=False
    assert remaining_patterns(pending,pending[:1],bad)==pending
    with pytest.raises(AssertionError):remaining_patterns(pending,pending[:1],records[:-1])
