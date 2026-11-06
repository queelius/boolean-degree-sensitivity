"""Find a small infeasible subset of native rows (untrusted; certified later by LRAT).

1. CP-SAT with one assumption literal per row -> sufficient assumptions core.
2. Deletion pass over the core: drop a row if the rest stays INFEASIBLE within
   a per-test time limit (rows whose test times out are kept).
The output lists native row ids; correctness never depends on this file, only
on the later CNF + LRAT check of exactly those rows.
"""
import argparse, json, time
from ortools.sat.python import cp_model
import models


def check(m, subset, seconds, workers=2, assume=False):
    cp = cp_model.CpModel()
    x = [cp.NewBoolVar(f'x{i}') for i in range(len(m['variables']))]
    lits = {}
    for k in subset:
        terms, lo, hi, _ = m['rows'][k]
        c = cp.AddLinearConstraint(sum(cc * x[v] for v, cc in terms), lo, hi)
        if assume:
            a = cp.NewBoolVar(f'a{k}'); c.OnlyEnforceIf(a); lits[k] = a
    if assume:
        cp.AddAssumptions(list(lits.values()))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = seconds
    s.parameters.num_workers = 1 if assume else workers
    st = s.StatusName(s.Solve(cp))
    core = None
    if assume and st == 'INFEASIBLE':
        idx = {a.Index(): k for k, a in lits.items()}
        core = sorted(idx[i] for i in s.SufficientAssumptionsForInfeasibility())
    return st, core


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--index', type=int, required=True); p.add_argument('--core-seconds', type=float, default=600)
    p.add_argument('--test-seconds', type=float, default=20); p.add_argument('--out', required=True)
    p.add_argument('--raw', action='store_true', help='restrict to the original rows (no 1518/1519 rows)')
    a = p.parse_args()
    s = models.load_sources(); m = models.build(s, s['inventory']['contexts'][a.index])
    n_orig = s['inventory']['contexts'][a.index]['original_row_count']
    universe = range(n_orig) if a.raw else range(len(m['rows']))
    t0 = time.time()
    st, core = check(m, universe, a.core_seconds, assume=True)
    print('assumption solve', st, None if core is None else len(core), round(time.time() - t0, 1), flush=True)
    if core is None:
        raise SystemExit('no core')
    keep = list(core)
    # delete large rows first: they are the expensive ones to encode
    for k in sorted(core, key=lambda k: -len(m['rows'][k][0])):
        trial = [j for j in keep if j != k]
        st2, _ = check(m, trial, a.test_seconds)
        if st2 == 'INFEASIBLE':
            keep = trial
    from collections import Counter
    fam = Counter(m['rows'][k][3]['family'] for k in keep)
    rec = dict(index=a.index, label=models.label(m['model_id']), model_id=m['model_id'],
               raw=a.raw, core_initial=len(core), core_rows=sorted(keep), families=fam,
               terms=sum(len(m['rows'][k][0]) for k in keep), wall=round(time.time() - t0, 1),
               status='UNTRUSTED_CANDIDATE_CORE')
    json.dump(rec, open(a.out, 'w'), indent=1)
    print({k: rec[k] for k in ['label', 'core_initial', 'families', 'terms', 'wall']})
