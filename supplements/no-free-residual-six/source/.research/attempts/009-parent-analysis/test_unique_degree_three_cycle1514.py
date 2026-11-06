import itertools,unittest
import unique_degree_three_controls_cycle1514 as c
class TinySphereControls(unittest.TestCase):
 def test_octahedron_single_stack_positive(self):
  octa=c.octahedron();base=c.check_sphere(6,octa);self.assertEqual(base['degrees'],[4]*6)
  face=octa[0];stacked=c.stack(octa,face,6);report=c.check_sphere(7,stacked);self.assertEqual(sorted(report['degrees']),[3,4,4,4,5,5,5]);self.assertEqual(report['degrees'][6],3)
  A=[i for i in range(6) if face>>i&1];self.assertTrue(all(report['degrees'][i]==5 for i in A));self.assertEqual(c.unstack(stacked,6),octa)
 def test_uniqueness_and_max_degree_guards(self):
  octa=c.octahedron();f=octa[0];opposite=((1<<6)-1)^f;twice=c.stack(c.stack(octa,f,6),opposite,7);r=c.check_sphere(8,twice);self.assertEqual(r['degrees'].count(3),2);self.assertLessEqual(max(r['degrees']),5)
  pent=[(1<<a)|(1<<(2+i))|(1<<(2+(i+1)%5)) for a in [0,1] for i in range(5)];larger=c.stack(pent,pent[0],7);r=c.check_sphere(8,larger);self.assertEqual(r['degrees'].count(3),1);self.assertEqual(max(r['degrees']),6)
 def test_patch_counts_and_no_positive_interior_count(self):
  octa=c.octahedron();missing=octa[0];patch=[t for t in octa if t!=missing];s=c.summary(patch);self.assertEqual(s['f_vector'],[6,12,7]);self.assertEqual(s['Euler'],1);self.assertEqual(s['boundary_edges'],[missing^(1<<i) for i in range(6) if missing>>i&1][::-1])
  feasible=[]
  for m in range(13):
   for bi in range(4):
    ii=3*m-bi;cap=m*(m-1)//2 if m<3 else 3*m-6
    if 0<=ii<=cap and 2*ii+bi>=4*m:feasible.append((m,bi,ii))
  self.assertEqual(feasible,[(0,0,0)])
 def test_alias_omission_and_noninvolutive_transport(self):
  o=c.octahedron()
  for n,t in [(True,o),(6,o+[o[0]]),(6,o[:-1]),(6,[True]+o[1:])]:
   with self.assertRaises(ValueError):c.check_sphere(n,t)
  p=[1,2,3,4,5,0];t=[sum(1<<p[i] for i in range(6) if f>>i&1) for f in o];self.assertEqual(c.check_sphere(6,t)['degrees'],[4]*6)
if __name__=='__main__':unittest.main()
