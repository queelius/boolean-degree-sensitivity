import copy
import json
from pathlib import Path
import tempfile
import unittest

import make_positive_tip_inventory_cycle1511 as source


class SourceTests(unittest.TestCase):
    def test_changed_source_and_size_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'input.json'; p.write_text('{"value":7}')
            ref = source.pin(p)
            self.assertEqual(source.pinned(ref), {'value': 7})
            bad = dict(ref, bytes=ref['bytes']+1)
            with self.assertRaises(ValueError): source.pinned(bad)
            p.write_text('{"value":8}')
            with self.assertRaises(ValueError): source.pinned(ref)

    def test_no_closed_or_aliased_pilot(self):
        wanted = dict(order=8, original_index=3, constant=1)
        context = dict(model_id=dict(native_identity=dict(order=8, original_index=3),constant=1),
                       genuine_context_status='OPEN',skip_future_queries=False)
        self.assertIs(source.select_pilot([context], wanted), context)
        for records in [[], [context,context],
                        [dict(context,genuine_context_status='EXCLUDED',skip_future_queries=True)]]:
            with self.assertRaises(ValueError): source.select_pilot(records,wanted)


if __name__ == '__main__':
    unittest.main()
