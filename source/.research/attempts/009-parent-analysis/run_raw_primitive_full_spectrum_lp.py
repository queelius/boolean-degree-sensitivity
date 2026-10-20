"""Preserve raw HiGHS duals before exact full-spectrum certificate reconstruction."""
from argparse import ArgumentParser
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from time import monotonic
import gc
import json
import resource
import sys
import numpy as np
import scipy
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from core_slice_degree_lp import PatternBlock
from selfdual_core_projection import ProjectedCoefficient
from bounded_core_spectrum_lp import CoefficientTotal,prepare
from primitive_box_rows import primitive_row
from raw_box_ipm import solve, reconstruct
from scipy.optimize._highspy import _core as highs_core

H=Path(__file__).resolve().parent


def run(authority_path,seconds,memory_mib,output):
    assert not output.exists() and seconds>0 and memory_mib>0
    start=monotonic();started=datetime.now(timezone.utc).isoformat();b=Bindings();limit=memory_mib<<20
    resource.setrlimit(resource.RLIMIT_AS,(limit,limit))
    authority=b.read(authority_path);assert authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FULL_OUTSIDE_SPECTRUM_LP_MODEL'
    ref=authority['source'];original=b.read(ref['path'],ref['sha256']);old=read_certificate(b,original['proof'])
    assert original['input_authority']==authority['input_authority'] and old['include_moments'] is True
    ref=original['input_source'];source=b.read(ref['path'],ref['sha256']);p=read_certificate(b,source['proof']);blocks=[]
    for record in p['blocks']:
        ref=record['values'];b.bind(ref['path'],ref['sha256']);values=np.load(ref['path'],allow_pickle=False)
        assert list(values.shape)==ref['shape'] and str(values.dtype)==ref['dtype']
        blocks.append(PatternBlock(tuple(record['features']),values))
    coefficients=[ProjectedCoefficient(r['feature'],r['character'],r['support'],tuple(r['values'])) for r in p['projected_coefficients']]
    totals=[CoefficientTotal(tuple(t['supports']),t['target']) for t in old['totals']]
    model=prepare(p['word_pools'],blocks,coefficients,totals=totals);cost=model.inventory()
    assert cost==original['model_inventory'] and model.coefficient_records()==old['coefficients']
    rows=[];divisors=[];max_old=max_new=max_old_rhs=max_new_rhs=0
    for row in model.rows():
        normalized,divisor=primitive_row(row);rows.append(normalized);divisors.append(divisor)
        max_old=max(max_old,max((abs(a) for _,a in row.terms),default=0));max_new=max(max_new,max((abs(a) for _,a in normalized.terms),default=0))
        max_old_rhs=max(max_old_rhs,abs(row.lower),abs(row.upper));max_new_rhs=max(max_new_rhs,abs(normalized.lower),abs(normalized.upper))
    assert len(rows)==cost['rows'] and sum(len(r.terms) for r in rows)==cost['nonzeros']
    scaling=dict(divisor_counts=[dict(divisor=d,rows=n) for d,n in sorted(Counter(divisors).items())],
        maximum_original_coefficient=max_old,maximum_primitive_coefficient=max_new,
        maximum_original_bound=max_old_rhs,maximum_primitive_bound=max_new_rhs)
    print(json.dumps(dict(stage='primitive_full_spectrum_inventory',model_inventory=cost,scaling=scaling,seconds=monotonic()-start)),flush=True)
    candidate=None;dual_candidate=None;numerical_report=None
    if cost['estimated_peak_bytes']>limit:
        result=dict(status='RESOURCE_GUARD_MODEL_ESTIMATE',estimated_peak_bytes=cost['estimated_peak_bytes'],proof_verified=False)
    else:
        try:
            answer=solve(rows,model.variable_count,seconds=seconds,display=True);result=answer.report
            raw_path=output.with_suffix('.numerical.json')
            with raw_path.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
            numerical_report=b.bind(raw_path)
            if answer.row_dual is not None:
                dual_path=output.with_suffix('.dual.npy');assert not dual_path.exists()
                np.save(dual_path,answer.row_dual,allow_pickle=False)
                dual_candidate=dict(**b.bind(dual_path),shape=list(answer.row_dual.shape),dtype=str(answer.row_dual.dtype),
                    solver_dual_valid=result['dual_valid'],exact_certificate=False)
            if answer.primal is not None:
                vector=answer.primal;path=output.with_suffix('.primal.npy');assert not path.exists();np.save(path,vector,allow_pickle=False)
                by_kind={}
                for kind in sorted({v['kind'] for v in model.variables}):
                    positions=[i for i,v in enumerate(model.variables) if v['kind']==kind];values=vector[positions]
                    by_kind[kind]=dict(variables=len(positions),fractional_variables=int(np.count_nonzero(np.abs(values-np.rint(values))>1e-7)),
                        positive_variables=int(np.count_nonzero(values>1e-7)),minimum=float(np.min(values)),maximum=float(np.max(values)))
                metadata_path=output.with_suffix('.variables.json.gz');write_certificate(metadata_path,list(model.variables))
                candidate=dict(vector=dict(**b.bind(path),shape=list(vector.shape),dtype=str(vector.dtype)),
                    variables=b.bind(metadata_path),by_kind=by_kind,exact_boolean_function_verified=False)
            reconstruction=reconstruct(rows,model.variable_count,answer.row_dual)
            result['reconstruction']={k:v for k,v in reconstruction.items() if k!='certificate'}
            result['numerical_result_status']=result['status']
            if reconstruction['status']=='EXACT_BOX_ROW_LP_CONTRADICTION':
                result.update(status=reconstruction['status'],proof_verified=True,certificate=reconstruction['certificate'])
        except MemoryError:
            rows=None;gc.collect();result=dict(status='RESOURCE_LIMIT_MEMORY',proof_verified=False)
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(original_model_authority=b.bind(authority_path),original_model=authority['source'],
        divisors=divisors,scaling_inventory=scaling,model_inventory=cost,result=result,candidate=candidate,
        dual_candidate=dual_candidate,numerical_report=numerical_report))
    for name in ('run_raw_primitive_full_spectrum_lp.py','primitive_box_rows.py','raw_box_ipm.py','test_raw_box_ipm.py',
                 'bounded_core_spectrum_lp.py','raw_highs_dual_recovery_cycle551_plan.md'):
        b.bind(H/name)
    b.bind(highs_core.__file__)
    proposal=dict(schema_version=1,status='PROPOSED_PRIMITIVE_FULL_OUTSIDE_SPECTRUM_LP',global_status='UNRESOLVED',
        geometry_index=original['geometry_index'],first_row=original['first_row'],group_index=original['group_index'],
        original_model_authority=b.bind(authority_path),original_model=authority['source'],
        input_authority=original['input_authority'],input_source=original['input_source'],
        proof=b.bind(proof_path),model_inventory=cost,scaling_inventory=scaling,result_status=result['status'],candidate=candidate,
        dual_candidate=dual_candidate,numerical_report=numerical_report,
        conditional_product_group_excluded_claim=result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION',
        independent_audit='PENDING',whole_first_case_excluded=False,actual_boolean_function=False,
        whole_geometry_excluded=False,global_goal_complete=False,
        parameters=dict(solver_seconds=seconds,memory_mib=memory_mib,method='direct-bundled-highs-ipm',run_crossover='off',scipy_version=scipy.__version__,highs_version=highs_core._Highs().version()),
        process_peak_resident_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        started_at=started,finished_at=datetime.now(timezone.utc).isoformat(),seconds=monotonic()-start,argv=sys.argv,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(proposal,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(dict(result_status=proposal['result_status'],result={k:v for k,v in result.items() if k!='certificate'},
        candidate=candidate,dual_candidate=dual_candidate,process_peak_resident_kib=proposal['process_peak_resident_kib'],seconds=proposal['seconds'])),flush=True)


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__);parser.add_argument('--authority',type=Path,required=True)
    parser.add_argument('--seconds',type=float,default=60);parser.add_argument('--memory-mib',type=int,default=4096)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    run(args.authority,args.seconds,args.memory_mib,args.output)
