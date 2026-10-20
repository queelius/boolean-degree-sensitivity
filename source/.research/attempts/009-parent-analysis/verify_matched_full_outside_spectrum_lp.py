"""Reconstruct full spectral and moment rows on independently certified inputs."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from literal_bounded_core_spectrum_rows import LiteralBoundedSpectrumRows

H=Path(__file__).resolve().parent


def run(source_path,output):
    assert not output.exists();start=monotonic();b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_MATCHED_FULL_OUTSIDE_SPECTRUM_LP';proof=read_certificate(b,source['proof'])
    ref=source['input_authority'];authority=b.read(ref['path'],ref['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FULL_OUTSIDE_INPUTS' and not authority['empty_points']
    assert authority['complete_original_pattern_cover'] and authority['complete_word_pool_cover'] and authority['complete_projected_coefficient_cover']
    assert source['input_source']==authority['source']==proof['input_source'] and proof['input_authority']==ref
    original=b.read(source['input_source']['path'],source['input_source']['sha256']);p=read_certificate(b,original['proof'])
    for key in ('base_authority','zero_product_authority','quotient_authority','refinement_authority',
                'geometry_index','first_row','group_index'):assert source[key]==original[key]==authority[key]
    assert proof['include_moments'] is True
    singletons=sorted(c['support'] for c in p['projected_coefficients'] if c['support'].bit_count()==1)
    assert singletons==[1<<i for i in range(14)]
    totals=[dict(supports=singletons,target=16)];assert proof['totals']==totals
    blocks=[]
    for record in p['blocks']:
        ref=record['values'];b.bind(ref['path'],ref['sha256']);values=np.load(ref['path'],allow_pickle=False)
        assert list(values.shape)==ref['shape'] and str(values.dtype)==ref['dtype']
        blocks.append((tuple(record['features']),values))
    model=LiteralBoundedSpectrumRows(p['word_pools'],blocks,p['projected_coefficients'],totals,include_moments=True)
    assert model.coefficient_records()==proof['coefficients'] and model.partition_records()==proof['partitions']
    cost=model.inventory();assert source['model_inventory']==proof['model_inventory']
    assert all(source['model_inventory'][k]==v for k,v in cost.items())
    result=proof['result'];assert result['status']==source['result_status']
    assert result['status'] in {'INCONCLUSIVE_BOX_ROW_LP','NUMERICALLY_FEASIBLE_BOX_RELAXATION',
        'RESOURCE_GUARD_MODEL_ESTIMATE','RESOURCE_LIMIT_MEMORY','EXACT_BOX_ROW_LP_CONTRADICTION'}
    integer_rhs=None;excluded=False
    if result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION':integer_rhs=model.verify(result['certificate']);excluded=True
    assert source['conditional_product_group_excluded_claim']==excluded
    for name in ('verify_matched_full_outside_spectrum_lp.py','literal_bounded_core_spectrum_rows.py',
                 'test_literal_bounded_core_spectrum_rows.py','literal_categorical_core_slice_rows.py','literal_core_slice_rows.py',
                 'verify_matched_full_outside_inputs.py','full_outside_spectrum_soundness_cycle526.md'):
        b.bind(H/name)
    accepted=dict(schema_version=1,status='INDEPENDENTLY_VERIFIED_MATCHED_FULL_OUTSIDE_SPECTRUM_LP_MODEL',global_status='UNRESOLVED',
        geometry_index=source['geometry_index'],first_row=source['first_row'],group_index=source['group_index'],
        source=b.bind(source_path),input_authority=source['input_authority'],input_source=source['input_source'],
        input_cover_replayed_in_this_run=False,input_cover_independent_authority_referenced=True,
        complete_distribution_partitions_rebuilt=True,all_projected_coefficient_domains_rebuilt=True,
        all_value_moment_and_budget_rows_rebuilt=True,model_inventory=cost,result_status=result['status'],
        numerical_status_independently_reexecuted=False,exact_integer_rhs=integer_rhs,exact_certificate_verified=integer_rhs is not None,
        conditional_product_group_excluded=excluded,whole_first_case_excluded=False,actual_boolean_function=False,
        whole_geometry_excluded=False,global_goal_complete=False,producer_imported=False,
        producer_row_generator_imported=False,numerical_lp_solver_imported=False,seconds=monotonic()-start,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(accepted,stream,indent=2);stream.write('\n')
    print(json.dumps({k:accepted[k] for k in ('result_status','exact_integer_rhs',
        'conditional_product_group_excluded','model_inventory','seconds')}),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
