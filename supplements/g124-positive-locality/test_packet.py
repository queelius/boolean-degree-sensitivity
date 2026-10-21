"""Stdlib controls for two independent portable locality verifiers."""
from collections import Counter
from copy import deepcopy
from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory
import json,shutil,subprocess,sys,unittest
try:
 import packet_io as io
 import verify_union as union
 import verify_quartet as quartet
except ModuleNotFoundError:io=union=quartet=None
ROOT=Path(__file__).resolve().parent
def mask(vertices):return sum(1<<v for v in vertices)
def brute(graph,n):
 triples=list(combinations(range(n),3));quartets=list(combinations(range(n),4));rows=[];windows={}
 for t in triples:
  if t in graph:continue
  enlarged=graph|{t};obs=[q for q in quartets if sum(set(e)<=set(q) for e in enlarged)>2]
  required=set(t).union(*(set(q) for q in obs))
  local=[w for w in combinations(range(n),5) if obs and set(t)<=set(w) and all(set(q)<=set(w) for q in obs)]
  for w in local:windows.setdefault(mask(w),[]).append(mask(t))
  rows.append(dict(triple=mask(t),obstruction_quartets=list(map(mask,obs)),required_mask=mask(required),positive_local_five_sets=sorted(map(mask,local))))
 return dict(missing_triples=rows,missing_obstruction_histogram=[dict(obstructions=k,triples=v) for k,v in sorted(Counter(len(x['obstruction_quartets']) for x in rows).items())],positive_localizable_five_sets=[dict(five_set=w,missing_triples=sorted(v)) for w,v in sorted(windows.items())],maximum_positive_localizable_in_a_five_set=max(map(len,windows.values()),default=0),violating_five_sets=[dict(five_set=w,missing_triples=sorted(v)) for w,v in sorted(windows.items()) if len(v)>=2])
class PacketTests(unittest.TestCase):
 def setUp(self):self.assertIsNotNone(io,'Portable typed IO/entrypoint has not been implemented.')
 def test_all253_free_five_vertex_graphs_against_literal_restoration(self):
  triples=list(combinations(range(5),3));checked=0
  for state in range(1024):
   graph={t for i,t in enumerate(triples) if state>>i&1}
   if any(sum(set(t)<=set(q) for t in graph)>2 for q in combinations(range(5),4)):continue
   expected=brute(graph,5)
   self.assertEqual(union.locality(set(map(mask,graph)),5),expected)
   self.assertEqual(quartet.quartet_first_locality(graph,5),expected);checked+=1
  self.assertEqual(checked,253)
 def test_nonvacuous_counterexample_and_vacuous_exclusion(self):
  for record in [union.locality({7,11},5),quartet.quartet_first_locality({(0,1,2),(0,1,3)},5)]:self.assertEqual(record['violating_five_sets'],[dict(five_set=31,missing_triples=[13,14])])
  self.assertEqual(union.locality(set(),5)['maximum_positive_localizable_in_a_five_set'],0)
  self.assertEqual(quartet.quartet_first_locality(set(),5)['maximum_positive_localizable_in_a_five_set'],0)
 def test_graph_alias_duplicate_nonfree_and_wrong_vertex_count(self):
  for g in [{True},{3},{32},{7,11,13}]:
   with self.assertRaises(ValueError):union.locality(g,5)
  for edges in [[[0,1,2],[2,1,0]],[[False,1,2],[0,1,3]],[[0,1,5],[0,1,3]]]:
   with self.assertRaises(ValueError):quartet.literal_graph(edges,5,2)
  with self.assertRaises(ValueError):union.locality(set(),True)
  with self.assertRaises(ValueError):quartet.quartet_first_locality({(0,1,2),(0,1,3),(0,2,3)},5)
 def test_actual_tuple_invariants_noninvolution(self):
  g={(0,1,2),(0,1,3),(0,4,5),(1,2,5)};p=(1,2,0,3,4,5);inverse=tuple(p.index(i) for i in range(6));self.assertNotEqual(p,inverse)
  h={tuple(sorted(p[v] for v in t)) for t in g}
  self.assertEqual(union.invariant(set(map(mask,g)),6),union.invariant(set(map(mask,h)),6));self.assertEqual(quartet.incidence_invariant(g,6),quartet.incidence_invariant(h,6))
  with self.assertRaises(ValueError):quartet.require_distinct([quartet.incidence_invariant(g,6),quartet.incidence_invariant(h,6)])
 def test_first_actual_graph_both_methods_exact_certificate(self):
  catalog,cert,_=io.inputs();a,sa=union.audit_record(catalog['graphs'][0],0);b,sb=quartet.audit_record(catalog['graphs'][0],0)
  self.assertEqual(a,b);self.assertEqual(sa,sb);self.assertEqual(a,cert['records'][0]);self.assertEqual(len(a['missing_triples']),240)
 def test_record_mutations_rejected(self):
  catalog,cert,_=io.inputs();record,_=union.audit_record(catalog['graphs'][0],0)
  for mutation in ['obstruction','triple','alias','zero','window','edge','index','invariant']:
   bad=deepcopy(record)
   if mutation=='obstruction':next(r for r in bad['missing_triples'] if r['obstruction_quartets'])['obstruction_quartets'].pop()
   elif mutation=='triple':bad['missing_triples'].pop()
   elif mutation=='alias':bad['missing_triples'][0]=deepcopy(bad['missing_triples'][1])
   elif mutation=='zero':next(r for r in bad['missing_triples'] if not r['obstruction_quartets'])['positive_local_five_sets']=[31]
   elif mutation=='window':bad['positive_localizable_five_sets'].pop()
   elif mutation=='edge':bad['graph_edges'][0]=bad['graph_edges'][1]
   elif mutation=='index':bad['catalog_index']=False
   else:bad['invariant_sha256']='0'*64
   with self.subTest(mutation=mutation):
    with self.assertRaises(ValueError):io.same(bad,record,'damaged record')
    with self.assertRaises(ValueError):quartet.compare_record(bad,record)
 def test_complete_inventory_scope_alias_and_omission(self):
  cat,cert,_=io.inputs()
  for name,value in [('native_graphs',True),('original_Boolean_problem_solved',True),('records',cert['records'][:-1])]:
   bad=deepcopy(cert);bad[name]=value
   with self.assertRaises(ValueError):io.inventory(cat,bad)
  bad=deepcopy(cat);bad['graphs'].pop()
  with self.assertRaises(ValueError):io.inventory(bad,cert)
 def test_path_escape_file_pin_and_manifest_omission(self):
  with TemporaryDirectory(prefix='g124-controls-') as d:
   root=Path(d);shutil.copytree(ROOT/'data',root/'data')
   manifest=json.loads((root/'data/manifest.json').read_bytes())
   for path in ['/etc/passwd','../escape','data/../../escape']:
    with self.assertRaises(ValueError):io.safe(root,path)
   bad=deepcopy(manifest);bad['files'].pop();(root/'data/manifest.json').write_text(json.dumps(bad))
   with self.assertRaises(ValueError):io.inputs(root)
   (root/'data/manifest.json').write_text(json.dumps(manifest));(root/'data/catalog.json.gz').write_bytes(b'changed')
   with self.assertRaises(ValueError):io.inputs(root)
 def test_budget_is_incomplete_not_complete(self):
  for reader in (union,quartet):
   result=reader.audit(cpu_budget=0);self.assertEqual(result['status'],'INCOMPLETE');self.assertEqual(len(result['pending_native_indices']),75)
 def test_copy_entrypoint_unrelated_cwd_stdlib_and_no_overwrite(self):
  with TemporaryDirectory(prefix='g124-portable-') as d:
   copied=Path(d)/'copy';shutil.copytree(ROOT,copied,ignore=shutil.ignore_patterns('__pycache__'))
   output=Path(d)/'guard.json';output.write_text('unchanged')
   for script in ('verify_union.py','verify_quartet.py'):
    p=subprocess.run([sys.executable,'-S',str(copied/script),'--output',str(output)],cwd='/',capture_output=True,text=True)
    self.assertNotEqual(p.returncode,0);self.assertEqual(output.read_text(),'unchanged')
if __name__=='__main__':unittest.main()
