"""Restore the saved compacted LP buffers, then try exact original-row arithmetic."""
from argparse import ArgumentParser
from datetime import datetime,timezone
from pathlib import Path
from time import monotonic
import json
import resource
import sys
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from core_slice_degree_lp import PatternBlock
from selfdual_core_projection import ProjectedCoefficient
from bounded_core_spectrum_lp import CoefficientTotal,prepare
from primitive_box_rows import primitive_row
from raw_box_ipm import phase_one,reconstruct
from raw_highs_postsolve import restore

H=Path(__file__).resolve().parent


def run(authority_path,output,memory_mib):
    assert not output.exists();start=monotonic();started=datetime.now(timezone.utc).isoformat();b=Bindings()
    resource.setrlimit(resource.RLIMIT_AS,(memory_mib<<20,memory_mib<<20))
    authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_PRIMITIVE_FULL_OUTSIDE_SPECTRUM_LP_MODEL'
    assert authority['all_original_rows_and_divisors_rebuilt']
    ref=authority['source'];prior=b.read(ref['path'],ref['sha256']);previous=read_certificate(b,prior['proof'])
    ref=prior['original_model'];original=b.read(ref['path'],ref['sha256']);old=read_certificate(b,original['proof'])
    ref=prior['input_source'];inputs=b.read(ref['path'],ref['sha256']);p=read_certificate(b,inputs['proof'])
    blocks=[]
    for record in p['blocks']:
        ref=record['values'];b.bind(ref['path'],ref['sha256']);values=np.load(ref['path'],allow_pickle=False)
        assert list(values.shape)==ref['shape'] and str(values.dtype)==ref['dtype']
        blocks.append(PatternBlock(tuple(record['features']),values))
    coefficients=[ProjectedCoefficient(r['feature'],r['character'],r['support'],tuple(r['values'])) for r in p['projected_coefficients']]
    totals=[CoefficientTotal(tuple(t['supports']),t['target']) for t in old['totals']]
    model=prepare(p['word_pools'],blocks,coefficients,totals=totals)
    assert model.inventory()==prior['model_inventory'] and model.coefficient_records()==old['coefficients']
    rows=[];divisors=[]
    for row in model.rows():
        normalized,divisor=primitive_row(row);rows.append(normalized);divisors.append(divisor)
    assert divisors==previous['divisors']
    raw_report=b.read(prior['numerical_report']['path'],prior['numerical_report']['sha256'])
    assert raw_report['method']=='direct-bundled-highs-ipm' and raw_report['parameters']['presolve']=='on'
    def load(ref):
        b.bind(ref['path'],ref['sha256']);a=np.load(ref['path'],allow_pickle=False)
        assert list(a.shape)==ref['shape'] and str(a.dtype)==ref['dtype'];return a
    raw_x=np.r_[load(prior['candidate']['vector']),raw_report['candidate']['phase_slack']]
    raw_duals=load(prior['dual_candidate'])
    print(json.dumps(dict(stage='restoring_saved_buffers',variables=model.variable_count,rows=len(rows),seconds=monotonic()-start)),flush=True)
    recovered=restore(phase_one(rows,model.variable_count),raw_x,raw_duals,display=True)
    numerical_path=output.with_suffix('.numerical.json')
    with numerical_path.open('x') as stream:json.dump(recovered['report'],stream,indent=2,allow_nan=False);stream.write('\n')
    vector_path=output.with_suffix('.primal.npy');dual_path=output.with_suffix('.dual.npy')
    np.save(vector_path,recovered['values'][:-1],allow_pickle=False);np.save(dual_path,recovered['duals'],allow_pickle=False)
    candidate=dict(vector=dict(**b.bind(vector_path),shape=[model.variable_count],dtype=str(recovered['values'].dtype)),
        variables=prior['candidate']['variables'],exact_boolean_function_verified=False)
    dual_candidate=dict(**b.bind(dual_path),shape=list(recovered['duals'].shape),dtype=str(recovered['duals'].dtype),exact_certificate=False)
    result=reconstruct(rows,model.variable_count,recovered['duals'])
    result.update(method='saved-candidate-explicit-postsolve',numerical_diagnostics=recovered['report'],optimizer_run=False)
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(original_model_authority=prior['original_model_authority'],original_model=prior['original_model'],
        prior_raw_authority=b.bind(authority_path),prior_raw_source=authority['source'],divisors=divisors,
        scaling_inventory=prior['scaling_inventory'],model_inventory=prior['model_inventory'],result=result,candidate=candidate,
        dual_candidate=dual_candidate,numerical_report=b.bind(numerical_path)))
    for name in ('recover_saved_primitive_spectrum.py','raw_highs_postsolve.py','test_raw_highs_postsolve.py',
                 'raw_box_ipm.py','postsolve_recovery_cycle559_plan.md'):b.bind(H/name)
    result_keys=('geometry_index','first_row','group_index','original_model_authority','original_model','input_authority',
        'input_source','model_inventory','scaling_inventory')
    proposal=dict(schema_version=1,status='PROPOSED_PRIMITIVE_FULL_OUTSIDE_SPECTRUM_LP',global_status='UNRESOLVED',
        **{k:prior[k] for k in result_keys},prior_raw_authority=b.bind(authority_path),prior_raw_source=authority['source'],
        proof=b.bind(proof_path),result_status=result['status'],candidate=candidate,dual_candidate=dual_candidate,numerical_report=b.bind(numerical_path),
        conditional_product_group_excluded_claim=result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION',independent_audit='PENDING',
        whole_first_case_excluded=False,actual_boolean_function=False,whole_geometry_excluded=False,global_goal_complete=False,
        parameters=dict(memory_mib=memory_mib,method='saved-candidate-explicit-postsolve',optimizer_run=False),
        started_at=started,finished_at=datetime.now(timezone.utc).isoformat(),seconds=monotonic()-start,
        process_peak_resident_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,argv=sys.argv,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(proposal,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(dict(result={k:v for k,v in result.items() if k!='certificate'},seconds=proposal['seconds'],
        process_peak_resident_kib=proposal['process_peak_resident_kib'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--authority',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--memory-mib',type=int,default=4096)
    a=p.parse_args();run(a.authority,a.output,a.memory_mib)
