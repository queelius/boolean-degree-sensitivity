from copy import deepcopy
from pathlib import Path
import json,gzip
import pytest
from verify_fixed_cubic_energy import EnergyChecker


def fixture():
    h=Path(__file__).resolve().parent;s=json.loads((h/'fixed-cubic-energy-pilot-cycle107.json').read_text())
    r=s['records'][0];detail=json.loads(gzip.decompress(Path(r['proof']['path']).read_bytes()));parent=json.loads(gzip.decompress(Path(s['parent']['path']).read_bytes()))
    rows=json.loads((h/'two-positive-pair-embeddings.json').read_text())['domain']['rows'];return EnergyChecker(rows,s['geometry']),parent['domains'],detail


def test_scalar_energy_certificate():
    checker,domains,detail=fixture();assert checker.verify(domains,detail)['integer_rhs']<0


def test_bad_value_state_and_certificate_rejected():
    checker,domains,detail=fixture();bad=deepcopy(detail);bad['variables'][129]['value']+=1
    with pytest.raises(AssertionError):checker.verify(domains,bad)
    bad=deepcopy(detail);bad['result']['certificate']['integer_rhs']+=1
    with pytest.raises(AssertionError):checker.verify(domains,bad)
