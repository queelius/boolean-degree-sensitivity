"""Residual-six source/type bookkeeping and small weighted-link controls. No solver. MIT."""
from dataclasses import dataclass,asdict
from enum import IntEnum
from itertools import combinations,combinations_with_replacement,product
from collections import Counter
from pathlib import Path
from hashlib import sha256
from time import process_time
from datetime import datetime,timezone
import argparse,json,resource
H=Path(__file__).resolve().parent;ROOT=H.parents[2];A8=H.parent/'008-sparse-spectrum-proof';A6=H.parent/'006-solver-resume'
class Level(IntEnum):SINGLETON=1;CUBIC=3;QUINTIC=5
def need(ok,message):
 if not ok:raise ValueError(message)
def defect(level,value):
 need(type(level)is Level and type(value)is int,'Typed Fourier level and exact integer required.')
 if level==Level.SINGLETON:return (value-1)*(value-2)
 if level==Level.CUBIC:return value*(value+1)
 return value*(value-1)
@dataclass(frozen=True,order=True)
class Exception:
 level:Level
 value:int
 @property
 def cost(self):return defect(self.level,self.value)
def exception_types():return tuple(Exception(level,value) for level in Level for value in range(-9,10) if not(level==Level.QUINTIC and value<0) and 0<defect(level,value)<=6)
def allocations():
 types=exception_types();return tuple(a for size in range(4) for a in combinations_with_replacement(types,size) if sum(t.cost for t in a)<=6)
def local_status(constant,incident,pair_intersection):
 need(type(constant)is int and type(incident)is tuple and len(incident)<=3 and all(type(t)is Exception and t in exception_types() and t.level!=Level.SINGLETON for t in incident),'Valid signed derivative type required.')
 need(defect(Level.SINGLETON,constant)+sum(t.cost for t in incident)<=6,'Local actual coefficient costs exceed6.')
 two_pairs=len(incident)==2 and all(t.level==Level.CUBIC for t in incident)
 need((two_pairs and type(pair_intersection)is int and pair_intersection in(0,1)) or (not two_pairs and pair_intersection is None),'Distinct ordinary pair supports meet in0or1 vertices.')
 if not incident:return 'COVERED_BASELINE_C_LE3' if constant<=3 else 'UNSUPPORTED_CONSTANT_GUARD'
 if len(incident)==1:
  t=incident[0]
  if t.cost==6:return 'NEW_TRIPLED_QUARTIC_PARITY' if t.level==Level.QUINTIC else 'UNSUPPORTED_HEAVY_QUADRATIC'
  if t.level==Level.QUINTIC:return 'COVERED_ONE_DOUBLED_QUARTIC_NO_C_BOUND'
  return 'COVERED_ONE_SIGNED_QUADRATIC_C_LE3' if constant<=3 else 'UNSUPPORTED_CONSTANT_GUARD'
 if len(incident)==3:return 'NEW_THREE_EXCEPTION_GEOMETRY_REQUIRED'
 if constant not in(1,2):return 'UNSUPPORTED_CONSTANT_GUARD'
 if any(t.level==Level.QUINTIC for t in incident):return 'COVERED_TWO_WITH_DOUBLE_C12'
 if all(t.value==1 for t in incident):return 'COVERED_TWO_POSITIVE_C_LE2'
 if pair_intersection==0:return 'COVERED_DISJOINT_WITH_NEGATIVE_C12'
 return 'COVERED_ADJACENT_NEGATIVE_C12' if all(t.value==-2 for t in incident) else 'COVERED_ADJACENT_MIXED_C12'
def local_templates():
 rows=[]
 for native,allocation in enumerate(allocations()):
  singleton_positions=[j for j,t in enumerate(allocation) if t.level==Level.SINGLETON];other=[j for j,t in enumerate(allocation) if t.level!=Level.SINGLETON]
  for own in [None]+singleton_positions:
   for constant in ((1,2) if own is None else (allocation[own].value,)):
    for mask in range(1<<len(other)):
     selected=[other[j] for j in range(len(other)) if mask>>j&1];incident=tuple(allocation[j] for j in selected);geometries=(0,1) if len(incident)==2 and all(t.level==Level.CUBIC for t in incident) else (None,)
     for intersection in geometries:rows.append({'allocation_id':native,'global_exceptions':[asdict(t) for t in allocation],'own_singleton_exception_position':own,'actual_constant':constant,'incident_global_positions':selected,'incident_nonsingleton_types':[asdict(t) for t in incident],'pair_intersection':intersection,'status':local_status(constant,incident,intersection)})
 return rows
def coupled_cover():
 rows=[]
 for native,a in enumerate(allocations()):
  cost=sum(t.cost for t in a)
  if cost<=4:reason='INHERITED_RESIDUAL4_SUPPORT_COVER'
  elif len(a)==1:
   reason={Level.SINGLETON:'AVOID_ONE_COST6_SINGLETON',Level.CUBIC:'AVOID_THREE_VERTEX_COST6_CUBIC',Level.QUINTIC:'NEW_SINGLE_TRIPLED_QUARTIC_LEMMA'}[a[0].level]
  else:
   need(len(a)==3 and all(t.cost==2 for t in a),'Residual-six type allocation omitted.')
   if any(t.level==Level.SINGLETON for t in a):reason='AVOID_ALL_SINGLETON_OWNERS_USE_OLD_AT_MOST_TWO'
   elif any(t.level==Level.CUBIC for t in a):reason='FOUR_SET_NOT_SUBSET_OF_CUBIC_USE_OLD_AT_MOST_TWO'
   else:reason='SHARED_FOUR_PRIVATE_TIP_EXTRACTION'
  rows.append({'allocation_id':native,'types':[asdict(t) for t in a],'global_cost':cost,'distinct_actual_coefficients_required':True,'F0_size':4,'reason':reason,'status':'PROPOSED_COMPLETE_COUPLED_ALLOCATION'})
 return rows
def even_weighted(n,edges):return all(sum(w for (a,b),w in edges.items() if v in(a,b))%2==0 for v in range(n))
def partitions(length):
 def grow(prefix):
  if len(prefix)==length:yield prefix;return
  for value in range(1+max(prefix,default=-1)+1):yield from grow(prefix+(value,))
 return tuple(grow(()))
def tripled_quartic_controls():
 pairs=tuple(combinations(range(6),2));others=tuple(e for e in pairs if e!=(0,1));counts={4:0,5:0};paths=[]
 for size in(1,2):
  for extra in combinations(others,size):
   edges={(0,1):3,**{e:1 for e in extra}}
   if even_weighted(6,edges):counts[3+size]+=1;paths.append(extra)
 need(counts=={4:0,5:4} and all(len(set(e[0]).intersection(e[1]))==1 and set().union(*map(set,e))>=set((0,1)) for e in paths),'Tripled-edge residual path classification failed.')
 triangle={(0,1),(0,2),(1,2)};other7=tuple(e for e in combinations(range(7),2) if e not in triangle);allowed=0
 for size in range(3):
  for extra in combinations(other7,size):
   edges={e:1 for e in triangle.union(extra)}
   if len(edges)in(0,1,4,5) and even_weighted(7,edges):allowed+=1
 need(allowed==0,'A forbidden triangle has an allowed even completion.')
 D=frozenset(range(4));inside=tuple(combinations(range(4),2));patterns=partitions(6);consistent=[]
 for mids in patterns:
  unit=set()
  for A,color in zip(inside,mids):
   for b in D.difference(A):unit.add(frozenset(A)|{b,4+color})
  if all({U.difference(A) for U in unit if set(A)<=U}=={frozenset((b,4+color)) for b in D.difference(A)} for A,color in zip(inside,mids)):consistent.append((mids,unit))
 need(len(patterns)==203 and len(consistent)==1 and consistent[0][0]==(0,)*6 and len(consistent[0][1])==4,'Pair-overlap path coherence differs.')
 counter={(0,1):3,(0,2):1,(1,2):1,(3,4):1,(3,5):1,(4,5):1};need(sum(counter.values())==8 and even_weighted(6,counter),'Ordinary-coefficient-two guard countercontrol failed.')
 return {'heavy_edge3_even_size4_count':counts[4],'heavy_edge3_even_size5_count':counts[5],'all_size5_residual_paths':[[list(e) for e in path] for path in paths],'unit_triangle_allowed_completion_count':allowed,'triangle_graphs_checked':1+len(other7)+len(other7)*(len(other7)-1)//2,'middle_partition_assignments':len(patterns),'compatible_middle_partitions':len(consistent),'coherent_unit_quartics':[sorted(U) for U in sorted(consistent[0][1],key=lambda U:sorted(U))],'ordinary_m2_countercontrol':{'edges':[{'pair':list(e),'weight':w} for e,w in counter.items()],'m':2,'quadratic_numerator':0,'only_link_control_not_actual_ternary_polynomial':True},'actual_ternary_feasibility_query_performed':False}
def private_tip_maps(F,supports):
 need(type(F)is int and F>0 and F.bit_count()==4 and type(supports)is list and len(supports)==len(set(supports))==3 and all(type(S)is int and 0<S<16384 and S.bit_count()==5 and F&S==F for S in supports),'Four literal free coordinates and three distinct cofaces required.')
 v=(F&-F).bit_length()-1;derivatives=[S^(1<<v) for S in supports];tips=[S^F for S in supports]
 need(len(set(tips))==3 and all(t.bit_count()==1 and not(t&F) for t in tips) and all(sum(bool(D&t) for D in derivatives)==1 for t in tips),'Private derivative tip lost.')
 return {'chosen_negative_free_coordinate':v,'derivative_doubled_quartics':derivatives,'tips':tips,'each_tip_incident_to_exactly_one_doubled_quartic':True}
def private_tip_control():return {'global_shared_core':15,'tip_count':3,**private_tip_maps(15,[31,47,79])}
def shared_incidence_control():
 supports=(7,11,13);inc=[sum(S>>v&1 for S in supports) for v in range(4)];need(sorted(inc)==[2,2,2,3],'Shared incidence countercontrol differs.')
 return {'support_masks':list(supports),'exception_count':3,'shared_defect_cost':6,'incidences':inc,'not_an_actual_polynomial':True,'naive_separate_charge_of8_refuted':True}
def private_surface_control():
 possibilities=[[n4,n5] for n4 in range(7) for n5 in range(13) if 9+2*n4+n5==12];need(possibilities==[[0,3],[1,1]],'Private link curvature cases differ.')
 need(3*3>2*6-4,'Six-vertex sphere facet contradiction failed.')
 return {'sphere_degree_cases':possibilities,'five_vertex_case_rejected_by_degree5':True,'six_vertex_case_forced_triangles':9,'six_vertex_sphere_triangles':8,'proof_is_structural_not_surface_catalog_regeneration':True}
AUTHORITIES=(H/'low-residual-derivative-complete-manifest.json',H/'local-audits-cycle64-manifest.json',H/'two-exception-positive-quartic-special-edge-manifest.json',A6/'two-adjacent-negative-cubic-accepted-manifest.json',A6/'two-mixed-cubic-accepted-manifest.json',A6/'two-disjoint-cubic-ordinary-accepted-manifest.json',H/'empty-residual-four-accepted-manifest.json')
NOTES=(ROOT/'.research/findings/negative-free-derivative-support-refinements.md',A8/'negative-free-derivative-catalog-audit.md',A8/'one-positive-quadratic-derivative-independent-audit.md',A8/'one-negative-quadratic-compact-exclusion-audit.md',A8/'doubled-positive-quartic-derivative-independent-audit.md',A6/'two-exception-positive-extension.md',A6/'two-positive-cubic-free-derivative.md',A6/'two-negative-cubic-ordinary-derivative.md',A6/'two-mixed-cubic-derivative.md',A6/'two-disjoint-cubic-ordinary-exclusion.md',A8/'exact-linear-top-propagation-engine.md',A8/'empty-3211111-connected-odd.md',H/'empty-residual-four-parent-audit.md')
def reference(path):
 path=Path(path).resolve();return {'path':str(path),'sha256':sha256(path.read_bytes()).hexdigest()}
def source_audit():
 refs={};authorities=[]
 for path in AUTHORITIES:
  authorities.append({'reference':reference(path),'accepted_status':json.loads(path.read_text())['status']});refs[str(path.resolve())]=reference(path)
  data=json.loads(path.read_text());entries=data.get('files',data.get('artifacts',[]))
  if isinstance(entries,dict):entries=[{'path':p,'sha256':d} for p,d in entries.items()]
  for item in entries:
   p=Path(item['path']);p=p if p.is_absolute() else ROOT/p;actual=reference(p);need(actual['sha256']==item['sha256'],'Frozen authority source changed:'+str(p));refs[actual['path']]=actual
 for path in NOTES:refs[str(path.resolve())]=reference(path)
 return {'accepted_authorities':authorities,'direct_refs':list(refs.values()),'direct_ref_count':len(refs),'historical_complete_enumerations_rerun':False}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();need(not args.output.exists(),'Fresh output required.');resource.setrlimit(resource.RLIMIT_AS,(4<<30,4<<30));resource.setrlimit(resource.RLIMIT_CPU,(10,11));start=process_time();source=reference(__file__);audit=source_audit();types=exception_types();allocation_rows=coupled_cover();local=local_templates()
 result={'status':'PROPOSED_RESIDUAL6_FOUR_FREE_OBSTRUCTION_TYPE_AND_SMALL_CONTROLS_PASS','observed_at':datetime.now(timezone.utc).isoformat(),'source':source,'source_audit':audit,'derived_exception_types':[{'level':int(t.level),'value':t.value,'cost':t.cost} for t in types],'allocation_count':len(allocation_rows),'allocation_cost_counts':dict(sorted(Counter(r['global_cost'] for r in allocation_rows).items())),'allocation_reason_counts':dict(sorted(Counter(r['reason'] for r in allocation_rows).items())),'coupled_cover':allocation_rows,'actual_local_template_count':len(local),'local_status_counts':dict(sorted(Counter(r['status'] for r in local).items())),'local_templates':local,'tripled_quartic_small_controls':tripled_quartic_controls(),'private_tip_control':private_tip_control(),'private_surface_control':private_surface_control(),'shared_exception_countercontrol':shared_incidence_control(),'new_claims_pending_independent_review':['single tripled positive quartic local lemma','private-vertex extraction beyond two total exceptions','residual6 implies at most3 negative-free coordinates'],'actual_ternary_feasibility_runs':0,'new_solver_runs':0,'canonical_updates':0,'whole_patterns_newly_marked_excluded':0,'global_goal_complete':False,'CPU_seconds':process_time()-start}
 for item in audit['direct_refs']+[source]:need(reference(item['path'])==item,'Postrun source changed.')
 need(result['CPU_seconds']<10,'Small-control10CPU limit exceeded.')
 with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps({key:result[key] for key in('status','allocation_count','allocation_cost_counts','allocation_reason_counts','actual_local_template_count','local_status_counts','CPU_seconds')}))
if __name__=='__main__':main()
