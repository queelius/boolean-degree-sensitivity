from variable_cubic_energy import build,CubicKind
from fixed_projection_cube_domains import projection_values
from exact_box_row_lp import solve,verify_certificate


def test_coefficient_energy_accepts_projection_and_certifies_wrong_count():
    spectrum=[(q,1) for q in (11,14,25,35,49,70,76,88,98,112)]+[(q,-1) for q in (2,4,8,64)]+[(7,-2)]
    values=[[v] for v in projection_values(spectrum,7)];variables,rows=build(7,1,values);coeff=dict(spectrum)
    assignment=[int(coeff.get(v.support,0)==(-1 if v.kind==CubicKind.LINEAR else 1 if v.kind==CubicKind.POSITIVE else -2)) for v in variables]
    assert all(r.lower<=sum(k*assignment[i] for i,k in r.terms)<=r.upper for r in rows)
    assert solve(rows,len(variables),seconds=10)['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'
    wrong,bad=build(7,2,values);result=solve(bad,len(wrong),seconds=10)
    assert result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION' and verify_certificate(bad,len(wrong),result['certificate'])<0


def test_finite_value_weights_and_optional_energy():
    values=[[-4,4] for _ in range(16)];values[0]=[-12,4];values[15]=[-4,12]
    variables,rows=build(4,1,values);assert any(v.kind==CubicKind.VALUE for v in variables)
    plain,intervals=build(4,1,values,energy=False)
    assert all(v.kind!=CubicKind.VALUE for v in plain) and len(rows)>len(intervals)
