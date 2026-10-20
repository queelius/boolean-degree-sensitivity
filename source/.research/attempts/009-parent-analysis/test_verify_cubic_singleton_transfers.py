from pathlib import Path
from copy import deepcopy
import json
import pytest
from verify_cubic_singleton_transfers import actual_singletons


def fixture():
    h=Path(__file__).resolve().parent
    return json.loads((h/'two-positive-pair-embeddings.json').read_text()),json.loads((h/'safe-four-cycle-first-second-covers-independent-manifest.json').read_text())['actual_frames']


def test_actual_one_negative_diagonals_have_one_or_two_apices():
    data,frames=fixture();evidence=actual_singletons(data,frames)
    assert len(evidence)==42 and sum(r['apex_count']==1 for r in evidence)==5 and sum(r['apex_count']==2 for r in evidence)==37


def test_uncovered_empty_diagonal_is_rejected():
    data,frames=fixture();bad=deepcopy(data);bad['representatives'][frames[0]['geometry']]['negative_supports']=[]
    with pytest.raises(AssertionError):actual_singletons(bad,frames)
