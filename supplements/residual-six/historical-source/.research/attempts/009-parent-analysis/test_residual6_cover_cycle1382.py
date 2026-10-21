import unittest
from itertools import product
try:import residual6_type_cover_cycle1382 as r
except ModuleNotFoundError:r=None
class ResidualSixTests(unittest.TestCase):
 def setUp(self):self.assertIsNotNone(r)
 def test_exact_residual_types_and_complete_small_allocations(self):
  types=r.exception_types();self.assertEqual(len(types),10);self.assertEqual(sorted(t.value for t in types if t.level==r.Level.SINGLETON and t.cost==6),[-1,4]);self.assertEqual(sorted(t.value for t in types if t.level==r.Level.CUBIC and t.cost==6),[-3,2]);self.assertEqual([t.value for t in types if t.level==r.Level.QUINTIC and t.cost==6],[3])
  allocations=r.allocations();self.assertEqual(len(allocations),61);self.assertEqual(sum(sum(t.cost for t in a)==6 for a in allocations),40)
  brute={tuple(sorted(types[i] for i in row if i>=0)) for row in product(range(-1,len(types)),repeat=3) if sum(types[i].cost for i in row if i>=0)<=6};self.assertEqual(set(allocations),brute)
 def test_tripled_weight_link_paths_and_forbidden_triangle(self):
  report=r.tripled_quartic_controls();self.assertEqual(report['heavy_edge3_even_size4_count'],0);self.assertEqual(report['heavy_edge3_even_size5_count'],4);self.assertEqual(report['unit_triangle_allowed_completion_count'],0);self.assertEqual(report['middle_partition_assignments'],203);self.assertEqual(report['compatible_middle_partitions'],1)
 def test_old_constant_and_coefficient_guards_remain_strict(self):
  q=r.Exception(r.Level.CUBIC,-2);b=r.Exception(r.Level.QUINTIC,2)
  self.assertTrue(r.local_status(3,(q,),None).startswith('COVERED'))
  self.assertEqual(r.local_status(3,(q,q),0),'UNSUPPORTED_CONSTANT_GUARD')
  self.assertEqual(r.local_status(4,(),None),'UNSUPPORTED_CONSTANT_GUARD')
  self.assertTrue(r.local_status(1,(q,b),None).startswith('COVERED'))
  self.assertTrue(r.local_status(1,(r.Exception(r.Level.QUINTIC,3),),None).startswith('NEW_'))
  with self.assertRaises(ValueError):r.local_status(1,(q,q),2)
  with self.assertRaises(ValueError):r.defect(r.Level.CUBIC,True)
 def test_private_tips_and_no_duplicate_supports(self):
  report=r.private_tip_control();self.assertEqual(report['global_shared_core'],15);self.assertEqual(report['tip_count'],3);self.assertTrue(report['each_tip_incident_to_exactly_one_doubled_quartic'])
  with self.assertRaises(ValueError):r.private_tip_maps(15,[31,31,79])
 def test_shared_tetrahedron_faces_refute_independent_charging(self):
  report=r.shared_incidence_control();self.assertEqual(report['exception_count'],3);self.assertEqual(report['shared_defect_cost'],6);self.assertEqual(sorted(report['incidences']),[2,2,2,3])
 def test_every_allocation_has_explicit_coupled_reason(self):
  report=r.coupled_cover();self.assertEqual(len(report),61);self.assertTrue(all(x['F0_size']==4 and x['status']=='PROPOSED_COMPLETE_COUPLED_ALLOCATION' for x in report));self.assertEqual(sum(x['reason']=='SHARED_FOUR_PRIVATE_TIP_EXTRACTION' for x in report),1)
 def test_surface_private_curvature_controls(self):
  self.assertEqual(r.private_surface_control()['sphere_degree_cases'],[[0,3],[1,1]])
if __name__=='__main__':unittest.main()
