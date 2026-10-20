"""Restored vectors are checked in original coordinates and exact arithmetic."""
import numpy as np
import pytest
from scipy.optimize._highspy import _core as h
from baseline_full_truth_model import Row
from raw_box_ipm import phase_one,reconstruct
from raw_highs_postsolve import restore


def compact_candidate(phase):
    lp=h.HighsLp();lp.num_col_=len(phase.objective);lp.num_row_=len(phase.bounds)
    lp.col_cost_=phase.objective;lp.col_lower_=phase.lower;lp.col_upper_=phase.upper
    lp.row_lower_=np.full(lp.num_row_,-np.inf);lp.row_upper_=phase.bounds
    lp.a_matrix_.num_col_=lp.num_col_;lp.a_matrix_.num_row_=lp.num_row_
    lp.a_matrix_.format_=h.MatrixFormat.kColwise
    lp.a_matrix_.start_=phase.matrix.indptr;lp.a_matrix_.index_=phase.matrix.indices;lp.a_matrix_.value_=phase.matrix.data
    pre=h._Highs();pre.setOptionValue('output_flag',False);pre.setOptionValue('solver','ipm');pre.setOptionValue('run_crossover','off')
    assert pre.passModel(lp)==h.HighsStatus.kOk
    assert pre.presolve()!=h.HighsStatus.kError
    reduced=pre.getPresolvedLp();solver=h._Highs()
    solver.setOptionValue('output_flag',False);solver.setOptionValue('solver','ipm')
    solver.setOptionValue('presolve','off');solver.setOptionValue('run_crossover','off')
    assert solver.passModel(reduced)==h.HighsStatus.kOk
    assert solver.run()!=h.HighsStatus.kError
    solution=solver.getSolution()
    x=np.pad(np.array(solution.col_value),(0,len(phase.objective)-reduced.num_col_))
    d=np.pad(np.array(solution.row_dual),(0,len(phase.bounds)-reduced.num_row_))
    return x,d


@pytest.mark.parametrize('target', [1,3])
def test_positive_and_negative_controls_round_trip_to_original_rows(target):
    rows=[Row(((0,1),(1,1)),target,target,{})]
    phase=phase_one(rows,3)  # An intentionally unused column must be restored.
    x,d=compact_candidate(phase)
    answer=restore(phase,x,d)
    assert answer['report']['presolved_columns']<len(phase.objective)
    assert answer['report']['restored_phase_maximum_row_violation']<1e-6
    assert len(answer['values'])==4 and len(answer['duals'])==2
    exact=reconstruct(rows,3,answer['duals'])
    if target==3:assert exact['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
    else:assert exact['status']=='INCONCLUSIVE_BOX_ROW_LP'


def test_nonzero_discarded_tail_is_rejected():
    phase=phase_one([Row(((0,1),(1,1)),1,1,{})],3)
    x,d=compact_candidate(phase);x[-1]=7
    with pytest.raises(ValueError):restore(phase,x,d)


def test_wrong_length_or_nonfinite_arrays_are_rejected():
    phase=phase_one([Row(((0,1),),2,2,{})],1)
    with pytest.raises(ValueError):restore(phase,[0],[-1,-1])
    with pytest.raises(ValueError):restore(phase,[0,float('nan')],[-1,-1])
