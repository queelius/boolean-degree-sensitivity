"""Encode a candidate core (native row ids) to CNF, prove UNSAT with CaDiCaL
(LRAT), and check the proof with the pinned lrat-trim.

Variables 1..1079 are the native variable positions + 1 (mask order of the
pinned common block). The CNF is the conjunction of the decision-diagram
encodings (encode.py) of exactly the listed rows. Accepted only if lrat-trim
exits 20 with 's VERIFIED' on these exact files.
"""
import argparse, hashlib, json, subprocess, time
from pathlib import Path
import models
from encode import CNF

ROOT = models.H.parents[2]
CADICAL = ROOT / 'build/solvers/cadical-3.0.1/build/cadical'
LRAT_TRIM = models.H.parent / '006-solver-resume/lrat-trim/lrat-trim'
LRAT_TRIM_SHA = '179d041f645a98d51d3ca6dbbe4950806ad8eceb54c9a762f54e7acee154f8df'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encode_rows(m, row_ids):
    cnf = CNF(len(m['variables']))
    for k in row_ids:
        terms, lo, hi, _ = m['rows'][k]
        cnf.add_row([(v + 1, c) for v, c in terms], lo, hi, tag=k)
    return cnf


def run(argv, log, timeout):
    t = time.time()
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    Path(log).write_text(p.stdout + '\n--- stderr ---\n' + p.stderr)
    return p.returncode, p.stdout, round(time.time() - t, 2)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--core', required=True); ap.add_argument('--stem', required=True)
    ap.add_argument('--timeout', type=float, default=3600)
    a = ap.parse_args()
    core = json.load(open(a.core))
    s = models.load_sources()
    m = models.build(s, s['inventory']['contexts'][core['index']])
    assert m['model_id'] == core['model_id']
    rows = core['core_rows']
    cnf = encode_rows(m, rows)
    cnf_path, proof = Path(a.stem + '.cnf'), Path(a.stem + '.lrat')
    cnf_path.write_text(cnf.dimacs())
    labels_path = Path(a.stem + '.labels.json')
    json.dump(dict(row_ids=rows, labels=[[v, *cnf.labels[v]] for v in sorted(cnf.labels)]), open(labels_path, 'w'))
    assert sha(LRAT_TRIM) == LRAT_TRIM_SHA, 'lrat-trim binary changed'
    rc, out, t_solve = run([str(CADICAL), '--lrat=true', '--binary=false', '-q', str(cnf_path), str(proof)],
                           a.stem + '.cadical.log', a.timeout)
    solver = 'UNSAT' if rc == 20 else 'SAT' if rc == 10 else f'rc{rc}'
    rec = dict(index=core['index'], label=core['label'], model_id=core['model_id'],
               core_file=a.core, core_sha256=sha(a.core), row_ids=rows,
               cnf=dict(path=str(cnf_path), sha256=sha(cnf_path), variables=cnf.nvars, clauses=len(cnf.clauses)),
               labels=dict(path=str(labels_path), sha256=sha(labels_path)),
               solver=solver, solve_wall=t_solve)
    if solver == 'UNSAT':
        rc2, out2, t_chk = run([str(LRAT_TRIM), '--forward', '--no-trim', str(cnf_path), str(proof)],
                               a.stem + '.lrat-trim.log', a.timeout)
        verified = rc2 == 20 and any(line.strip() == 's VERIFIED' for line in out2.splitlines())
        rec.update(proof=dict(path=str(proof), sha256=sha(proof), bytes=proof.stat().st_size),
                   lrat_trim=dict(sha256=LRAT_TRIM_SHA, exit=rc2, wall=t_chk), verified=verified,
                   status='LRAT_VERIFIED_CORE_UNSAT' if verified else 'LRAT_NOT_VERIFIED')
    else:
        rec['status'] = 'NO_PROOF'
    json.dump(rec, open(a.stem + '.json', 'w'), indent=1)
    print({k: rec.get(k) for k in ['label', 'solver', 'solve_wall', 'status']}, rec['cnf']['variables'], rec['cnf']['clauses'])
