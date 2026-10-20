from pathlib import Path
import json
from fixed_cubic_energy import build
from exact_box_row_lp import solve


def test_exact_cubic_projection_passes_energy_and_wrong_count_fails():
    c=json.loads(Path(__file__).with_name('missing-diagonal-one-negative-control-cycle107.json').read_text())['control']
    coefs={q:1 for q in c['positive']}|{q:-2 for q in c['negative']}|{q:-1 for q in c['linear']}
    values=[[sum(k*(-1)**((q&x).bit_count()) for q,k in coefs.items())] for x in range(1024)]
    variables,rows=build(c['negative'],values,4)
    assert solve(rows,len(variables),seconds=5)['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'
    variables,rows=build(c['negative'],values,2)
    assert solve(rows,len(variables),seconds=5)['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
