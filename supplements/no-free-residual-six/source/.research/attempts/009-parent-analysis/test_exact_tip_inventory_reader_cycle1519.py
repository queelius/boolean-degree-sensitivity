import unittest
from itertools import combinations
from positive_inventory_reader_cycle1512 import native_order,transport
from exact_tip_inventory_reader_cycle1519 import derive_rows,evaluate
ROOTLINK=[50,76,104,112,140,146,162,168,196,208]
def context():return {'n':13,'root':0,'root_link':ROOTLINK,'model_id':{'constant':1,'native_identity':{'catalog_sha256':'fixture','order':7,'original_index':0}}}
class Tests(unittest.TestCase):
 def test_exact_rows_shared_pair_and_all_physical_slots(self):
  d=derive_rows(native_order(13),context());self.assertEqual(len(d['positive_tips']),2);self.assertEqual(len(d['negative_tips']),1);self.assertEqual(len(d['added_rows']),134);self.assertEqual(sum(len(r['terms']) for r in d['added_rows']),2504)
  shared=[(r,p) for r,p in zip(d['added_rows'],d['origins']) if r['key']['subject']==6 and r['key']['family']=='POSITIVE_TIP_OTHER_EDGE_VALENCE'];self.assertEqual(len(shared),1);row,origins=shared[0];self.assertEqual(len(origins),2);self.assertEqual(row['terms'][0],[6,-4]);self.assertEqual(len(row['terms']),56);self.assertEqual({p['vertex'] for p in origins},{1,2})
  degrees=[r for r in d['added_rows'] if r['key']['family']=='POSITIVE_TIP_EXACT_DEGREE'];self.assertEqual(len(degrees),2);self.assertTrue(all(len(r['terms'])==12 and r['lower']==r['upper']==7 for r in degrees))
  neg=[r for r in d['added_rows'] if r['key']['family']=='NEGATIVE_TIP_DEGREE_INTERVAL'];self.assertEqual(len(neg),1);self.assertEqual((neg[0]['lower'],neg[0]['upper'],len(neg[0]['terms'])),(9,11,12))
 def test_conditional_row_includes_absent_edge_zero(self):
  d=derive_rows(native_order(13),context());r=next(r for r in d['added_rows'] if r['key']['family']=='POSITIVE_TIP_OTHER_EDGE_VALENCE');pair=r['key']['subject'];tets=[m for m,c in r['terms'] if m.bit_count()==4]
  self.assertTrue(evaluate(r,{}));self.assertFalse(evaluate(r,{tets[0]:1}));self.assertTrue(evaluate(r,{pair:1,**{m:1 for m in tets[:4]}}));self.assertFalse(evaluate(r,{pair:1,**{m:1 for m in tets[:5]}}))
 def test_exact_degree_and_fixed_five_reject_weakening(self):
  rows=derive_rows(native_order(13),context())['added_rows'];d=next(r for r in rows if r['key']['family']=='POSITIVE_TIP_EXACT_DEGREE');ms=[m for m,c in d['terms']];self.assertTrue(evaluate(d,{m:1 for m in ms[:7]}));self.assertFalse(evaluate(d,{m:1 for m in ms[:8]}))
  r=next(r for r in rows if r['key']['family']=='POSITIVE_TIP_A_EDGE_VALENCE');ts=[m for m,c in r['terms']];self.assertEqual(len(ts),55);self.assertTrue(evaluate(r,{m:1 for m in ts[:5]}));self.assertFalse(evaluate(r,{m:1 for m in ts[:4]}))
 def test_relabel_preserves_native_semantics(self):
  p=list(range(13));p[0],p[10]=10,0;p[1],p[11]=11,1;c=context();new=context();new['root']=p[0];new['root_link']=[transport(t,p) for t in ROOTLINK]
  a=derive_rows(native_order(13),c)['added_rows'];b=derive_rows(native_order(13),new)['added_rows'];canonical=lambda r:(tuple(sorted((m,v) for m,v in r['terms'])),r['lower'],r['upper'])
  self.assertEqual({canonical(dict(r,terms=[[transport(m,p),v] for m,v in r['terms']])) for r in a},{canonical(r) for r in b})
 def test_negative_only_then_ordinary_complement(self):
  c=context();c['model_id']['native_identity']['order']=8;c['root_link']=[(1<<apex)|(1<<(3+i))|(1<<(3+(i+1)%6)) for apex in (1,2) for i in range(6)]
  d=derive_rows(native_order(13),c);self.assertEqual(d['positive_tips'],[]);self.assertEqual(len(d['negative_tips']),2);self.assertEqual([r['key']['family'] for r in d['added_rows'][:2]],['NEGATIVE_TIP_DEGREE_INTERVAL']*2);self.assertEqual(len(d['added_rows']),122)
 def test_all4096_ordinary_vectors_and_only_ordinary_vertices(self):
  d=derive_rows(native_order(13),context());ordinary=[r for r in d['added_rows'] if r['key']['family']=='ORDINARY_VERTEX_NO_DEGREE11'];special={p['tip_vertex'] for p in d['positive_tips']+d['negative_tips']}
  self.assertEqual({r['key']['subject'] for r in ordinary},{1<<v for v in range(13) if v!=0 and v not in special});self.assertEqual(len(ordinary),108);rows=[r for r in ordinary if r['key']['subject']==8];self.assertEqual(len(rows),12);masks=[m for m,c in rows[0]['terms']];rejected=0
  for state in range(4096):
   values={m:(state>>i)&1 for i,m in enumerate(masks)};good=all(evaluate(r,values) for r in rows);self.assertEqual(good,state.bit_count()!=11);rejected+=int(not good)
  self.assertEqual(rejected,12);self.assertTrue(all(r['lower']==-1 and r['upper']==10 for r in rows));self.assertEqual({r['key']['detail'] for r in rows},{1<<v for v in range(13) if v!=3})
 def test_boolean_control_alias_rejected(self):
  row=derive_rows(native_order(13),context())['added_rows'][0]
  with self.assertRaises(ValueError):evaluate(row,{row['key']['subject']:True})
 def test_disconnected_negative_link_rejected(self):
  c=context();c['model_id']['native_identity']['order']=8;cycles=[(2,3),(3,4),(4,2),(5,6),(6,7),(7,5)];c['root_link']=[(1<<1)|(1<<a)|(1<<b) for a,b in cycles]+[(1<<a)|(1<<b)|(1<<8) for a,b in ((2,5),(3,6),(4,7))]
  with self.assertRaises(ValueError):derive_rows(native_order(13),c)
  c['root_link']=c['root_link'][1:]
  with self.assertRaises(ValueError):derive_rows(native_order(13),c)
if __name__=='__main__':unittest.main()
