"""Portable exact controls; use explicit unittest checks under normal/-O Python."""
from itertools import combinations
from pathlib import Path
import copy
import json
import tempfile
import unittest

import controls as r
import verify_packet as v

ROOT = Path(__file__).resolve().parent


class PacketTests(unittest.TestCase):
    def test_exact_cost_types_allocations_and_aliases(self):
        self.assertEqual(len(r.allocations()), 61)
        self.assertEqual({s: sum(sum(t.cost for t in a) == s for a in r.allocations())
                          for s in (0, 2, 4, 6)}, {0: 1, 2: 5, 4: 15, 6: 40})
        with self.assertRaises(ValueError):
            r.validate_allocation_cover(r.allocations()[:-1])
        with self.assertRaises(ValueError):
            r.validate_allocation_cover(r.allocations() + r.allocations()[:1])
        with self.assertRaises(ValueError):
            r.route((r.ExceptionType(1, 0, 2), r.ExceptionType(1, 3, 2)), (1, 1))
        with self.assertRaises(ValueError):
            r.route((r.ExceptionType(3, -2, 2),), (15,))

    def test_complete_incidence_and_expected_data_tampers(self):
        actual = r.incidence_cover()
        self.assertEqual(actual['incidence_cases'], 54411)
        self.assertEqual(actual['impossible_full_support_aliases_discarded'], 1784)
        self.assertEqual(actual['route_counts'], {'OLD_LOCAL_BASELINE_CONSTANT': 54409,
                         'THREE_DOUBLES_PRIVATE_TIP': 1, 'TRIPLED_QUARTIC': 1})
        expected = json.loads((ROOT / 'data/expected-controls.json').read_text())
        v.check_expected_incidence(actual, expected['incidence'])
        for mutate in (lambda d: d['allocation_rows'].pop(),
                       lambda d: d.__setitem__('incidence_cases', 54410),
                       lambda d: d['allocation_rows'].__setitem__(1, d['allocation_rows'][0])):
            changed = copy.deepcopy(expected['incidence']); mutate(changed)
            with self.assertRaises(ValueError):
                v.check_expected_incidence(actual, changed)

    def test_old_local_guards_are_assumptions_and_not_extended(self):
        t = r.ExceptionType(3, -2, 2)
        for c in (0, 3, -1, 4):
            with self.assertRaises(ValueError):
                r.old_local_guard(c, (t, t))
        self.assertEqual(r.old_local_guard(1, (t, t)), 'TWO_QUADRATICS')
        self.assertEqual(r.old_local_guard(2, ()), 'BASELINE')
        for constant, exceptions in ((None, ()), (1, (t, t, t)),
                                     (1, (r.ExceptionType(1, 0, 2),))):
            with self.assertRaises(ValueError):
                r.old_local_guard(constant, exceptions)

    def test_heavy_paths_and_essential_link_guards(self):
        result = r.tripled_link_control()
        self.assertEqual((result['tested_links'], result['valid_links']), (1590, 60))
        self.assertEqual(r.triangle_completion_control()['even_completions'], 0)
        self.assertEqual(r.quartic_forcing_control()['labelled_cases'], 2520)
        self.assertNotIn(3, r.baseline_link_sizes())
        self.assertEqual(4 * 1 - 1, 3)  # +1 quadratic invalidates this step.
        self.assertTrue(r.even_degrees([(0, 1), (0, 2), (2, 3), (1, 3)],
                                     [3, 1, 1, 1], 4))  # Size six evades bound five.
        with self.assertRaises(ValueError):
            r.even_degrees([(0, 1), (0, 1)], [3, 1], 2)
        with self.assertRaises(ValueError):
            r.even_degrees([(0, 0)], [1], 2)

    def test_private_tip_locality_and_tampers(self):
        ds = [(0, 1, 2, 3), (0, 1, 2, 4), (0, 1, 2, 5)]
        self.assertEqual(r.private_tip(ds, [(4, 5)], 3), ds[0])
        for doubles, pairs, tip in ((ds, [], 0), (ds, [(3, 4)], 3),
                                    (ds + [ds[0]], [], 3), ([], [], 3)):
            with self.assertRaises(ValueError):
                r.private_tip(doubles, pairs, tip)

    def test_surface_positive_negative_and_pinched_controls(self):
        result = r.surface_control()
        self.assertEqual((result['degree_sequence_graphs'], result['eight_face_candidates'],
                          result['closed_surfaces']), (20, 900, 0))
        octahedron = [t for t in combinations(range(6), 3)
                      if all(not ({a, b} <= set(t)) for a, b in ((0, 1), (2, 3), (4, 5)))]
        rp2 = [(0, 1, 2), (0, 1, 3), (0, 2, 4), (0, 3, 5), (0, 4, 5),
               (1, 2, 5), (1, 3, 4), (1, 4, 5), (2, 3, 4), (2, 3, 5)]
        self.assertTrue(r.closed_surface(octahedron)); self.assertTrue(r.closed_surface(rp2))
        union = list(combinations(range(6, 10), 3)) + rp2
        self.assertTrue(r.closed_surface(union))
        self.assertEqual(r.surface_summary(union)['euler_characteristic'], 3)
        self.assertEqual(r.surface_summary(union)['degree_counts'], {3: 4, 5: 6})
        self.assertFalse(r.closed_surface(octahedron[:-1]))
        pinched = list(combinations((0, 1, 2, 3), 3)) + list(combinations((0, 4, 5, 6), 3))
        self.assertFalse(r.closed_surface(pinched))
        with self.assertRaises(ValueError):
            r.closed_surface(rp2 + [rp2[0]])

    def test_exact_normalization_and_shared_cost_countercontrol(self):
        self.assertEqual(r.normalization_control(), {'character_derivative_cases': 2560,
                         'ordinary_quadratic_cases': 20,
                         'quadratic_and_cubic_inversion_basis_cases': 30})
        supports = ({0, 1, 2}, {0, 1, 3}, {0, 2, 3})
        self.assertGreaterEqual(min(sum(v in s for s in supports) for v in range(4)), 2)
        self.assertEqual(2 * len(supports), 6)  # Shared cost is six, not eight.

    def test_claim_scope_and_dependency_omission_rejected(self):
        claims = json.loads((ROOT / 'CLAIMS.json').read_text())
        v.check_claims(claims)
        for mutate in (lambda d: d.__setitem__('global_goal_complete', True),
                       lambda d: d['claims'][2].__setitem__('conditional_on_inherited_theorems', False),
                       lambda d: d['claims'][2].__setitem__('depends_on', ['TRIPLED', 'PRIVATE_TIP']),
                       lambda d: d.__setitem__('new_version_doi', '10.5281/zenodo.23539867')):
            changed = copy.deepcopy(claims); mutate(changed)
            with self.assertRaises(ValueError):
                v.check_claims(changed)

    def test_manifest_rejects_omission_digest_and_path_tampers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / 'x').write_bytes(b'valid')
            manifest = v.make_manifest(root, ['x'])
            v.check_manifest(root, manifest)
            for mutate in (lambda d: d['files'].pop(),
                           lambda d: d['files'].append(copy.deepcopy(d['files'][0])),
                           lambda d: d['files'][0].__setitem__('path', '../x'),
                           lambda d: d['files'][0].__setitem__('sha256', '0' * 64)):
                changed = copy.deepcopy(manifest); mutate(changed)
                with self.assertRaises(ValueError):
                    v.check_manifest(root, changed)
            (root / 'alias').symlink_to(root / 'x')
            with self.assertRaises(ValueError):
                v.safe_file(root, 'alias')
            (root / 'alias').unlink()
            (root / 'x').write_bytes(b'tampered')
            with self.assertRaises(ValueError):
                v.check_manifest(root, manifest)


if __name__ == '__main__':
    unittest.main()
