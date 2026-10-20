"""Independently rebuild all whole-case equations and any exact contradiction."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import resource
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from first_case_spectrum_scope import input_scope,CaseScope
from literal_bounded_core_spectrum_rows import LiteralBoundedSpectrumRows
from literal_primitive_rows import LiteralPrimitiveRows

H=Path(__file__).resolve().parent


def run(model_path,run_path,output,memory_mib):
    assert not output.exists(); start=monotonic()
    resource.setrlimit(resource.RLIMIT_AS,(memory_mib<<20,memory_mib<<20))
    b=Bindings(); source=b.read(model_path)
    assert source['status']=='PROPOSED_FIRST_CASE_FULL_SPECTRUM_MODEL' and source['result_status']=='MODEL_ONLY'
    assert not source['solver_run']; scope=CaseScope.from_data(source['scope'])
    proof=read_certificate(b,source['proof']); assert proof['scope']==scope.to_data()
    ref=source['input_authority']; authority=b.read(ref['path'],ref['sha256'])
    assert input_scope(authority)==scope and proof['input_authority']==ref
    assert source['input_source']==proof['input_source']==authority['source']
    ref=authority['source']; inputs=b.read(ref['path'],ref['sha256']); p=read_certificate(b,inputs['proof'])
    assert inputs['scope']==p['scope']==scope.to_data() and proof['include_moments'] is True
    singletons=sorted(c['support'] for c in p['projected_coefficients'] if c['support'].bit_count()==1)
    assert singletons==[1<<i for i in range(14)]
    assert proof['totals']==[dict(supports=singletons,target=16)]; blocks=[]
    for record in p['blocks']:
        ref=record['values']; b.bind(ref['path'],ref['sha256']); values=np.load(ref['path'],allow_pickle=False)
        assert list(values.shape)==ref['shape'] and str(values.dtype)==ref['dtype']
        blocks.append((tuple(record['features']),values))
    base=LiteralBoundedSpectrumRows(p['word_pools'],blocks,p['projected_coefficients'],proof['totals'],include_moments=True)
    assert base.coefficient_records()==proof['coefficients'] and base.partition_records()==proof['partitions']
    model=LiteralPrimitiveRows(base); cost=base.inventory()
    assert source['model_inventory']==proof['model_inventory'] and all(source['model_inventory'][k]==v for k,v in cost.items())
    assert list(model.divisors)==proof['divisors']
    assert model.scaling_inventory()==proof['scaling_inventory']==source['scaling_inventory']
    matrix=read_certificate(b,proof['primitive_matrix']); assert len(matrix)==model.row_count
    for i,saved in enumerate(matrix):
        terms,lower,upper=model.row(i)
        assert saved==[lower,upper,[[j,a] for j,a in sorted(terms.items())]]
    del matrix
    print(json.dumps(dict(stage='all_literal_rows_equal_saved_matrix',scope=scope.to_data(),
                         rows=model.row_count,variables=model.variable_count,seconds=monotonic()-start)),flush=True)
    rhs=None; result_status='MODEL_ONLY'; run_reference=None; numerical_status=None
    if run_path is not None:
        executed=b.read(run_path); assert executed['status']=='PROPOSED_FIRST_CASE_FULL_SPECTRUM_LP_RUN'
        assert executed['scope']==scope.to_data() and executed['model_source']==b.bind(model_path)
        ref=executed['model_authority']; prior=b.read(ref['path'],ref['sha256'])
        assert prior['status']=='INDEPENDENTLY_VERIFIED_FIRST_CASE_FULL_SPECTRUM_MODEL'
        assert prior['all_original_rows_and_divisors_rebuilt'] and prior['saved_primitive_matrix_equal_literal_rows']
        assert prior['scope']==scope.to_data() and prior['model_source']==b.bind(model_path)
        result_proof=read_certificate(b,executed['proof'])
        assert result_proof['scope']==scope.to_data() and result_proof['model_source']==b.bind(model_path)
        assert result_proof['model_authority']==executed['model_authority']
        assert result_proof['primitive_matrix']==proof['primitive_matrix']
        result=result_proof['result']; result_status=result['status']; assert result_status==executed['result_status']
        assert result_status in {'INCONCLUSIVE_BOX_ROW_LP','NUMERICALLY_FEASIBLE_BOX_RELAXATION',
                                'RESOURCE_GUARD_MODEL_ESTIMATE','RESOURCE_LIMIT_MEMORY','EXACT_BOX_ROW_LP_CONTRADICTION'}
        if result_status=='EXACT_BOX_ROW_LP_CONTRADICTION': rhs=model.verify(result['certificate'])
        assert executed['whole_first_case_excluded_claim']==(rhs is not None)
        numerical_status=result.get('highs_model_status'); run_reference=b.bind(run_path)
    for name in ('verify_first_case_spectrum_lp.py','first_case_spectrum_scope.py','test_first_case_spectrum_scope.py',
                 'literal_primitive_rows.py','test_literal_primitive_rows.py','literal_bounded_core_spectrum_rows.py',
                 'test_literal_bounded_core_spectrum_rows.py','literal_categorical_core_slice_rows.py',
                 'literal_core_slice_rows.py','full_outside_spectrum_soundness_cycle526.md'): b.bind(H/name)
    result=dict(schema_version=1,status='INDEPENDENTLY_VERIFIED_FIRST_CASE_FULL_SPECTRUM_MODEL',global_status='UNRESOLVED',
        scope=scope.to_data(),model_source=b.bind(model_path),run_source=run_reference,
        input_authority=source['input_authority'],input_source=source['input_source'],
        input_cover_replayed_in_this_run=False,input_cover_independent_authority_referenced=True,
        all_original_rows_and_divisors_rebuilt=True,saved_primitive_matrix_equal_literal_rows=True,
        complete_distribution_partitions_rebuilt=True,all_projected_coefficient_domains_rebuilt=True,
        all_value_moment_and_budget_rows_rebuilt=True,model_inventory=cost,scaling_inventory=model.scaling_inventory(),
        result_status=result_status,numerical_solver_status=numerical_status,numerical_status_independently_reexecuted=False,
        exact_integer_rhs=rhs,exact_certificate_verified=rhs is not None,whole_first_case_excluded=rhs is not None,
        whole_geometry_excluded=False,actual_boolean_function=False,global_goal_complete=False,
        producer_imported=False,producer_row_generator_imported=False,producer_row_normalizer_imported=False,
        numerical_lp_solver_imported=False,seconds=monotonic()-start,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream: json.dump(result,stream,indent=2); stream.write('\n')
    print(json.dumps({k:result[k] for k in ('scope','result_status','exact_integer_rhs','whole_first_case_excluded','seconds')}),flush=True)


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__); parser.add_argument('--model',type=Path,required=True)
    parser.add_argument('--run',type=Path); parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--memory-mib',type=int,default=4096); a=parser.parse_args()
    run(a.model,a.run,a.output,a.memory_mib)
