import unittest

import step4_count as s4

ORDERS = s4.allowed_orders()
SHAPES = s4.shapes()


def survivors(**kw):
    return [(g, sg, c) for g, sg, e, sn, v in SHAPES for c in (1, 2) if s4.feasible(g, sg, e, v, ORDERS, c, **kw)]


class TestStep4(unittest.TestCase):
    def test_twenty_three_shapes(self):
        self.assertEqual(len(SHAPES), 23)
        self.assertNotIn(('star', '+++'), [(g, sg) for g, sg, *_ in SHAPES])

    def test_no_survivor(self):
        self.assertEqual(survivors(), [])

    def test_rules_are_load_bearing(self):
        self.assertEqual(len(survivors(universal=False)), 32)
        self.assertEqual(survivors(zero_rule=False), [('P4', '+++', 2)])

    def test_larger_cross_budget_survives(self):
        # with M = 7 + c replaced by a large budget the search is not vacuous
        g, sg, e, sn, v = next(x for x in SHAPES if x[:2] == ('3K2', '+++'))
        self.assertIsNotNone(s4.feasible(g, sg, e, v, ORDERS, 5))

    def test_triangle_minus_ignores_catalog(self):
        g, sg, e, sn, v = next(x for x in SHAPES if x[:2] == ('triangle', '---'))
        for signs in (sg, sn):
            opts = s4.cross_options(g, signs, e, v, {})
            self.assertTrue(all(o[0] == [2, 3, 4, 5, 6] for o in opts.values()))

    def test_cross_options(self):
        g, sg, e, sn, v = next(x for x in SHAPES if x[:2] == ('3K2', '+++'))
        opts = s4.cross_options(g, sn, e, v, ORDERS)
        self.assertTrue(all(o[0] == [1] for o in opts.values()))  # lone +1 endpoint: order 7


if __name__ == '__main__':
    unittest.main()
