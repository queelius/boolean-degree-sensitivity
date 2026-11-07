"""Controls for make_acceptance_1534: the successor ledger may change only the two target patterns,
and the assembly gate refuses anything short of a clean, current pass. Writes only to temp dirs."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

import make_acceptance_1534 as mk

OLD = json.loads(mk.L1388.read_text())
NEW = mk.ledger(OLD, mk.H / 'no-free-residual6-acceptance-cycle1534.json')


def pattern(doc, mags):
    return next(p for p in doc['empty_pair']['patterns'] if p['negative_magnitudes'] == mags)


class TestSuccessor(unittest.TestCase):
    def test_real_successor_passes(self):
        s = mk.check_successor(OLD, NEW)
        self.assertEqual((s['open_before'], s['open_after']), (29, 27))
        for t in mk.TARGETS:
            self.assertEqual(pattern(NEW, t)['status'], 'excluded')
            self.assertEqual(pattern(NEW, t)['partial_reductions'], pattern(OLD, t)['partial_reductions'])

    def bad(self, f):
        new = copy.deepcopy(NEW)
        f(new)
        with self.assertRaises(SystemExit):
            mk.check_successor(OLD, new)

    def test_other_pattern_changed(self):
        self.bad(lambda d: pattern(d, [3, 2, 1, 1, 1, 1, 1]).update(status='excluded'))

    def test_target_detail_changed(self):
        self.bad(lambda d: pattern(d, [2, 2, 2, 2]).update(remaining_defect=5))

    def test_one_edge_changed(self):
        self.bad(lambda d: d['one_edge'].update(open_count=1))

    def test_pattern_dropped(self):
        self.bad(lambda d: d['empty_pair']['patterns'].pop())

    def test_open_count_wrong(self):
        self.bad(lambda d: d['empty_pair'].update(open_count=28))

    def test_target_not_excluded(self):
        self.bad(lambda d: pattern(d, [2, 2, 2, 2, 1]).update(status='open'))


class TestAssemblyGate(unittest.TestCase):
    def gate(self, **change):
        dep = Path(mk.__file__)
        doc = dict(status='ALL_L1_CASES_VERIFIED', rejected=[], missing_count=0, targets_exact=True,
                   target_inventories=[list(t) for t in mk.TARGETS], certificates=1,
                   dependencies=[mk.pin(dep)])
        doc.update(change)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'ra.json'
            p.write_text(json.dumps(doc))
            return mk.assembly(p)

    def test_clean_pass_accepted(self):
        self.assertEqual(self.gate()['status'], 'ALL_L1_CASES_VERIFIED')

    def test_refusals(self):
        for change in (dict(status='INCOMPLETE'), dict(rejected=[{}]), dict(missing_count=1),
                       dict(targets_exact=False), dict(target_inventories=[[2, 2, 2, 2]]),
                       dict(dependencies=[dict(path=mk.__file__, sha256='0' * 64)])):
            with self.subTest(change=list(change)), self.assertRaises(SystemExit):
                self.gate(**change)


if __name__ == '__main__':
    unittest.main()
