import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '015-sphere-catalog-audit'))
import spheres  # noqa: E402
import cases  # noqa: E402
import cover_reader as cr  # noqa: E402
import near_flag  # noqa: E402
import roots  # noqa: E402

CAT = json.loads((HERE / 'roots-catalog.json').read_text())['catalog']
DELTA = json.loads((HERE / 'deltahedra.json').read_text())['spheres']
SPH = spheres.enumerate_spheres(12)


class TestCatalogs(unittest.TestCase):
    def test_root_catalog_regenerates(self):
        self.assertEqual(roots.catalog(SPH), CAT)

    def test_accepted_counts(self):
        self.assertEqual([r['order'] for r in CAT['1,0']], [9, 10, 11])
        self.assertEqual([r['order'] for r in CAT['0,1']], [7])
        self.assertEqual([r['order'] for r in CAT['1,1']], [8, 9])
        self.assertEqual(len(CAT['2,0']), 9)

    def test_deltahedra(self):
        self.assertEqual([d['order'] for d in DELTA], [6, 7, 8, 9, 10, 12])
        for d in DELTA:
            self.assertTrue(near_flag.classify([frozenset(f) for f in d['faces']])['flag'])

    def test_near_flag_types(self):
        got = json.loads((HERE / 'near-flag-result.json').read_text())['near_flag_types']
        self.assertEqual(sorted(map(tuple, got)), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)])


class TestCover(unittest.TestCase):
    def test_main_cover_passes(self):
        cover = json.loads((HERE / 'cover-cases.json').read_text())
        rows = cr.read(cover, CAT)
        self.assertEqual(sum(r['cases'] for r in rows), 2775)
        self.assertEqual(len(rows), 22)

    def test_special_covers_pass(self):
        for name, n in (('triangle-cover.json', 81), ('shape1-cover.json', 328)):
            rows = cr.read(json.loads((HERE / name).read_text()), CAT, DELTA)
            self.assertEqual(rows[0]['cases'], n)

    def test_dropped_case_is_caught(self):
        cover = json.loads((HERE / 'cover-cases.json').read_text())
        cover = dict(cover, shapes=[s for s in cover['shapes'] if s['graph'] == 'P4' and s['signs'] == '---'])
        cover['shapes'][0] = copy.deepcopy(cover['shapes'][0])
        cover['shapes'][0]['cases'].pop(17)
        with self.assertRaises(cr.CoverError):
            cr.read(cover, CAT)

    def test_wrong_doubled_is_caught(self):
        cover = json.loads((HERE / 'shape1-cover.json').read_text())
        cover['shapes'][0]['cases'][0]['doubled'] = [[1, 2, 3, 5]]
        with self.assertRaises(cr.CoverError):
            cr.read(cover, CAT, DELTA)

    def test_negative_root_index_is_caught(self):
        cover = json.loads((HERE / 'cover-cases.json').read_text())
        shape = copy.deepcopy(next(s for s in cover['shapes'] if s['graph'] == 'star' and s['signs'] == '---'))
        bad = copy.deepcopy(shape['cases'][0])
        bad['root_index'] = -1
        bad['faces'] = CAT['3,0'][-1]['faces']
        bad['order'] = CAT['3,0'][-1]['order']
        shape['cases'].append(bad)
        with self.assertRaises(cr.CoverError):
            cr.read(dict(cover, shapes=[shape]), CAT)

    def test_regenerated_cover_matches(self):
        self.assertEqual(cases.cover(CAT), json.loads((HERE / 'cover-cases.json').read_text()))

    def test_automorphisms_two_methods(self):
        for key in ('2,0', '3,0', '0,2'):
            for r in CAT[key]:
                a = {tuple(sorted(m.items())) for m in cases.automorphisms(r['faces'])}
                b = {tuple(sorted(m.items())) for m in cr.auts(r['faces'])}
                self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
