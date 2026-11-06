"""Pilot: solve the exact row model with CP-SAT (exploration, not evidence).

  pilot.py control N      small-n positive control, no exceptions, checked
                          by an independent Fourier evaluation on all inputs
  pilot.py star SECONDS   star --- rooted at the centre, first root sphere
"""
import itertools
import json
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '015-sphere-catalog-audit'))
from ortools.sat.python import cp_model  # noqa: E402

import model as mdl  # noqa: E402


def solve(m, seconds, workers=8):
    cp = cp_model.CpModel()
    x = [cp.NewBoolVar(str(i)) for i in range(len(m['variables']))]
    for terms, lo, hi, _ in m['rows']:
        cp.AddLinearConstraint(sum(c * x[v] for v, c in terms), lo, hi)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = seconds
    s.parameters.num_workers = workers
    t = time.time()
    st = s.Solve(cp)
    vals = [int(s.Value(v)) for v in x] if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    return s.StatusName(st), round(time.time() - t, 1), vals


def fourier_check(m, vals, n):
    """Independent evaluation: 16 p(x) = c + sum k chi + sum l chi on all 2^n inputs."""
    names = m['variables']
    l = {nm[1] for nm, v in zip(names, vals) if nm[0] == 'l' and v}
    k = {frozenset(a): kk for a, kk in m['exceptions'].items()}
    for nm, v in zip(names, vals):
        if nm[0] == 'kappa':
            k[nm[1]] = -v
    out = set()
    for bits in range(1 << n):
        X = {i for i in range(n) if bits >> i & 1}
        s = m['c'] + sum(kk * (-1) ** len(a & X) for a, kk in k.items()) + sum((-1) ** len(q & X) for q in l)
        out.add(s)
        if bits == 0 and s != 16 or bin(bits).count('1') == 1 and s != 0:
            return 'bad origin/unit'
    return sorted(out)


def main():
    if sys.argv[1] == 'control':
        n = int(sys.argv[2])
        for c in range(0, 4):
            m = mdl.build({}, c, n=n)
            st, sec, vals = solve(m, 60)
            print(json.dumps(dict(n=n, c=c, status=st, sec=sec,
                                  fourier=None if vals is None else fourier_check(m, vals, n),
                                  row_check=None if vals is None else len(mdl.check(m, vals)))))
    else:
        cat = json.loads((Path(__file__).resolve().parent / 'roots-catalog.json').read_text())['catalog']
        seconds = float(sys.argv[2])
        for idx, root in enumerate(cat['3,0']):
            faces = [frozenset(f) for f in root['faces']]
            deg = {}
            for f in faces:
                for a, b in itertools.combinations(sorted(f), 2):
                    deg[a] = deg.get(a, 0) + 0.5
                    deg[b] = deg.get(b, 0) + 0.5
            six = [v for v, d in deg.items() if d == 6]
            exc = {frozenset((0, v)): -2 for v in six}
            for c in (1, 2):
                m = mdl.build(exc, c, fixed=mdl.root_fixings(0, faces))
                st, sec, _ = solve(m, seconds)
                print(json.dumps(dict(root=idx, order=root['order'], c=c, status=st, sec=sec)), flush=True)

if __name__ == '__main__':
    main()


def unrooted(shape_edges, seconds, wide_all):
    import itertools as it
    exc = {frozenset(e): k for e, k in shape_edges}
    wide = [frozenset(t) for t in it.combinations(range(mdl.N), 3)] if wide_all else []
    for c in (1, 2):
        m = mdl.build(exc, c, wide_triples=wide)
        st, sec, _ = solve(m, seconds, workers=10)
        print(json.dumps(dict(c=c, wide_all=wide_all, rows=len(m['rows']), status=st, sec=sec)), flush=True)
