"""Certify one L1 cover case (018): core rows -> CNF -> CaDiCaL LRAT -> pinned lrat-trim.

Adapted from 017 certify017.py (frozen); only the model builder differs.

Untrusted producer. The case's rows (model018.py) have the root fixings
substituted (fixed variables removed, bounds shifted), which is sound: if the
substituted rows have no 0/1 solution on the free variables, the case has
none. A CP-SAT assumption core and a deletion pass pick a row subset (or,
with seed_k and seed_core, a core inside the structural subset of every
non-value row plus the value rows with |X| <= seed_k, with no deletion pass);
the 014 decision-diagram encoder writes its CNF; CaDiCaL proves UNSAT with
LRAT; lrat-trim checks it. Refuting any subset of a case's rows refutes the
case. The certificate stores the variable names, the chosen rows (key,
ordered terms by name, bounds) and the file hashes, so that reader018.py can
rebuild every row independently.

  certify018.py CASE_JSON --m M --stem STEM [--core-seconds S] [--test-seconds T]
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
import model018 as mdl  # noqa: E402
from encode import CNF  # noqa: E402

ROOT = HERE.parents[2]
CADICAL = ROOT / 'build/solvers/cadical-3.0.1/build/cadical'
LRAT_TRIM = HERE.parent / '006-solver-resume/lrat-trim/lrat-trim'
LRAT_TRIM_SHA = '179d041f645a98d51d3ca6dbbe4950806ad8eceb54c9a762f54e7acee154f8df'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def substituted(case, m):
    model, fixed = mdl.case_model(case, m)
    names = model['variables']
    value = {i: fixed[nm] for i, nm in enumerate(names) if nm in fixed}
    rows = []
    for terms, lo, hi, key in model['rows']:
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


def certify(case, mag, stem, core_seconds, test_seconds, timeout=3600, delete_budget=600, seed_k=None,
            seed_core=False):
    t0 = time.time()
    m = substituted(case, mag)
    if seed_k is not None:
        # structural subset: every non-value row and the value rows with |X| <= seed_k
        keep = [i for i, r in enumerate(m['rows']) if r[3][0] != 'value' or len(r[3][1]) <= seed_k]
        if seed_core:
            # a CP-SAT core inside that subset (keeps cores small and free of large value rows;
            # used for case 754, whose full-model core needed a 253-term row CaDiCaL could not refute)
            st, sub = check(m, keep, core_seconds, assume=True)
            if sub is None:
                return dict(status='NO_CORE', solver=st, seed_k=seed_k)
            keep = list(sub)
        core = keep
        delete_budget = 0
    else:
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
    # variants (type, magnitude) whose substituted rows coincide with these, row by row
    keys = {m['rows'][k][3]: (m['rows'][k][0], m['rows'][k][1], m['rows'][k][2]) for k in keep}
    variants = []
    types = ['none', 'c0', 'c3'] if case['type'] in ('none', 'c0', 'c3') else [case['type']]
    for t2 in types:
        for m2 in (1, 2):
            if (t2, m2) == (case['type'], mag):
                variants.append([t2, m2])
                continue
            alt = substituted(dict(case, type=t2), m2)
            alt_rows = {r[3]: (r[0], r[1], r[2]) for r in alt['rows']}
            if alt['variables'] == m['variables'] and all(alt_rows.get(key) == val for key, val in keys.items()):
                variants.append([t2, m2])
    rec = dict(case=case, magnitude=mag, variants=variants, seed_k=seed_k, variables=[jname(nm) for nm in m['variables']],
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
    return dict(status=rec['status'], rows=len(keep), clauses=len(cnf.clauses), wall=rec['wall'], variants=variants)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case'); ap.add_argument('--m', type=int, required=True); ap.add_argument('--stem', required=True)
    ap.add_argument('--core-seconds', type=float, default=600); ap.add_argument('--test-seconds', type=float, default=10)
    a = ap.parse_args()
    case = json.loads(Path(a.case).read_text())
    print(json.dumps(certify(case, a.m, a.stem, a.core_seconds, a.test_seconds)))


if __name__ == '__main__':
    main()
