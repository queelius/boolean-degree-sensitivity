"""Successor of H/signed-star-genuine-frontier-cycle1510.json from the 014 certificates.

Every entry whose model_id has a verified raw certificate in
signed-star-raw-certificates.json becomes raw EXCLUDED and genuine EXCLUDED,
citing that file and the 1531 acceptance. Every other field is carried over.
Writes a new file only; refuses to overwrite.
"""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
H = HERE.parent / '009-parent-analysis'
PRED = H / 'signed-star-genuine-frontier-cycle1510.json'
PRED_SHA = '3621b82295391042e64d4ba49091e98ab74170801a36af9ee19a211efc722da2'
CERTS = HERE / 'signed-star-raw-certificates.json'


def pin(path):
    return dict(path=str(path.resolve()), sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def key(model_id):
    return json.dumps(model_id, sort_keys=True)


def build(pred, certs, cert_pin, acceptance_pin):
    verified = {key(c['model_id']) for c in certs['contexts'] if c['verdict'] == 'ROWS_INFEASIBLE_VERIFIED'}
    entries = []
    for e in pred['entries']:
        e = dict(e)
        if key(e['model_id']) in verified:
            auth = dict(certificates=cert_pin, acceptance=acceptance_pin)
            e['raw_row_model_status'] = 'EXCLUDED'
            e['raw_row_exclusion_authority'] = auth
            e['genuine_context_status'] = 'EXCLUDED'
            e['genuine_exclusion_authority'] = auth
            verified.discard(key(e['model_id']))
        entries.append(e)
    if verified:
        raise SystemExit(f'certificates for models absent from the frontier: {sorted(verified)}')
    status = {key(e['model_id']): e['genuine_context_status'] for e in entries}
    roots = []
    for r in pred['roots']:
        consts = [dict(constant=c['constant'],
                       status=status[key(dict(native_identity=r['native_identity'], constant=c['constant']))])
                  for c in r['constants']]
        roots.append(dict(native_identity=r['native_identity'], constants=consts,
                          genuine_status='EXCLUDED' if all(c['status'] == 'EXCLUDED' for c in consts) else 'OPEN'))
    return dict(
        schema_version=1, scope=pred['scope'], predecessor=dict(path=str(PRED), sha256=PRED_SHA),
        new_certificate=cert_pin, acceptance=acceptance_pin, entries=entries, roots=roots,
        raw_row_counts=dict(Counter(e['raw_row_model_status'] for e in entries)),
        genuine_context_counts=dict(Counter(e['genuine_context_status'] for e in entries)),
        genuine_root_counts=dict(Counter(r['genuine_status'] for r in roots)),
        raw_row_UNSAT_for_c2_claimed=pred['raw_row_UNSAT_for_c2_claimed'],
        whole_patterns_changed=0, global_goal_complete=False)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--acceptance', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    if a.out.exists():
        raise SystemExit(f'{a.out} exists; frozen files are never overwritten')
    if hashlib.sha256(PRED.read_bytes()).hexdigest() != PRED_SHA:
        raise SystemExit('1510 frontier hash mismatch')
    doc = build(json.loads(PRED.read_text()), json.loads(CERTS.read_text()), pin(CERTS), pin(a.acceptance))
    a.out.write_text(json.dumps(doc, indent=1) + '\n')
    print(json.dumps({k: doc[k] for k in ('raw_row_counts', 'genuine_context_counts', 'genuine_root_counts')}))


if __name__ == '__main__':
    main()
