import unittest

import one_seven_spheres as oss
from spheres import enumerate_spheres

CAT = enumerate_spheres(10)


def bipyramid(n):
    return frozenset(frozenset((i, (i + 1) % n, p)) for i in range(n) for p in (n, n + 1))


def stack(faces, face, new):
    """Insert a new vertex inside `face`."""
    a, b, c = sorted(face)
    return (faces - {face}) | {frozenset((a, b, new)), frozenset((b, c, new)), frozenset((a, c, new))}


class TestOneSeven(unittest.TestCase):
    def test_pattern_recognizes_a_constructed_sphere(self):
        # Heptagonal bipyramid: poles have degree 7, so the pattern (one 7) fails.
        self.assertFalse(oss.has_pattern(bipyramid(7)))
        # Stack a vertex on a face of the pentagonal bipyramid: degrees 3,5,5,5,4,4,4,6.
        f = stack(bipyramid(5), frozenset((0, 1, 5)), 7)
        self.assertEqual(sorted(oss.degrees(f).values()), [3, 4, 4, 4, 5, 5, 5, 6])
        self.assertFalse(oss.has_pattern(f, allowed=(3, 4, 5)))

    def test_pattern_accepts_a_synthetic_match(self):
        # Not a sphere: a graph (edges as 2-element faces) with one degree-7 hub
        # over a 7-vertex circulant of degree 4, so every other degree is 5.
        edges = {frozenset((0, i)) for i in range(1, 8)}
        edges |= {frozenset((1 + i, 1 + (i + d) % 7)) for i in range(7) for d in (1, 2)}
        self.assertTrue(oss.has_pattern(frozenset(edges)))
        self.assertFalse(oss.has_pattern(frozenset(edges), allowed=(4,)))

    def test_relaxed_control_finds_spheres(self):
        self.assertGreater(sum(oss.count(CAT[n].values(), allowed=(3, 4, 5)) for n in CAT), 0)
        hit = next(f for n in CAT for f in CAT[n].values() if oss.has_pattern(f, allowed=(3, 4, 5)))
        self.assertIn(3, oss.degrees(hit).values())
        self.assertFalse(oss.has_pattern(hit))

    def test_main(self):
        out = oss.main()
        self.assertEqual(set(out['enumerated'].values()) | set(out['catalog_006'].values()), {0})
        self.assertEqual(out['relaxed_control_with_degree_3'][8], 1)


if __name__ == '__main__':
    unittest.main()
