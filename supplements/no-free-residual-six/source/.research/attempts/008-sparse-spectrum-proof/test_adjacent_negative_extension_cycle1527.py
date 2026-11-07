"""Tiny controls written before the cycle1527 retained-row reader."""
import copy
from itertools import combinations, product
import resource
import signal
import unittest

import adjacent_negative_extension_cycle1527 as a


ROOT_LINK = {
    "order": 8, "index": 12,
    "face_masks": [67, 76, 82, 88, 97, 100, 131, 140, 146, 152, 161, 164],
    "degree_vector": [4, 4, 4, 4, 4, 4, 6, 6],
    "exceptional_vertices": [6, 7],
}


def row(terms, low, high, reason="root_link"):
    return {"terms": sorted([v, c] for v, c in terms.items()),
            "lower": low, "upper": high, "reason": reason}


class TinyControls(unittest.TestCase):
    def test_exact_intervals_against_all_assignments(self):
        r = row({3: -2, 5: 1, 6: 3}, -5, 5)
        for fixed_values in product((None, 0, 1), repeat=3):
            fixed = {v: x for v, x in zip((3, 5, 6), fixed_values) if x is not None}
            values = [sum(c*x for (v, c), x in zip(r["terms"], bits))
                      for bits in product((0, 1), repeat=3)
                      if all(bits[(3, 5, 6).index(v)] == x for v, x in fixed.items())]
            self.assertEqual(a.interval(r, fixed), (min(values), max(values)))

    def test_valid_opposite_value_and_final_contradiction(self):
        rows = [row({3: 1}, 1, 1), row({3: 1}, 0, 0)]
        proof = [{"variable": 3, "value": 1, "row": 0}]
        result = a.replay(rows, proof, 1)
        self.assertEqual(result["deductions"], 1)
        self.assertEqual(result["final_interval"], [1, 1])
        for corrupted in ([{"variable": 3, "value": 0, "row": 0}],
                          proof + proof,
                          [{"variable": 5, "value": 1, "row": 0}],
                          [{"variable": 3, "value": True, "row": 0}]):
            with self.assertRaises(a.AuditError):
                a.replay(rows, corrupted, 1)
        with self.assertRaises(a.AuditError):
            a.replay(rows, proof, 0)

    def test_literal_root_and_bad_metadata(self):
        checked = a.check_root(ROOT_LINK)
        self.assertEqual(checked["private_vertices"], [7, 8])
        corrupted = copy.deepcopy(ROOT_LINK)
        corrupted["degree_vector"][0] = 5
        with self.assertRaises(a.AuditError):
            a.check_root(corrupted)
        corrupted = copy.deepcopy(ROOT_LINK)
        corrupted["face_masks"].pop()
        with self.assertRaises(a.AuditError):
            a.check_root(corrupted)

    def test_semantic_cofaces_and_global_count_rejection(self):
        e = (1 << 1) | (1 << 2)
        tets = {e | (1 << u) | (1 << v): 1
                for u, v in combinations([x for x in range(13) if x not in (1, 2)], 2)}
        r = row({**tets, e: -4}, 0, 1, "ordinary_edge_four_or_five")
        a.recognize(r, ROOT_LINK)
        corrupt = copy.deepcopy(r)
        corrupt["terms"] = [[v, -5 if c == -4 else c] for v, c in r["terms"]]
        with self.assertRaises(a.AuditError):
            a.recognize(corrupt, ROOT_LINK)
        with self.assertRaises(a.AuditError):
            a.recognize(row({3: 1}, 49, 49, "face_count"), ROOT_LINK)
        # A common-endpoint flag row must not inherit ordinary/private flagness.
        q = sum(1 << i for i in (0, 1, 2, 3))
        flags = {q ^ (1 << i): 1 for i in (1, 2, 3)}
        with self.assertRaises(a.AuditError):
            a.recognize(row({**flags, q: -1}, -1, 2, "ordinary_vertex_link_flag"), ROOT_LINK)

    def test_schema_and_optimization_safe_failure(self):
        for bad in (row({True: 1}, 0, 1), row({3: True}, 0, 1), row({3: 1}, True, 1),
                    {"terms": [[3, 1], [3, 1]], "lower": 0, "upper": 2, "reason": "root_link"}):
            with self.assertRaises(a.AuditError):
                a.validate_row(bad)
        with self.assertRaises(a.AuditError):
            a.require(False, "must fail under -O")

    def test_cross_degree_price_and_limit_guard(self):
        answer = a.cross_degree_controls()
        self.assertEqual(answer["minimum_if_nine_good_at_least_two"], 11)
        self.assertEqual(answer["universal_neighbor_minimum"], 11)
        self.assertEqual(answer["cross_upper_by_constant"], [7, 8, 9, 10])
        # Merely changing the old upper bound to 11 would lose both contradictions.
        self.assertFalse(11 < answer["minimum_if_nine_good_at_least_two"])

    def test_complete_case_binding_rejects_omission_and_alias(self):
        cases = [{"link": ROOT_LINK}]
        self.assertTrue(a.check_cover(cases, [ROOT_LINK]))
        for corrupt in ([], cases+cases):
            with self.assertRaises(a.AuditError):
                a.check_cover(corrupt, [ROOT_LINK])
        changed = copy.deepcopy(cases)
        changed[0]["link"]["face_masks"][0] = 7
        with self.assertRaises(a.AuditError):
            a.check_cover(changed, [ROOT_LINK])
        with self.assertRaises(a.AuditError):
            a.check_cover(cases, [ROOT_LINK, ROOT_LINK])
        self.assertFalse(a.connected({}))


if __name__ == "__main__":
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    signal.alarm(15)
    unittest.main()
