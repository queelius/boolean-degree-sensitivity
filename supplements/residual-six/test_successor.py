"""Successor contracts: mathematical scope, lifecycle separation, pure kernels."""
from pathlib import Path
import copy
import json
import subprocess
import sys
import tempfile
import unittest

import verify_packet as v
from kernels import endpoint, core, disk

ROOT = Path(__file__).resolve().parent


class SuccessorTests(unittest.TestCase):
    def test_math_dag_requires_baseline_le3_and_inherited_premises(self):
        claims = json.loads((ROOT / 'CLAIMS.json').read_text())
        v.check_claims(claims)
        self.assertIn('UNION12', {row['id'] for row in claims['claims']})
        inherited = {row['id']: row for row in claims['assumptions']}
        self.assertEqual(inherited['BASELINE_LE3']['constant_upper_bound'], 3)
        self.assertEqual(inherited['OLD_LOCAL_012']['constants'], [1, 2])
        for removed in ('BASELINE_LE3', 'OLD_LOCAL_012'):
            changed = copy.deepcopy(claims)
            changed['assumptions'] = [a for a in changed['assumptions'] if a['id'] != removed]
            with self.assertRaises(ValueError):
                v.check_claims(changed)
        changed = copy.deepcopy(claims)
        next(c for c in changed['claims'] if c['id'] == 'UNION12')['full_dependency_closure_bundled'] = True
        with self.assertRaises(ValueError):
            v.check_claims(changed)

    def test_staging_reserved_published_metadata_do_not_change_math(self):
        claims = json.loads((ROOT / 'CLAIMS.json').read_text())
        original = copy.deepcopy(claims)
        plan = json.loads((ROOT / 'PUBLICATION-PLAN.json').read_text())
        cff = json.loads((ROOT / 'CITATION.cff').read_text())
        v.check_publication(plan, cff); v.check_claims(claims)
        reserved, citation = copy.deepcopy(plan), copy.deepcopy(cff)
        reserved['state'] = 'DOI_RESERVED'
        reserved['archive'].update(doi='10.5281/zenodo.99999999', reserved_on=plan['prepared_on'],
                                   reservation_evidence='https://example.org/test-fixture/reservation')
        citation['doi'] = reserved['archive']['doi']
        citation['message'] = 'Hypothetical reserved metadata fixture; not a real reservation.'
        v.check_publication(reserved, citation); v.check_claims(claims)
        published = copy.deepcopy(reserved)
        published['state'] = 'PUBLISHED'
        published['archive'].update(published_on=plan['prepared_on'],
                                    publication_evidence='https://example.org/test-fixture/publication')
        published['source_disclosure'] = {'commit': 'a' * 40,
                                         'url': plan['canonical_source'] + '/tree/' + 'a' * 40,
                                         'observed_on': plan['prepared_on'],
                                         'evidence': 'https://example.org/test-fixture/source'}
        v.check_publication(published, citation); v.check_claims(claims)
        self.assertEqual(claims, original)

    def test_false_archival_identifiers_dates_and_citation_mismatch_rejected(self):
        plan = json.loads((ROOT / 'PUBLICATION-PLAN.json').read_text())
        citation = json.loads((ROOT / 'CITATION.cff').read_text())
        changed = copy.deepcopy(plan); changed['archive']['published_on'] = plan['prepared_on']
        with self.assertRaises(ValueError):
            v.check_publication(changed, citation)
        for forbidden in (plan['concept_doi'], plan['predecessor_version_doi']):
            changed, cff = copy.deepcopy(plan), copy.deepcopy(citation)
            changed['state'] = 'DOI_RESERVED'
            changed['archive'].update(doi=forbidden, reserved_on=plan['prepared_on'],
                                       reservation_evidence='https://example.org/test-fixture')
            cff['doi'] = forbidden
            with self.assertRaises(ValueError):
                v.check_publication(changed, cff)
        changed = copy.deepcopy(citation); changed['version'] = '1.3.0'
        with self.assertRaises(ValueError):
            v.check_publication(plan, changed)
        changed = copy.deepcopy(plan); changed['source_disclosure']['observed_on'] = '2020-01-01'
        with self.assertRaises(ValueError):
            v.check_publication(changed, citation)

    def test_retained_kernel_definitions_have_exact_normalized_ast(self):
        checked = v.check_kernel_sources(ROOT)
        self.assertGreaterEqual(checked['sources'], 3)
        self.assertGreater(checked['definitions'], 20)
        self.assertEqual(v.definition_signatures('def f(x):\n return x+1\n', []),
                         v.definition_signatures('def f(x): return x + 1\n', []))
        self.assertNotEqual(v.definition_signatures('def f(x): return x+1\n', []),
                            v.definition_signatures('def f(x): return x-1\n', []))

    def test_endpoint_pure_functions_and_preserved_original_cli_policy(self):
        result = endpoint.run_controls()
        self.assertEqual(result['pentagon']['target_degree_sequence_count'], 0)
        self.assertEqual(result['heptagon']['triangulations'], 42)
        figure8 = ((0, 1), (0, 2), (0, 3), (0, 5), (1, 2), (3, 4), (4, 5))
        with self.assertRaises(ValueError):
            endpoint.cycle_components(figure8)
        with self.assertRaises(ValueError):
            endpoint.supports(((0, 1, True),), 3)
        provenance = json.loads((ROOT / 'PROVENANCE.json').read_text())
        original = ROOT / next(r['original_path'] for r in provenance['kernel_sources']
                               if r['kernel_path'] == 'kernels/endpoint.py')
        with tempfile.TemporaryDirectory() as directory:
            for flag in ('-O', '-OO'):
                target = Path(directory) / (flag + '.json')
                done = subprocess.run([sys.executable, '-S', flag, str(original), '--output', str(target)],
                                      capture_output=True, text=True)
                self.assertNotEqual(done.returncode, 0)
                self.assertIn('normal Python', done.stderr)
                self.assertFalse(target.exists())

    def test_disk_guards_omissions_and_noninvolution(self):
        values = disk.control_disks()
        self.assertTrue(all(not row['all_target_guards'] for row in values.values()))
        with self.assertRaises(ValueError):
            disk.require_target_guards(values['cone_I1'])
        faces = disk.fan(list(range(7)), 7)
        for wrong in (faces[:-1], faces + [faces[0]], [True] + faces[1:]):
            with self.assertRaises(ValueError):
                disk.profile(list(range(7)), [7], wrong)
        permutation = [1, 2, 3, 4, 5, 6, 0, 7]
        image = disk.transport(faces, permutation)
        self.assertNotEqual(permutation, disk.inverse(permutation))
        self.assertEqual(disk.transport(image, disk.inverse(permutation)), faces)
        self.assertEqual(disk.ear_controls()['rooted_base_checks'], 414)

    def test_complete_new_payload_and_omission_rejection(self):
        expected = json.loads((ROOT / 'data/expected-new-controls.json').read_text())
        actual = v.new_mathematical_controls()
        v.check_new_expected(actual, expected)
        changed = copy.deepcopy(expected); changed['core']['blocks']['offcycle_words'].pop()
        with self.assertRaises(ValueError):
            v.check_new_expected(actual, changed)
        self.assertEqual(actual['core']['offcycle_combinations']['four_offcycle_combinations'], 1296)
        self.assertEqual(actual['disk']['ears']['rooted_base_checks'], 414)


if __name__ == '__main__':
    unittest.main()
