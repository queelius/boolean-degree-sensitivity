"""One independent read-only replay; no1521/1518 producer imports or queries."""
import argparse,json,resource,signal,time
from pathlib import Path
from read_positive_inventory_cycle1512 import identity,ref,load
from positive_inventory_reader_cycle1512 import need,exact,native_order
from exact_tip_inventory_reader_cycle1519 import derive_rows
from extended_trace_reader_cycle1522 import verify_candidate

def main():
 ap=argparse.ArgumentParser();ap.add_argument('config');ap.add_argument('--sha256',required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_CPU,(10,11));resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912));signal.alarm(30)
 start=time.process_time();cfg=load(dict(path=a.config,sha256=a.sha256));H=Path(a.config).resolve().parent;out=H/'extended-trace-result-cycle1522.json';need(not out.exists(),'fresh reader output required');sources=[]
 def get(r):sources.append(r);return load(r)
 for r in cfg['reader_sources']:need(ref(r['path'])['sha256']==r['sha256'],'frozen independent reader source');sources.append(r)
 auth=get(cfg['authorization']);need(auth['status']=='AUTHORIZED_ONE_BOUNDED_EXACT_INTERVAL_PROPAGATION_PILOT' and auth['one_query']==1 and auth['no_retries'] is True and auth['genuine_projection_only'] is True and auth['raw_original_row_entailment_claimed'] is False,'one genuine-only producer authorization')
 bindings=auth['sources'];gate=get(bindings['original_row_authority']);need(gate['status']=='INDEPENDENTLY_VERIFIED_NATIVE26_SIGNED_STAR_FULL_P_ROWS' and gate['models_compared']==26,'accepted complete original row gate')
 common=get(gate['common_source']);packet=get(gate['context_source']);need(exact(gate['common_source'],bindings['common_rows']) and exact(gate['context_source'],bindings['context_rows']),'unchanged original source identities')
 igate=get(bindings['independent_inventory_authority']);need(igate['status']=='INDEPENDENT_COMPLETE_ALL26_EXACT_TIP_AND_LINEAR_ORDINARY_INVENTORY_ACCEPTED' and igate['model_count']==26,'accepted complete cut gate')
 inventory=get(bindings['inventory']);reviewed=get(igate['result']);need(inventory['status']=='PROPOSED_COMPLETE_SIGNED_STAR_TIP_STRUCTURE_INVENTORY','frozen inventory schema')
 wanted=auth['model_id'];select=lambda rows:[c for c in rows if exact(c['model_id'],wanted)]
 ctxs,pros,checks=select(packet['contexts']),select(inventory['contexts']),select(reviewed['contexts']);need(len(ctxs)==len(pros)==len(checks)==1,'unique exact native context');ctx,pro,checked=ctxs[0],pros[0],checks[0]
 need(pro['genuine_context_status']=='OPEN' and pro['skip_future_queries'] is False,'authorized open genuine context')
 variables=native_order(13);need(exact(common['variables'],variables),'full original native variable order');d=derive_rows(variables,ctx);added=d['added_rows']
 need(exact(added,pro['added_rows']) and exact(added,checked['added_rows']) and exact(d['origins'],pro['row_provenance']) and exact(d['origins'],checked['row_provenance']),'fresh independently reconstructed accepted cuts/provenance')
 need(len(common['rows'])==12130 and len(ctx['rows'])==382 and len(added)==123 and len(variables)==1079,'exact authorized native block sizes')
 need(exact(wanted,dict(constant=1,native_identity=dict(catalog_sha256='df2dd7cc5c4ba26a5dde0736c3ec8c6d9f33292dfdd66f067badb0d67ea0e879',order=8,original_index=3))),'sole authorized target')
 header=dict(kind='NECESSARY_GENUINE_SIGNED_STAR_EXTENDED_P',n=common['n'],constant=wanted['constant'],native_identity=wanted['native_identity'],root=ctx['root'],source_to_physical=ctx['source_to_physical'],root_link=ctx['root_link'],special_edges=ctx['special_edges'],root_nonneighbor_physical_slots=ctx['root_nonneighbor_physical_slots'],common_source=gate['common_source'],context_source=gate['context_source'],row_gate=bindings['original_row_authority'],inventory_source=bindings['inventory'],inventory_authority=bindings['independent_inventory_authority'],genuine_projection=True,original_row_count=12512,row_order='common.rows followed by context.rows followed by accepted inventory added_rows')
 model=dict(schema_version=1,header=header,variables=variables,rows=common['rows']+ctx['rows']+added)
 candidate=get(cfg['candidate']);terminal=get(cfg['terminal']);need(exact(candidate['model_id'],wanted),'candidate target identity')
 # Terminal schema is bound by config after final1521 freeze; exit and candidate ref are independently checked.
 need(type(terminal[cfg['terminal_exit_field']]) is int and terminal[cfg['terminal_exit_field']]==0,'producer did not terminate normally')
 need(exact(terminal[cfg['terminal_candidate_field']],cfg['candidate']),'terminal references another candidate')
 for k,r in [('common_source',gate['common_source']),('context_source',gate['context_source']),('row_authority',bindings['original_row_authority']),('inventory_source',bindings['inventory']),('inventory_authority',bindings['independent_inventory_authority'])]:need(exact(candidate[k],r),'candidate source alias '+k)
 for r in candidate['sources']:need(ref(r['path'])['sha256']==r['sha256'],'candidate declared source hash');sources.append(r)
 replay=verify_candidate(model,candidate,12130,382,123)
 for r in sources:need(ref(r['path'])['sha256']==r['sha256'],'post-read source changed')
 result=dict(schema_version=1,status='INDEPENDENT_EXTENDED_CONTRADICTION_ACCEPTED' if replay['nonexistence_proved'] else 'INDEPENDENT_EXTENDED_PREFIX_ACCEPTED_INCONCLUSIVE',model_id=wanted,model_binding=replay['model_binding'],candidate=cfg['candidate'],terminal=cfg['terminal'],authorization=cfg['authorization'],reader_sources=cfg['reader_sources'],sources=sources,rows=12635,original_rows=12512,added_rows=123,terms=sum(len(r['terms']) for r in model['rows']),variables=1079,full_row_permutation_and_inverse_checked=True,raw_to_native_translation_checked=True,added_rows_independently_reconstructed=True,checked_prefix=replay,fixedpoint_completeness_certified=False,generator_evaluations_diagnostic_only=candidate['native_certificate']['evaluations'],native_queries_performed_by_reader=0,genuine_projection_only=True,original_raw_row_entailment_claimed=False,case_excluded=replay['nonexistence_proved'],whole_pattern_excluded=False,global_goal_complete=False,CPU_seconds=time.process_time()-start,peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(dict(status=result['status'],result=ref(out),CPU_seconds=result['CPU_seconds'],fixed_variables=replay['fixed_variables'],steps=len(replay['steps_checked']),contradiction=replay['contradiction'])))

if __name__=='__main__':main()
