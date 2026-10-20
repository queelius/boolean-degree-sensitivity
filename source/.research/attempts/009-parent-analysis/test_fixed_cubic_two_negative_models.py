from two_negative_cubic_controls import controls
from fixed_cubic_box import build as box
from fixed_cubic_energy import build as energy
from exact_box_row_lp import solve


def fixture():
    c=controls(6,[0,1])[0];coefs={q:1 for q in c['positive']}|{q:-2 for q in c['negative']}
    return c,[[sum(k*(-1)**((q&x).bit_count()) for q,k in coefs.items())] for x in range(1024)]


def test_two_negative_interval_and_energy_positive_control():
    c,values=fixture()
    for variables,rows in (box(10,c['negative'],values),energy(c['negative'],values,0)):
        assert solve(rows,len(variables),seconds=5)['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'


def test_two_negative_wrong_linear_count_rejected():
    c,values=fixture();variables,rows=energy(c['negative'],values,2)
    assert solve(rows,len(variables),seconds=5)['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
