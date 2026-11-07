import copy
import json
import unittest
from pathlib import Path

import frontier_reader as fr
import make_frontier as mf

HERE = Path(__file__).resolve().parent
DOC = json.loads((HERE / 'no-free-frontier.json').read_text())


class TestFrontier(unittest.TestCase):
    def test_passes(self):
        self.assertEqual(fr.read(DOC)['open'], 22)

    def test_multisets_independent(self):
        self.assertEqual(len(fr.multisets(22, 28)), 39)
        self.assertIn((2, 2, 2, 2), fr.multisets(22, 28))      # cost 24, r = 4
        self.assertNotIn((2, 2, 2), fr.multisets(22, 28))      # cost 18, r = 10

    def bad(self, f):
        d = copy.deepcopy(DOC)
        f(d)
        with self.assertRaises(fr.ReaderError):
            fr.read(d)

    def test_rejects_dropped_row(self):
        self.bad(lambda d: (d['rows'].pop(), d.update(open_rows=21)))

    def test_rejects_wrong_cost(self):
        self.bad(lambda d: d['rows'][0].update(negative_cost=d['rows'][0]['negative_cost'] + 2))

    def test_rejects_wrong_basis(self):
        def f(d):
            r = next(r for r in d['rows'] if r['remaining_defect'] == 6)
            r['union_14_basis']['kind'] = 'RESIDUAL_FOUR_SUPPORT_CONSTRAINTS'
        self.bad(f)

    def test_rejects_bad_pin(self):
        self.bad(lambda d: d['ledger'].update(sha256='0' * 64))


if __name__ == '__main__':
    unittest.main()
