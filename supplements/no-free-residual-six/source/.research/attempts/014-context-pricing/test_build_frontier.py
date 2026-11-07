import json
import sys

sys.dont_write_bytecode = True
import pytest

import build_frontier as bf

PIN = dict(path='x', sha256='0' * 64)


def mid(order, c):
    return dict(native_identity=dict(catalog_sha256='a', order=order, original_index=0), constant=c)


def pred():
    entries = [dict(model_id=mid(o, c), raw_row_model_status='OPEN', raw_row_exclusion_authority=None,
                    genuine_context_status='OPEN', genuine_exclusion_authority=None)
               for o in (7, 8) for c in (1, 2)]
    entries[0].update(raw_row_model_status='EXCLUDED', genuine_context_status='EXCLUDED', raw_row_exclusion_authority='old')
    roots = [dict(native_identity=mid(o, 1)['native_identity'],
                  constants=[dict(constant=1, status='OPEN'), dict(constant=2, status='OPEN')], genuine_status='OPEN')
             for o in (7, 8)]
    return dict(scope='S', entries=entries, roots=roots, raw_row_UNSAT_for_c2_claimed=False)


def certs(*models, verdict='ROWS_INFEASIBLE_VERIFIED'):
    return dict(contexts=[dict(model_id=m, verdict=verdict) for m in models])


def test_only_certified_entries_change():
    doc = bf.build(pred(), certs(mid(8, 1), mid(8, 2)), PIN, PIN)
    st = [(e['raw_row_model_status'], e['genuine_context_status']) for e in doc['entries']]
    assert st == [('EXCLUDED', 'EXCLUDED'), ('OPEN', 'OPEN'), ('EXCLUDED', 'EXCLUDED'), ('EXCLUDED', 'EXCLUDED')]
    assert doc['entries'][0]['raw_row_exclusion_authority'] == 'old'
    assert [r['genuine_status'] for r in doc['roots']] == ['OPEN', 'EXCLUDED']
    assert doc['genuine_context_counts'] == {'EXCLUDED': 3, 'OPEN': 1}
    assert doc['whole_patterns_changed'] == 0 and doc['global_goal_complete'] is False


def test_unverified_verdict_ignored():
    doc = bf.build(pred(), certs(mid(8, 1), verdict='UNTRUSTED'), PIN, PIN)
    assert doc['genuine_context_counts'] == {'EXCLUDED': 1, 'OPEN': 3}


def test_foreign_certificate_rejected():
    with pytest.raises(SystemExit):
        bf.build(pred(), certs(mid(9, 1)), PIN, PIN)


def test_key_ignores_dict_order():
    a = mid(8, 1)
    b = dict(constant=1, native_identity=dict(original_index=0, order=8, catalog_sha256='a'))
    assert bf.key(a) == bf.key(b)


def test_pin_is_absolute(tmp_path, monkeypatch):
    (tmp_path / 'a.json').write_text('{}')
    monkeypatch.chdir(tmp_path)
    p = bf.pin(bf.Path('a.json'))
    assert p['path'] == str(tmp_path / 'a.json') and len(p['sha256']) == 64
