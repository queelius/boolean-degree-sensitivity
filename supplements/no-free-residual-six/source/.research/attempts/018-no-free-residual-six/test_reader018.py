import copy
import json
import tempfile
import unittest
from pathlib import Path

import reader018 as rd

FX = Path(__file__).resolve().parent / 'fixtures'
B = json.loads((FX / 'cap-1.json').read_text())
A = json.loads((FX / 'A-pp-m2.json').read_text())


def read(doc):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'c.json'
        p.write_text(json.dumps(doc))
        return rd.read(p)


def mutated(base, f):
    doc = copy.deepcopy(base)
    f(doc)
    return doc


class TestReader018(unittest.TestCase):
    def test_fixtures_verify(self):
        for doc in (B, A):
            self.assertEqual(read(doc)['verdict'], 'CASE_ROWS_INFEASIBLE_VERIFIED')

    def bad(self, base, f):
        with self.assertRaises(rd.ReaderError):
            read(mutated(base, f))

    def test_variants_must_hold_row_by_row(self):
        # B's core uses no Q-weighted and no constant row: valid for every constant-only type and both m
        r = read(mutated(B, lambda d: d.update(variants=[[t, m] for t in ('none', 'c0', 'c3') for m in (1, 2)])))
        self.assertEqual(len(r['variants']), 6)
        # A's core uses Q-weighted rows: claiming the other magnitude must fail
        self.bad(A, lambda d: d.update(variants=[[d['case']['type'], 2], [d['case']['type'], 1]]))

    def test_rejects_variant_changing_pair_type(self):
        self.bad(A, lambda d: d.update(variants=[['pp', 2], ['pm', 2]]))

    def test_rejects_magnitude_three(self):
        self.bad(B, lambda d: d.update(magnitude=3))

    def test_rejects_moved_Q(self):
        self.bad(B, lambda d: d['case'].update(Q=[1, 2, 3, 6]))

    def test_rejects_wrong_type(self):
        self.bad(A, lambda d: d['case'].update(type='pm'))

    def test_rejects_degcap_outside_B_ord(self):
        def f(d):
            d['case']['part'] = 'B-exc'
        self.bad(B, f)

    def test_rejects_degcap_at_Q_vertex(self):
        def f(d):
            r = next(r for r in d['rows'] if r['key'][0] == 'degcap')
            r['key'][1] = d['case']['Q'][0]
        self.bad(B, f)

    def test_rejects_flag_rows_in_part_A(self):
        def f(d):
            d['rows'].append(dict(id=10 ** 6, key=['flag', 5, [6, 7, 8]], terms=[], lo=0, hi=0))
        self.bad(A, f)

    def test_rejects_root_in_Q(self):
        self.bad(B, lambda d: d['case'].update(Q=[0, 1, 2, 3]))

    def test_rejects_forged_vertex(self):
        def f(d):
            d['rows'][0]['key'] = ['vertex', 13]
        self.bad(B, f)


class TestReaderPaths(unittest.TestCase):
    """Row kinds the fixtures' cores do not contain, rebuilt and compared with model018."""

    def test_every_row_kind_matches_model018(self):
        import model018 as M
        cover = json.loads((FX.parent / 'l1-cover.json').read_text())['rows']
        for case in (next(r for r in cover if r['part'] == 'B-ord' and r['type'] == 'c3'),
                     next(r for r in cover if r['part'] == 'B-exc')):
            for mag in (1, 2):
                model, fixed = M.case_model(case, mag)
                names = model['variables']
                rc = rd.Case(case, mag)
                seen = set()
                for terms, lo, hi, key in model['rows']:
                    kind = key[0]
                    if kind in seen and kind not in ('vertex', 'implied_P', 'degcap'):
                        continue
                    seen.add(kind)
                    jkey = [kind] + [list(x) if isinstance(x, tuple) else x for x in key[1:]]
                    want, wlo, whi = rc.substituted(rd.parse_key(jkey))
                    shift = sum(co * fixed[names[v]] for v, co in terms if names[v] in fixed)
                    got = {(names[v][0], tuple(sorted(names[v][1]))): co for v, co in terms if names[v] not in fixed}
                    self.assertEqual((got, lo - shift, hi - shift), (want, wlo, whi), key)
                self.assertTrue({'constant', 'vertex', 'implied_P', 'implied_k', 'value', 'pair', 'triple', 'flag'} <= seen)
                if case['part'] == 'B-ord':
                    self.assertIn('degcap', seen)


class TestBinding(unittest.TestCase):
    def test_forged_root_metadata_is_not_bound(self):
        import read_all018
        doc = copy.deepcopy(B)
        cover = json.loads((FX.parent / 'l1-cover.json').read_text())['rows']
        real = read_all018.placement(doc['case'])
        self.assertIn(real, {read_all018.placement(c) for c in cover})
        doc['case']['root'] = {'kind': 'forged-catalog', 'index': 999999}
        self.assertNotIn(read_all018.placement(doc['case']), {read_all018.placement(c) for c in cover})


if __name__ == '__main__':
    unittest.main()
