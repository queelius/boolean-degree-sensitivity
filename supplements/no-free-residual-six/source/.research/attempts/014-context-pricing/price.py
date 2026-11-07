"""Bounded CP-SAT pricing of every extended context model.

Solver verdicts here are UNTRUSTED: INFEASIBLE is a solver claim (no
certificate), FEASIBLE is re-checked exactly against every row and only then
reported as "relaxation satisfiable" (not a Boolean function). UNKNOWN is
inconclusive.
"""
import argparse, json, sys, time
from concurrent.futures import ProcessPoolExecutor
from ortools.sat.python import cp_model
import models

PREFIX = models.H / 'tip-interval-pilot-cycle1521.json'


def solve(m, seconds, workers, fixed=()):
    cp = cp_model.CpModel()
    x = [cp.NewBoolVar(f'x{i}') for i in range(len(m['variables']))]
    for terms, lo, hi, _ in m['rows']:
        cp.AddLinearConstraint(sum(c * x[v] for v, c in terms), lo, hi)
    for v, val in fixed:
        cp.Add(x[v] == val)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = seconds
    s.parameters.num_workers = workers
    t = time.time(); st = s.Solve(cp); wall = time.time() - t
    name = s.StatusName(st)
    values = [int(s.Value(xi)) for xi in x] if name in ('FEASIBLE', 'OPTIMAL') else None
    return name, wall, values


def job(args):
    index, seconds, workers, raw, drop = args
    s = models.load_sources()
    m = models.build(s, s['inventory']['contexts'][index])
    n_orig = s['inventory']['contexts'][index]['original_row_count']
    m['rows'] = [r for k, r in enumerate(m['rows'])
                 if not (raw and k >= n_orig) and r[3]['family'] not in drop]
    name, wall, values = solve(m, seconds, workers)
    rec = dict(index=index, label=models.label(m['model_id']), model_id=m['model_id'],
               prior_status=m['status'], prior_raw_status=m['raw_status'],
               rows=len(m['rows']), raw=raw, dropped=sorted(drop), solver=name, wall=round(wall, 2), seconds=seconds, workers=workers)
    if values is not None:
        bad = models.violated(m, values)
        rec['exact_row_violations'] = len(bad)
        rec['verdict'] = 'RELAXATION_SATISFIABLE_EXACT' if not bad else 'SOLVER_MODEL_FAILS_EXACT_CHECK'
        rec['ones'] = sum(values)
        if PREFIX.exists() and rec['label'] == 'o8-i3-c1':
            steps = json.load(open(PREFIX))['native_certificate']['steps']
            pos = {mask: i for i, mask in enumerate(m['variables'])}
            rec['prefix_disagreements'] = sum(values[pos[st['variable']]] != st['value'] for st in steps)
        rec['solution_masks'] = [mask for mask, v in zip(m['variables'], values) if v]
    else:
        rec['verdict'] = {'INFEASIBLE': 'SOLVER_CLAIMS_INFEASIBLE_UNCERTIFIED'}.get(name, 'INCONCLUSIVE')
    return rec


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--seconds', type=float, default=60); p.add_argument('--workers', type=int, default=4)
    p.add_argument('--jobs', type=int, default=3); p.add_argument('--only', nargs='*', type=int)
    p.add_argument('--out', required=True)
    p.add_argument('--raw', action='store_true', help='original 12512-row model only (no 1518/1519 rows)')
    p.add_argument('--drop', nargs='*', default=[], help='row families to omit (ablation)')
    a = p.parse_args()
    idx = a.only if a.only else list(range(26))
    with ProcessPoolExecutor(a.jobs) as ex, open(a.out, 'a') as f:
        for rec in ex.map(job, [(i, a.seconds, a.workers, a.raw, set(a.drop)) for i in idx]):
            f.write(json.dumps(rec) + '\n'); f.flush()
            print({k: rec.get(k) for k in ['label', 'prior_raw_status', 'rows', 'solver', 'wall', 'verdict', 'exact_row_violations', 'prefix_disagreements']}, flush=True)
