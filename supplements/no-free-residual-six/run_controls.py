"""Positive and negative controls for the v1.5.0 replay (run by replay_packet.py, normal and -O).

Each control states the outcome it requires. Altered copies are written beside the materialized
certificate in the scratch certs/ directory and removed afterwards; frozen files are never
changed. The readers signal rejection with their own exceptions (not assert), so -O does not
weaken them; running both modes checks that.

  014  verify_core.py --require-raw: the untouched certificate passes; a proof with its final
       (empty-clause) step removed and the pin updated is NOT_VERIFIED by lrat-trim; an altered
       proof under the old pin exits with 'proof changed'.
  017  reader017.read: untouched passes; truncated proof with updated pin is NOT_VERIFIED;
       a changed row bound is rejected.
  018  reader018.read: the same three; plus the assembly: the archived results with one
       certificate removed leave an obligation missing and status INCOMPLETE, the full results
       leave none. This exercises the assembly bookkeeping (missing() and status() of
       read_all018) on the archived result records; it does not rerun discovery after deleting
       a real certificate (the full c018 stage does the discovery).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import replay_packet as RP  # noqa: E402

A = RP.A
OUT = RP.RESULTS / ('controls-O.json' if not __debug__ else 'controls.json')
results = []


def record(name, want, got):
    results.append(dict(control=name, required=want, observed=got, passed=want == got))
    print(json.dumps(results[-1]), flush=True)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def smallest(attempt, suffix):
    """The certificate JSON whose proof is smallest (by original bytes)."""
    proofs = [e for e in RP.store().files if e['original_path'].startswith(str(A / attempt / 'certs') + '/')
              and e['original_path'].endswith(suffix)]
    return min(proofs, key=lambda e: e['original_bytes'])['original_path']


def materialize_case(cert_path, keys):
    cert = RP.store().materialize(cert_path)
    doc = json.loads(cert.read_text())
    files = [RP.store().materialize(doc[k]['path']) for k in keys]
    return cert, doc, files


def truncated_copy(doc, cert, tag):
    """A copy of the certificate whose proof lacks its final line, with the proof pin updated."""
    proof = Path(doc['proof']['path'])
    lines = proof.read_bytes().rstrip(b'\n').split(b'\n')
    bad = proof.with_name(f'control-{tag}.lrat')
    bad.write_bytes(b'\n'.join(lines[:-1]) + b'\n')
    copy = dict(doc, proof=dict(doc['proof'], path=str(bad), sha256=sha(bad)))
    p = cert.with_name(f'control-{tag}.json')
    p.write_text(json.dumps(copy))
    return p, [bad, p]


def stale_copy(doc, cert, tag):
    """A copy pointing at an altered proof but keeping the old pin."""
    bad = Path(doc['proof']['path']).with_name(f'control-{tag}.lrat')
    bad.write_bytes(Path(doc['proof']['path']).read_bytes() + b'c altered\n')
    p = cert.with_name(f'control-{tag}.json')
    p.write_text(json.dumps(dict(doc, proof=dict(doc['proof'], path=str(bad)))))
    return p, [bad, p]


def reader_outcome(read, path):
    try:
        return read(path)['verdict']
    except Exception as e:      # the frozen readers raise their own ReaderError on a mismatch
        return 'REJECTED:' + type(e).__name__


def control_reader(attempt, module, suffix, tag):
    sys.path[:0] = [str(A / attempt), str(A / '017-type-ii-three-exception')]
    mod = __import__(module)
    cert_path = smallest(attempt, suffix)[:-len(suffix)] + suffix.replace('.lrat', '.json')
    cert, doc, files = materialize_case(cert_path, ('cnf', 'labels', 'proof'))
    extra = []
    try:
        record(f'{tag} untouched certificate', 'CASE_ROWS_INFEASIBLE_VERIFIED', reader_outcome(mod.read, cert))
        p, made = truncated_copy(doc, cert, tag + '-trunc')
        extra += made
        record(f'{tag} proof without its empty-clause step', 'NOT_VERIFIED', reader_outcome(mod.read, p))
        p, made = stale_copy(doc, cert, tag + '-stale')
        extra += made
        record(f'{tag} altered proof under the old pin', 'REJECTED:ReaderError', reader_outcome(mod.read, p))
        rows = [dict(r) for r in doc['rows']]
        rows[0]['lo'] = rows[0]['lo'] - 1
        p = cert.with_name(f'control-{tag}-row.json')
        p.write_text(json.dumps(dict(doc, rows=rows)))
        extra.append(p)
        record(f'{tag} changed row bound', 'REJECTED:ReaderError', reader_outcome(mod.read, p))
    finally:
        RP.drop(cert, *files, *extra)
    return mod


def control_014():
    D = A / '014-context-pricing'
    cert, doc, files = materialize_case(D / 'certs/raw-1.json', ('cnf', 'labels', 'proof'))
    vc = [sys.executable, str(D / 'verify_core.py'), '--require-raw']

    def run(p):
        """(exit code, the reader's verdict or its exit message): distinguishes a checker
        rejection from a pin rejection and from an unrelated failure."""
        r = subprocess.run(vc + [str(p)], cwd=RP.REPO, capture_output=True, text=True)
        if r.stdout.strip():
            return [r.returncode, json.loads(r.stdout.strip().splitlines()[-1])['verdict']]
        return [r.returncode, (r.stderr.strip().splitlines() or [''])[-1]]
    extra = []
    try:
        record('014 untouched certificate', [0, 'ROWS_INFEASIBLE_VERIFIED'], run(cert))
        p, made = truncated_copy(doc, cert, '014-trunc')
        extra += made
        record('014 proof without its empty-clause step (lrat-trim rejects)', [1, 'NOT_VERIFIED'], run(p))
        p, made = stale_copy(doc, cert, '014-stale')
        extra += made
        record('014 altered proof under the old pin (pin check rejects)', [1, 'proof changed'], run(p))
    finally:
        RP.drop(cert, *files, *extra)


def control_assembly_018(read_all018):
    D = A / '018-no-free-residual-six'
    archived = json.loads((D / 'read-all-l1.json').read_text())
    cover = json.loads((D / 'l1-cover.json').read_text())['rows']
    record('018 assembly, archived results', 0, len(read_all018.missing(archived['results'], cover)))
    drop = next(i for i, r in enumerate(archived['results']) if r['verdict'] == 'CASE_ROWS_INFEASIBLE_VERIFIED')
    fewer = archived['results'][:drop] + archived['results'][drop + 1:]
    miss = read_all018.missing(fewer, cover)
    record('018 assembly, one certificate removed', True, len(miss) > 0)
    ok = dict(status='L1_COVER_READER_PASS')
    fr = dict(status='NO_FREE_FRONTIER_READER_PASS')
    record('018 status with a missing obligation', 'INCOMPLETE', read_all018.status(miss, [], ok, fr, True))
    record('018 status with nothing missing', 'ALL_L1_CASES_VERIFIED', read_all018.status([], [], ok, fr, True))


def main():
    control_014()
    control_reader('017-type-ii-three-exception', 'reader017', '-c1.lrat', '017')
    control_reader('018-no-free-residual-six', 'reader018', '-m1.lrat', '018')
    sys.path.insert(0, str(A / '018-no-free-residual-six'))
    import read_all018
    control_assembly_018(read_all018)
    summary = dict(controls=len(results), passed=sum(r['passed'] for r in results), optimized=not __debug__)
    OUT.write_text(json.dumps(dict(summary=summary, results=results), indent=1) + '\n')
    print(json.dumps(summary))
    sys.exit(0 if summary['passed'] == summary['controls'] else 1)


if __name__ == '__main__':
    main()
