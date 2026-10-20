"""End-to-end finite controls for a changed categorical row basis."""
import numpy as np
import pytest
from bounded_core_spectrum_lp import prepare
from core_slice_degree_lp import PatternBlock
from selfdual_core_projection import ProjectedCoefficient
from transfer_spectrum_row_weights import transfer
from simplex_row_reconstruction import reconstruct
from exact_box_row_lp import verify_certificate


def model(domain):
    return prepare([[tuple([v]) for v in domain]],
                   [PatternBlock((0,),np.array([[[v]] for v in domain],dtype=np.int8))],
                   [ProjectedCoefficient(0,0,0,(0,))],include_moments=False)


@pytest.mark.parametrize('domain,expected_columns,expected_rhs', [
    ((1,2),[2,2,-1,0],-1),
    ((0,1,2),[0,2,2,0,-1,0],1),
])
def test_transferred_equality_combination_respects_feasible_and_infeasible_domains(domain,expected_columns,expected_rhs):
    source=model((0,1,2)); target=model(domain)
    source_rows=list(source.rows()); target_rows=list(target.rows())
    weights=[]
    for row in source_rows:
        kind=row.reason['kind']
        weights.append(-1 if kind=='bounded_spectrum_value' else
                       1 if kind=='slice_tuple_distribution' and row.reason['value']==[1] else 0)
    moved=transfer([r.reason for r in source_rows],weights,[r.reason for r in target_rows],
                   target.base.partition_records())
    columns=[0]*target.variable_count
    for row,w in zip(target_rows,moved):
        for j,a in row.terms: columns[j]+=w*a
    assert columns==expected_columns
    length=len(domain)
    result=reconstruct(target_rows,target.variable_count,moved,[list(range(length)),list(range(length,2*length))])
    assert result['integer_rhs']==expected_rhs
    if expected_rhs<0:
        assert verify_certificate(target_rows,target.variable_count,result['certificate'])==-1
    else:
        assert result['status']=='INCONCLUSIVE_BOX_ROW_LP' and 'certificate' not in result
