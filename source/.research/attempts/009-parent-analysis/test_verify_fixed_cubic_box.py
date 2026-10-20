from copy import deepcopy
from pathlib import Path
import json,gzip
import pytest
from verify_fixed_cubic_box import FixedCubicChecker


def fixture():
    h=Path(__file__).resolve().parent;s=json.loads((h/'fixed-cubic-box-pilot-cycle107.json').read_text());record=s['records'][0]
    detail=json.loads(gzip.decompress(Path(record['proof']['path']).read_bytes()));parent=json.loads(gzip.decompress(Path(s['parent']['path']).read_bytes()))
    rows=json.loads((h/'two-positive-pair-embeddings.json').read_text())['domain']['rows'];return FixedCubicChecker(rows,s['geometry']),parent['domains'],detail


def test_literal_fixed_cubic_certificate():
    checker,domains,detail=fixture();assert checker.verify(domains,detail)['integer_rhs']<0


def test_changed_certificate_and_variable_support_rejected():
    checker,domains,detail=fixture();bad=deepcopy(detail);bad['result']['certificate']['integer_rhs']+=1
    with pytest.raises(AssertionError):checker.verify(domains,bad)
    bad=deepcopy(detail);bad['variables'][0][0]=0
    with pytest.raises(AssertionError):checker.verify(domains,bad)
