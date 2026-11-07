import unittest
from positive_inventory_reader_cycle1512 import native_order,derive,transport,exact
ROOTLINK=[50,76,104,112,140,146,162,168,196,208]
def context():return {'n':13,'root':0,'root_link':ROOTLINK,'model_id':{'constant':1,'native_identity':{'catalog_sha256':'fixture','order':7,'original_index':0}}}
class Tests(unittest.TestCase):
 def test_known_root7_and_all13_degree_slots(self):
  rows=derive(native_order(13),context());self.assertEqual([r['opposite_triangle_mask'] for r in rows],[176,200]);self.assertEqual([r['edge_mask'] for r in rows],[3,5])
  for r in rows:
   self.assertEqual(r['degree_row']['lower'],7);self.assertEqual(r['degree_row']['upper'],12);self.assertEqual(len(r['degree_row']['terms']),12);self.assertTrue(all(m.bit_count()==2 and c==1 for m,c in r['degree_row']['terms']));self.assertTrue(all(m&r['tip_mask'] for m,c in r['degree_row']['terms']));self.assertTrue(any(m&(1<<12) for m,c in r['degree_row']['terms']))
 def test_structured_relabel(self):
  old=context();permutation=list(range(13));permutation[0],permutation[9]=9,0;permutation[2],permutation[12]=12,2
  new=context();new['root']=permutation[old['root']];new['root_link']=[transport(x,permutation) for x in old['root_link']]
  expected=derive(native_order(13),old);actual=derive(native_order(13),new)
  self.assertEqual({r['opposite_triangle_mask'] for r in actual},{transport(r['opposite_triangle_mask'],permutation) for r in expected})
  self.assertEqual({r['edge_mask'] for r in actual},{transport(r['edge_mask'],permutation) for r in expected})
  self.assertEqual({tuple(sorted((m,c) for m,c in r['degree_row']['terms'])) for r in actual},{tuple(sorted((transport(m,permutation),c) for m,c in r['degree_row']['terms'])) for r in expected})
 def test_incomplete_cycle(self):
  c=context();c['root_link']=[(1<<1)|(1<<2)|(1<<3),(1<<1)|(1<<2)|(1<<4)];c['model_id']['native_identity']['order']=4
  with self.assertRaises(ValueError):derive(native_order(13),c)
 def test_alias_scope_and_bool_guards(self):
  for kind in ('duplicate','rootface','boolroot','wrongorder'):
   c=context();variables=native_order(13)
   if kind=='duplicate':c['root_link']=ROOTLINK+[ROOTLINK[0]]
   elif kind=='rootface':c['root_link']=[7]+ROOTLINK
   elif kind=='boolroot':c['root']=False
   else:variables=variables[::-1]
   with self.assertRaises(ValueError):derive(variables,c)
 def test_no_degree_three_vertices_gives_no_rows(self):
  import itertools
  c=context();c['model_id']['native_identity']['order']=6;c['root_link']=[sum(1<<v for v in t) for t in itertools.product((1,2),(3,4),(5,6))]
  self.assertEqual(derive(native_order(13),c),[])
 def test_strict_rows_reject_boolean_alias_or_omitted_degree_slot(self):
  row=derive(native_order(13),context())[0]['degree_row'];wrong=dict(row,terms=row['terms'][:-1]);self.assertFalse(exact(row,wrong));self.assertFalse(exact({'terms':[[3,True]]},{'terms':[[3,1]]}));self.assertFalse(exact([],{}));self.assertTrue(exact({'lower':7},{'lower':7}));self.assertFalse(exact({'lower':7},{'upper':7}))
 def test_bad_transport(self):
  for permutation in ([0,0,2], [False,1,2]):
   with self.assertRaises(ValueError):transport(3,permutation)
if __name__=='__main__':unittest.main()
