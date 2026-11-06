import unittest

import vertex_type_screen as vts

OUT = vts.main()


class TestVertexTypeScreen(unittest.TestCase):
    def test_only_three_plus_ones_is_empty(self):
        empty = [k for k, v in OUT.items() if not v]
        self.assertEqual(empty, ['minus2=0,plus1=3'])

    def test_known_single_exception_orders(self):
        # One -2: the accepted one-six-edge orders 9..11; one +1: the (7,2) sphere;
        # adjacent -2,+1: the accepted mixed root orders 8, 9.
        self.assertEqual(OUT['minus2=1,plus1=0'], {9: 1, 10: 1, 11: 1})
        self.assertEqual(OUT['minus2=0,plus1=1'], {7: 1})
        self.assertEqual(OUT['minus2=1,plus1=1'], {8: 1, 9: 1})


if __name__ == '__main__':
    unittest.main()
