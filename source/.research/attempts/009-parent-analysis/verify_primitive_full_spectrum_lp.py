"""Independent primitive rows and Farkas arithmetic on the accepted full model."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from literal_bounded_core_spectrum_rows import LiteralBoundedSpectrumRows
from literal_primitive_rows import LiteralPrimitiveRows

H=Path(__file__).resolve().parent


def run(source_path,output):
    assert not output.exists();start=monotonic();b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_PRIMITIVE_FULL_OUTSIDE_SPECTRUM_LP';proof=read_certificate(b,source['proof'])
    ref=source['original_model_authority'];authority=b.read(ref['path'],ref['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FULL_OUTSIDE_SPECTRUM_LP_MODEL'
    assert authority['all_value_moment_and_budget_rows_rebuilt'] and authority['complete_distribution_partitions_rebuilt']
    assert source['original_model']==authority['source']==proof['original_model']
    assert proof['original_model_authority']==source['original_model_authority']
    original=b.read(source['original_model']['path'],source['original_model']['sha256']);old=read_certificate(b,original['proof'])
    for key in ('geometry_index','first_row','group_index','input_authority','input_source'):assert source[key]==original[key]==authority[key]
    inputs=b.read(source['input_source']['path'],source['input_source']['sha256']);p=read_certificate(b,inputs['proof'])
    assert old['include_moments'] is True;singletons=sorted(c['support'] for c in p['projected_coefficients'] if c['support'].bit_count()==1)
    assert singletons==[1<<i for i in range(14)] and old['totals']==[dict(supports=singletons,target=16)]
    blocks=[]
    for record in p['blocks']:
        ref=record['values'];b.bind(ref['path'],ref['sha256']);values=np.load(ref['path'],allow_pickle=False)
        assert list(values.shape)==ref['shape'] and str(values.dtype)==ref['dtype']
        blocks.append((tuple(record['features']),values))
    base=LiteralBoundedSpectrumRows(p['word_pools'],blocks,p['projected_coefficients'],old['totals'],include_moments=True)
    assert base.coefficient_records()==old['coefficients'] and base.partition_records()==old['partitions']
    model=LiteralPrimitiveRows(base)
    assert list(model.divisors)==proof['divisors']
    assert model.scaling_inventory()==proof['scaling_inventory']==source['scaling_inventory']
    assert source['model_inventory']==proof['model_inventory']==original['model_inventory']
    assert source['model_inventory']['variables']==model.variable_count and source['model_inventory']['rows']==model.row_count
    assert source['model_inventory']['nonzeros']==model.nonzeros
    result=proof['result'];assert result['status']==source['result_status']
    assert result['status'] in {'INCONCLUSIVE_BOX_ROW_LP','NUMERICALLY_FEASIBLE_BOX_RELAXATION',
        'RESOURCE_GUARD_MODEL_ESTIMATE','RESOURCE_LIMIT_MEMORY','EXACT_BOX_ROW_LP_CONTRADICTION'}
    integer_rhs=None;excluded=False
    if result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION':integer_rhs=model.verify(result['certificate']);excluded=True
    assert source['conditional_product_group_excluded_claim']==excluded
    for name in ('verify_primitive_full_spectrum_lp.py','literal_primitive_rows.py','test_literal_primitive_rows.py',
                 'literal_bounded_core_spectrum_rows.py','literal_categorical_core_slice_rows.py','literal_core_slice_rows.py',
                 'primitive_full_spectrum_ipm_cycle535_plan.md'):b.bind(H/name)
    accepted=dict(schema_version=1,status='INDEPENDENTLY_VERIFIED_PRIMITIVE_FULL_OUTSIDE_SPECTRUM_LP_MODEL',global_status='UNRESOLVED',
        geometry_index=source['geometry_index'],first_row=source['first_row'],group_index=source['group_index'],
        source=b.bind(source_path),original_model_authority=source['original_model_authority'],original_model=source['original_model'],
        input_authority=source['input_authority'],input_source=source['input_source'],input_cover_replayed_in_this_run=False,
        all_original_rows_and_divisors_rebuilt=True,model_inventory=source['model_inventory'],scaling_inventory=model.scaling_inventory(),
        result_status=result['status'],numerical_status_independently_reexecuted=False,exact_integer_rhs=integer_rhs,
        exact_certificate_verified=integer_rhs is not None,conditional_product_group_excluded=excluded,
        whole_first_case_excluded=False,actual_boolean_function=False,whole_geometry_excluded=False,global_goal_complete=False,
        producer_imported=False,producer_row_normalizer_imported=False,numerical_lp_solver_imported=False,seconds=monotonic()-start,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(accepted,stream,indent=2);stream.write('\n')
    print(json.dumps({k:accepted[k] for k in ('result_status','exact_integer_rhs','conditional_product_group_excluded',
        'scaling_inventory','seconds')}),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
