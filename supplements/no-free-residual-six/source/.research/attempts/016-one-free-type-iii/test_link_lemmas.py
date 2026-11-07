import unittest

import link_lemmas as ll
from spheres import AuditError, enumerate_spheres

CAT = enumerate_spheres(8)


def bipyramid(n):
    """Faces of the bipyramid over an n-cycle 0..n-1 with poles n, n+1."""
    return frozenset(frozenset((i, (i + 1) % n, p)) for i in range(n) for p in (n, n + 1))


class TestLinkLemmas(unittest.TestCase):
    def test_main_reports_the_single_degree_45_classes(self):
        out = ll.main()
        self.assertEqual(out['classes_with_degrees_4_5'], {7: 1, 8: 1})
        self.assertEqual(out['lemma8_min_edges_to_link_of_w'], 7)

    def test_pentagonal_bipyramid_is_the_degree_45_seven_sphere(self):
        self.assertEqual(ll.lemma7([bipyramid(5)]), 2)
        only = [f for f in CAT[7].values() if ll.degree_45(ll.adjacency(f))]
        self.assertEqual(len(only), 1)
        self.assertEqual(sorted(len(n) for n in ll.adjacency(only[0]).values()), [4] * 5 + [5] * 2)

    def test_degree_filter_rejects_other_spheres(self):
        self.assertFalse(ll.degree_45(ll.adjacency(bipyramid(6))))
        self.assertEqual(ll.lemma7([bipyramid(6)]), 0)

    def test_lemma8_bound_is_tight_at_seven(self):
        ll.lemma8(CAT[8].values(), need=7)
        with self.assertRaises(AuditError):
            ll.lemma8(CAT[8].values(), need=8)

    def test_lemma7_detects_a_violation(self):
        # Not a sphere: a degree-4/5 graph (edges given as 2-element faces) where
        # the outsider 6 misses neighbour 3 of the degree-5 vertex 0.
        adj = {0: {1, 2, 3, 4, 5}, 1: {0, 2, 5, 6}, 2: {0, 1, 3, 6}, 3: {0, 2, 4, 5}, 4: {0, 3, 5, 6},
               5: {0, 1, 3, 4, 6}, 6: {1, 2, 4, 5}}
        faces = frozenset(frozenset((a, b)) for a in adj for b in adj[a])
        self.assertTrue(ll.degree_45(ll.adjacency(faces)))
        with self.assertRaises(AuditError):
            ll.lemma7([faces])

    def test_lemma8_detects_a_violation(self):
        adj = {0: {1, 2, 3, 4, 5}, 1: {0, 2, 5, 6}, 2: {0, 1, 3, 7}, 3: {0, 2, 4, 7}, 4: {0, 3, 5, 6},
               5: {0, 1, 4, 6, 7}, 6: {1, 4, 5, 7}, 7: {2, 3, 5, 6}}
        faces = frozenset(frozenset((a, b)) for a in adj for b in adj[a])
        self.assertTrue(ll.degree_45(ll.adjacency(faces)))
        _, rest, m = ll.outside(ll.adjacency(faces), 0)
        self.assertEqual((rest, m), ({6, 7}, 6))
        with self.assertRaises(AuditError):
            ll.lemma8([faces], need=7)


if __name__ == '__main__':
    unittest.main()
