from pathlib import Path
import json
from fixed_cubic_box import build
from exact_box_row_lp import solve


def fixture():
    c=json.loads(Path(__file__).with_name('missing-diagonal-one-negative-control-cycle107.json').read_text())['control']
    coefs={q:1 for q in c['positive']}|{q:-2 for q in c['negative']}|{q:-1 for q in c['linear']}
    values=[[sum(k*(-1)**((q&x).bit_count()) for q,k in coefs.items())] for x in range(1<<c['n'])]
    return c,values


def test_exact_cubic_positive_control():
    c,values=fixture();variables,rows=build(c['n'],c['negative'],values)
    assignment=[int(q in c['linear'] if sign==-1 else q in c['positive']) for q,sign in variables]
    assert all(r.lower<=sum(k*assignment[i] for i,k in r.terms)<=r.upper for r in rows)
    assert solve(rows,len(variables),seconds=5)['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'


def test_forbidden_high_degree_perturbation_negative_control():
    c,values=fixture();values[0]=[12];values[-1]=[-12]
    variables,rows=build(c['n'],c['negative'],values)
    assert solve(rows,len(variables),seconds=5)['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
