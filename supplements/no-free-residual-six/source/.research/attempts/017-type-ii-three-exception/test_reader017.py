import copy
import json
import tempfile
import unittest
from pathlib import Path

import reader017 as rd

FIX = Path(__file__).resolve().parent / 'fixtures' / 'case0-c1.json'
CERT = json.loads(FIX.read_text())


def read_mutated(f):
    doc = copy.deepcopy(CERT)
    f(doc)
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'cert.json'
        p.write_text(json.dumps(doc))
        return rd.read(p)


class TestReader017(unittest.TestCase):
    def test_fixture_verifies(self):
        r = rd.read(FIX)
        self.assertEqual(r['verdict'], 'CASE_ROWS_INFEASIBLE_VERIFIED')
        self.assertEqual(r['rows'], 104)

    def test_rejects_changed_coefficient(self):
        def f(doc):
            doc['rows'][0]['terms'][0][1] += 1
        with self.assertRaises(rd.ReaderError):
            read_mutated(f)

    def test_rejects_changed_bound(self):
        def f(doc):
            doc['rows'][0]['hi'] += 1
        with self.assertRaises(rd.ReaderError):
            read_mutated(f)

    def test_constant_free_core_holds_at_both_constants(self):
        # c enters only through the constant row; this core does not use it
        self.assertNotIn('constant', [r['key'][0] for r in CERT['rows']])
        r = read_mutated(lambda doc: doc.update(c=2))
        self.assertEqual(r['verdict'], 'CASE_ROWS_INFEASIBLE_VERIFIED')
        r = read_mutated(lambda doc: doc.update(constants=[1, 2]))
        self.assertEqual(r['constants'], [1, 2])

    def test_rejects_constant_row_claimed_for_both(self):
        def f(doc):
            doc['constants'] = [1, 2]
            doc['rows'].append(dict(id=10 ** 6, key=['constant'], terms=[], lo=0, hi=0))
        with self.assertRaises(rd.ReaderError):
            read_mutated(f)

    def test_rejects_changed_exception(self):
        def f(doc):
            doc['case']['exceptions'][1][1] = 1
        with self.assertRaises(rd.ReaderError):
            read_mutated(f)

    def test_rejects_changed_root_link(self):
        def f(doc):
            doc['case']['faces'] = doc['case']['faces'][1:] + doc['case']['faces'][:1]
            doc['case']['faces'][0] = [1, 2, 12]
        with self.assertRaises(rd.ReaderError):
            read_mutated(f)

    def test_rejects_flag_row_at_root(self):
        def f(doc):
            row = next(r for r in doc['rows'] if r['key'][0] == 'flag')
            row['key'][1] = 0
        with self.assertRaises(rd.ReaderError):
            read_mutated(f)

    def test_rejects_unknown_row_kind(self):
        def f(doc):
            doc['rows'][0]['key'] = ['wish', 1]
        with self.assertRaises(rd.ReaderError):
            read_mutated(f)

    def test_rejects_c_outside_type_ii(self):
        def f(doc):
            doc['c'] = 3
        with self.assertRaises(rd.ReaderError):
            read_mutated(f)


class TestReaderAdversarial(unittest.TestCase):
    """Codex counterexample (REVIEW-chain-codex.md): out-of-domain keys must not yield false rows."""

    def forged(self, key, lo, hi):
        doc = copy.deepcopy(CERT)
        with tempfile.TemporaryDirectory() as d:
            cnf, lab, prf = Path(d) / 'f.cnf', Path(d) / 'f.labels.json', Path(d) / 'f.lrat'
            cnf.write_text('p cnf 0 1\n0\n')
            lab.write_text('[]')
            prf.write_text('')
            doc.update(variables=[], constants=[1, 2],
                       rows=[dict(id=0, key=key, terms=[], lo=lo, hi=hi)])
            for k, path in (('cnf', cnf), ('labels', lab), ('proof', prf)):
                doc[k] = dict(path=str(path), sha256=rd.sha(path))
            p = Path(d) / 'cert.json'
            p.write_text(json.dumps(doc))
            return rd.read(p)

    def test_rejects_vertex_13(self):
        for key, b in ((['vertex', 13], 8), (['implied_P', 13], -4), (['implied_k', 13], 12)):
            with self.assertRaises(rd.ReaderError):
                self.forged(key, b, b)

    def test_rejects_bool_and_negative_vertices(self):
        for key in (['vertex', True], ['vertex', -1], ['pair', [3, 3]], ['pair', [4, 3]], ['triple', [1, 2]],
                    ['value', [5]], ['flag', 1, [1, 2, 3]], ['constant', 0], ['vertex', 1, 2]):
            with self.assertRaises(rd.ReaderError):
                self.forged(key, 0, 0)

    def test_rejects_bad_variable_name(self):
        def f(doc):
            doc['variables'][0] = ['l', [0, 1, 2]]
        with self.assertRaises(rd.ReaderError):
            read_mutated(f)


S1 = Path(__file__).resolve().parent / 'fixtures' / 's1a-c1.json'


class TestReaderShape1(unittest.TestCase):
    def mutated(self, f):
        doc = json.loads(S1.read_text())
        f(doc)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'cert.json'
            p.write_text(json.dumps(doc))
            return rd.read(p)

    def test_fixture_verifies(self):
        self.assertEqual(rd.read(S1)['verdict'], 'CASE_ROWS_INFEASIBLE_VERIFIED')

    def test_rejects_unit_weight_doubled_quartic(self):
        with self.assertRaises(rd.ReaderError):
            self.mutated(lambda doc: doc['case'].pop('doubled'))

    def test_rejects_wrong_doubled_quartic(self):
        with self.assertRaises(rd.ReaderError):
            self.mutated(lambda doc: doc['case'].update(doubled=[[1, 2, 3, 5]]))

    def test_rejects_flag_row_in_doubled_quartic(self):
        def f(doc):
            row = next(r for r in doc['rows'] if r['key'][0] == 'flag')
            row['key'][1] = doc['case']['doubled'][0][0]
        with self.assertRaises(rd.ReaderError):
            self.mutated(f)


if __name__ == '__main__':
    unittest.main()
