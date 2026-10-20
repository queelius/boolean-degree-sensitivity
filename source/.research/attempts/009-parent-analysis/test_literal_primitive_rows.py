"""Independent gcd reconstruction must certify the scaled integer inequalities."""
from copy import deepcopy
from importlib.util import find_spec
import pytest
from baseline_full_truth_model import Row
from diagnostic_box_ipm_nocrossover import solve
from primitive_box_rows import primitive_row


class Matrix:
    def __init__(self,rows,n):self.rows=rows;self.row_count=len(rows);self.variable_count=n
    def row(self,index):
        assert type(index) is int and 0<=index<self.row_count
        return self.rows[index]


def reader(base):
    assert find_spec('literal_primitive_rows') is not None, 'literal primitive rows are missing'
    from literal_primitive_rows import LiteralPrimitiveRows
    return LiteralPrimitiveRows(base)


def test_signed_bounds_and_zero_rows_have_exact_independent_divisors():
    base=Matrix([({0:8,1:-12},-4,16),({},0,0),({0:-6,1:12},6,6)],2)
    checked=reader(base)
    assert list(checked.divisors)==[4,1,6]
    assert [checked.row(i) for i in range(3)]==[({0:2,1:-3},-1,4),({},0,0),({0:-1,1:2},1,1)]
    assert checked.scaling_inventory()['maximum_original_coefficient']==12
    assert checked.scaling_inventory()['maximum_primitive_coefficient']==3


def test_scaled_farkas_certificate_and_damaged_rhs_or_multiplier():
    original=Row(((0,4),),8,8,{});row,_=primitive_row(original)
    result=solve([row],1,seconds=5,presolve=False).report;assert result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
    checked=reader(Matrix([(dict(original.terms),original.lower,original.upper)],1));certificate=result['certificate']
    assert checked.verify(certificate)<0
    for fault in ('rhs','multiplier','row'):
        bad=deepcopy(certificate)
        if fault=='rhs':bad['integer_rhs']+=1
        elif fault=='multiplier':bad['terms'][0][2]*=2
        else:bad['terms'][0][0]=1
        with pytest.raises(AssertionError):checked.verify(bad)
