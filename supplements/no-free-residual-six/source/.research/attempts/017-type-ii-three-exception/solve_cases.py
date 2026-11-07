"""CP-SAT verdicts for cover cases (untrusted triage; certificates come later).

  solve_cases.py GRAPH SIGNS --c C [--sample K] [--seconds S] [--workers W] [--jobs J]
"""
import argparse
import json
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cases as cv  # noqa: E402
import model as mdl  # noqa: E402
import step4_count  # noqa: E402


# (n(-2), n(+1)) whose link catalogs are all near-flag (NEAR-FLAG.md)
NEAR_FLAG_TYPES = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)}


def minus_triangle(exc):
    """The all -2 exceptional triangle, if the shape is triangle --- (Lemma 1: only it may have incidence 4)."""
    minus = [p for p, k in exc.items() if k == -2]
    verts = set().union(*minus) if minus else set()
    if len(minus) == 3 and len(verts) == 3:
        return frozenset(verts)
    return None


def flag_vertices(exc, doubled=()):
    out = {}
    tri = minus_triangle(exc) or frozenset()
    special = set(tri).union(*[set(q) for q in doubled])
    for v in range(1, mdl.N):          # the root's link is fixed
        if v in special:               # triangle --- links may split or pinch; doubled-quartic vertices
            continue
        t = (sum(1 for p, k in exc.items() if v in p and k == -2), sum(1 for p, k in exc.items() if v in p and k == 1))
        if t in NEAR_FLAG_TYPES:
            out[v] = sorted(x for p, k in exc.items() if v in p and k == 1 for x in p if x != v)
    return out


def case_model(case, c, extra=False):
    exc = {frozenset(p): k for p, k in case['exceptions']}
    if not extra:
        return mdl.build(exc, c, fixed=mdl.root_fixings(0, case['faces']))
    tri = minus_triangle(exc)
    return mdl.build(exc, c, fixed=mdl.root_fixings(0, case['faces']), flag_vertices=flag_vertices(exc), implied=True,
                     wide_triples=[tri] if tri else [])


def run_one(arg):
    case, c, seconds, workers, extra = arg
    from ortools.sat.python import cp_model
    m = case_model(case, c, extra)
    cp = cp_model.CpModel()
    x = [cp.NewBoolVar(str(i)) for i in range(len(m['variables']))]
    for terms, lo, hi, _ in m['rows']:
        cp.AddLinearConstraint(sum(co * x[v] for v, co in terms), lo, hi)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = seconds
    s.parameters.num_workers = workers
    t = time.time()
    st = s.StatusName(s.Solve(cp))
    return dict(exceptions=case['exceptions'], root_index=case['root_index'], c=c, status=st,
                sec=round(time.time() - t, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('graph'); ap.add_argument('signs'); ap.add_argument('--c', type=int, required=True)
    ap.add_argument('--sample', type=int); ap.add_argument('--seconds', type=float, default=120)
    ap.add_argument('--workers', type=int, default=1); ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--out'); ap.add_argument('--extra', action='store_true')
    a = ap.parse_args()
    cat = json.loads((HERE / 'roots-catalog.json').read_text())['catalog']
    shape = next(x for x in step4_count.shapes() if x[0] == a.graph and x[1] == a.signs)
    _, cs = cv.cases(shape[2], shape[3], cat)
    if a.sample:
        cs = random.Random(0).sample(cs, min(a.sample, len(cs)))
    out = open(a.out, 'a') if a.out else None
    with ProcessPoolExecutor(a.jobs) as ex:
        for r in ex.map(run_one, [(cs_, a.c, a.seconds, a.workers, a.extra) for cs_ in cs]):
            line = json.dumps(r)
            print(line, flush=True)
            if out:
                out.write(line + '\n'); out.flush()


if __name__ == '__main__':
    main()
