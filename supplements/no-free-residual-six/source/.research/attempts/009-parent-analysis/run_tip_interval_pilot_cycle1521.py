"""One authorized native interval query; the returned transcript is untrusted."""
import argparse
from datetime import datetime,timezone
from pathlib import Path
import resource
import signal
import time
from types import SimpleNamespace

import augmented_interval_pilot_cycle1521 as schedule
import context_first_rows_cycle1438 as translation
import gap_transcript_reader_cycle1436 as reader
import native_sat_pilot_io_cycle1457 as io
from run_context_first_controls_cycle1438 import load_generator


def check_authorization(auth,plan):
    io.need(auth['status']=='AUTHORIZED_ONE_BOUNDED_EXACT_INTERVAL_PROPAGATION_PILOT' and
            type(auth['one_query']) is int and auth['one_query']==1 and auth['no_retries'] is True,
            'exact one-query parent contract required')
    io.need(auth['genuine_projection_only'] is True and auth['raw_original_row_entailment_claimed'] is False and
            auth['SAT_LP_MILP_queries_authorized'] is False,'scope differs')
    for key in ['model_id','sources','limits','output_prefix']:
        io.need(reader.exact(auth[key],plan[key]),'changed authorized '+key)
    io.need(reader.exact(auth['limits'],dict(setup_stop_CPU_seconds=4,generation_CPU_budget_seconds=10,
        total_CPU_soft_seconds=14,total_CPU_hard_seconds=15,wall_seconds=40,AS_bytes=536870912)),
        'changed resource contract')


def main():
    io.need(__debug__,'normal Python required before I/O')
    parser=argparse.ArgumentParser();parser.add_argument('--plan',type=Path,required=True)
    parser.add_argument('--plan-sha256',required=True);parser.add_argument('--preflight',type=Path,required=True)
    parser.add_argument('--preflight-sha256',required=True);args=parser.parse_args()
    resource.setrlimit(resource.RLIMIT_CPU,(14,15));resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
    plan_ref=dict(path=str(args.plan.resolve()),sha256=args.plan_sha256)
    preflight_ref=dict(path=str(args.preflight.resolve()),sha256=args.preflight_sha256)
    plan=io.read_pinned(plan_ref);preflight=io.read_pinned(preflight_ref)
    io.need(preflight['status']=='PRE_TARGET_CONTROLS_PASS_ONE_QUERY_READY' and
            reader.exact(preflight['plan'],io.pin(args.plan)),'preflight does not bind this plan')
    auth=io.read_pinned(plan['authorization']);check_authorization(auth,plan)
    sources=[plan_ref,preflight_ref,plan['authorization']]+list(auth['sources'].values())+plan['code_sources']+preflight['control_sources']
    for ref in sources:
        actual=io.pin(ref['path']);io.need(actual['sha256']==ref['sha256'],'source changed before query')
    prefix=Path(auth['output_prefix']);output=Path(str(prefix)+'.json');launch=Path(str(prefix)+'.launch.json')
    io.need(not output.exists() and not launch.exists(),'sole attempt already exists')
    src=auth['sources'];gate=io.read_pinned(src['original_row_authority'])
    inventory_gate=io.read_pinned(src['independent_inventory_authority'])
    io.need(gate['status']=='INDEPENDENTLY_VERIFIED_NATIVE26_SIGNED_STAR_FULL_P_ROWS' and gate['models_compared']==26,
            'original full row gate differs')
    io.need(inventory_gate['status']=='INDEPENDENT_COMPLETE_ALL26_EXACT_TIP_AND_LINEAR_ORDINARY_INVENTORY_ACCEPTED'
            and inventory_gate['model_count']==26,'added row gate differs')
    io.need(any(reader.exact(ref,src['inventory']) for ref in inventory_gate['sources']),
            'independent gate does not bind the accepted inventory')
    io.need(reader.exact(gate['common_source'],src['common_rows']) and
            reader.exact(gate['context_source'],src['context_rows']),'original row source binding differs')
    common=io.read_pinned(src['common_rows']);packet=io.read_pinned(src['context_rows'])
    inventory=io.read_pinned(src['inventory']);wanted=auth['model_id']
    overlay=io.unique_context(packet['contexts'],wanted);extra=schedule.select_open(inventory['contexts'],wanted)
    io.need(len(inventory['contexts'])==len(packet['contexts'])==26 and
            sum(reader.exact(c['model_id'],wanted) for c in gate['contexts'])==1,'incomplete native context domain')
    model=io.native_model(common,overlay,gate,src['original_row_authority'])
    original_count=len(model['rows'])
    io.need(original_count==auth['original_rows'] and len(extra['added_rows'])==auth['added_rows'] and
            extra['added_row_native_ids']==list(range(original_count,auth['extended_rows'])),
            'native appended row IDs/count differ')
    model['rows']+=extra['added_rows']
    model['header'].update(kind='NECESSARY_GENUINE_SIGNED_STAR_EXTENDED_P',
        inventory_source=src['inventory'],inventory_authority=src['independent_inventory_authority'],
        genuine_projection=True,original_row_count=original_count,
        row_order='common.rows followed by context.rows followed by accepted inventory added_rows')
    io.need(len(model['variables'])==auth['native_variables'] and len(model['rows'])==auth['extended_rows'] and
            sum(len(row['terms']) for row in model['rows'])==auth['extended_terms'],'complete native model dimensions differ')
    binding=reader.binding(model)
    order,inverse=schedule.priority_order(len(common['rows']),len(overlay['rows']),len(extra['added_rows']))
    native_rows=[SimpleNamespace(terms=tuple(map(tuple,row['terms'])),lower=row['lower'],upper=row['upper'])
                 for row in model['rows']]
    generator_rows=[native_rows[i] for i in order];generator=load_generator()
    setup=time.process_time()
    result=dict(schema_version=1,observed_at=datetime.now(timezone.utc).isoformat(),
        status='PREPARED_NO_GENERATION_YET',authorization=plan['authorization'],plan=plan_ref,preflight=preflight_ref,
        sources=sources,model_id=wanted,model_header=model['header'],model_binding=binding,
        common_source=src['common_rows'],context_source=src['context_rows'],row_authority=src['original_row_authority'],
        inventory_source=src['inventory'],inventory_authority=src['independent_inventory_authority'],
        variables=model['variables'],generator_to_native=order,native_to_generator=inverse,
        native_original_rows=original_count,native_added_rows=len(extra['added_rows']),native_rows=len(model['rows']),
        native_terms=auth['extended_terms'],limits=auth['limits'],setup_CPU_seconds=setup,
        native_queries=0,raw_generator_certificate=None,native_certificate=None,envelope=None,
        no_preserved_prefix_if_timeout=True,independent_actual_replay_required=True,
        genuine_projection_only=True,raw_original_row_entailment_claimed=False,
        fixedpoint_completeness_claimed=False,actual_derivative_constructed=False,
        native_context_excluded=False,whole_pattern_excluded=False,global_goal_complete=False)
    try:schedule.cpu_plan(setup)
    except ValueError as error:result.update(status='SETUP_BUDGET_INCONCLUSIVE',error=str(error))
    else:
        io.write_json(launch,dict(schema_version=1,status='SOLE_NATIVE_INTERVAL_ATTEMPT_LAUNCH',
            wrapper=io.pin(__file__),authorization=plan['authorization'],plan=plan_ref,preflight=preflight_ref,
            model_id=wanted,model_binding=binding,setup_CPU_seconds=setup,limits=auth['limits']))
        def timeout(signum,frame):raise TimeoutError('CPU signal '+str(signum)+' reached')
        signal.signal(signal.SIGXCPU,timeout);signal.signal(signal.SIGPROF,timeout)
        start=time.process_time();result['native_queries']=1;signal.setitimer(signal.ITIMER_PROF,10)
        try:
            raw=generator.propagate(generator_rows);signal.setitimer(signal.ITIMER_PROF,0)
            result['raw_generator_certificate']=raw;native=translation.translate(raw,order)
            result.update(status='UNTRUSTED_'+raw['status'],native_certificate=native,
                envelope=dict(schema_version=1,model_binding=binding,certificate=native))
        except TimeoutError as error:result.update(status='GENERATOR_TIMEOUT_INCONCLUSIVE',error=str(error))
        except Exception as error:result.update(status='GENERATOR_ERROR_INCONCLUSIVE',error_type=type(error).__name__,error=str(error))
        finally:signal.setitimer(signal.ITIMER_PROF,0)
        result['generation_CPU_seconds']=time.process_time()-start
    for ref in sources:io.need(io.pin(ref['path'])['sha256']==ref['sha256'],'post-query source changed')
    result.update(total_CPU_seconds=time.process_time(),peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                  wrapper=io.pin(__file__))
    ref=io.write_json(output,result)
    print({k:result[k] for k in ['status','native_queries','setup_CPU_seconds','total_CPU_seconds','peak_RSS_bytes']})
    print(ref)


if __name__=='__main__':main()
