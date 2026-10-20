"""Raw numerical state is only a candidate for an exact certificate."""
from itertools import product
import json
import numpy as np
import pytest
from baseline_full_truth_model import Row
from exact_box_row_lp import verify_certificate
from raw_box_ipm import phase_one, reconstruct, solve


def test_phase_one_rows_match_literal_two_sided_inequalities():
    rows = [Row(((0,3),(1,-2)),1,4,{}), Row(((1,2),(1,-1)),0,3,{}), Row((),-1,2,{})]
    phase = phase_one(rows,2)
    assert phase.matrix.shape == (6,3)
    assert list(phase.objective) == [0,0,1]
    assert list(phase.lower) == [0,0,0] and list(phase.upper) == [1,1,float('inf')]
    for x in product((0,.25,1),repeat=3):
        got = phase.matrix @ np.array(x)
        for i,row in enumerate(rows):
            value = sum(a*x[j] for j,a in row.terms)
            assert got[2*i] == value-x[-1]
            assert got[2*i+1] == -value-x[-1]
            assert phase.bounds[2*i] == row.upper and phase.bounds[2*i+1] == -row.lower


@pytest.mark.parametrize('dual', [[0,-1], [0,-.53123], [-.000001,-.7]])
def test_arbitrary_perturbed_dual_yields_only_an_exactly_checked_contradiction(dual):
    rows = [Row(((0,1),),2,2,{})]
    answer = reconstruct(rows,1,dual)
    assert answer['status'] == 'EXACT_BOX_ROW_LP_CONTRADICTION'
    assert verify_certificate(rows,1,answer['certificate']) < 0
    json.dumps(answer,allow_nan=False)


@pytest.mark.parametrize('dual', [None,[],[0],[0,float('nan')],[float('inf'),0]])
def test_absent_invalid_or_wrong_size_dual_is_inconclusive(dual):
    answer = reconstruct([Row(((0,1),),2,2,{})],1,dual)
    assert answer['status'] == 'INCONCLUSIVE_BOX_ROW_LP'
    assert not answer['proof_verified'] and 'certificate' not in answer
    json.dumps(answer,allow_nan=False)


def test_zero_dual_and_feasible_rows_do_not_prove_infeasibility():
    rows = [Row(((0,2),),1,1,{})]
    for dual in ([0,0],[-1,-.2],[.4,-3]):
        answer = reconstruct(rows,1,dual)
        assert answer['status'] == 'INCONCLUSIVE_BOX_ROW_LP' and answer['integer_rhs'] >= 0
        assert not answer['proof_verified']


def test_direct_api_returns_interior_point_and_validity_flags():
    answer = solve([Row(((0,1),(1,1)),1,1,{})],2,seconds=5,presolve=False)
    assert answer.report['status'] == 'NUMERICALLY_FEASIBLE_BOX_RELAXATION'
    assert answer.report['highs_model_status'] == 'Optimal'
    assert answer.primal == pytest.approx([.5,.5],abs=1e-6)
    assert answer.report['value_valid'] and answer.report['dual_valid']
    assert len(answer.row_dual) == 2 and answer.report['iterations'] > 0
    assert not answer.report['proof_verified']
    json.dumps(answer.report,allow_nan=False)


def test_direct_negative_control_requires_separate_exact_reconstruction():
    rows = [Row(((0,1),),2,2,{})]
    answer = solve(rows,1,seconds=5,presolve=False)
    assert answer.report['status'] == 'INCONCLUSIVE_BOX_ROW_LP'
    assert answer.report['candidate']['phase_slack'] == pytest.approx(1,abs=1e-6)
    exact = reconstruct(rows,1,answer.row_dual)
    assert verify_certificate(rows,1,exact['certificate']) < 0


def test_iteration_limit_is_not_a_feasibility_or_exclusion_claim():
    answer = solve([Row(((0,1),(1,1)),1,1,{})],2,seconds=5,presolve=False,max_iterations=0)
    assert answer.report['highs_model_status'] == 'Iteration limit reached'
    assert answer.report['status'] == 'INCONCLUSIVE_BOX_ROW_LP'
    assert not answer.report['proof_verified']


@pytest.mark.parametrize('row,n', [(Row(((0,.5),),0,1,{}),1), (Row(((2,1),),0,1,{}),1),
    (Row((),2,1,{}),0), (Row((),0,1,{}),-1)])
def test_bad_integer_model_is_rejected(row,n):
    with pytest.raises(ValueError):
        phase_one([row],n)


def test_invalid_scale_and_solver_limits_are_rejected():
    rows=[Row(((0,1),),2,2,{})]
    with pytest.raises(ValueError):reconstruct(rows,1,[0,-1],scale=0)
    with pytest.raises(ValueError):solve(rows,1,seconds=0)
    with pytest.raises(ValueError):solve(rows,1,max_iterations=-1)


def test_reconstruction_rejects_noninteger_rows_before_rounding():
    with pytest.raises(ValueError):
        reconstruct([Row(((0,.5),),2,2,{})],1,[0,-1])


def test_malformed_or_overflowing_candidate_is_inconclusive():
    rows=[Row(((0,1),),2,2,{})]
    for dual in (['not a number',0],[0,1e308]):
        answer=reconstruct(rows,1,dual)
        assert answer['status']=='INCONCLUSIVE_BOX_ROW_LP' and not answer['proof_verified']


def test_phase_matrix_matches_the_frozen_kernel_before_optimization(monkeypatch):
    from types import SimpleNamespace
    import diagnostic_box_ipm_nocrossover as frozen
    rows=[Row(((0,3),(1,-2)),1,4,{}),Row(((0,1),(1,1)),1,1,{})]
    captured={}
    def capture(objective,**kwargs):
        captured.update(objective=objective,**kwargs)
        return SimpleNamespace(status=1,message='matrix capture only',nit=0,crossover_nit=0,x=None,fun=None)
    monkeypatch.setattr(frozen,'linprog',capture)
    frozen.solve(rows,2)
    phase=phase_one(rows,2)
    assert (phase.matrix-captured['A_ub']).nnz==0
    assert np.array_equal(phase.bounds,captured['b_ub'])
    assert np.array_equal(phase.objective,captured['objective'])
    assert captured['bounds']==[(0,1),(0,1),(0,None)]
