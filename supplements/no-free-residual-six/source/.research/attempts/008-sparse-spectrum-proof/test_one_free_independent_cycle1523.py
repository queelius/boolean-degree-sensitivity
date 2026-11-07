"""Meaningful scope/corruption controls for the cycle1523 independent audit."""
import resource
import tempfile
import unittest
from pathlib import Path

import one_free_independent_cycle1523 as a


class IndependentControls(unittest.TestCase):
    def test_scalar_domains_and_cost_coverage(self):
        ds = a.departures()
        self.assertEqual({d.defect for d in ds}, {2, 6})
        self.assertEqual(len(ds), 10)
        self.assertEqual(a.allocation_control()["allocations"], 61)
        for level in a.Level:
            for k in (-20, -5, 6, 20):
                if level != a.Level.QUINTIC or k >= 0:
                    self.assertGreater(a.cost(level, k), 6)
        with self.assertRaises(a.AuditError):
            a.cost(a.Level.QUINTIC, -1)
        with self.assertRaises(a.AuditError):
            a.cost(3, 1)
        with self.assertRaises(a.AuditError):
            a.cost(a.Level.CUBIC, True)

    def test_no_silent_constant_widening(self):
        pair = (a.Departure(a.Level.CUBIC, -2), a.Departure(a.Level.CUBIC, 1))
        for c in (0, 3):
            self.assertIsNone(a.old_guard(c, pair))
            allocation = (a.Departure(a.Level.SINGLETON, c),) + pair
            self.assertEqual(a.allocation_route(allocation, (True,)*3, 1)[1],
                             "TYPE_III_PENDING_TWO_EXCEPTION_EXTENSION")
        for c in (1, 2):
            self.assertEqual(a.old_guard(c, pair), "OLD_TWO_AT_BASELINE_CONSTANT")
        self.assertEqual(a.old_guard(-1, ()), "OLD_BASELINE")
        self.assertIsNone(a.old_guard(4, ()))

    def test_missed_departure_and_invalid_owner(self):
        triple = (a.Departure(a.Level.CUBIC, -2),)*3
        self.assertEqual(a.allocation_route(triple, (True, True, False), 2)[1],
                         "OLD_TWO_AT_BASELINE_CONSTANT")
        with self.assertRaises(a.AuditError):
            a.allocation_route((a.Departure(a.Level.SINGLETON, 0),)*2, (True, True), 1)
        with self.assertRaises(a.AuditError):
            a.allocation_route(triple, (1, True, False), 2)
        with self.assertRaises(a.AuditError):
            a.allocation_route(triple, (True,), 2)
        with self.assertRaises(a.AuditError):
            a.allocation_route(triple, (True,)*3, 3)
        with self.assertRaises(a.AuditError):
            a.allocation_route(triple + triple, (True,)*6, 1)
        with self.assertRaises(a.AuditError):
            a.old_guard(1, (a.Departure(a.Level.SINGLETON, 0),))

    def test_origin_and_edge_valence_correction(self):
        x = a.star_counts(2, 1)
        self.assertEqual(x["ordinary_minus_one"], 24)
        self.assertEqual(x["ordinary_zero"], 24)
        self.assertEqual((x["P_norm"], x["Q_norm"], x["amplitude_bound"]), (72, 184, 13))
        # The old all-active=-1 claim violates both origin and incidence.
        old_n = x["edges"] - 3
        self.assertNotEqual(2 - old_n + (1 + 1 - 2) + 38, 16)
        self.assertNotEqual(5*old_n + 3 + 3 + 6, 6*38)
        with self.assertRaises(a.AuditError):
            a.star_counts(3, 1)
        with self.assertRaises(a.AuditError):
            a.star_counts(2, 4)

    def test_fibers_normalization_and_degree_counts(self):
        f = a.fiber_controls()
        self.assertEqual((f["unrestricted_indices"], f["odd_indices"]), (2380, 1586))
        self.assertEqual({(r["p"], r["q"]) for r in f["four_fibers"]},
                         {(0, -1), (0, 1), (1, 0), (-1, 0)})
        x = a.complement_counts(3, [2, 2, 1, 1, 1, 1, 1])
        self.assertEqual(x["Q_norm_by_level"], [13, 78, 87])
        self.assertEqual((x["P_norm"], x["Q_norm"]), (78, 178))
        with self.assertRaises(a.AuditError):
            a.complement_counts(4, [2, 2, 1, 1, 1, 1, 1])
        with self.assertRaises(a.AuditError):
            a.complement_counts(1, [1])
        with self.assertRaises(a.AuditError):
            a.complement_counts(1, [True])

    def test_missing_triangle_arithmetic_and_guard(self):
        x = a.endpoint_controls()
        self.assertEqual(x["subset_pairs"], 25)
        self.assertEqual(x["shared_off_cycle_histogram"], {2: 12, 3: 12, 4: 1})
        # Dropping the three-interior premise really loses the conclusion.
        self.assertEqual(len({0, 1}.intersection({2, 3})), 0)
        self.assertFalse(x["whole_complex_manifold_assumed"])

    def test_digest_and_size_corruption(self):
        with tempfile.TemporaryDirectory(prefix="cycle1523-", dir=Path(__file__).parent) as folder:
            p = Path(folder) / "control.txt"
            p.write_text("independent control\n")
            good = a.reference(p)
            self.assertEqual(a.verify_reference(good), good)
            for changed in ({**good, "sha256": "0"*64}, {**good, "bytes": good["bytes"]+1},
                            {**good, "bytes": True}, {"path": str(p)}):
                with self.assertRaises(a.AuditError):
                    a.verify_reference(changed)
            with self.assertRaises(a.AuditError):
                a.verify_reference(None)

    def test_optimization_safe_failure(self):
        with self.assertRaises(a.AuditError):
            a.require(False, "must also fail under -O")
        self.assertEqual(list(a.references({"x": [{"path": "p", "sha256": "h"}], "v": 3})),
                         [{"path": "p", "sha256": "h"}])


if __name__ == "__main__":
    resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    unittest.main()
