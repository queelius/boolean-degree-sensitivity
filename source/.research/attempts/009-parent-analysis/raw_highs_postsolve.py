"""Rebuild deterministic presolve and restore a saved compacted numerical candidate."""
from time import monotonic
import numpy as np
from scipy.optimize._highspy import _core as h
from scipy.sparse import csc_matrix


def restore(phase, raw_values, raw_duals, *, display=False):
    start=monotonic();x=np.asarray(raw_values,dtype=float);dual=np.asarray(raw_duals,dtype=float)
    columns=len(phase.objective);rows=len(phase.bounds)
    if x.shape!=(columns,) or dual.shape!=(rows,) or not np.all(np.isfinite(x)) or not np.all(np.isfinite(dual)):
        raise ValueError('Require finite original-sized buffers.')
    lp=h.HighsLp();lp.num_col_=columns;lp.num_row_=rows
    lp.col_cost_=phase.objective;lp.col_lower_=phase.lower;lp.col_upper_=phase.upper
    lp.row_lower_=np.full(rows,-np.inf);lp.row_upper_=phase.bounds
    lp.a_matrix_.num_col_=columns;lp.a_matrix_.num_row_=rows;lp.a_matrix_.format_=h.MatrixFormat.kColwise
    lp.a_matrix_.start_=phase.matrix.indptr;lp.a_matrix_.index_=phase.matrix.indices;lp.a_matrix_.value_=phase.matrix.data
    highs=h._Highs()
    for key,value in dict(output_flag=bool(display),solver='ipm',run_crossover='off',presolve='on',time_limit=60.0).items():
        assert highs.setOptionValue(key,value)==h.HighsStatus.kOk
    assert highs.passModel(lp)==h.HighsStatus.kOk
    presolve_status=highs.presolve()
    if presolve_status==h.HighsStatus.kError:raise ValueError('Presolve failed.')
    reduced=highs.getPresolvedLp();n=reduced.num_col_;m=reduced.num_row_
    if n>columns or m>rows or np.any(x[n:]!=0) or np.any(dual[m:]!=0):
        raise ValueError('Saved buffers do not have the required zero padding.')
    assert reduced.a_matrix_.format_==h.MatrixFormat.kColwise
    matrix=csc_matrix((reduced.a_matrix_.value_,reduced.a_matrix_.index_,reduced.a_matrix_.start_),shape=(m,n))
    x=x[:n].copy();dual=dual[:m].copy();row_values=matrix@x
    violation=max(float(np.max(row_values-np.asarray(reduced.row_upper_),initial=0)),
        float(np.max(np.asarray(reduced.row_lower_)-row_values,initial=0)),
        float(np.max(np.asarray(reduced.col_lower_)-x,initial=0)),float(np.max(x-np.asarray(reduced.col_upper_),initial=0)))
    if violation>1e-5:raise ValueError('The compacted candidate does not satisfy the presolved phase model.')
    solution=h.HighsSolution();solution.col_value=x;solution.row_value=row_values
    solution.row_dual=dual;solution.col_dual=np.asarray(reduced.col_cost_)-matrix.T@dual
    solution.value_valid=True;solution.dual_valid=True
    postsolve_status=highs.postsolve(solution)
    if postsolve_status==h.HighsStatus.kError:raise ValueError('Postsolve failed.')
    restored=highs.getSolution();values=np.asarray(restored.col_value,dtype=float);duals=np.asarray(restored.row_dual,dtype=float)
    if values.shape!=(columns,) or duals.shape!=(rows,) or not np.all(np.isfinite(values)) or not np.all(np.isfinite(duals)):
        raise ValueError('Restored buffers are missing or nonfinite.')
    phase_violation=float(np.max(phase.matrix@values-phase.bounds,initial=0))
    box=max(float(np.max(phase.lower-values,initial=0)),float(np.max(values-phase.upper,initial=0)))
    report=dict(status='RESTORED_NUMERICAL_CANDIDATE_ONLY',proof_verified=False,presolve_status=int(presolve_status),
        postsolve_status=int(postsolve_status),original_columns=columns,original_rows=rows,presolved_columns=n,presolved_rows=m,
        discarded_column_padding=columns-n,discarded_row_padding=rows-m,presolved_maximum_violation=violation,
        restored_phase_maximum_row_violation=phase_violation,restored_maximum_box_violation=box,
        restored_phase_objective=float(values[-1]),value_valid=bool(restored.value_valid),dual_valid=bool(restored.dual_valid),
        optimizer_run=False,seconds=monotonic()-start)
    return dict(report=report,values=values,duals=duals)
