"""One bounded source-only inventory and read-only resource measurement."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time

from positive_tip_inventory_cycle1511 import identity, inventory, require


def pin(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    return dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))


def pinned(ref):
    actual = pin(ref['path'])
    require(actual['sha256'] == ref['sha256'] and
            ('bytes' not in ref or actual['bytes'] == ref['bytes']), 'changed source')
    return json.loads(Path(ref['path']).read_bytes())


def select_pilot(contexts, wanted):
    matches = [c for c in contexts if
               (c['model_id']['native_identity']['order'],
                c['model_id']['native_identity']['original_index'],
                c['model_id']['constant']) ==
               (wanted['order'], wanted['original_index'], wanted['constant'])]
    require(len(matches) == 1 and matches[0]['genuine_context_status'] == 'OPEN' and
            matches[0]['skip_future_queries'] is False, 'sole open requested pilot')
    return matches[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--plan-sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'fresh output required')
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2, 512 * 1024**2))
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    start = time.process_time()
    plan_ref = dict(path=str(args.plan.resolve()), sha256=args.plan_sha256)
    plan = pinned(plan_ref)
    require(plan['status'] == 'SOURCE_ONLY_INVENTORY_NO_TARGET_PROPAGATION_AUTHORIZED',
            'source-only plan')
    refs = plan['premise_bindings']
    objects = {key: pinned(ref) for key, ref in refs.items()}
    for ref in plan['sources']:
        require(pin(ref['path'])['sha256'] == ref['sha256'], 'changed plan source')
    common, packet, gate, frontier = (objects[k] for k in
                                    ('common', 'contexts', 'row_authority', 'frontier'))
    require(gate['status'] == 'INDEPENDENTLY_VERIFIED_NATIVE26_SIGNED_STAR_FULL_P_ROWS'
            and gate['models_compared'] == 26 and common['n'] == 13, 'accepted native domain')
    require(gate['common_source']['sha256'] == refs['common']['sha256'] and
            gate['context_source']['sha256'] == refs['contexts']['sha256'], 'accepted source link')
    require(objects['absence_parent']['status'] == 'ACCEPTED_GENERAL_WRITTEN_STRUCTURAL_THEOREM'
            and objects['absence_parent']['independent_authority']['sha256'] ==
            refs['absence_authority']['sha256'], 'accepted absence theorem')
    require(objects['degree_authority']['new_written_conclusions']['positive_tip_minimum_degree'] == 7
            and objects['degree_parent']['positive_tip_minimum_degree'] == 7,
            'accepted lower degree bound')
    require(objects['sphere_parent']['status'] ==
            'PARENT_ACCEPTED_SIGNED_STAR_CONNECTED_3SPHERE_NECESSARY_THEOREM',
            'genuine sphere premise')
    loading_cpu = time.process_time() - start
    result = inventory(common, packet, gate, frontier)
    pilot = select_pilot(result['contexts'], plan['pilot_identity'])
    derived_cpu = time.process_time() - start - loading_cpu
    previous = objects['previous_context_first_terminal']
    result.update(schema_version=1,
        status='PROPOSED_COMPLETE_POSITIVE_TIP_CONSTRAINT_INVENTORY',
        plan=plan_ref, premise_bindings=refs, sources=plan['sources'] + [pin(__file__), pin(args.plan)],
        index_convention='All variable and row indices are zero-based original native indices; no SAT IDs.',
        appended_row_order='All positive-tip opposite-triangle units by increasing tip, then degree-lower-bound rows in the same tip order.',
        theorem_contracts=dict(
            absence='Genuine PL3sphere; positive edge valence3; all three opposite edges ordinary valence4/5; minimum degree6. Opposite triangle absent.',
            degree='Every vertex link S2; positive tip incident with exactly one valence3 exceptional edge and all other edges valence4/5; minimum degree6. Tip degree at least7.',
            exact_degree_seven_established_by_this_packet=False,
            old_raw_rows_entail_new_constraints_established=False,
            complete_native_domain_inherited_from_1431=True),
        proposed_pilot=dict(model_id=pilot['model_id'],
            original_variables=len(common['variables']), original_rows=pilot['original_row_count'],
            added_rows=len(pilot['added_rows']), extended_rows=pilot['extended_row_count'],
            added_terms=sum(len(r['terms']) for r in pilot['added_rows']),
            original_terms=next(c['expanded_nonzero_coefficients'] for c in packet['contexts']
                                if identity(c['model_id']) == identity(pilot['model_id'])),
            new_row_ids=pilot['added_row_native_ids'],
            previous_generation_CPU_seconds=previous['generation_CPU_seconds'],
            previous_setup_CPU_seconds=previous['setup_CPU_seconds'],
            previous_peak_RSS_bytes=previous['peak_RSS_bytes'],
            forecast_kind='Historical same-dimension scheduling prior, not a target propagation runtime guarantee.',
            proposed_generation_CPU_budget_seconds=10,
            proposed_setup_stop_CPU_seconds=4,
            proposed_total_process_CPU_soft_seconds=14,
            proposed_total_process_CPU_hard_seconds=15,
            proposed_wall_seconds=40, proposed_AS_bytes=512*1024**2,
            propagation_authorized=False,
            independent_inventory_gate_required='cycle1512', parent_authorization_required=True),
        source_loading_CPU_seconds=loading_cpu, inventory_derivation_CPU_seconds=derived_cpu,
        source_only_CPU_seconds=time.process_time()-start,
        peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        propagation_queries=0, SAT_queries=0, LP_queries=0, MILP_queries=0,
        constraints_applied_to_target=False, new_context_exclusions=0,
        actual_derivative_constructed=False, whole_pattern_excluded=False, global_goal_complete=False)
    for ref in result['sources']:
        require(pin(ref['path'])['sha256'] == ref['sha256'], 'post-run source changed')
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2); stream.write('\n')
    print(json.dumps({k: result[k] for k in
          ('status', 'model_count', 'positive_tip_count', 'added_row_count',
           'genuine_context_counts', 'source_only_CPU_seconds', 'peak_RSS_bytes')}))


if __name__ == '__main__':
    main()
