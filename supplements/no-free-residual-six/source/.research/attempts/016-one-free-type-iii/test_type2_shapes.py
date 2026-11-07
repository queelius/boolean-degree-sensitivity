import itertools
import unittest
from collections import Counter

import type2_shapes as t2

DOC = t2.main()


def brute_pair_classes():
    """Pair-only classes by minimising over all relabellings of six vertices."""
    pairs = list(itertools.combinations(range(6), 2))
    perms = list(itertools.permutations(range(6)))
    classes = set()
    for trio in itertools.combinations(pairs, 3):
        for signs in itertools.product(('-2', '+1'), repeat=3):
            classes.add(min(tuple(sorted((s, tuple(sorted((p[a], p[b])))) for s, (a, b) in zip(signs, trio)))
                            for p in perms))
    return Counter('/'.join(f'{k}x{n}' for k, n in sorted(Counter(s for s, _ in c).items())) for c in classes)


class TestTypeIIShapes(unittest.TestCase):
    def test_pair_only_counts_match_brute_force(self):
        got = {r['kinds']: r['classes'] for r in DOC['rows'] if 'Q2' not in r['kinds']}
        self.assertEqual(got, dict(brute_pair_classes()))
        self.assertEqual(sum(got.values()), 24)

    def test_totals(self):
        self.assertEqual(DOC['classes'], 136)
        open_ = sum(r['classes'] for r in DOC['rows'] if r['status'] == 'OPEN')
        self.assertEqual(open_, 31)
        self.assertEqual(len(DOC['open_with_doubled_quartic']), 7)

    def test_private_vertex_filter(self):
        q = frozenset({0, 1, 2, 3})
        self.assertTrue(t2.private_quartic([('Q2', q), ('-2', frozenset({0, 1})), ('+1', frozenset({2, 4}))]))
        self.assertFalse(t2.private_quartic([('Q2', q), ('-2', frozenset({0, 1})), ('+1', frozenset({2, 3}))]))
        self.assertFalse(t2.private_quartic([('-2', frozenset({0, 1})), ('-2', frozenset({1, 2})),
                                             ('+1', frozenset({5, 6}))]))

    def test_invalid_same_pair_rejected(self):
        self.assertFalse(t2.valid([('-2', frozenset({0, 1})), ('+1', frozenset({0, 1})), ('Q2', frozenset({0, 1, 2, 3}))]))


if __name__ == '__main__':
    unittest.main()
