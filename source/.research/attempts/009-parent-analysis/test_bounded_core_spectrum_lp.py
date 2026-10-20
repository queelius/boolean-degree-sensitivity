"""Endpoint Fourier domains, shared word squares, and coefficient totals."""
from importlib.util import find_spec
from fractions import Fraction
from dataclasses import replace
import pytest
from selfdual_core_projection import ProjectedCoefficient
from diagnostic_box_ipm import solve
from exact_box_row_lp import verify_certificate
from test_core_slice_degree_lp import literal_pools,prepare_fixed,sign


def api():
    assert find_spec('bounded_core_spectrum_lp') is not None, 'bounded spectral model is missing'
    import bounded_core_spectrum_lp
    return bounded_core_spectrum_lp


def character_control():
    pools=literal_pools(6,lambda y,z:sign(y,15)*sign(z,1));old=prepare_fixed(pools)
    coefficients=[ProjectedCoefficient(0,0,0,(0,)),ProjectedCoefficient(1,15,241,(0,16))]
    coefficients.extend(ProjectedCoefficient(f,0,f,(0,)) for f in (2,4,8))
    return pools,old.blocks,coefficients


def test_boolean_degree_five_character_has_an_exact_integral_lift():
    m=api();model=m.prepare(*character_control(),totals=[m.CoefficientTotal((241,),16)])
    assignment=[Fraction(1)]*model.variable_count
    for row in model.rows():assert row.lower<=sum(assignment[i]*v for i,v in row.terms)<=row.upper
    result=solve(list(model.rows()),model.variable_count,seconds=5).report
    assert result['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'
    assert model.inventory()['spectral_norm_rows']==5 and model.inventory()['spectral_flags']==1


def test_wrong_global_coefficient_total_is_exactly_excluded():
    m=api();model=m.prepare(*character_control(),totals=[m.CoefficientTotal((241,),15)])
    rows=list(model.rows());result=solve(rows,model.variable_count,seconds=5).report
    assert result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
    assert verify_certificate(rows,model.variable_count,result['certificate'])<0


def test_square_of_the_average_cannot_replace_average_of_squares():
    m=api();pools=[[(-1,),(1,)]]*2;coefficients=[ProjectedCoefficient(0,0,0,(0,))]
    weak=m.prepare(pools,[],coefficients,include_moments=False)
    assert solve(list(weak.rows()),weak.variable_count,seconds=5).report['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'
    strong=m.prepare(pools,[],coefficients);rows=list(strong.rows())
    result=solve(rows,strong.variable_count,seconds=5).report
    assert result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
    assert verify_certificate(rows,strong.variable_count,result['certificate'])<0


def test_fixed_negative_and_negative_to_zero_domains_use_the_right_squared_sign():
    m=api();pools=[[(-3,)],[(-1,)]]
    coefficients=[ProjectedCoefficient(0,0,0,(-2,)),ProjectedCoefficient(0,1,1,(-1,0))]
    model=m.prepare(pools,[],coefficients);assignment=[1,1,0]
    assert model.variable_count==3
    for row in model.rows():assert row.lower<=sum(assignment[i]*v for i,v in row.terms)<=row.upper
    assert solve(list(model.rows()),model.variable_count,seconds=5).report['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'


def test_missing_character_is_a_real_restriction_and_not_silently_free():
    m=api();pools=[[(1,)],[(-1,)]]
    model=m.prepare(pools,[],[ProjectedCoefficient(0,0,0,(-1,1))])
    assert solve(list(model.rows()),model.variable_count,seconds=5).report['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'


@pytest.mark.parametrize('fault',['duplicate_character','duplicate_support','bad_feature','bad_character',
    'three_values','unordered_values','noninteger_value','unknown_total','duplicate_total_support'])
def test_inconsistent_domains_and_totals_are_rejected(fault):
    m=api();coefficients=[ProjectedCoefficient(0,0,0,(0,1))];totals=[]
    if fault=='duplicate_character':coefficients.append(replace(coefficients[0],support=1))
    elif fault=='duplicate_support':coefficients.append(replace(coefficients[0],character=1))
    elif fault=='bad_feature':coefficients[0]=replace(coefficients[0],feature=1)
    elif fault=='bad_character':coefficients[0]=replace(coefficients[0],character=2)
    elif fault=='three_values':coefficients[0]=replace(coefficients[0],values=(0,1,2))
    elif fault=='unordered_values':coefficients[0]=replace(coefficients[0],values=(1,0))
    elif fault=='noninteger_value':coefficients[0]=replace(coefficients[0],values=(0,0.5))
    elif fault=='unknown_total':totals=[m.CoefficientTotal((1,),0)]
    else:totals=[m.CoefficientTotal((0,0),0)]
    with pytest.raises(ValueError):m.prepare([[(0,)],[(1,)]],[],coefficients,totals=totals)
