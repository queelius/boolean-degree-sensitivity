from copy import deepcopy
import pytest
from verify_matched_first_row_cover import row_map_coverage


def test_explicit_row_cover_rejects_missing_duplicate_and_external_targets():
    representatives = [dict(index=0, row=0), dict(index=1, row=2)]
    maps = [dict(source_row=0, representative=0), dict(source_row=1, representative=0), dict(source_row=2, representative=1)]
    assert row_map_coverage(maps, representatives, 3) == [0, 2]
    wrong = deepcopy(maps); wrong[1]['source_row'] = 0
    outside = deepcopy(maps); outside[0]['representative'] = 2
    for damaged in (maps[:-1], wrong, outside):
        with pytest.raises(AssertionError): row_map_coverage(damaged, representatives, 3)
