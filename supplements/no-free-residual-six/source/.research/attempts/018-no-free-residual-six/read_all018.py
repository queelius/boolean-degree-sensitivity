"""Assembly check for L1: every cover case, at m = 1 and m = 2, has a verified certificate.

Runs reader018.read on every certificate in certs/ (l1-*-m1.json, l1-*-m2.json),
then requires, for each case of l1-cover.json and each m in {1,2}, a reader-
verified certificate whose checked case equals the cover case in every field
except possibly the type, and whose verified variant list contains
(the cover case's type, m). The case and hash bound are the ones reader018
returns for the bytes it checked. Runs cover_reader018 on the cover and
frontier_reader on no-free-frontier.json, and requires its target rows to be
exactly (2^4) and (2^4,1). The status is ALL_L1_CASES_VERIFIED only if
nothing is missing or rejected and both readers pass; the exit code is 0 only
then. The receipt pins every source and input the result depends on.

  read_all018.py OUT_JSON [--jobs J]
"""
import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C017 = HERE.parent / '017-type-ii-three-exception'
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(C017))
import reader018  # noqa: E402

TARGETS = ([2, 2, 2, 2], [2, 2, 2, 2, 1])
DEPENDENCIES = [HERE / n for n in ('read_all018.py', 'reader018.py', 'cover_reader018.py', 'frontier_reader.py',
                                   'L1.md', 'l1-cover.json', 'no-free-frontier.json')] + \
               [C017 / n for n in ('deltahedra.json', 'roots-catalog.json', 'surfaces.py')] + [reader018.LRAT_TRIM]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def one(path):
    try:
        r = reader018.read(path)
    except Exception as e:
        return dict(path=str(path), verdict='REJECTED', error=repr(e)[:300])
    return dict(path=str(path), sha256=r['cert_sha256'], verdict=r['verdict'], variants=r['variants'], case=r['case'],
                rows=r['rows'], clauses=r['clauses'], files=r['files'])


def placement(case):
    """Every field except the type, in normal form."""
    d = {k: v for k, v in case.items() if k != 'type'}
    d['Q'], d['pair'] = sorted(d['Q']), sorted(d['pair'])
    d['faces'] = sorted(sorted(f) for f in d['faces'])
    return json.dumps(d, sort_keys=True)


def missing(results, cover_rows):
    """The (cover case, m) obligations that no reader-verified certificate covers."""
    ok = set()
    for r in results:
        if r['verdict'] == 'CASE_ROWS_INFEASIBLE_VERIFIED':
            for t, m in r['variants']:
                ok.add((placement(r['case']), t, m))
    return [dict(case=i, m=m) for i, c in enumerate(cover_rows) for m in (1, 2)
            if (placement(c), c['type'], m) not in ok]


def targets(frontier):
    """frontier_reader's verdict, and whether the target rows are exactly TARGETS, once each."""
    import frontier_reader
    try:
        fr = frontier_reader.read(frontier)
    except Exception as e:
        fr = dict(status='REJECTED', error=repr(e)[:300])
    found = [r['negative_magnitudes'] for r in frontier['rows'] if r['negative_magnitudes'] in TARGETS]
    return fr, found, sorted(found) == sorted(TARGETS)


def status(miss, rejected, cov, fr, exact):
    passed = (not miss and not rejected and cov['status'] == 'L1_COVER_READER_PASS'
              and fr['status'] == 'NO_FREE_FRONTIER_READER_PASS' and exact)
    return 'ALL_L1_CASES_VERIFIED' if passed else 'INCOMPLETE'


def main(out, jobs=6):
    certs = sorted(p for p in (HERE / 'certs').glob('l1-*-m[12].json'))
    with ProcessPoolExecutor(jobs) as ex:
        results = list(ex.map(one, certs, chunksize=8))
    cover = json.loads((HERE / 'l1-cover.json').read_text())
    import cover_reader018
    try:
        cov = cover_reader018.read(cover)
    except Exception as e:
        cov = dict(status='REJECTED', cases=None, error=repr(e)[:300])
    miss = missing(results, cover['rows'])
    rejected = [r for r in results if r['verdict'] != 'CASE_ROWS_INFEASIBLE_VERIFIED']
    fr, found, exact = targets(json.loads((HERE / 'no-free-frontier.json').read_text()))
    doc = dict(status=status(miss, rejected, cov, fr, exact),
               dependencies=[dict(path=str(p), sha256=sha(p)) for p in DEPENDENCIES],
               cover_reader=dict(status=cov['status'], cases=cov['cases']),
               frontier_reader=fr, target_inventories=found, targets_exact=exact,
               certificates=len(results), rejected=rejected,
               missing=miss[:200], missing_count=len(miss), results=results)
    Path(out).write_text(json.dumps(doc) + '\n')
    print(json.dumps(dict(status=doc['status'], certificates=len(results), rejected=len(rejected),
                          missing=len(miss), cover=cov['status'], frontier=fr['status'], targets_exact=exact)))
    return doc


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--jobs', type=int, default=6)
    a = ap.parse_args()
    sys.exit(0 if main(a.out, a.jobs)['status'] == 'ALL_L1_CASES_VERIFIED' else 1)
