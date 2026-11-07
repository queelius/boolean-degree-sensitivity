"""Certify one cover case: core rows -> CNF -> CaDiCaL LRAT -> pinned lrat-trim.

Untrusted producer. The case's rows (model.py) have the root fixings
substituted (fixed variables removed, bounds shifted), which is sound: if the
substituted rows have no 0/1 solution on the free variables, the case has
none. A CP-SAT assumption core and a deletion pass pick a row subset; the
014 decision-diagram encoder writes its CNF; CaDiCaL proves UNSAT with LRAT;
lrat-trim checks it. The certificate stores the variable names, the chosen
rows (key, ordered terms by name, bounds) and the file hashes, so that
reader017.py can rebuild every row independently.

  certify017.py CASE_JSON --c C --stem STEM [--core-seconds S] [--test-seconds T]
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / '014-context-pricing'))
import model as mdl  # noqa: E402
from encode import CNF  # noqa: E402

ROOT = HERE.parents[2]
CADICAL = ROOT / 'build/solvers/cadical-3.0.1/build/cadical'
LRAT_TRIM = HERE.parent / '006-solver-resume/lrat-trim/lrat-trim'
LRAT_TRIM_SHA = '179d041f645a98d51d3ca6dbbe4950806ad8eceb54c9a762f54e7acee154f8df'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def substituted(case, c):
    import itertools
    from solve_cases import flag_vertices, minus_triangle
    exc = {frozenset(p): k for p, k in case['exceptions']}
    doubled = [frozenset(q) for q in case.get('doubled', [])]
    fixed = dict(mdl.root_fixings(0, case['faces']))
    for q in doubled:
        fixed[('l', q)] = 1                    # encodes l_q = 2 (coefficient 2 in every row)
    tri = minus_triangle(exc)
    wide = ([tri] if tri else []) + [frozenset(t) for q in doubled for t in itertools.combinations(sorted(q), 3)]
    m = mdl.build(exc, c, flag_vertices=flag_vertices(exc, doubled), implied=True, wide_triples=wide, doubled=doubled)
    names = m['variables']
    value = {i: fixed[nm] for i, nm in enumerate(names) if nm in fixed}
    rows = []
    for terms, lo, hi, key in m['rows']:
        shift = sum(co * value[v] for v, co in terms if v in value)
        rest = [(v, co) for v, co in terms if v not in value]
        if not rest:
            if not lo <= shift <= hi:
                raise SystemExit(f'fixings violate row {key}')
            continue
        rows.append((rest, lo - shift, hi - shift, key))
    return dict(variables=names, rows=rows)


def check(m, subset, seconds, assume=False, workers=1):
    from ortools.sat.python import cp_model
    cp = cp_model.CpModel()
    x = [cp.NewBoolVar(f'x{i}') for i in range(len(m['variables']))]
    lits = {}
    for k in subset:
        terms, lo, hi, _ = m['rows'][k]
        con = cp.AddLinearConstraint(sum(co * x[v] for v, co in terms), lo, hi)
        if assume:
            a = cp.NewBoolVar(f'a{k}')
            con.OnlyEnforceIf(a)
            lits[k] = a
    if assume:
        cp.AddAssumptions(list(lits.values()))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = seconds
    s.parameters.num_workers = 1 if assume else workers
    st = s.StatusName(s.Solve(cp))
    core = None
    if assume and st == 'INFEASIBLE':
        idx = {a.Index(): k for k, a in lits.items()}
        core = sorted(idx[i] for i in s.SufficientAssumptionsForInfeasibility())
    return st, core


def run(argv, log, timeout):
    t = time.time()
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    Path(log).write_text(p.stdout + '\n--- stderr ---\n' + p.stderr)
    return p.returncode, p.stdout, round(time.time() - t, 2)


def jname(nm):
    return [nm[0], sorted(nm[1])]


def jkey(key):
    return [key[0]] + [list(x) if isinstance(x, tuple) else x for x in key[1:]]


LARGE = 30


def certify(case, c, stem, core_seconds, test_seconds, timeout=3600, delete_budget=600):
    t0 = time.time()
    m = substituted(case, c)
    st, core = check(m, range(len(m['rows'])), core_seconds, assume=True)
    if core is None:
        return dict(status='NO_CORE', solver=st)
    keep = list(core)
    # deletion pass over the rows that are expensive to encode, largest first, within a time budget
    t_del = time.time()
    for k in sorted(core, key=lambda k: -len(m['rows'][k][0])):
        if len(m['rows'][k][0]) <= LARGE or time.time() - t_del > delete_budget:
            break
        trial = [j for j in keep if j != k]
        if check(m, trial, test_seconds)[0] == 'INFEASIBLE':
            keep = trial
    cnf = CNF(len(m['variables']))
    for k in keep:
        terms, lo, hi, _ = m['rows'][k]
        cnf.add_row([(v + 1, co) for v, co in terms], lo, hi, tag=k)
    cnf_path, proof, labels_path = Path(stem + '.cnf'), Path(stem + '.lrat'), Path(stem + '.labels.json')
    cnf_path.write_text(cnf.dimacs())
    labels_path.write_text(json.dumps([[v, *cnf.labels[v]] for v in sorted(cnf.labels)]))
    if sha(LRAT_TRIM) != LRAT_TRIM_SHA:
        raise SystemExit('lrat-trim binary changed')
    rc, _, t_solve = run([str(CADICAL), '--lrat=true', '--binary=false', '-q', str(cnf_path), str(proof)],
                         stem + '.cadical.log', timeout)
    uses_constant = any(m['rows'][k][3][0] == 'constant' for k in keep)
    rec = dict(case=case, c=c, constants=[c] if uses_constant else [1, 2], variables=[jname(nm) for nm in m['variables']],
               rows=[dict(id=k, key=jkey(m['rows'][k][3]),
                          terms=[[jname(m['variables'][v]), co] for v, co in m['rows'][k][0]],
                          lo=m['rows'][k][1], hi=m['rows'][k][2]) for k in keep],
               core_initial=len(core),
               cnf=dict(path=str(cnf_path), sha256=sha(cnf_path), variables=cnf.nvars, clauses=len(cnf.clauses)),
               labels=dict(path=str(labels_path), sha256=sha(labels_path)),
               solver='UNSAT' if rc == 20 else f'rc{rc}', solve_wall=t_solve)
    if rc == 20:
        rc2, out2, t_chk = run([str(LRAT_TRIM), '--forward', '--no-trim', str(cnf_path), str(proof)],
                               stem + '.lrat-trim.log', timeout)
        ok = rc2 == 20 and any(line.strip() == 's VERIFIED' for line in out2.splitlines())
        rec.update(proof=dict(path=str(proof), sha256=sha(proof), bytes=proof.stat().st_size),
                   lrat_trim=dict(sha256=LRAT_TRIM_SHA, exit=rc2, wall=t_chk),
                   status='LRAT_VERIFIED_CORE_UNSAT' if ok else 'LRAT_NOT_VERIFIED')
    else:
        rec['status'] = 'NO_PROOF'
    rec['wall'] = round(time.time() - t0, 1)
    Path(stem + '.json').write_text(json.dumps(rec) + '\n')
    return dict(status=rec['status'], rows=len(keep), clauses=len(cnf.clauses), wall=rec['wall'],
                constants=rec['constants'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case'); ap.add_argument('--c', type=int, required=True); ap.add_argument('--stem', required=True)
    ap.add_argument('--core-seconds', type=float, default=600); ap.add_argument('--test-seconds', type=float, default=10)
    a = ap.parse_args()
    case = json.loads(Path(a.case).read_text())
    print(json.dumps(certify(case, a.c, a.stem, a.core_seconds, a.test_seconds)))


if __name__ == '__main__':
    main()
