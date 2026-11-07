"""Build only new labeled consequence rows, never a target propagation model."""
import argparse
from collections import Counter
import json
from pathlib import Path
import resource
import time

from make_positive_tip_inventory_cycle1511 import pin, pinned, select_pilot
from positive_tip_inventory_cycle1511 import identity, require
from tip_structure_inventory_cycle1518 import exact, rows_for_context


def build(weak, common, packet, row_gate, frontier):
    keys=[identity(c['model_id']) for c in weak['contexts']]
    require(len(keys)==len(set(keys))==26 and
            keys==[identity(c['model_id']) for c in packet['contexts']] and
            keys==[identity(c['model_id']) for c in row_gate['contexts']] and
            keys==[identity(m) for m in packet['expected_model_ids']], 'complete native context domain')
    fronts={identity(c['model_id']):c for c in frontier['entries']}
    require(len(fronts)==len(frontier['entries'])==len(keys) and set(fronts)==set(keys),
            'complete unchanged frontier')
    contexts=[]
    for old, original in zip(weak['contexts'],packet['contexts']):
        front=fronts[identity(old['model_id'])]
        require(all(exact(old[k],front[k]) for k in
                    ('genuine_context_status','raw_row_model_status','genuine_exclusion_authority'))
                and old['skip_future_queries'] is (front['genuine_context_status']=='EXCLUDED'),
                'unchanged genuine/raw scope')
        require(all(exact(old[k],original[k]) for k in
                    ('n','root','source_to_physical','root_link','special_edges')),
                'original physical context')
        record={k:old[k] for k in ('model_id','n','root','root_mask','source_to_physical',
            'root_link','special_edges','positive_tips','genuine_context_status','raw_row_model_status',
            'skip_future_queries','genuine_exclusion_authority','original_row_count')}
        generated=rows_for_context(old,common['variables'])
        start=common['row_count']+original['row_count']
        require(start==old['original_row_count'], 'unchanged original row count')
        record.update(generated,added_row_native_ids=list(range(start,start+len(generated['added_rows']))),
            extended_row_count=start+len(generated['added_rows']),
            original_nonzero_coefficients=original['expanded_nonzero_coefficients'],
            extended_nonzero_coefficients=original['expanded_nonzero_coefficients']+generated['added_nonzero_coefficients'])
        contexts.append(record)
    return dict(contexts=contexts,model_count=len(contexts),
        positive_tip_instances=sum(len(c['positive_tips']) for c in contexts),
        negative_tip_instances=sum(len(c['negative_tips']) for c in contexts),
        ordinary_vertex_instances=sum(len(c['ordinary_vertices']) for c in contexts),
        total_row_occurrences=sum(c['row_occurrences_before_deduplication'] for c in contexts),
        total_distinct_added_rows=sum(len(c['added_rows']) for c in contexts),
        total_duplicate_row_occurrences=sum(c['duplicate_row_occurrences'] for c in contexts),
        total_added_nonzero_coefficients=sum(c['added_nonzero_coefficients'] for c in contexts),
        row_family_counts=dict(Counter(r['key']['family'] for c in contexts for r in c['added_rows'])),
        genuine_context_counts=dict(Counter(c['genuine_context_status'] for c in contexts)),
        raw_row_counts=dict(Counter(c['raw_row_model_status'] for c in contexts)))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--plan',type=Path,required=True)
    parser.add_argument('--plan-sha256',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    require(not args.output.exists(),'fresh output')
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(5,5))
    started=time.process_time()
    planref=dict(path=str(args.plan.resolve()),sha256=args.plan_sha256)
    plan=pinned(planref); refs=plan['premise_bindings']
    data={k:pinned(v) for k,v in refs.items()}
    for ref in plan['sources']:
        require(pin(ref['path'])['sha256']==ref['sha256'],'pre-run source pin')
    require(data['weak_authority']['status']=='INDEPENDENT_COMPLETE_ALL26_POSITIVE_CONSTRAINT_INVENTORY_ACCEPTED'
            and any(s['sha256']==refs['weak_inventory']['sha256'] for s in data['weak_authority']['sources']),
            'accepted weak inventory')
    require(data['parent_acceptance']['status']=='ACCEPTED_NECESSARY_GENUINE_SIGNED_STAR_LINK_RESTRICTIONS'
            and data['parent_acceptance']['accepted']['positive_exact']['authority']['sha256']==refs['positive_structure_authority']['sha256']
            and data['parent_acceptance']['accepted']['all_tip_profiles']['authority']['sha256']==refs['link_profile_authority']['sha256'],
            'accepted mathematical premises')
    require(data['positive_structure_authority']['signed_star_consequences']['positive_tip_graph_degree']==7
            and data['link_profile_authority']['necessary_nonroot_degrees']==
            dict(positive_tip=[7],negative_tip=[9,10,11],ordinary=[6,7,8,9,10,12]),
            'exact degree-set contract')
    require(data['weak_inventory']['premise_bindings']['common']['sha256']==refs['common']['sha256']
            and data['weak_inventory']['premise_bindings']['contexts']['sha256']==refs['contexts']['sha256'],
            'unchanged accepted native sources')
    loading=time.process_time()-started
    result=build(data['weak_inventory'],data['common'],data['contexts'],data['row_authority'],data['frontier'])
    pilot=select_pilot(result['contexts'],plan['pilot_identity'])
    result.update(schema_version=1,status='PROPOSED_COMPLETE_SIGNED_STAR_TIP_STRUCTURE_INVENTORY',
        sources=plan['sources']+[pin(__file__),pin(args.plan)],premise_bindings=refs,plan=planref,
        scope='Necessary genuine signed-star projection only; no old raw-row entailment claim.',
        weak1511_rows_not_appended=True,
        row_order='Perpositive: absence,degree,pairs by neighbor; then negative degrees; then ordinary vertices and neighbor slots. Literal duplicates keep first position with all provenance.',
        terms_order='Increasing numerical support mask; native_term_variable_indices are positions in the unchanged1079-variable list.',
        ordinary_degree11_encoding='For each ordinary v and j != v: -1 <= D_v-2*x_vj <=10. Conjunction exactly forbids degree11 among12 Boolean edge indicators.',
        new_auxiliary_variables=0,full_original_row_models_built=0,
        proposed_pilot=dict(model_id=pilot['model_id'],native_variables=len(data['common']['variables']),
            original_rows=pilot['original_row_count'],added_rows=len(pilot['added_rows']),
            extended_rows=pilot['extended_row_count'],added_terms=pilot['added_nonzero_coefficients'],
            extended_terms=pilot['extended_nonzero_coefficients'],
            setup_stop_CPU_seconds=4,generation_CPU_budget_seconds=10,
            total_CPU_soft_seconds=14,total_CPU_hard_seconds=15,wall_seconds=40,AS_bytes=512*1024**2,
            target_propagation_authorized=False,required_independent_gate='cycle1519'),
        source_loading_CPU_seconds=loading,source_only_CPU_seconds=time.process_time()-started,
        peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        target_propagation_queries=0,solver_queries=0,new_context_exclusions=0,
        actual_derivative_constructed=False,whole_pattern_excluded=False,global_goal_complete=False)
    for ref in result['sources']:
        require(pin(ref['path'])['sha256']==ref['sha256'],'post-run source pin')
    with args.output.open('x') as stream:
        json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('status','model_count','total_distinct_added_rows',
        'total_duplicate_row_occurrences','total_added_nonzero_coefficients','source_only_CPU_seconds','peak_RSS_bytes')}))


if __name__=='__main__':main()
