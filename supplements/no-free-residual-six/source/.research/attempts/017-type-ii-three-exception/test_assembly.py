import json
import unittest
from pathlib import Path

import read_all

HERE = Path(__file__).resolve().parent


class TestAssembly(unittest.TestCase):
    def test_canon_uses_every_field(self):
        case = json.loads((HERE / 'shape1-cover.json').read_text())['shapes'][0]['cases'][0]
        other = dict(case, root_kind='exceptional')
        self.assertNotEqual(read_all.canon(case), read_all.canon(other))
        self.assertNotEqual(read_all.canon(case), read_all.canon(dict(case, doubled=[[1, 2, 3, 5]])))

    def test_canon_normalizes_order(self):
        case = json.loads((HERE / 'shape1-cover.json').read_text())['shapes'][0]['cases'][0]
        shuffled = dict(case, doubled=[list(reversed(case['doubled'][0]))],
                        exceptions=list(reversed(case['exceptions'])), faces=list(reversed(case['faces'])))
        self.assertEqual(read_all.canon(case), read_all.canon(shuffled))

    def test_universe_binding(self):
        covers = ['cover-cases.json', 'triangle-cover.json', 'shape1-cover.json']
        shapes = [s for cv in covers for s in json.loads((HERE / cv).read_text())['shapes']]
        self.assertTrue(read_all.bind_universe(shapes))
        self.assertFalse(read_all.bind_universe(shapes[1:]))
        self.assertFalse(read_all.bind_universe(shapes + shapes[:1]))
        self.assertFalse(read_all.bind_universe([]))


if __name__ == '__main__':
    unittest.main()
