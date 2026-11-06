"""Replay every v1.5.0 certificate with the frozen readers, inside the isolated container.

See REPRODUCE.md for the mounts. Inside the container the historical research path
/home/spinoza/github/math-theory is the packet's read-only source/ tree, except the three
certs/ directories, which are empty writable scratch mounts. Certificates are taken from the
extracted certificates tar (/certificates), decompressed one case at a time into the scratch
directory, checked against the SHA-256 the manifests pin, read by the frozen reader, and
deleted again. Nothing frozen is edited: the frozen assembly drivers (017 read_all.main, 018
read_all018.main) run unchanged, with their per-certificate function wrapped so that the
certificate's CNF, labels and proof exist exactly while it is read.

Stages: sources, certificate store, 014 (verify_core.py --require-raw, each output compared with
the archived verify record), 017 and 018 (frozen read-all, compared with the archived read-all
receipt), controls in normal and -O mode, the packet unit tests of 014 to 018 in both modes.
Writes /results/REPLAY-RECEIPT.json only if every stage passes; exits nonzero otherwise.

  python /packet/replay_packet.py [--jobs J] [--stages a,b,...]
"""
import argparse
import hashlib
import json
import lzma
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
PACKET = Path(os.environ.get('REPLAY_PACKET', '/packet'))
CERTIFICATES = Path(os.environ.get('REPLAY_CERTIFICATES', '/certificates'))
RESULTS = Path(os.environ.get('REPLAY_RESULTS', '/results'))
REPO = Path('/home/spinoza/github/math-theory')
R = REPO / '.research'
A = R / 'attempts'
CHUNK = 1 << 22
STAGES = ['sources', 'store', 'c014', 'c017', 'c018', 'controls', 'tests']


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(CHUNK), b''):
            h.update(b)
    return h.hexdigest()


class Store:
    """The certificate manifest, indexed by original path."""

    def __init__(self):
        doc = json.loads((PACKET / 'CERTIFICATE-MANIFEST.json').read_text())
        self.files = doc['files']
        self.by_original = {e['original_path']: e for e in self.files + doc['aliases']}

    def materialize(self, original):
        """Write the original bytes of `original` (an absolute path in a certs/ dir); check the pin."""
        e = self.by_original[str(original)]
        src = CERTIFICATES / e['member']
        h = hashlib.sha256()
        opener = lzma.open if e['encoding'] == 'xz' else open
        with opener(src, 'rb') as fin, open(original, 'wb') as fout:
            for b in iter(lambda: fin.read(CHUNK), b''):
                h.update(b)
                fout.write(b)
        if h.hexdigest() != e['original_sha256']:
            raise RuntimeError(f'decompressed bytes differ from the pin: {original}')
        return Path(original)


STORE = None


def store():
    global STORE
    if STORE is None:
        STORE = Store()
    return STORE


def drop(*paths):
    for p in paths:
        try:
            os.unlink(p)
        except FileNotFoundError:
            pass


def certs_dir(attempt):
    d = A / attempt / 'certs'
    if any(d.iterdir()):
        raise RuntimeError(f'scratch {d} is not empty; use a fresh scratch directory')
    return d


# ---------------------------------------------------------------- stages

def stage_sources(_jobs):
    doc = json.loads((PACKET / 'SOURCE-MANIFEST.json').read_text())
    bad = [e['original_path'] for e in doc['files'] if digest(e['original_path']) != e['sha256']]
    if bad:
        raise RuntimeError(f'{len(bad)} source files differ from SOURCE-MANIFEST, first {bad[0]}')
    return dict(files=len(doc['files']), bytes=doc['total_bytes'])


def stage_store(_jobs):
    s = store()
    bad = []
    for e in s.files:
        p = CERTIFICATES / e['member']
        if p.stat().st_size != e['stored_bytes'] or digest(p) != e['stored_sha256']:
            bad.append(e['member'])
    if bad:
        raise RuntimeError(f'{len(bad)} stored certificate files differ, first {bad[0]}')
    return dict(files=len(s.files), stored_bytes=sum(e['stored_bytes'] for e in s.files),
                original_bytes=sum(e['original_bytes'] for e in s.files))


def last_json(text):
    return json.loads(text.strip().splitlines()[-1])


def stage_c014(_jobs):
    D = A / '014-context-pricing'
    certs_dir('014-context-pricing')
    summary = json.loads((D / 'signed-star-raw-certificates.json').read_text())
    # 2..25: the 24 contexts of 1531; 1: o7-i0-c2 (1533); 0: o7-i0-c1, a control (ROOT7-CONTROL.md) that
    # reproduces on raw rows an exclusion accepted earlier from 009 cycle 1476, not cited by 1531 to 1534
    cases = [(c['index'], f'raw-{c["index"]}.verify2.json') for c in summary['contexts']] + \
        [(1, 'raw-1.verify.json'), (0, 'raw-0.verify.json')]
    out = []
    for i, record in cases:
        names = [f'raw-{i}.{k}' for k in ('json', 'cnf', 'lrat', 'labels.json')] + [record]
        files = [store().materialize(D / 'certs' / n) for n in names]
        try:
            p = subprocess.run([sys.executable, str(D / 'verify_core.py'), '--require-raw', str(files[0])],
                               cwd=REPO, capture_output=True, text=True)
            got = last_json(p.stdout) if p.stdout.strip() else None
            want = last_json(files[-1].read_text())
            ok = p.returncode == 0 and got == want and got['verdict'] == 'ROWS_INFEASIBLE_VERIFIED' \
                and got['row_scope'] == 'RAW'
            out.append(dict(index=i, label=want['label'], returncode=p.returncode, matches_archived=got == want,
                            verdict=got and got['verdict'], ok=ok, stderr=p.stderr[-300:]))
        finally:
            drop(*files)
        print(json.dumps(dict(stage='c014', index=i, ok=out[-1]['ok'])), flush=True)
    if not all(r['ok'] for r in out):
        raise RuntimeError(f'014: {[r for r in out if not r["ok"]][:2]}')
    return dict(certificates=len(out), contexts_1531=len(summary['contexts']), root7_c2_1533=1,
                root7_c1_control=1, results=out)


def wrap_one(module, attempt):
    """Wrap module.one so the certificate's CNF, labels and proof exist exactly while it is read."""
    original = module.one

    def one(path):
        cert = json.loads(Path(path).read_text())
        files = [store().materialize(cert[k]['path']) for k in ('cnf', 'labels', 'proof')]
        try:
            return original(path)
        finally:
            drop(*files)
    one.__qualname__ = one.__name__ = f'one_{attempt}'
    globals()[one.__name__] = one          # picklable by reference for the (forked) pool workers
    module.one = one


def results_key(r, fields):
    return json.dumps({k: r.get(k) for k in fields}, sort_keys=True)


def read_all(attempt, module_name, pattern, archived_name, out_name, passing, fields, jobs):
    D = A / attempt
    sys.path[:0] = [str(D), str(A / '017-type-ii-three-exception')]
    module = __import__(module_name)
    d = certs_dir(attempt)
    certs = [e['original_path'] for e in store().files
             if e['original_path'].startswith(str(d) + '/') and Path(e['original_path']).match(pattern)]
    for c in certs:
        store().materialize(c)
    wrap_one(module, attempt[:3])
    started = time.monotonic()
    doc = module.main(str(RESULTS / out_name), jobs)
    seconds = time.monotonic() - started
    archived = json.loads((D / archived_name).read_text())
    same = sorted(results_key(r, fields) for r in doc['results']) == \
        sorted(results_key(r, fields) for r in archived['results'])
    ok = doc['status'] == passing and archived['status'] == passing and same and not doc['rejected'] \
        and doc['missing_count'] == 0 and doc['certificates'] == archived['certificates']
    left = [p.name for p in d.iterdir() if not p.name.endswith('.json')]
    drop(*[d / n for n in os.listdir(d)])
    if not ok or left:
        raise RuntimeError(f'{attempt}: status {doc["status"]}, same results {same}, leftover {left[:3]}')
    return dict(status=doc['status'], certificates=doc['certificates'], rejected=len(doc['rejected']),
                missing=doc['missing_count'], results_equal_archived=same, seconds=round(seconds, 1),
                receipt=out_name, receipt_sha256=digest(RESULTS / out_name))


def stage_c017(jobs):
    return read_all('017-type-ii-three-exception', 'read_all', '*-c[12].json', 'read-all-result.json',
                    'read-all-017.json', 'ALL_CASES_VERIFIED',
                    ('path', 'sha256', 'verdict', 'constants', 'case', 'rows', 'clauses', 'files'), jobs)


def stage_c018(jobs):
    return read_all('018-no-free-residual-six', 'read_all018', 'l1-*-m[12].json', 'read-all-l1.json',
                    'read-all-018.json', 'ALL_L1_CASES_VERIFIED',
                    ('path', 'sha256', 'verdict', 'variants', 'case', 'rows', 'clauses', 'files'), jobs)


def run_logged(name, argv, cwd, timeout):
    started = time.monotonic()
    with (RESULTS / f'{name}.log').open('x') as log:
        p = subprocess.run(argv, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, timeout=timeout)
    return dict(name=name, argv=argv, returncode=p.returncode, seconds=round(time.monotonic() - started, 1))


def stage_controls(_jobs):
    out = [run_logged(f'controls{"-O" if o else ""}', [sys.executable] + (['-O'] if o else []) +
                      [str(PACKET / 'run_controls.py')], REPO, 3600) for o in (False, True)]
    if any(r['returncode'] for r in out):
        raise RuntimeError(f'controls failed: {out}')
    return dict(runs=out, receipts=[json.loads((RESULTS / f'controls{s}.json').read_text())['summary']
                                    for s in ('', '-O')])


def stage_tests(_jobs):
    # 014's verify_core tests read the raw-19 certificate from certs/
    certs_dir('014-context-pricing')
    test_files = [store().materialize(A / '014-context-pricing/certs' / f'raw-19.{k}')
                  for k in ('json', 'cnf', 'labels.json', 'lrat')]
    try:
        return run_tests()
    finally:
        drop(*test_files)


def run_tests():
    out = []
    for a in ('014-context-pricing', '015-sphere-catalog-audit', '016-one-free-type-iii',
              '017-type-ii-three-exception', '018-no-free-residual-six'):
        for o in (False, True):
            out.append(run_logged(f'tests-{a[:3]}{"-O" if o else ""}',
                                  [sys.executable] + (['-O'] if o else []) +
                                  ['-m', 'pytest', '-q', '-p', 'no:cacheprovider'], A / a, 7200))
    if any(r['returncode'] for r in out):
        raise RuntimeError(f'tests failed: {[r["name"] for r in out if r["returncode"]]}')
    return dict(runs=out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jobs', type=int, default=2)
    ap.add_argument('--stages', default=','.join(STAGES))
    a = ap.parse_args()
    stages = a.stages.split(',')
    started = now()
    records = {}
    for s in stages:
        t = time.monotonic()
        print(json.dumps(dict(stage=s, started=now())), flush=True)
        records[s] = dict(globals()['stage_' + s](a.jobs), seconds=round(time.monotonic() - t, 1))
        (RESULTS / f'stage-{s}.json').write_text(json.dumps(records[s], indent=1) + '\n')
        print(json.dumps(dict(stage=s, passed=True, seconds=records[s]['seconds'])), flush=True)
    receipt = dict(schema_version=1, kind='V1_5_0_REPLAY_RECEIPT', started=started, finished=now(),
                   complete=stages == STAGES, stages=stages, jobs=a.jobs, python=sys.version,
                   driver_sha256=digest(__file__),
                   manifests={n: digest(PACKET / n) for n in ('SOURCE-MANIFEST.json', 'CERTIFICATE-MANIFEST.json')},
                   controls_sha256=digest(PACKET / 'run_controls.py'),
                   summary={s: {k: v for k, v in r.items() if k != 'results'} for s, r in records.items()})
    name = 'REPLAY-RECEIPT.json' if receipt['complete'] else f'PARTIAL-RECEIPT-{"-".join(stages)}.json'
    with (RESULTS / name).open('x') as f:
        f.write(json.dumps(receipt, indent=1) + '\n')
    print(json.dumps(dict(receipt=name, complete=receipt['complete'])))


if __name__ == '__main__':
    main()
