from pathlib import Path
from copy import deepcopy
import json
import pytest
from verify_cubic_negative_pair_cover import verify_cover,signature


def fixture():return json.loads(Path(__file__).with_name('cubic-two-negative-position-cover-cycle108.json').read_text())


def test_complete_literal_pair_cover():
    data=fixture();assert verify_cover(data)==data['representative_count']


def test_missing_map_and_broken_permutation_rejected():
    data=fixture();bad=deepcopy(data);bad['maps'].pop()
    with pytest.raises(AssertionError):verify_cover(bad)
    bad=deepcopy(data);bad['maps'][0]['map'][0]=bad['maps'][0]['map'][1]
    with pytest.raises(AssertionError):verify_cover(bad)


def test_signature_retains_apex_and_intersection_information():
    assert signature([13,50],[0,1])==signature([14,49],[0,1])==(1,2,0)
    assert signature([13,14],[0,1])==(1,2,2)
