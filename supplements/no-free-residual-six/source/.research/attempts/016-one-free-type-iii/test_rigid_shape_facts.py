import unittest

import rigid_shape_facts as rsf
from spheres import AuditError, enumerate_spheres


class TestRigidShapeFacts(unittest.TestCase):
    def test_facts_on_full_enumeration(self):
        out = rsf.main()
        self.assertEqual(out['s6_orders'], {7: 1})

    def test_s6_rejects_a_missing_order(self):
        # Restricting to spheres up to 6 vertices removes the unique S6 sphere.
        with self.assertRaises(AuditError):
            rsf.facts({n: c for n, c in enumerate_spheres(6).items()})


if __name__ == '__main__':
    unittest.main()
