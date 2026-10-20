"""Independent scalar value, squared-norm and total equations."""
from dataclasses import asdict
from copy import deepcopy
from importlib.util import find_spec
import pytest
from bounded_core_spectrum_lp import prepare,CoefficientTotal
from selfdual_core_projection import ProjectedCoefficient
from diagnostic_box_ipm import solve
from test_bounded_core_spectrum_lp import character_control


def readers(pools,blocks,coefficients,totals=(),include_moments=True):
    assert find_spec('literal_bounded_core_spectrum_rows') is not None, 'literal bounded spectrum rows are missing'
    from literal_bounded_core_spectrum_rows import LiteralBoundedSpectrumRows
    literal=LiteralBoundedSpectrumRows(pools,[(b.features,b.values) for b in blocks],
        [asdict(c) for c in coefficients],[asdict(t) for t in totals],include_moments=include_moments)
    model=prepare(pools,blocks,coefficients,totals=totals,include_moments=include_moments)
    assert literal.coefficient_records()==model.coefficient_records()
    assert literal.partition_records()==model.base.partition_records()
    assert literal.variable_count==model.variable_count
    assert [literal.row(i) for i in range(literal.row_count)]==[(dict(r.terms),r.lower,r.upper) for r in model.rows()]
    inventory=model.inventory();assert all(inventory[k]==v for k,v in literal.inventory().items())
    return model,literal


@pytest.mark.parametrize('target',[15,16])
def test_literal_rows_and_integer_certificates_for_real_character(target):
    model,literal=readers(*character_control(),totals=[CoefficientTotal((241,),target)])
    result=solve(list(model.rows()),model.variable_count,seconds=5).report
    if target==16:assert result['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'
    else:
        assert result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
        assert literal.verify(result['certificate'])<0
        bad=deepcopy(result['certificate']);bad['integer_rhs']+=1
        with pytest.raises(AssertionError):literal.verify(bad)


@pytest.mark.parametrize('moments',[False,True])
def test_literal_average_of_squares_distinguishes_the_weak_model(moments):
    model,literal=readers([[(-1,),(1,)]]*2,[],[ProjectedCoefficient(0,0,0,(0,))],include_moments=moments)
    result=solve(list(model.rows()),model.variable_count,seconds=5).report
    if moments:assert literal.verify(result['certificate'])<0
    else:assert result['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'


def test_negative_coefficients_and_fixed_square_offset_are_literal():
    readers([[(-3,)],[(-1,)]],[],[ProjectedCoefficient(0,0,0,(-2,)),ProjectedCoefficient(0,1,1,(-1,0))],
        totals=[CoefficientTotal((0,1),-3)])
