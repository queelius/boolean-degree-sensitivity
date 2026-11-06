import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '015-sphere-catalog-audit'))
import spheres  # noqa: E402
import surfaces  # noqa: E402
import vertex_types as vt  # noqa: E402

SPH = spheres.enumerate_spheres(12)
RP2 = {n: surfaces.brute(n, 1) for n in range(6, 10)}
CTYPES = vt.component_types(SPH, RP2)
RESULT = vt.classify(CTYPES)


def orders(t):
    return sorted({cf[0][1] for cf in RESULT[t] if len(cf) == 1 and cf[0][0] == 2})


class TestSurfaces(unittest.TestCase):
    def test_sphere_brute_matches_015(self):
        for n in range(4, 10):
            self.assertEqual(set(surfaces.brute(n, 2)), {surfaces.certificate(f) for f in SPH[n].values()}, n)

    def test_rp2_routes_agree_and_census(self):
        split = surfaces.rp2(9)
        self.assertEqual({n: len(v) for n, v in split.items()}, {6: 1, 7: 3, 8: 16, 9: 134})
        for n in range(6, 10):
            self.assertEqual(set(split[n]), set(RP2[n]), n)

    def test_rejects_non_surface(self):
        bowtie = frozenset(map(frozenset, [(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 3),
                                           (0, 4, 5), (0, 5, 6), (0, 6, 4), (4, 5, 6)]))
        self.assertFalse(surfaces.is_closed_surface(bowtie))


class TestVertexTypes(unittest.TestCase):
    def test_accepted_two_exception_catalogs(self):
        self.assertEqual(orders((1, 0, 0)), [9, 10, 11])   # one -2 (C6): 9, 10, 11
        self.assertEqual(orders((0, 0, 1)), [7])           # one +1: the (7,2) sphere
        self.assertEqual(orders((1, 0, 1)), [8, 9])        # adjacent -2,+1 at the common vertex
        self.assertEqual(RESULT[(0, 1, 0)], [])            # lone split excluded (one-six-edge)
        self.assertEqual(RESULT[(0, 0, 3)], [])            # three-+1 star (016)

    def test_splits_only_in_pairs(self):
        with_split = {t for t, found in RESULT.items() if t[1] and found}
        self.assertEqual(with_split, {(0, 2, 0), (1, 2, 0)})

    def test_unsplit_links_are_single_spheres(self):
        for t, found in RESULT.items():
            if t[1] == 0:
                self.assertTrue(all(len(cf) == 1 and cf[0][0] == 2 for cf in found), t)

    def test_realizable_controls(self):
        k6 = (1, 6, 0, 0, 0)
        self.assertFalse(vt.realizable([k6, k6], 0, 0, 1))
        faces = frozenset(map(frozenset, [(0, 1, 2), (0, 2, 3), (0, 3, 1), (4, 1, 2), (4, 2, 3), (4, 3, 1)]))
        self.assertEqual(vt.max_internal_pairs(vt.adjacency(faces), [0, 4]), 0)  # apices share neighbours
        bipyramid = (2, 5, 0, 2, 0)
        self.assertTrue(vt.realizable([bipyramid], 0, 0, 2))
        self.assertTrue(vt.realizable([bipyramid, bipyramid], 0, 2, 0))
        self.assertFalse(vt.realizable([bipyramid], 0, 1, 0))


if __name__ == '__main__':
    unittest.main()
