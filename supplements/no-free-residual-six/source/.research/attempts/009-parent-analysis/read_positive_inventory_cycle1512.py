"""Sole independent1512 all-context inventory pass; no target query API."""
import argparse,hashlib,json,resource,signal,time
from pathlib import Path
from positive_inventory_reader_cycle1512 import need,native_order,derive,exact
def ref(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p.resolve()),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def load(r):
 need(ref(r['path'])['sha256']==r['sha256'],'frozen source pin changed');return json.loads(Path(r['path']).read_text())
def identity(model):
 need(type(model) is dict and model.keys()=={'constant','native_identity'} and type(model['constant']) is int and model['constant'] in (1,2),'typed model constant')
 d=model['native_identity'];need(type(d) is dict and d.keys()=={'catalog_sha256','order','original_index'} and type(d['catalog_sha256']) is str and len(d['catalog_sha256'])==64 and all(c in '0123456789abcdef' for c in d['catalog_sha256']) and type(d['order']) is int and 7<=d['order']<=12 and type(d['original_index']) is int and d['original_index']>=0,'complete original native identity')
 return model['constant'],d['catalog_sha256'],d['order'],d['original_index']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('config');ap.add_argument('--sha256',required=True);args=ap.parse_args();resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912));resource.setrlimit(resource.RLIMIT_CPU,(5,5));signal.alarm(15)
 started=time.process_time();config=load(dict(path=args.config,sha256=args.sha256));H=Path(args.config).resolve().parent;output=H/'positive-inventory-result-cycle1512.json';need(not output.exists(),'fresh output required');sources=[]
 def get(r):sources.append(r);return load(r)
 gate=get(config['row_authority']);need(gate['status']=='INDEPENDENTLY_VERIFIED_NATIVE26_SIGNED_STAR_FULL_P_ROWS' and gate['models_compared']==26,'accepted complete26 native row gate')
 common=get(gate['common_source']);packet=get(gate['context_source']);variables=native_order(13);need(common['n']==13 and common['variables']==variables,'independent1079 native masks/order')
 source_contexts=packet['contexts'];need(len(source_contexts)==26 and [c['model_id'] for c in source_contexts]==[c['model_id'] for c in gate['contexts']],'all26 accepted context identities and order')
 ids=[identity(c['model_id']) for c in source_contexts];need(len(set(ids))==26,'no native identity alias')
 theorem=get(config['triangle_authority']);parent=get(config['triangle_parent']);need(theorem['status']=='INDEPENDENT_WRITTEN_REVIEW_ACCEPTS_GENERAL_POSITIVE_OPPOSITE_TRIANGLE_OBSTRUCTION' and parent['status']=='ACCEPTED_GENERAL_WRITTEN_STRUCTURAL_THEOREM' and parent['independent_authority']['sha256']==config['triangle_authority']['sha256'],'general all-root opposite-triangle theorem binding')
 tip=get(config['degree_authority']);tipparent=get(config['degree_parent']);need(tip['new_written_conclusions']['positive_tip_minimum_degree']==7 and tipparent['independent_authority']['sha256']==config['degree_authority']['sha256'],'positive-tip degree7 bound source')
 frontier=get(config['frontier']);need(frontier['scope']=='TWO_NEGATIVE_FREE_COORDINATES_SIGNED_STAR_GENUINE_CONTEXTS' and frontier['genuine_context_counts']=={'EXCLUDED':2,'OPEN':24} and frontier['raw_row_UNSAT_for_c2_claimed'] is False,'unchanged genuine/raw frontier distinction')
 front={identity(e['model_id']):e for e in frontier['entries']};need(len(front)==26 and set(front)==set(ids),'complete frontier identity matching')
 inventory=get(config['inventory']);need(inventory['status']=='PROPOSED_COMPLETE_POSITIVE_TIP_CONSTRAINT_INVENTORY','frozen1511 inventory schema')
 for r in inventory['sources']:
  need(ref(r['path'])['sha256']==r['sha256'],'producer declared source pin');sources.append(r)
 proposed=inventory['contexts'];need(len(proposed)==26 and [identity(c['model_id']) for c in proposed]==ids,'literal26 inventory order and identities')
 checked=[];zero=degree=skip=0
 for ctx,pro in zip(source_contexts,proposed):
  model=ctx['model_id'];key=identity(model);old=front[key];need(ctx['n']==13 and ctx['root']==0,'actual native physical context')
  for field in ('model_id','n','root','source_to_physical','root_link','special_edges'):need(exact(pro[field],ctx[field]),'inventory literal source field '+field)
  need(type(pro['root_mask']) is int and pro['root_mask']==1<<ctx['root'],'literal root bit')
  need(pro['genuine_context_status']==old['genuine_context_status'] and pro['raw_row_model_status']==old['raw_row_model_status'] and pro['genuine_exclusion_authority']==old['genuine_exclusion_authority'] and type(pro['skip_future_queries']) is bool and pro['skip_future_queries']==(old['genuine_context_status']=='EXCLUDED'),'source-bound genuine skip status')
  if old['genuine_exclusion_authority'] is not None:
   r=old['genuine_exclusion_authority'];need(ref(r['path'])['sha256']==r['sha256'],'inherited genuine closure pin');sources.append(r)
  derivation=derive(variables,ctx);tips=[];units=[];degrees=[];positions={v:i for i,v in enumerate(variables)}
  for row in derivation:
   A=row['opposite_triangle_mask'];tipbit=row['tip_mask'];opposite_edges=sorted(A^(1<<v) for v in range(13) if A>>v&1);edge_masks=[m for m,c in row['degree_row']['terms']]
   tips.append(dict(tip=row['tip_vertex'],tip_mask=tipbit,positive_edge_mask=row['edge_mask'],opposite_triangle_mask=A,opposite_edge_masks=opposite_edges,native_triangle_variable_index=positions[A],degree_edge_masks=edge_masks,native_degree_variable_indices=[positions[m] for m in edge_masks]))
   units.append(dict(key=dict(family='POSITIVE_OPPOSITE_TRIANGLE_ABSENT',subject=A,detail=0),terms=[[A,1]],lower=0,upper=0))
   degrees.append(dict(key=dict(family='POSITIVE_TIP_DEGREE_LOWER_BOUND',subject=tipbit,detail=0),**row['degree_row']))
  expected=units+degrees;original=len(common['rows'])+len(ctx['rows']);need(exact(pro['positive_tips'],tips) and exact(pro['added_rows'],expected),'all literal derived native constraints')
  need(type(pro['original_row_count']) is int and pro['original_row_count']==original and type(pro['extended_row_count']) is int and pro['extended_row_count']==original+len(expected) and exact(pro['added_row_native_ids'],list(range(original,original+len(expected)))),'zero-based original/extended native row positions')
  zero+=len(units);degree+=len(degrees);skip+=int(pro['skip_future_queries']);checked.append(dict(model_id=model,positive_tips=tips,added_rows=expected,added_row_native_ids=pro['added_row_native_ids'],original_row_count=original,extended_row_count=original+len(expected),genuine_context_status=old['genuine_context_status'],raw_row_model_status=old['raw_row_model_status'],skip_future_queries=pro['skip_future_queries']))
 need(skip==2,'exactly two previously excluded genuine contexts skipped')
 for extra in config.get('extra_refs',[]):get(extra)
 for r in sources:need(ref(r['path'])['sha256']==r['sha256'],'post-read pin')
 result=dict(status='INDEPENDENT_COMPLETE_ALL26_NATIVE_POSITIVE_RESTRICTION_INVENTORY_ACCEPTED',sources=sources,reader=ref(__file__),helper=ref(H/'positive_inventory_reader_cycle1512.py'),contexts=checked,context_count=26,native_variables=len(variables),forced_zero_units=zero,positive_tip_degree_rows=degree,skipped_genuine_contexts=skip,remaining_genuine_contexts=26-skip,raw_c2_root7_UNSAT_claimed=False,degree_exact7_claimed=False,CPU_seconds=time.process_time()-started,propagation_replayed=False,solver_queries=0,native_models_excluded=0,whole_pattern_excluded=False,global_goal_complete=False)
 output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status=result['status'],CPU_seconds=result['CPU_seconds'],forced_zero_units=zero,degree_rows=degree,result=ref(output))))
if __name__=='__main__':main()
