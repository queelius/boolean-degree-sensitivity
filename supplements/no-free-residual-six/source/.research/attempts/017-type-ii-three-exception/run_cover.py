"""Certify every case of cover-cases.json (resumable).

For each case: certify at c = 1; if its core uses the constant row, certify
c = 2 separately. One line per certificate in certs/results.jsonl. Cases
already recorded as LRAT_VERIFIED_CORE_UNSAT are skipped on restart.

  run_cover.py [--jobs J] [--core-seconds S] [--only GRAPH:SIGNS ...]
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


def stem(shape, idx, c):
    tag = f"{shape['graph']}_{shape['signs']}".replace('+', 'p').replace('-', 'm')
    return str(CERTS / f'{tag}-{idx:04d}-c{c}')


def job(arg):
    shape, idx, c, core_seconds, test_seconds = arg
    import certify017
    t = time.time()
    try:
        r = certify017.certify(shape['cases'][idx], c, stem(shape, idx, c), core_seconds, test_seconds)
    except Exception as e:  # recorded, never treated as a proof
        r = dict(status='ERROR', error=repr(e)[:300])
    r['job_wall'] = round(time.time() - t, 1)
    return dict(graph=shape['graph'], signs=shape['signs'], case=idx, c=c, **r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jobs', type=int, default=6); ap.add_argument('--core-seconds', type=float, default=600)
    ap.add_argument('--test-seconds', type=float, default=5); ap.add_argument('--only', nargs='*')
    ap.add_argument('--cover', default=str(HERE / 'cover-cases.json'))
    a = ap.parse_args()
    CERTS.mkdir(exist_ok=True)
    cover = json.loads(Path(a.cover).read_text())
    shapes = [s for s in cover['shapes'] if not a.only or f"{s['graph']}:{s['signs']}" in a.only]
    log = CERTS / 'results.jsonl'
    done, needs_c2 = set(), set()
    if log.exists():
        for line in log.read_text().splitlines():
            r = json.loads(line)
            if r['status'] == 'LRAT_VERIFIED_CORE_UNSAT':
                for c in r.get('constants', [r['c']]):
                    done.add((r['graph'], r['signs'], r['case'], c))

    # c = 2 is pending wherever c = 1 is verified but c = 2 is not (whatever the record format)
    needs_c2 = {(g, sg, i) for g, sg, i, c in done if c == 1 and (g, sg, i, 2) not in done}
    # every missing (case, constant) obligation; +1-heavy shapes are the slow ones: run them last
    order = sorted(shapes, key=lambda s: (s['signs'].count('+'), len(s['cases'])))
    todo = [(s, i, 1) for s in order for i in range(len(s['cases'])) if (s['graph'], s['signs'], i, 1) not in done]
    todo += [(s, i, 2) for s in order for i in range(len(s['cases']))
             if (s['graph'], s['signs'], i) in needs_c2 and (s['graph'], s['signs'], i, 2) not in done]
    with ProcessPoolExecutor(a.jobs) as ex, log.open('a') as out:
        futs = {ex.submit(job, (s, i, c, a.core_seconds, a.test_seconds)): (s, i, c) for s, i, c in todo}
        while futs:
            for f in as_completed(list(futs)):
                s, i, c = futs.pop(f)
                r = f.result()
                out.write(json.dumps(r) + '\n')
                out.flush()
                if c == 1 and r.get('constants') == [1] and (s['graph'], s['signs'], i, 2) not in done:
                    futs[ex.submit(job, (s, i, 2, a.core_seconds, a.test_seconds))] = (s, i, 2)
                break


if __name__ == '__main__':
    main()
