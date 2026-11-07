"""Independent reader for a core certificate. Shares no code with models.py,
encode.py or certify.py.

Claim checked: the native rows R (by id) of the named context have no 0/1
solution. Evidence: CNF + labels + LRAT.
  1. Rebuild the context's rows from the pinned 009 JSON sources directly
     (common rows, then context rows, then inventory added rows), and map
     masks to variables 1..1079 by position in the common variable list.
  2. Soundness of the CNF w.r.t. R: give each labelled aux var (r, k, s) the
     value [sum of the first k terms of row r equals s]. For any x satisfying
     every row in R, each clause must then be true. Checked per clause shape:
       [a]                 a = (r,0,0)                              (true: empty sum is 0)
       [-a, -l, b]         a = (r,k,s), l = literal of term k of r,
                           b = (r,k+1,s + c_k*[l positive])         (true: partial sums step)
       [-a, -l]            a = (r,k,s), the partial sum s' after taking l makes
                           [s'+minrest, s'+maxrest] miss [lo,hi]     (true: row would fail)
       []                  only if row r alone is infeasible
     Any other clause shape is rejected. Hence CNF UNSAT => R infeasible.
  3. Run the pinned lrat-trim on exactly these files: exit 20 and 's VERIFIED'.
Row ids must be distinct integers in range; with --require-raw they must
also lie below the raw row count (common + context, no added rows). The
record names the model, a label derived from it (never the certificate's
own label), the row-id scope and the hashes of every input.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

H = Path(__file__).resolve().parents[1] / '009-parent-analysis'
AUTH = H / 'tip-interval-parent-authorization-cycle1520.json'
AUTH_SHA = '0a43aedf58c5e16b376b9706cde4858748d1e4bbc79596acd8d3ba3c47f5dcd5'
LRAT_TRIM = H.parent / '006-solver-resume/lrat-trim/lrat-trim'
LRAT_TRIM_SHA = '179d041f645a98d51d3ca6dbbe4950806ad8eceb54c9a762f54e7acee154f8df'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pinned(ref):
    if sha(ref['path']) != ref['sha256']:
        raise SystemExit('pin mismatch: ' + ref['path'])
    return json.load(open(ref['path']))


def canon(o):
    return json.dumps(o, sort_keys=True)


def context_rows(model_id):
    """(rows, raw_count, source pins); rows are common, context, then added."""
    if sha(AUTH) != AUTH_SHA:
        raise SystemExit('authorization changed')
    src = json.load(open(AUTH))['sources']
    common, packet, inv = pinned(src['common_rows']), pinned(src['context_rows']), pinned(src['inventory'])
    ctx = [c for c in packet['contexts'] if canon(c['model_id']) == canon(model_id)]
    add = [c for c in inv['contexts'] if canon(c['model_id']) == canon(model_id)]
    if len(ctx) != 1 or len(add) != 1:
        raise SystemExit('context not unique')
    rows = common['rows'] + ctx[0]['rows'] + add[0]['added_rows']
    var = {m: i + 1 for i, m in enumerate(common['variables'])}
    if len(var) != 1079:
        raise SystemExit('variable list')
    pins = {k: src[k]['sha256'] for k in ('common_rows', 'context_rows', 'inventory')}
    return ([([(var[m], c) for m, c in r['terms']], r['lower'], r['upper']) for r in rows],
            len(common['rows']) + len(ctx[0]['rows']), pins)


def check_row_ids(row_ids, nrows, raw_count, require_raw):
    if not row_ids or any(type(r) is not int for r in row_ids) or len(set(row_ids)) != len(row_ids):
        raise SystemExit('row ids must be distinct integers')
    if min(row_ids) < 0 or max(row_ids) >= nrows:
        raise SystemExit('row id out of range')
    if require_raw and max(row_ids) >= raw_count:
        raise SystemExit('row id outside the raw rows')
    return 'RAW' if max(row_ids) < raw_count else 'EXTENDED'


def label(model_id):
    n = model_id['native_identity']
    return f"o{n['order']}-i{n['original_index']}-c{model_id['constant']}"


def read_cnf(path):
    clauses, cur, header = [], [], None
    for line in open(path):
        t = line.split()
        if not t or t[0] == 'c':
            continue
        if t[0] == 'p':
            header = (int(t[2]), int(t[3])); continue
        for x in map(int, t):
            if x == 0:
                clauses.append(cur); cur = []
            else:
                cur.append(x)
    if cur or header is None or header[1] != len(clauses):
        raise SystemExit('malformed CNF')
    return header[0], clauses


def check_clauses(rows, row_ids, nvars, clauses, labels):
    allowed = set(row_ids)
    lab = {}
    for v, r, k, s in labels:
        if v <= 1079 or v > nvars or v in lab or r not in allowed or not 0 <= k <= len(rows[r][0]):
            raise SystemExit(f'bad label {v}')
        lab[v] = (r, k, s)
    rest = {}
    for r in allowed:
        terms = rows[r][0]
        mn = [0] * (len(terms) + 1); mx = [0] * (len(terms) + 1)
        for k in range(len(terms) - 1, -1, -1):
            mn[k] = mn[k + 1] + min(terms[k][1], 0); mx[k] = mx[k + 1] + max(terms[k][1], 0)
        rest[r] = (mn, mx)
    for cl in clauses:
        if len(cl) == 0:
            # must be justified by some allowed row being infeasible alone
            if not any(rest[r][0][0] > rows[r][2] or rest[r][1][0] < rows[r][1] for r in allowed):
                raise SystemExit('unjustified empty clause')
            continue
        if len(cl) == 1 and cl[0] in lab and lab[cl[0]][1:] == (0, 0):
            continue
        if len(cl) in (2, 3) and cl[0] < 0 and -cl[0] in lab:
            r, k, s = lab[-cl[0]]
            terms, lo, hi = rows[r]
            if k >= len(terms):
                raise SystemExit('step past end')
            v, c = terms[k]
            lit = -cl[1]
            if abs(lit) != v:
                raise SystemExit('clause literal is not term k of its row')
            s2 = s + (c if lit > 0 else 0)
            if len(cl) == 3:
                b = cl[2]
                if b in lab and lab[b] == (r, k + 1, s2):
                    continue
                raise SystemExit('bad step clause')
            mn, mx = rest[r]
            if s2 + mn[k + 1] > hi or s2 + mx[k + 1] < lo:
                continue
            raise SystemExit('unjustified dead-end clause')
        raise SystemExit(f'unrecognized clause {cl[:4]}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cert')
    ap.add_argument('--require-raw', action='store_true')
    a = ap.parse_args()
    cert = json.load(open(a.cert))
    rows, raw_count, pins = context_rows(cert['model_id'])
    hashes = {k: sha(cert[k]['path']) for k in ('cnf', 'labels', 'proof')}
    for k in hashes:
        if hashes[k] != cert[k]['sha256']:
            raise SystemExit(k + ' changed')
    lab = json.load(open(cert['labels']['path']))
    if lab['row_ids'] != cert['row_ids']:
        raise SystemExit('row ids differ')
    scope = check_row_ids(cert['row_ids'], len(rows), raw_count, a.require_raw)
    nvars, clauses = read_cnf(cert['cnf']['path'])
    check_clauses(rows, cert['row_ids'], nvars, clauses, lab['labels'])
    if sha(LRAT_TRIM) != LRAT_TRIM_SHA:
        raise SystemExit('checker changed')
    p = subprocess.run([str(LRAT_TRIM), '--forward', '--no-trim', cert['cnf']['path'], cert['proof']['path']],
                       capture_output=True, text=True)
    ok = p.returncode == 20 and any(l.strip() == 's VERIFIED' for l in p.stdout.splitlines())
    print(json.dumps(dict(label=label(cert['model_id']), model_id=cert['model_id'], row_ids=cert['row_ids'],
                          row_scope=scope, raw_row_count=raw_count, rows=len(cert['row_ids']),
                          clauses=len(clauses), clause_soundness='PASS', lrat_trim_exit=p.returncode,
                          input_sha256=dict(hashes, authorization=AUTH_SHA, lrat_trim=LRAT_TRIM_SHA, **pins),
                          verdict='ROWS_INFEASIBLE_VERIFIED' if ok else 'NOT_VERIFIED')))
    sys.exit(0 if ok else 1)
