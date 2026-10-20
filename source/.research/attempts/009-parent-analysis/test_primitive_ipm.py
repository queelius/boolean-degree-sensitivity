"""Exact row rescaling and IPM without crossover must preserve the intended LP."""
from fractions import Fraction
from importlib.util import find_spec
from itertools import product
import json
import pytest
from baseline_full_truth_model import Row
from exact_box_row_lp import verify_certificate


def primitive(row):
    assert find_spec('primitive_box_rows') is not None, 'primitive integer row normalizer is missing'
    from primitive_box_rows import primitive_row
    return primitive_row(row)


def solve(*args,**kwargs):
    assert find_spec('diagnostic_box_ipm_nocrossover') is not None, 'no-crossover IPM kernel is missing'
    from diagnostic_box_ipm_nocrossover import solve as run
    return run(*args,**kwargs)


@pytest.mark.parametrize('row,want',[
    (Row(((0,8),(1,-12)),-4,16,{}),4),
    (Row(((0,-6),(1,12)),6,6,{}),6),
    (Row((),0,0,{}),1),
    (Row((),6,6,{}),6)])
def test_integer_primitive_rows_preserve_all_rational_box_assignments(row,want):
    normalized,divisor=primitive(row);assert divisor==want
    for assignment in product([Fraction(i,4) for i in range(5)],repeat=2):
        old=sum(assignment[i]*a for i,a in row.terms);new=sum(assignment[i]*a for i,a in normalized.terms)
        assert (row.lower<=old<=row.upper)==(normalized.lower<=new<=normalized.upper)


def test_no_crossover_returns_the_interior_point_on_a_nonunique_optimal_face():
    row=Row(((0,1),(1,1)),1,1,{})
    answer=solve([row],2,seconds=5,presolve=False)
    assert answer.report['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'
    assert answer.primal==pytest.approx([.5,.5],abs=1e-6)
    assert answer.report['iterations']>0 and answer.report['crossover_iterations']==0
    assert answer.report['proof_verified'] is False
    json.dumps(answer.report,allow_nan=False)


def test_scaled_infeasible_box_row_still_has_an_exact_certificate():
    row,_=primitive(Row(((0,4),),8,8,{}));answer=solve([row],1,seconds=5,presolve=False)
    assert answer.report['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
    assert verify_certificate([row],1,answer.report['certificate'])<0
    json.dumps(answer.report,allow_nan=False)


def test_zero_iterations_remain_inconclusive_without_crossover():
    answer=solve([Row(((0,1),(1,1)),1,1,{})],2,seconds=5,presolve=False,max_iterations=0)
    assert answer.report['solver_status']==1 and answer.report['status']=='INCONCLUSIVE_BOX_ROW_LP'
    assert not answer.report['proof_verified'] and 'certificate' not in answer.report


def test_noninteger_row_is_not_silently_rounded():
    with pytest.raises(ValueError):primitive(Row(((0,.5),),0,1,{}))
