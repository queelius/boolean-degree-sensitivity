"""Frozen-kernel variant: explicit IPM without crossover; retain all API warnings."""
from dataclasses import dataclass
from math import isfinite
from numbers import Integral
from time import monotonic
import warnings
import numpy as np
from scipy.optimize import linprog,OptimizeWarning
from scipy.sparse import coo_matrix
from exact_box_row_lp import verify_certificate


@dataclass(frozen=True)
class Outcome:
    report: dict
    primal: np.ndarray | None


def solve(rows,variable_count,*,seconds=60,presolve=True,display=False,max_iterations=None):
    start=monotonic()
    if not isinstance(variable_count,Integral) or variable_count<0 or not isfinite(seconds) or seconds<=0:
        raise ValueError('Require a nonnegative variable count and positive finite time limit.')
    variable_count=int(variable_count);rows=tuple(rows)
    if max_iterations is not None and (not isinstance(max_iterations,Integral) or max_iterations<0):
        raise ValueError('Iteration limit must be a nonnegative integer.')
    for row in rows:
        if not isinstance(row.lower,Integral) or not isinstance(row.upper,Integral) or row.lower>row.upper:
            raise ValueError('Row bounds must be ordered integers.')
        if any(not isinstance(j,Integral) or not 0<=j<variable_count or not isinstance(a,Integral) for j,a in row.terms):
            raise ValueError('Row terms need valid column indices and integer coefficients.')
    count=2*sum(len(row.terms)+1 for row in rows)
    rr=np.empty(count,dtype=np.int64);cc=np.empty(count,dtype=np.int64);vv=np.empty(count,dtype=np.float64)
    bounds=np.empty(2*len(rows),dtype=np.float64);cursor=0
    for index,row in enumerate(rows):
        for side,sign in enumerate((1,-1)):
            ordinal=2*index+side
            for column,coefficient in row.terms:
                rr[cursor]=ordinal;cc[cursor]=column;vv[cursor]=sign*coefficient;cursor+=1
            rr[cursor]=ordinal;cc[cursor]=variable_count;vv[cursor]=-1;cursor+=1
            bounds[ordinal]=row.upper if sign==1 else -row.lower
    assert cursor==count
    matrix=coo_matrix((vv,(rr,cc)),shape=(2*len(rows),variable_count+1)).tocsr();del rr,cc,vv
    objective=np.zeros(variable_count+1);objective[-1]=1
    options=dict(time_limit=float(seconds),presolve=bool(presolve),disp=bool(display),run_crossover='off')
    if max_iterations is not None:options['maxiter']=int(max_iterations)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always',OptimizeWarning)
        result=linprog(objective,A_ub=matrix,b_ub=bounds,bounds=[(0,1)]*variable_count+[(0,None)],
            method='highs-ipm',options=options)
    report=dict(status='INCONCLUSIVE_BOX_ROW_LP',solver_status=int(result.status),message=str(result.message),
        method='highs-ipm',iterations=int(result.nit),crossover_iterations=int(result.crossover_nit),
        variables=variable_count,rows=len(rows),proof_verified=False,
        parameters=dict(seconds=float(seconds),presolve=bool(presolve),display=bool(display),max_iterations=max_iterations,run_crossover='off'),
        api_warnings=[dict(category=w.category.__name__,message=str(w.message)) for w in caught])
    primal=None
    if result.x is not None and np.all(np.isfinite(result.x)):
        primal=np.array(result.x[:-1],copy=True)
        violation=max((max(float(row.lower)-sum(float(a)*primal[int(j)] for j,a in row.terms),
            sum(float(a)*primal[int(j)] for j,a in row.terms)-float(row.upper),0.0) for row in rows),default=0.0)
        box=max(float(np.max(-primal,initial=0)),float(np.max(primal-1,initial=0)))
        report['candidate']=dict(phase_slack=float(result.x[-1]),maximum_row_violation=float(violation),
            maximum_box_violation=box,fractional_variables=int(np.count_nonzero(np.abs(primal-np.rint(primal))>1e-7)))
    if result.fun is not None and isfinite(result.fun):report['minimum_row_violation']=float(result.fun)
    if result.status==0 and primal is not None:
        if result.fun<=1e-8 and report['candidate']['maximum_row_violation']<=1e-7 and report['candidate']['maximum_box_violation']<=1e-7:
            report['status']='NUMERICALLY_FEASIBLE_BOX_RELAXATION'
        elif result.fun>1e-8:
            scale=10**12;terms=[];residual=[0]*variable_count;rhs=0
            for ordinal,value in enumerate(result.ineqlin.marginals):
                multiplier=max(0,round(-float(value)*scale))
                if not multiplier:continue
                index,side=divmod(ordinal,2);sign=1 if side==0 else -1;row=rows[index]
                terms.append([index,sign,multiplier]);rhs+=multiplier*int(row.upper if sign==1 else -row.lower)
                for column,coefficient in row.terms:residual[int(column)]+=multiplier*sign*int(coefficient)
            box_terms=[]
            for column,value in enumerate(residual):
                if value:
                    sign=-1 if value>0 else 1;box_terms.append([column,sign,abs(value)])
                    if sign==1:rhs+=abs(value)
            if rhs<0:
                certificate=dict(terms=terms,box_terms=box_terms,integer_rhs=rhs,reconstruction_scale=scale)
                verify_certificate(rows,variable_count,certificate)
                report.update(status='EXACT_BOX_ROW_LP_CONTRADICTION',proof_verified=True,certificate=certificate)
            else:report['reconstruction_failed']=True
    report['elapsed_seconds']=monotonic()-start
    return Outcome(report,primal)
