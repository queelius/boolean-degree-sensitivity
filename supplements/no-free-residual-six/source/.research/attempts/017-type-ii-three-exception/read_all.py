"""Assembly check: every cover case, at c = 1 and c = 2, has a verified certificate.

Runs reader017.read on every certificate in certs/ (files *-c1.json and
*-c2.json), then requires, for each shape and case of cover-cases.json and
each constant in {1,2}, a certificate verified by the reader whose stored
case equals the cover's case exactly and whose constant list contains it.
Writes a summary with the hash of every certificate, CNF, labels and proof.
Does not re-run the cover reader (cover_reader.py) or check the lemma notes.

  read_all.py OUT_JSON [--jobs J]   (covers: cover-cases.json and triangle-cover.json)
"""
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import reader017  # noqa: E402
import cover_reader  # noqa: E402

FRONTIER = HERE.parent / '009-parent-analysis' / 'one-free-residual6-frontier-cycle1532.json'


def signed_canon(deps):
    """Departures [(kind, vertices)] up to relabelling (brute force over the used vertices)."""
    import itertools
    vs = sorted({x for _, q in deps for x in q})
    best = None
    for perm in itertools.permutations(range(len(vs))):
        m = dict(zip(vs, perm))
        key = tuple(sorted((k, tuple(sorted(m[x] for x in q))) for k, q in deps))
        best = key if best is None or key < best else best
    return best


def bind_universe(covers):
    """The covered shapes must be exactly the OPEN rows of the frozen 1532 frontier."""
    fr = json.loads(FRONTIER.read_text())
    want = sorted(signed_canon([(k, q) for k, q in r['departures']]) for r in fr['type_ii_classes'] if r['status'] == 'OPEN')
    got = []
    for s in covers:
        deps = [('-2' if sg == '-' else '+1', e) for e, sg in zip(s['edges'], s['signs'] if not s.get('doubled') else '--')]
        if s.get('doubled'):
            deps.append(('Q2', sorted({x for e in s['edges'] for x in e})))
        got.append(signed_canon(deps))
    return len(want) == 24 and sorted(got) == want


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def one(path):
    try:
        r = reader017.read(path)
    except Exception as e:
        return dict(path=str(path), verdict='REJECTED', error=repr(e)[:300])
    cert = json.loads(Path(path).read_text())
    return dict(path=str(path), sha256=sha(path), verdict=r['verdict'], constants=r['constants'],
                case=cert['case'], rows=r['rows'], clauses=r['clauses'],
                files={k: dict(path=cert[k]['path'], sha256=cert[k]['sha256']) for k in ('cnf', 'labels', 'proof')})


def canon(case):
    """The complete case dictionary in normal form (every field, sets sorted)."""
    out = {}
    for k, v in case.items():
        if k == 'faces':
            v = sorted(sorted(f) for f in v)
        elif k == 'exceptions':
            v = sorted([sorted(p), kk] for p, kk in v)
        elif k == 'doubled':
            v = sorted(sorted(q) for q in v)
        out[k] = v
    return json.dumps(out, sort_keys=True)


def main(out, jobs=6):
    certs = sorted(p for p in (HERE / 'certs').glob('*-c[12].json'))
    with ProcessPoolExecutor(jobs) as ex:
        results = list(ex.map(one, certs, chunksize=8))
    ok = {}
    for r in results:
        if r['verdict'] == 'CASE_ROWS_INFEASIBLE_VERIFIED':
            for c in r['constants']:
                ok.setdefault((canon(r['case']), c), r['path'])
    covers = [HERE / 'cover-cases.json', HERE / 'triangle-cover.json', HERE / 'shape1-cover.json']
    shapes = [s for cv in covers for s in json.loads(cv.read_text())['shapes']]
    catalog = json.loads((HERE / 'roots-catalog.json').read_text())['catalog']
    deltahedra = json.loads((HERE / 'deltahedra.json').read_text())['spheres']
    for cv in covers:
        cover_reader.read(json.loads(cv.read_text()), catalog, deltahedra)   # raises unless complete
    universe_ok = bind_universe(shapes)
    missing, per_shape = [], []
    for s in shapes:
        miss = [(i, c) for i, case in enumerate(s['cases']) for c in (1, 2) if (canon(case), c) not in ok]
        missing += [dict(graph=s['graph'], signs=s['signs'], case=i, c=c) for i, c in miss]
        per_shape.append(dict(graph=s['graph'], signs=s['signs'], cases=len(s['cases']), missing=len(miss)))
    doc = dict(status='ALL_CASES_VERIFIED' if not missing and universe_ok else 'INCOMPLETE',
               universe_matches_frontier_1532=universe_ok,
               frontier=dict(path=str(FRONTIER), sha256=sha(FRONTIER)),
               catalogs=[dict(path=str(HERE / n), sha256=sha(HERE / n)) for n in ('roots-catalog.json', 'deltahedra.json')],
               covers=[dict(path=str(cv), sha256=sha(cv)) for cv in covers],
               reader=dict(path=str(HERE / 'reader017.py'), sha256=sha(HERE / 'reader017.py')),
               certificates=len(results), rejected=[r for r in results if r['verdict'] != 'CASE_ROWS_INFEASIBLE_VERIFIED'],
               per_shape=per_shape, missing=missing[:200], missing_count=len(missing), results=results)
    Path(out).write_text(json.dumps(doc) + '\n')
    print(json.dumps(dict(status=doc['status'], certificates=len(results), rejected=len(doc['rejected']),
                          missing=len(missing))))
    return doc


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[2] == '--jobs' else 6)
