from pathlib import Path
from copy import deepcopy
import json,gzip
import pytest
from verify_cubic_energy_values import verify_energy
from verify_missing_diagonal_witnesses import ScalarValues
from two_negative_cubic_controls import controls
from fixed_cubic_energy import build
from exact_box_row_lp import solve


def test_existing_one_negative_certificate_and_changed_count():
    h=Path(__file__).resolve().parent;s=json.loads((h/'fixed-cubic-energy-pilot-cycle107.json').read_text())
    detail=json.loads(gzip.decompress(Path(s['records'][0]['proof']['path']).read_bytes()));parent=json.loads(gzip.decompress(Path(s['parent']['path']).read_bytes()))
    rows=json.loads((h/'two-positive-pair-embeddings.json').read_text())['domain']['rows'];values=ScalarValues(rows,s['geometry']).allowed(tuple(d['rows'][0] for d in parent['domains']),3)
    assert verify_energy(detail,values)['integer_rhs']<0
    bad=deepcopy(detail);bad['result']['certificate']['integer_rhs']+=1
    with pytest.raises(AssertionError):verify_energy(bad,values)


def test_genuine_two_negative_control_and_impossible_count_certificate():
    c=controls(6,[0,1])[0];coefs={q:1 for q in c['positive']}|{q:-2 for q in c['negative']}
    values=[[sum(k*(-1)**((q&x).bit_count()) for q,k in coefs.items())] for x in range(1024)]
    variables,rows=build(c['negative'],values,0);assert solve(rows,len(variables),seconds=5)['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'
    variables,rows=build(c['negative'],values,2);result=solve(rows,len(variables),seconds=5)
    detail=dict(core_mask=3,negative=c['negative'],linear_count=2,variables=[v.metadata() for v in variables],result=result)
    assert verify_energy(detail,values)['integer_rhs']<0
    bad=deepcopy(detail);bad['negative']=bad['negative'][:1]
    with pytest.raises(AssertionError):verify_energy(bad,values)
