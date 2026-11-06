"""Certify every case of l1-cover.json at m = 1 and m = 2 (resumable).

One line per certificate in certs/results.jsonl; (case index, m) pairs
already recorded as LRAT_VERIFIED_CORE_UNSAT are skipped on restart.

  run018.py [--jobs J] [--core-seconds S] [--m 1 2] [--seed-core K]

--seed-core K takes the CP-SAT core inside the structural subset (all
non-value rows and value rows with |X| <= K) with no deletion pass, falling
back to the full-model core if that subset is feasible. Adopted for the run
after case 754 and a benchmark (about 8 s against about 450 s per pm case,
README.md). Soundness does not depend on the choice: reader018 verifies
whatever row subset a certificate uses.
"""
import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
CERTS = HERE / 'certs'


def job(arg):
    idx, case, m, core_seconds, test_seconds, seed_core = arg
    import certify018
    t = time.time()
    stem = str(CERTS / f'l1-{idx:05d}-m{m}')
    try:
        r = None
        if seed_core is not None:
            r = certify018.certify(case, m, stem, core_seconds, test_seconds, seed_k=seed_core, seed_core=True)
            r['seed_k'] = seed_core
        if r is None or r['status'] == 'NO_CORE':
            r = certify018.certify(case, m, stem, core_seconds, test_seconds)
    except Exception as e:  # recorded, never treated as a proof
        r = dict(status='ERROR', error=repr(e)[:300])
    r['job_wall'] = round(time.time() - t, 1)
    return dict(case=idx, m=m, part=case['part'], type=case['type'], **r)


def placement_key(case):
    return json.dumps(dict(part=case['part'], root=case['root'], Q=sorted(case['Q']), pair=sorted(case['pair'])),
                      sort_keys=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jobs', type=int, default=6); ap.add_argument('--core-seconds', type=float, default=900)
    ap.add_argument('--test-seconds', type=float, default=5); ap.add_argument('--m', type=int, nargs='*', default=[1, 2])
    ap.add_argument('--seed-core', type=int, default=None)
    a = ap.parse_args()
    CERTS.mkdir(exist_ok=True)
    rows = json.loads((HERE / 'l1-cover.json').read_text())['rows']
    index = {(placement_key(r), r['type']): i for i, r in enumerate(rows)}
    log = CERTS / 'results.jsonl'
    done = set()

    def mark(r):
        if r['status'] != 'LRAT_VERIFIED_CORE_UNSAT':
            return
        base = rows[r['case']]
        for t, m in r.get('variants') or [[base['type'], r['m']]]:
            j = index.get((placement_key(base), t))
            if j is not None:
                done.add((j, m))

    # results-extra.jsonl: certificates made outside this driver (e.g. case 754 with seed_k=3, README)
    for prior in (log, CERTS / 'results-extra.jsonl'):
        if prior.exists():
            for line in prior.read_text().splitlines():
                mark(json.loads(line))
    # m = 1 and type 'none' first: their variants usually cover c0, c3 and m = 2
    order = {'none': 0, 'pm': 1, 'pp': 1, 'c0': 2, 'c3': 2}
    todo = sorted(((i, m) for m in a.m for i in range(len(rows))), key=lambda x: (x[1], order[rows[x[0]]['type']], x[0]))
    with ProcessPoolExecutor(a.jobs) as ex, log.open('a') as out:
        pending = {}
        it = iter(todo)
        while True:
            while len(pending) < 2 * a.jobs:
                nxt = next((t for t in it if t not in done), None)
                if nxt is None:
                    break
                i, m = nxt
                pending[ex.submit(job, (i, rows[i], m, a.core_seconds, a.test_seconds, a.seed_core))] = nxt
            if not pending:
                break
            f = next(as_completed(list(pending)))
            pending.pop(f)
            r = f.result()
            out.write(json.dumps(r) + '\n')
            out.flush()
            mark(r)


if __name__ == '__main__':
    main()
