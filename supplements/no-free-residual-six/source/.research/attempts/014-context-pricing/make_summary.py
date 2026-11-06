"""Write signed-star-raw-certificates.json from the hardened verify records.

The model, label and row scope come from each certs/raw-<i>.verify2.json
(produced by verify_core.py --require-raw), cross-checked against the core
file; every file is pinned by SHA-256.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCES = ['models.py', 'encode.py', 'core.py', 'certify.py', 'verify_core.py', 'test_encode.py',
           'test_verify_core.py', 'run_all.sh', 'make_summary.py', 'build_frontier.py', 'test_build_frontier.py']
LRAT_TRIM_SHA = '179d041f645a98d51d3ca6dbbe4950806ad8eceb54c9a762f54e7acee154f8df'


def sha(p):
    return hashlib.sha256((HERE / p).read_bytes()).hexdigest()


def context(i):
    core = json.loads((HERE / f'cores/raw-{i}.json').read_text())
    rec = json.loads((HERE / f'certs/raw-{i}.verify2.json').read_text().strip().splitlines()[-1])
    if rec['verdict'] != 'ROWS_INFEASIBLE_VERIFIED' or rec['clause_soundness'] != 'PASS' or rec['lrat_trim_exit'] != 20:
        raise SystemExit(f'{i}: not verified')
    if rec['row_scope'] != 'RAW' or rec['model_id'] != core['model_id'] or rec['row_ids'] != core['core_rows']:
        raise SystemExit(f'{i}: record does not match its core')
    files = {k: f'certs/raw-{i}.{k}' for k in ('cnf', 'lrat', 'labels.json', 'json', 'verify.json', 'verify2.json')}
    files['core'] = f'cores/raw-{i}.json'
    return dict(index=i, label=rec['label'], model_id=rec['model_id'], row_scope=rec['row_scope'],
                raw_row_count=rec['raw_row_count'], core_rows=rec['rows'], families=core['families'],
                cnf_clauses=rec['clauses'], lrat_bytes=(HERE / files['lrat']).stat().st_size,
                core_search_wall_s=core['wall'], verdict=rec['verdict'], input_sha256=rec['input_sha256'],
                files={k: dict(path=p, sha256=sha(p)) for k, p in files.items()})


def main():
    contexts = [context(i) for i in range(2, 26)]
    labels = [c['label'] for c in contexts]
    if len(set(labels)) != len(labels):
        raise SystemExit('duplicate context')
    doc = dict(
        status='VERIFIED_CANDIDATE_PENDING_PARENT_ACCEPTANCE',
        claim='Each of the 24 signed-star native contexts open in H/signed-star-genuine-frontier-cycle1510.json '
              'has an infeasible subset of its raw native rows (common block 1432 plus context rows, no added '
              'rows), certified by CaDiCaL 3.0.1 LRAT, the pinned lrat-trim, and the independent clause-soundness '
              'reader verify_core.py --require-raw.',
        scope='Closes only the conditional branch residual defect <= 6 with >= 2 negative-free coordinates, '
              'conditional on the premises listed in 015-sphere-catalog-audit/REVIEW.md. No whole '
              'negative-quintic pattern, no one-free/no-free case, no residual > 6 case. Problem remains OPEN.',
        lrat_trim_sha256=LRAT_TRIM_SHA, sources={s: sha(s) for s in SOURCES}, contexts=contexts)
    (HERE / 'signed-star-raw-certificates.json').write_text(json.dumps(doc, indent=1) + '\n')
    print(len(contexts), 'contexts;', sorted(set(c['row_scope'] for c in contexts)))


if __name__ == '__main__':
    main()
