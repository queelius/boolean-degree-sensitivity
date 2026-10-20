"""Pinned direct HiGHS phase-I diagnostics and separate exact reconstruction."""
from dataclasses import dataclass
from math import isfinite
from numbers import Integral
from time import monotonic
import numpy as np
import scipy
from scipy.optimize._highspy import _core as highs_core
from scipy.sparse import coo_matrix
from exact_box_row_lp import verify_certificate


@dataclass(frozen=True)
class PhaseOne:
    matrix: object
    bounds: np.ndarray
    objective: np.ndarray
    lower: np.ndarray
    upper: np.ndarray


@dataclass(frozen=True)
class Outcome:
    report: dict
    primal: np.ndarray | None
    row_dual: np.ndarray | None


def validate_rows(rows, variable_count):
    if not isinstance(variable_count, Integral) or variable_count < 0:
        raise ValueError('Require a nonnegative integer variable count.')
    rows = tuple(rows)
    for row in rows:
        if not isinstance(row.lower, Integral) or not isinstance(row.upper, Integral) or row.lower > row.upper:
            raise ValueError('Bounds must be ordered integers.')
        if any(not isinstance(j, Integral) or not 0 <= j < variable_count or not isinstance(a, Integral) for j,a in row.terms):
            raise ValueError('Require valid column indices and integer coefficients.')
    return rows


def phase_one(rows, variable_count):
    rows = validate_rows(rows, variable_count)
    count = 2*sum(len(row.terms)+1 for row in rows)
    rr = np.empty(count,dtype=np.int64)
    cc = np.empty(count,dtype=np.int64)
    vv = np.empty(count,dtype=np.float64)
    bounds = np.empty(2*len(rows),dtype=np.float64)
    cursor = 0
    for i,row in enumerate(rows):
        for side,sign in enumerate((1,-1)):
            for j,a in row.terms:
                rr[cursor],cc[cursor],vv[cursor] = 2*i+side,j,sign*a
                cursor += 1
            rr[cursor],cc[cursor],vv[cursor] = 2*i+side,variable_count,-1
            cursor += 1
            bounds[2*i+side] = row.upper if sign == 1 else -row.lower
    assert cursor == count
    matrix = coo_matrix((vv,(rr,cc)),shape=(2*len(rows),variable_count+1)).tocsc()
    objective = np.zeros(variable_count+1)
    objective[-1] = 1
    upper = np.ones(variable_count+1)
    upper[-1] = np.inf
    return PhaseOne(matrix,bounds,objective,np.zeros(variable_count+1),upper)


def reconstruct(rows, variable_count, row_dual, *, scale=10**12):
    if not isinstance(scale, Integral) or scale <= 0:
        raise ValueError('Require a positive integer reconstruction scale.')
    scale = int(scale)
    rows = validate_rows(rows, variable_count)
    report = dict(status='INCONCLUSIVE_BOX_ROW_LP',proof_verified=False,reconstruction_scale=scale)
    if row_dual is None:
        return dict(report,reason='NO_DUAL_CANDIDATE')
    try:
        dual = np.asarray(row_dual,dtype=float)
    except (ValueError,TypeError):
        return dict(report,reason='NONNUMERIC_DUAL_CANDIDATE')
    if dual.shape != (2*len(rows),) or not np.all(np.isfinite(dual)):
        return dict(report,reason='INVALID_DUAL_SHAPE_OR_NONFINITE')
    if not all(isfinite(float(v)*scale) for v in dual):
        return dict(report,reason='NONFINITE_SCALED_DUAL')
    residual = [0]*variable_count
    terms = []
    rhs = 0
    for ordinal,value in enumerate(dual):
        multiplier = max(0,round(-float(value)*scale))
        if not multiplier:
            continue
        i,side = divmod(ordinal,2)
        sign = 1 if side == 0 else -1
        row = rows[i]
        terms.append([i,sign,multiplier])
        rhs += multiplier*int(row.upper if sign == 1 else -row.lower)
        for j,a in row.terms:
            residual[int(j)] += multiplier*sign*int(a)
    row_rhs = rhs
    box = []
    for j,value in enumerate(residual):
        if value:
            sign = -1 if value > 0 else 1
            box.append([j,sign,abs(value)])
            if sign == 1:
                rhs += abs(value)
    report.update(integer_rhs=rhs,row_rhs=row_rhs,box_correction=rhs-row_rhs,
        residual_l1=sum(map(abs,residual)),nonzero_row_multipliers=len(terms),nonzero_box_multipliers=len(box))
    if rhs < 0:
        certificate = dict(terms=terms,box_terms=box,integer_rhs=rhs,reconstruction_scale=scale)
        verify_certificate(rows,variable_count,certificate)
        report.update(status='EXACT_BOX_ROW_LP_CONTRADICTION',proof_verified=True,certificate=certificate)
    return report


def solve(rows, variable_count, *, seconds=60, presolve=True, display=False, max_iterations=None):
    if not isfinite(seconds) or seconds <= 0:
        raise ValueError('Require a positive finite solver time limit.')
    if max_iterations is not None and (not isinstance(max_iterations, Integral) or max_iterations < 0):
        raise ValueError('Require a nonnegative integer iteration limit.')
    started = monotonic()
    rows = tuple(rows)
    phase = phase_one(rows,variable_count)
    lp = highs_core.HighsLp()
    lp.num_col_,lp.num_row_ = phase.matrix.shape[1],phase.matrix.shape[0]
    lp.a_matrix_.num_col_,lp.a_matrix_.num_row_ = lp.num_col_,lp.num_row_
    lp.a_matrix_.format_ = highs_core.MatrixFormat.kColwise
    lp.a_matrix_.start_ = phase.matrix.indptr
    lp.a_matrix_.index_ = phase.matrix.indices
    lp.a_matrix_.value_ = phase.matrix.data
    lp.col_cost_,lp.col_lower_,lp.col_upper_ = phase.objective,phase.lower,phase.upper
    lp.row_lower_ = np.full(lp.num_row_,-np.inf)
    lp.row_upper_ = phase.bounds
    highs = highs_core._Highs()
    parameters = dict(solver='ipm',run_crossover='off',time_limit=float(seconds),
        presolve='on' if presolve else 'off',output_flag=bool(display))
    if max_iterations is not None:
        parameters['ipm_iteration_limit'] = int(max_iterations)
    for key,value in parameters.items():
        assert highs.setOptionValue(key,value) == highs_core.HighsStatus.kOk
    assert highs.passModel(lp) == highs_core.HighsStatus.kOk
    run_status = highs.run()
    model_status = highs.getModelStatus()
    info = highs.getInfo()
    solution = highs.getSolution()
    report = dict(status='INCONCLUSIVE_BOX_ROW_LP',proof_verified=False,method='direct-bundled-highs-ipm',
        solver_status=int(model_status),solver_status_namespace='HiGHS-HighsModelStatus',
        highs_model_status=highs.modelStatusToString(model_status),highs_run_status=int(run_status),
        iterations=int(info.ipm_iteration_count),crossover_iterations=int(info.crossover_iteration_count),
        value_valid=bool(solution.value_valid),dual_valid=bool(solution.dual_valid),
        variables=int(variable_count),rows=len(rows),parameters=parameters,scipy_version=scipy.__version__,highs_version=highs.version())
    if isfinite(info.objective_function_value):
        report['reported_objective'] = float(info.objective_function_value)
    primal = None
    raw = np.asarray(solution.col_value,dtype=float)
    if raw.shape == (variable_count+1,) and np.all(np.isfinite(raw)):
        primal = raw[:-1].copy()
        lhs = phase.matrix @ raw
        violation = float(np.max(lhs+raw[-1]-phase.bounds,initial=0))
        box = max(float(np.max(-primal,initial=0)),float(np.max(primal-1,initial=0)))
        report['candidate'] = dict(phase_slack=float(raw[-1]),maximum_row_violation=violation,
            maximum_box_violation=box,fractional_variables=int(np.count_nonzero(np.abs(primal-np.rint(primal))>1e-7)))
        if model_status == highs_core.HighsModelStatus.kOptimal and solution.value_valid and abs(raw[-1])<=1e-8 and violation<=1e-7 and box<=1e-7:
            report['status'] = 'NUMERICALLY_FEASIBLE_BOX_RELAXATION'
    row_dual = np.asarray(solution.row_dual,dtype=float)
    if row_dual.shape != (len(rows)*2,) or not np.all(np.isfinite(row_dual)):
        row_dual = None
    report['finite_dual_candidate_returned'] = row_dual is not None
    report['elapsed_seconds'] = monotonic()-started
    return Outcome(report,primal,row_dual)
