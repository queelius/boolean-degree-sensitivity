import itertools
import random
import sys
import unittest

sys.dont_write_bytecode = True
import audit
import spheres


def F(*ts):
    return frozenset(frozenset(t) for t in ts)


# 7-vertex torus (Moebius): closed surface, Euler characteristic 0.
TORUS7 = F(*[(i % 7, (i + 1) % 7, (i + 3) % 7) for i in range(7)],
           *[(i % 7, (i + 2) % 7, (i + 3) % 7) for i in range(7)])
# q=1 fixture from 1414/1424: cone from 6 over the 6-cycle, plus 012,025,235,345.
Q1 = F(*[(6, i, (i + 1) % 6) for i in range(6)], (0, 1, 2), (0, 2, 5), (2, 3, 5), (3, 4, 5))


class Spheres(unittest.TestCase):
    def test_small_counts(self):
        self.assertEqual({n: len(v) for n, v in spheres.enumerate_spheres(9).items()},
                         {n: audit.OEIS_A000109[n] for n in range(4, 10)})

    def test_rejects_non_spheres(self):
        self.assertTrue(spheres.is_sphere(spheres.K4))
        self.assertFalse(spheres.is_sphere(TORUS7))
        two = spheres.K4 | frozenset(frozenset(x + 4 for x in f) for f in spheres.K4)
        self.assertFalse(spheres.is_sphere(two))                  # disconnected
        self.assertFalse(spheres.is_sphere(spheres.K4 - {frozenset({0, 1, 2})}))  # boundary
        pinch = F((0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 3),
                  (0, 4, 5), (0, 5, 6), (0, 6, 4), (4, 5, 6))
        self.assertFalse(spheres.is_sphere(pinch))                # two cones glued at 0

    def test_every_split_is_a_sphere(self):
        rng = random.Random(1)
        layer = list(spheres.enumerate_spheres(8)[8].values())
        for faces in rng.sample(layer, 5):
            for g in spheres.splits(faces):
                self.assertTrue(spheres.is_sphere(g))
                self.assertEqual(len(g), 2 * len(spheres.vertices(g)) - 4)

    def test_certificate_is_relabel_invariant_and_separating(self):
        faces = next(iter(spheres.enumerate_spheres(9)[9].values()))
        perm = list(range(9))
        random.Random(2).shuffle(perm)
        moved = frozenset(frozenset(perm[x] for x in f) for f in faces)
        self.assertEqual(spheres.certificate(faces), spheres.certificate(moved))
        certs = {spheres.certificate(f) for f in spheres.enumerate_spheres(9)[9].values()}
        self.assertEqual(len(certs), 50)


class Guards(unittest.TestCase):
    def test_q1_fixture_survives(self):
        self.assertTrue(spheres.is_sphere(Q1))
        self.assertEqual(audit.first_failed_guard(Q1), (None, (0, 2)))

    def test_degree_and_special_guards(self):
        octa = F(*[(a, b, c) for a in (0, 1) for b in (2, 3) for c in (4, 5)])
        self.assertEqual(audit.first_failed_guard(octa)[0], 'special_vertex_count')  # all degree 4
        stacked = spheres.K4
        for k in range(4, 10):   # repeatedly stack on a face containing 0: degree of 0 grows
            f = next(f for f in sorted(stacked, key=sorted) if 0 in f)
            stacked = (stacked - {f}) | {frozenset(e) | {k} for e in itertools.combinations(f, 2)}
        self.assertEqual(audit.first_failed_guard(stacked)[0], 'degree_support')

    def test_euler_range_direct(self):
        self.assertEqual(audit.induced_euler_range(spheres.K4), (0, 2))
        # stack all four faces of K4: the four new vertices are independent, chi = 4
        stacked = frozenset(frozenset(e) | {4 + k} for k, f in enumerate(sorted(spheres.K4, key=sorted))
                            for e in itertools.combinations(f, 2))
        self.assertTrue(spheres.is_sphere(stacked))
        self.assertEqual(audit.induced_euler_range(stacked)[1], 4)


    def test_native_euler_witness_rejected(self):
        # 1424 witness (11, 761): passes degree and special guards, fails [-1, 3]
        import json, os
        path = os.path.join(os.path.dirname(audit.HERE), '006-solver-resume', 'sphere-triangulations-11.json')
        rec = json.load(open(path))['classes'][761]
        guard, rng = audit.first_failed_guard(spheres.from_masks(rec['face_masks']))
        self.assertEqual(guard, 'induced_euler_interval')
        self.assertEqual(rng[1], 4)


class Catalog(unittest.TestCase):
    def setUp(self):
        self.layer = spheres.enumerate_spheres(8)[8]
        self.classes = [dict(index=k, face_masks=sorted(sum(1 << x for x in f) for f in faces))
                        for k, faces in enumerate(self.layer.values())]

    def test_genuine_catalog_accepted(self):
        self.assertEqual(len(audit.check_catalog(8, self.classes, self.layer)), 14)

    def test_relabelled_duplicate_rejected(self):
        faces = spheres.from_masks(self.classes[3]['face_masks'])
        perm = [7, 6, 5, 4, 3, 2, 1, 0]
        dup = sorted(sum(1 << perm[x] for x in f) for f in faces)
        bad = self.classes[:-1] + [dict(index=13, face_masks=dup)]
        with self.assertRaisesRegex(spheres.AuditError, 'duplicate'):
            audit.check_catalog(8, bad, self.layer)

    def test_missing_class_rejected(self):
        with self.assertRaisesRegex(spheres.AuditError, 'missing'):
            audit.check_catalog(8, self.classes[:-1], self.layer)

    def test_non_sphere_record_rejected(self):
        bad = [dict(c) for c in self.classes]
        bad[0]['face_masks'] = bad[0]['face_masks'][:-1] + [bad[0]['face_masks'][0] ^ 0b11000000 or 1]
        with self.assertRaises(spheres.AuditError):
            audit.check_catalog(8, bad, self.layer)


if __name__ == '__main__':
    unittest.main()
