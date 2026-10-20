"""Transfer an exact complete-case functional onto other verified open domains."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import resource
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from first_case_spectrum_scope import CaseScope,input_scope
from core_slice_degree_lp import PatternBlock
from selfdual_core_projection import ProjectedCoefficient
from bounded_core_spectrum_lp import CoefficientTotal,prepare
from primitive_box_rows import primitive_row
from spectrum_dual_functional import lift_multipliers,compile_functional,simplex_bound
from propagated_spectrum_minimum import minimum
from matched_component_frontier import guarded_words
from read_matched_cross_arrays import load

H=Path(__file__).resolve().parent


def run(authority_path,frontier_path,propagation_paths,first_rows,output,memory_mib):
    assert not output.exists(); start=monotonic()
    resource.setrlimit(resource.RLIMIT_AS,(memory_mib<<20,memory_mib<<20))
    b=Bindings(); authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_FIRST_CASE_FULL_SPECTRUM_MODEL'
    assert authority['exact_certificate_verified'] and authority['whole_first_case_excluded']
    assert authority['result_status']=='EXACT_BOX_ROW_LP_CONTRADICTION' and authority['exact_integer_rhs']<0
    scope=CaseScope.from_data(authority['scope']); ref=authority['input_authority']; accepted_inputs=b.read(ref['path'],ref['sha256'])
    assert input_scope(accepted_inputs)==scope and accepted_inputs['source']==authority['input_source']
    ref=authority['model_source']; source=b.read(ref['path'],ref['sha256']); model_proof=read_certificate(b,source['proof'])
    ref=authority['run_source']; executed=b.read(ref['path'],ref['sha256']); run_proof=read_certificate(b,executed['proof'])
    assert executed['model_source']==authority['model_source'] and executed['scope']==scope.to_data()
    ref=authority['input_source']; inputs=b.read(ref['path'],ref['sha256']); p=read_certificate(b,inputs['proof'])
    assert source['scope']==model_proof['scope']==p['scope']==scope.to_data()
    assert model_proof['include_moments'] is True; blocks=[]
    for record in p['blocks']:
        ref=record['values']; b.bind(ref['path'],ref['sha256']); values=np.load(ref['path'],allow_pickle=False)
        assert list(values.shape)==ref['shape'] and str(values.dtype)==ref['dtype']
        blocks.append(PatternBlock(tuple(record['features']),values))
    coefficients=[ProjectedCoefficient(c['feature'],c['character'],c['support'],tuple(c['values'])) for c in p['projected_coefficients']]
    totals=[CoefficientTotal(tuple(t['supports']),t['target']) for t in model_proof['totals']]
    model=prepare(p['word_pools'],blocks,coefficients,totals=totals,include_moments=True); rows=list(model.rows())
    assert model.coefficient_records()==model_proof['coefficients'] and model.base.partition_records()==model_proof['partitions']
    matrix=read_certificate(b,model_proof['primitive_matrix']); assert len(rows)==len(matrix)==len(model_proof['divisors'])
    for row,saved,divisor in zip(rows,matrix,model_proof['divisors']):
        normalized,d=primitive_row(row); assert d==divisor
        assert saved==[normalized.lower,normalized.upper,[[j,a] for j,a in sorted(normalized.terms)]]
    del matrix
    certificate=run_proof['result']['certificate']; assert certificate['integer_rhs']==authority['exact_integer_rhs']
    scale,weights=lift_multipliers(model_proof['divisors'],certificate['terms'])
    functional=compile_functional(rows,model.variable_count,weights)
    base=model.base.basis.base; word_costs=[[] for _ in p['word_pools']]
    for i,v in enumerate(model.variables[:base.word_variable_count]):
        cost=functional.word_score(v['outside_point'],v['features']); assert cost==functional.coefficients[i]
        word_costs[v['outside_point']].append(cost)
    pattern_costs=[]
    for block,(record,offset) in enumerate(zip(blocks,base.block_offsets)):
        costs=functional.pattern_scores(block,record.values,record.features)
        assert list(map(int,costs))==list(functional.coefficients[offset:offset+len(record.values)])
        pattern_costs.append(costs)
    flags=[functional.coefficients[i] for i,v in enumerate(model.variables) if v['kind']=='full_spectral_flag']
    original=simplex_bound(word_costs+pattern_costs,flags,functional.rhs)
    assert original['contradiction'] and original['gap']>=-scale*authority['exact_integer_rhs']
    print(json.dumps(dict(stage='original_rows_and_columns_verified',scale=scale,variables=model.variable_count,
                         rows=len(rows),original_gap=original['gap'],seconds=monotonic()-start)),flush=True)
    frontier=b.read(frontier_path)
    assert frontier['status']=='VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER'
    assert frontier['scope']['geometry_index']==scope.geometry_index
    assert frontier['scope']['quotient_authority']==scope.to_data()['quotient_authority']
    assert first_rows and len(first_rows)==len(set(first_rows)) and set(first_rows)<=set(frontier['remaining_first_rows'])
    selected={}; refinement=None; authorities=[]
    for path in propagation_paths:
        prop=b.read(path); assert prop['status']=='INDEPENDENTLY_VERIFIED_MATCHED_WHOLE_FAMILY_DELETIONS'
        assert prop['geometry_index']==scope.geometry_index and prop['quotient_authority']==scope.to_data()['quotient_authority']
        if refinement is None: refinement=prop['refinement_authority']
        assert refinement==prop['refinement_authority']
        ref=prop['source']; old=b.read(ref['path'],ref['sha256'])
        assert old['refinement_authority']==refinement
        assert [r['first_row'] for r in prop['records']]==[r['first_row'] for r in old['records']]
        for accepted,record in zip(prop['records'],old['records']):
            first=record['first_row']
            if first not in first_rows: continue
            assert first not in selected and not accepted['conditional_case_excluded']
            domain_proof=read_certificate(b,record['proof'])
            assert domain_proof['first_row']==first and list(map(len,domain_proof['final_domains']))==accepted['final_domain_sizes']
            selected[first]=(b.bind(path),record['proof'],domain_proof)
        authorities.append(b.bind(path))
    assert set(selected)==set(first_rows)
    data=load(b,refinement['path']); assert b.bind(refinement['path'])==refinement
    assert data.quotient_reference==scope.to_data()['quotient_authority']
    instance=read_certificate(b,data.quota['instance'])
    assert instance['geometry']==p['geometry'] and instance['outside']==p['outside']
    points=len(p['word_pools']); assert points==512
    features=instance['core_pair_order']; marked=data.quota['component_index']
    pools=[guarded_words(x.bit_count(),1-(x&1)-((x>>1)&1)) for x in range(points)]; records=[]
    for first in first_rows:
        prop_ref,domain_ref,domain_proof=selected[first]
        candidate=data.quota['selected_row_indices'].index(first)
        assert domain_proof['parent_candidate_index']==candidate
        final=domain_proof['final_domains']; assert final[marked]==[candidate]
        initial=[list(range(len(t))) for t in data.tables]; initial[marked]=[candidate]
        before=minimum(functional,data.tables,initial,features,pools,flags)
        after=minimum(functional,data.tables,final,features,pools,flags)
        if after['bound'] is not None: assert before['bound'] is not None and after['bound']['gap']>=before['bound']['gap']
        record=dict(first_row=first,propagation_authority=prop_ref,domain_proof=domain_ref,
            retained_domain_sizes=list(map(len,final)),before=before,after=after)
        records.append(record)
        print(json.dumps(dict(stage='transfer_minimum',first_row=first,retained_domain_sizes=record['retained_domain_sizes'],
            gap=None if after['bound'] is None else after['bound']['gap'],candidate_contradiction=after['candidate_contradiction'],
            seconds=monotonic()-start)),flush=True)
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(source_scope=scope.to_data(),exact_authority=b.bind(authority_path),
        frontier_authority=b.bind(frontier_path),propagation_authorities=authorities,scale=scale,row_weights=list(weights),
        original_bound=original,records=records))
    for name in ('probe_first_case_spectrum_transfer.py','first_case_spectrum_scope.py','test_first_case_spectrum_scope.py',
                 'primitive_box_rows.py','spectrum_dual_functional.py','test_spectrum_dual_functional.py',
                 'propagated_spectrum_minimum.py','test_propagated_spectrum_minimum.py',
                 'read_matched_cross_arrays.py','matched_component_frontier.py'): b.bind(H/name)
    result=dict(schema_version=1,status='PROPOSED_COMPLETE_FIRST_CASE_SPECTRUM_TRANSFER',global_status='UNRESOLVED',
        source_scope=scope.to_data(),exact_authority=b.bind(authority_path),frontier_authority=b.bind(frontier_path),
        propagation_authorities=authorities,proof=b.bind(proof_path),original_gap=original['gap'],
        candidate_excluded_first_rows=[r['first_row'] for r in records if r['after']['candidate_contradiction']],
        records=[dict(first_row=r['first_row'],retained_domain_sizes=r['retained_domain_sizes'],
            before_gap=None if r['before']['bound'] is None else r['before']['bound']['gap'],
            after_gap=None if r['after']['bound'] is None else r['after']['bound']['gap'],empty_points=r['after']['empty_points']) for r in records],
        source_case_word_filters_transferred=False,propagation_independently_verified=True,extended_score_independent_audit='PENDING',
        whole_geometry_excluded=False,actual_boolean_function=False,global_goal_complete=False,
        parameters=dict(memory_mib=memory_mib),seconds=monotonic()-start,
        process_peak_resident_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream: json.dump(result,stream,indent=2); stream.write('\n')
    print(json.dumps(dict(records=result['records'],candidate_excluded_first_rows=result['candidate_excluded_first_rows'],
                         seconds=result['seconds'])),flush=True)


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__); parser.add_argument('--authority',type=Path,required=True)
    parser.add_argument('--frontier',type=Path,required=True); parser.add_argument('--propagation-authorities',type=Path,nargs='+',required=True)
    parser.add_argument('--first-rows',type=int,nargs='+',required=True); parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--memory-mib',type=int,default=4096); a=parser.parse_args()
    run(a.authority,a.frontier,a.propagation_authorities,a.first_rows,a.output,a.memory_mib)
