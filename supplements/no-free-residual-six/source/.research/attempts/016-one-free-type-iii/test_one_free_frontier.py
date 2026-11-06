import copy
import json
import tempfile
import unittest
from pathlib import Path

import one_free_frontier as producer
import one_free_frontier_reader as reader

DOC = producer.frontier()


class TestFrontier(unittest.TestCase):
    def test_reader_passes(self):
        r = reader.read(DOC)
        self.assertEqual((r['classes'], r['open']), (136, 24))
        self.assertEqual(r['by_reason'], {'NEEDS_THREE_EXCEPTION_MODEL': 24, 'PRIVATE_VERTEX_DOUBLED_QUARTIC': 105,
                                          'RIGID_SHAPE_LOCAL_ARGUMENT': 6, 'THREE_PLUS_ONE_STAR': 1})

    def test_reader_universe_is_independent(self):
        self.assertEqual(len(reader.classes()), 136)
        pair_only = [k for k in reader.classes() if 'Q2' not in k[0]]
        self.assertEqual(len(pair_only), 24)

    def test_open_rows(self):
        rows = [r for r in DOC['type_ii_classes'] if r['status'] == 'OPEN']
        with_q2 = [r for r in rows if any(k == 'Q2' for k, _ in r['departures'])]
        self.assertEqual(len(with_q2), 1)
        self.assertEqual(with_q2[0]['rigid_label'], 1)

    def mutated(self, f):
        doc = copy.deepcopy(DOC)
        f(doc)
        with self.assertRaises(reader.ReaderError):
            reader.read(doc)

    def test_rejects_flipped_status(self):
        def f(doc):
            row = next(r for r in doc['type_ii_classes'] if r['status'] == 'OPEN')
            row.update(status='EXCLUDED', reason='THREE_PLUS_ONE_STAR', basis='star')
        self.mutated(f)

    def test_rejects_dropped_class(self):
        self.mutated(lambda doc: doc['type_ii_classes'].pop())

    def test_rejects_duplicate_class(self):
        self.mutated(lambda doc: doc['type_ii_classes'].append(doc['type_ii_classes'][0]))

    def test_rejects_bad_pin(self):
        self.mutated(lambda doc: doc['types'][1]['note'].update(sha256='0' * 64))

    def test_rejects_wrong_counts(self):
        self.mutated(lambda doc: doc['types'][2].update(open_shape_classes=23))

    def test_rejects_closed_type_ii(self):
        self.mutated(lambda doc: doc['types'][2].update(status='EXCLUDED'))

    def test_cli_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'f.json'
            producer.main(['--out', str(out)])
            r = reader.main([str(out)])
            self.assertEqual(r['status'], 'ONE_FREE_FRONTIER_READER_PASS')
            self.assertEqual(json.loads(out.read_text())['types'][2]['open_shape_classes'], 24)


if __name__ == '__main__':
    unittest.main()
