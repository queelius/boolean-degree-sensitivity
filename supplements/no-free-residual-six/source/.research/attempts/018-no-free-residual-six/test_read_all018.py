"""Assembly controls for read_all018: each must turn a covered obligation into a missing one or a
failed status. Uses the fixtures in temporary copies; certs/ is never touched."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import read_all018 as ra

HERE = Path(__file__).resolve().parent
FX = HERE / 'fixtures'
B = json.loads((FX / 'cap-1.json').read_text())
COVER = json.loads((HERE / 'l1-cover.json').read_text())['rows']
FRONTIER = json.loads((HERE / 'no-free-frontier.json').read_text())
PASS = dict(status='L1_COVER_READER_PASS'), dict(status='NO_FREE_FRONTIER_READER_PASS')


def verified(doc):
    """ra.one on a temporary copy of the certificate doc."""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'c.json'
        p.write_text(json.dumps(doc))
        r = ra.one(p)
        r['written_sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
        return r


def mutated(f):
    doc = copy.deepcopy(B)
    f(doc)
    return doc


# the cover case B was built for, and B claimed for both magnitudes of its own type
CASE = next(c for c in COVER if ra.placement(c) == ra.placement(B['case']) and c['type'] == B['case']['type'])
BOTH = mutated(lambda d: d.update(variants=[[d['case']['type'], m] for m in (1, 2)]))


class TestAssembly(unittest.TestCase):
    def test_fixture_covers_its_case_at_both_m(self):
        r = verified(BOTH)
        self.assertEqual(r['verdict'], 'CASE_ROWS_INFEASIBLE_VERIFIED')
        self.assertEqual(r['sha256'], r['written_sha256'])
        self.assertEqual(ra.missing([r], [CASE]), [])

    def test_bound_case_is_the_checked_one(self):
        r = verified(BOTH)
        self.assertEqual(r['case'], BOTH['case'])

    def test_no_provider_means_missing(self):
        self.assertEqual(ra.missing([], [CASE]), [dict(case=0, m=1), dict(case=0, m=2)])

    def test_only_one_m_leaves_the_other_missing(self):
        r = verified(B)
        self.assertEqual(ra.missing([r], [CASE]), [dict(case=0, m=3 - B['magnitude'])])

    def test_rejected_certificate_covers_nothing(self):
        r = verified(mutated(lambda d: d.update(variants=[['pp', 1], [d['case']['type'], d['magnitude']]])))
        self.assertEqual(r['verdict'], 'REJECTED')
        self.assertEqual(len(ra.missing([r], [CASE])), 2)

    def test_forged_root_covers_nothing(self):
        r = verified(mutated(lambda d: d['case'].update(root={'kind': 'forged-catalog', 'index': 999999})))
        # the reader may accept rows that ignore the root, but assembly must not bind it to CASE
        self.assertEqual(len(ra.missing([r], [CASE])), 2)

    def test_tampered_proof_is_rejected(self):
        r = verified(mutated(lambda d: d['proof'].update(sha256='0' * 64)))
        self.assertEqual(r['verdict'], 'REJECTED')

    def test_status_requires_every_condition(self):
        cov, fr = PASS
        self.assertEqual(ra.status([], [], cov, fr, True), 'ALL_L1_CASES_VERIFIED')
        self.assertEqual(ra.status([dict(case=0, m=1)], [], cov, fr, True), 'INCOMPLETE')
        self.assertEqual(ra.status([], [dict(verdict='REJECTED')], cov, fr, True), 'INCOMPLETE')
        self.assertEqual(ra.status([], [], dict(status='REJECTED'), fr, True), 'INCOMPLETE')
        self.assertEqual(ra.status([], [], cov, dict(status='REJECTED'), True), 'INCOMPLETE')
        self.assertEqual(ra.status([], [], cov, fr, False), 'INCOMPLETE')


class TestTargets(unittest.TestCase):
    def test_real_frontier_has_exactly_the_targets(self):
        fr, found, exact = ra.targets(FRONTIER)
        self.assertEqual(fr['status'], 'NO_FREE_FRONTIER_READER_PASS')
        self.assertTrue(exact)
        self.assertEqual(sorted(found), sorted(ra.TARGETS))

    def test_dropped_target_fails(self):
        doc = copy.deepcopy(FRONTIER)
        doc['rows'] = [r for r in doc['rows'] if r['negative_magnitudes'] != [2, 2, 2, 2]]
        fr, found, exact = ra.targets(doc)
        self.assertFalse(exact)
        self.assertNotEqual(fr['status'], 'NO_FREE_FRONTIER_READER_PASS')

    def test_duplicated_target_fails(self):
        doc = copy.deepcopy(FRONTIER)
        doc['rows'] = doc['rows'] + [next(r for r in doc['rows'] if r['negative_magnitudes'] == [2, 2, 2, 2])]
        self.assertFalse(ra.targets(doc)[2])


if __name__ == '__main__':
    unittest.main()
