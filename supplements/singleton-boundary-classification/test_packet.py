"""Standalone positive, tamper, graph-lemma, and portability controls (MIT)."""
from copy import deepcopy
from itertools import combinations
from math import comb
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
import subprocess
import sys
import unittest

import numpy as np

from generate_catalog import make_catalog
from verify_catalog import VerificationError, check_batch, require_fourier_match, validate_catalog, verify_catalog

ROOT = Path(__file__).resolve().parent


class PacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = make_catalog()

    def test_complete_catalog_and_every_cube_and_fourier_entry(self):
        report = verify_catalog(self.catalog)
        self.assertEqual(report['forms_checked'], 30240)
        self.assertEqual(report['cube_values_checked'], 30240*1024)
        self.assertEqual(report['walsh_coefficients_checked'], 30240*1024)
        self.assertEqual(report['value_histogram'], {'-8': 967680, '0': 25159680, '8': 4838400})
        self.assertFalse(report['fourteen_variable_problem_solved'])

    def test_one_constructive_form(self):
        row = self.catalog['forms'][0]
        values = check_batch([row])
        unique, counts = np.unique(values, return_counts=True)
        self.assertEqual(dict(zip(map(int, unique), map(int, counts))), {-8: 32, 0: 832, 8: 160})
        self.assertEqual(int(values[0, 0]), 0)

    def test_omitted_catalog_form_is_rejected(self):
        changed = deepcopy(self.catalog)
        changed['forms'].pop()
        with self.assertRaises(VerificationError):
            validate_catalog(changed)

    def test_aliased_catalog_form_is_rejected(self):
        changed = deepcopy(self.catalog)
        changed['forms'][0] = changed['forms'][1]
        with self.assertRaises(VerificationError):
            validate_catalog(changed)

    def test_cycle_meeting_exceptional_pair_is_rejected(self):
        changed = deepcopy(self.catalog)
        changed['forms'][0]['cycle_edges'][0] = changed['forms'][0]['exceptional_pair']
        with self.assertRaises(VerificationError):
            validate_catalog(changed)

    def test_wrong_coefficient_constant_is_rejected(self):
        changed = deepcopy(self.catalog)
        changed['constant_coefficient'] = 2
        with self.assertRaises(VerificationError):
            validate_catalog(changed)

    def test_scope_promotion_is_rejected(self):
        for field in ['actual_boolean_function', 'fourteen_variable_problem_solved']:
            changed = deepcopy(self.catalog)
            changed[field] = True
            with self.assertRaises(VerificationError):
                validate_catalog(changed)

    def test_tampered_fourier_claim_is_rejected(self):
        values = check_batch([self.catalog['forms'][0]])
        coefficients = np.zeros((1, 1024), dtype=np.int32)
        coefficients[0, 0] = 2
        with self.assertRaises(VerificationError):
            require_fourier_match(values, coefficients)

    def test_even_four_and_five_edge_graph_lemmas(self):
        edges = [sum(1 << v for v in e) for e in combinations(range(8), 2)]
        for size, expected in [(4, comb(8, 4)*3), (5, comb(8, 5)*12)]:
            found = 0
            for graph in combinations(edges, size):
                odd = 0
                for edge in graph:
                    odd ^= edge
                if odd:
                    continue
                degrees = [sum(bool(edge & (1 << v)) for edge in graph) for v in range(8)]
                self.assertEqual(sum(d > 0 for d in degrees), size)
                self.assertEqual({d for d in degrees if d}, {2})
                found += 1
            self.assertEqual(found, expected)

    def test_bipartite_degree_obstruction(self):
        edges = [sum(1 << v for v in (a, b)) for a in [0, 1] for b in [2, 3]]
        for selected in range(16):
            graph = [e for i, e in enumerate(edges) if selected >> i & 1]
            degrees = [sum(bool(e & (1 << v)) for e in graph) for v in range(4)]
            self.assertNotEqual(degrees, [0, 0, 1, 1])

    def test_replay_from_unrelated_working_directory(self):
        env = dict(os.environ)
        env.pop('PYTHONPATH', None)
        with TemporaryDirectory() as directory:
            directory = Path(directory)
            data, report = directory/'catalog.json', directory/'report.json'
            subprocess.run([sys.executable, str(ROOT/'generate_catalog.py'), '--output', str(data)],
                           cwd=directory, env=env, check=True, capture_output=True)
            subprocess.run([sys.executable, str(ROOT/'verify_catalog.py'), str(data), '--output', str(report)],
                           cwd=directory, env=env, check=True, capture_output=True)
            self.assertEqual(json.loads(report.read_text())['forms_checked'], 30240)

    def test_optimized_cli_rejects_tampering_without_output(self):
        with TemporaryDirectory() as directory:
            directory = Path(directory)
            changed = deepcopy(self.catalog)
            changed['forms'].pop()
            source = directory/'bad.json'
            source.write_text(json.dumps(changed))
            for flag in ['-O', '-OO']:
                output = directory/(flag[1:]+'.json')
                result = subprocess.run([sys.executable, flag, str(ROOT/'verify_catalog.py'), str(source),
                    '--output', str(output)], cwd=directory, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
