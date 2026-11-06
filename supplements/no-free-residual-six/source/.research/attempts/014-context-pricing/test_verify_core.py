"""The reader accepts genuine encodings and rejects tampered clauses."""
import random
import pytest
from encode import CNF
from verify_core import check_clauses

N = 1079   # reader requires aux vars above the 1079 native variables


def rows_and_cnf(seed):
    r = random.Random(seed)
    rows = []
    for _ in range(3):
        vs = r.sample(range(1, 30), r.randint(2, 7))
        terms = [(v, r.choice([-3, -2, -1, 1, 2])) for v in vs]
        lo = r.randint(-3, 2); rows.append((terms, lo, lo + r.randint(0, 2)))
    cnf = CNF(N)
    for k, (t, lo, hi) in enumerate(rows):
        cnf.add_row(t, lo, hi, tag=k)
    labels = [[v, *cnf.labels[v]] for v in sorted(cnf.labels)]
    return rows, cnf, labels


@pytest.mark.parametrize('seed', range(20))
def test_genuine_accepted(seed):
    rows, cnf, labels = rows_and_cnf(seed)
    check_clauses(rows, [0, 1, 2], cnf.nvars, cnf.clauses, labels)


@pytest.mark.parametrize('seed', range(20))
def test_tampering_rejected(seed):
    rows, cnf, labels = rows_and_cnf(seed)
    r = random.Random(1000 + seed)
    attacks = [lambda c: c + [[-1]],                               # extra native unit clause
               lambda c: c + [[1, 2, 3]]]                          # arbitrary clause
    steps = [i for i, cl in enumerate(cnf.clauses) if len(cl) == 3]
    # a dead-end clause whose OTHER branch is live (the encoder stepped into it);
    # flipping it to that branch is a false claim. (Both branches can be dead
    # legitimately when [lo, hi] falls in a gap between the two child ranges.)
    live = {(cl[0], cl[1]) for cl in cnf.clauses if len(cl) == 3}
    deads = [i for i, cl in enumerate(cnf.clauses) if len(cl) == 2 and (cl[0], -cl[1]) in live]
    if steps:
        i = r.choice(steps)
        attacks.append(lambda c, i=i: c[:i] + [[c[i][0], -c[i][1], c[i][2]]] + c[i + 1:])   # wrong branch
    if deads:
        i = r.choice(deads)
        attacks.append(lambda c, i=i: c[:i] + [[c[i][0], -c[i][1]]] + c[i + 1:])            # kill live branch
    for attack in attacks:
        bad = attack([list(cl) for cl in cnf.clauses])
        with pytest.raises(SystemExit):
            check_clauses(rows, [0, 1, 2], cnf.nvars, bad, labels)


def test_labels_must_name_allowed_rows():
    rows, cnf, labels = rows_and_cnf(0)
    with pytest.raises(SystemExit):
        check_clauses(rows, [0, 1], cnf.nvars, cnf.clauses, labels)


# Binding checks added after the independent review (context label, raw scope,
# row-id range). The CLI tests tamper copies in tmp_path, never certs/.
import json
import subprocess
import sys
from pathlib import Path

from verify_core import check_row_ids, label

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PY = str(ROOT / '.research/venv-exact/bin/python')


@pytest.mark.parametrize('ids', [[], [0, 0], [True, 1], [1.0], [-1], [99]])
def test_row_ids_rejected(ids):
    with pytest.raises(SystemExit):
        check_row_ids(ids, 50, 40, False)


def test_row_scope():
    assert check_row_ids([0, 39], 50, 40, False) == 'RAW'
    assert check_row_ids([0, 40], 50, 40, False) == 'EXTENDED'
    with pytest.raises(SystemExit, match='raw'):
        check_row_ids([0, 40], 50, 40, True)


def test_label_derived_from_model():
    m = dict(native_identity=dict(catalog_sha256='x', order=11, original_index=185), constant=2)
    assert label(m) == 'o11-i185-c2'


def run_cli(cert_path):
    return subprocess.run([PY, str(HERE / 'verify_core.py'), str(cert_path), '--require-raw'],
                          capture_output=True, text=True, cwd=ROOT)


def tampered(tmp_path, **change):
    cert = json.loads((HERE / 'certs/raw-19.json').read_text())
    cert.update(change)
    if 'row_ids' in change:   # keep the labels file consistent so only the id check can fire
        lab = json.loads(Path(cert['labels']['path']).read_text())
        lab['row_ids'] = change['row_ids']
        p = tmp_path / 'labels.json'
        p.write_text(json.dumps(lab))
        import hashlib
        cert['labels'] = dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    out = tmp_path / 'cert.json'
    out.write_text(json.dumps(cert))
    return out


def test_cli_genuine_record_names_model(tmp_path):
    p = run_cli(HERE / 'certs/raw-19.json')
    rec = json.loads(p.stdout.strip().splitlines()[-1])
    assert p.returncode == 0 and rec['verdict'] == 'ROWS_INFEASIBLE_VERIFIED'
    assert rec['label'] == 'o11-i185-c2' and rec['row_scope'] == 'RAW'
    assert set(rec['input_sha256']) >= {'cnf', 'labels', 'proof', 'authorization', 'lrat_trim'}


def test_cli_relabel_cannot_rename(tmp_path):
    p = run_cli(tampered(tmp_path, label='o8-i7-c1', index=4))
    rec = json.loads(p.stdout.strip().splitlines()[-1])
    assert rec['label'] == 'o11-i185-c2'           # the model's own label, not the claim


@pytest.mark.parametrize('extra', [12600, -1])
def test_cli_added_or_negative_row_rejected(tmp_path, extra):
    ids = json.loads((HERE / 'certs/raw-19.json').read_text())['row_ids'] + [extra]
    p = run_cli(tampered(tmp_path, row_ids=ids))
    assert p.returncode != 0 and 'ROWS_INFEASIBLE_VERIFIED' not in p.stdout
