"""Phase-I LP search with integer Farkas reconstruction for box-bounded rows."""
from time import monotonic
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def verify_certificate(rows, variable_count, certificate):
    residual=[0]*variable_count;rhs=0
    for index,sign,multiplier in certificate['terms']:
        assert type(index) is int and 0<=index<len(rows)
        assert sign in (-1,1) and type(multiplier) is int and multiplier>0
        row=rows[index]
        bound=row.upper if sign==1 else -row.lower
        rhs+=multiplier*bound
        for column,coefficient in row.terms:residual[column]+=multiplier*sign*coefficient
    for column,sign,multiplier in certificate['box_terms']:
        assert type(column) is int and 0<=column<variable_count
        assert sign in (-1,1) and type(multiplier) is int and multiplier>0
        residual[column]+=sign*multiplier
        if sign==1:rhs+=multiplier
    assert not any(residual) and rhs<0 and rhs==certificate['integer_rhs']
    return rhs


def solve(rows, variable_count, *, seconds=30):
    start=monotonic();rr=[];cc=[];vv=[];bounds=[]
    for index,row in enumerate(rows):
        assert row.lower<=row.upper
        for side,sign in enumerate((1,-1)):
            ordinal=2*index+side
            for column,coefficient in row.terms:
                assert 0<=column<variable_count
                rr.append(ordinal);cc.append(column);vv.append(sign*coefficient)
            rr.append(ordinal);cc.append(variable_count);vv.append(-1)
            bounds.append(row.upper if sign==1 else -row.lower)
    matrix=coo_matrix((np.array(vv,dtype=np.float64),(rr,cc)),shape=(2*len(rows),variable_count+1)).tocsr()
    objective=np.zeros(variable_count+1);objective[-1]=1
    result=linprog(objective,A_ub=matrix,b_ub=np.array(bounds,dtype=np.float64),
                   bounds=[(0,1)]*variable_count+[(0,None)],method='highs',
                   options=dict(time_limit=float(seconds)))
    report=dict(status='INCONCLUSIVE_BOX_ROW_LP',solver_status=int(result.status),message=result.message,
                variables=variable_count,rows=len(rows),parameters=dict(seconds=seconds),
                elapsed_seconds=monotonic()-start,proof_verified=False)
    if result.status!=0:return report
    report['minimum_row_violation']=float(result.fun)
    if result.fun<=1e-8:
        report['status']='NUMERICALLY_FEASIBLE_BOX_RELAXATION'
        report['fractional_variables']=sum(abs(x-round(x))>1e-7 for x in result.x[:-1])
        return report
    scale=10**12;terms=[];residual=[0]*variable_count;rhs=0
    for ordinal,value in enumerate(result.ineqlin.marginals):
        multiplier=max(0,round(-float(value)*scale))
        if not multiplier:continue
        index,side=divmod(ordinal,2);sign=1 if side==0 else -1;row=rows[index]
        terms.append([index,sign,multiplier]);rhs+=multiplier*(row.upper if sign==1 else -row.lower)
        for column,coefficient in row.terms:residual[column]+=multiplier*sign*coefficient
    box_terms=[]
    for column,value in enumerate(residual):
        if value:
            sign=-1 if value>0 else 1
            box_terms.append([column,sign,abs(value)])
            if sign==1:rhs+=abs(value)
    if rhs>=0:
        report['reconstruction_failed']=True
        return report
    certificate=dict(terms=terms,box_terms=box_terms,integer_rhs=rhs,
                     reconstruction_scale=scale)
    verify_certificate(rows,variable_count,certificate)
    report.update(status='EXACT_BOX_ROW_LP_CONTRADICTION',proof_verified=True,certificate=certificate)
    return report
