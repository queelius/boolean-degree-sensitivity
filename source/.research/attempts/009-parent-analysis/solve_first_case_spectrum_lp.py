"""Run a bounded raw IPM on the already audited whole-case integer matrix."""
from argparse import ArgumentParser
from datetime import datetime,timezone
from pathlib import Path
from time import monotonic
import gc
import json
import resource
import sys
import numpy as np
import scipy
from scipy.optimize._highspy import _core as highs_core
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from first_case_spectrum_scope import CaseScope
from baseline_full_truth_model import Row
from raw_box_ipm import solve,reconstruct

H=Path(__file__).resolve().parent


def run(authority_path,seconds,memory_mib,output):
    assert not output.exists() and seconds>0 and memory_mib>0
    started=datetime.now(timezone.utc).isoformat(); start=monotonic(); limit=memory_mib<<20
    resource.setrlimit(resource.RLIMIT_AS,(limit,limit)); b=Bindings(); authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_FIRST_CASE_FULL_SPECTRUM_MODEL'
    assert authority['all_original_rows_and_divisors_rebuilt'] and authority['saved_primitive_matrix_equal_literal_rows']
    scope=CaseScope.from_data(authority['scope']); ref=authority['model_source']
    source=b.read(ref['path'],ref['sha256']); assert source['scope']==scope.to_data()
    p=read_certificate(b,source['proof']); cost=source['model_inventory']; assert p['scope']==scope.to_data()
    assert cost==p['model_inventory'] and source['scaling_inventory']==authority['scaling_inventory']
    for key,value in authority['model_inventory'].items(): assert cost[key]==value
    matrix=read_certificate(b,p['primitive_matrix'])
    rows=[Row(tuple((int(j),int(a)) for j,a in terms),int(lo),int(hi),{}) for lo,hi,terms in matrix]
    del matrix; gc.collect()
    assert len(rows)==cost['rows'] and sum(len(row.terms) for row in rows)==cost['nonzeros']
    candidate=None; dual_candidate=None; numerical_report=None
    print(json.dumps(dict(stage='audited_matrix_loaded',scope=scope.to_data(),model_inventory=cost,
                         presolve=False,seconds=monotonic()-start)),flush=True)
    if cost['estimated_peak_bytes']>limit:
        result=dict(status='RESOURCE_GUARD_MODEL_ESTIMATE',proof_verified=False,estimated_peak_bytes=cost['estimated_peak_bytes'])
    else:
        try:
            answer=solve(rows,cost['variables'],seconds=seconds,presolve=False,display=True); result=answer.report
            raw_path=output.with_suffix('.numerical.json')
            with raw_path.open('x') as stream: json.dump(result,stream,indent=2,allow_nan=False); stream.write('\n')
            numerical_report=b.bind(raw_path)
            if answer.row_dual is not None:
                path=output.with_suffix('.dual.npy'); assert not path.exists(); np.save(path,answer.row_dual,allow_pickle=False)
                dual_candidate=dict(**b.bind(path),shape=list(answer.row_dual.shape),dtype=str(answer.row_dual.dtype),
                                    solver_dual_valid=result['dual_valid'],exact_certificate=False)
            if answer.primal is not None:
                vector=answer.primal; path=output.with_suffix('.primal.npy'); assert not path.exists()
                np.save(path,vector,allow_pickle=False)
                variables=read_certificate(b,p['variables']); assert len(variables)==len(vector)
                by_kind={}
                for kind in sorted({v['kind'] for v in variables}):
                    positions=[i for i,v in enumerate(variables) if v['kind']==kind]; values=vector[positions]
                    by_kind[kind]=dict(variables=len(positions),fractional_variables=int(np.count_nonzero(np.abs(values-np.rint(values))>1e-7)),
                        positive_variables=int(np.count_nonzero(values>1e-7)),minimum=float(np.min(values)),maximum=float(np.max(values)))
                candidate=dict(vector=dict(**b.bind(path),shape=list(vector.shape),dtype=str(vector.dtype)),
                               variables=p['variables'],by_kind=by_kind,exact_boolean_function_verified=False)
            reconstruction=reconstruct(rows,cost['variables'],answer.row_dual)
            result['reconstruction']={k:v for k,v in reconstruction.items() if k!='certificate'}
            result['numerical_result_status']=result['status']
            if reconstruction['status']=='EXACT_BOX_ROW_LP_CONTRADICTION':
                result.update(status=reconstruction['status'],proof_verified=True,certificate=reconstruction['certificate'])
        except MemoryError:
            rows=None; gc.collect(); result=dict(status='RESOURCE_LIMIT_MEMORY',proof_verified=False)
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(scope=scope.to_data(),model_authority=b.bind(authority_path),
        model_source=authority['model_source'],primitive_matrix=p['primitive_matrix'],result=result,
        candidate=candidate,dual_candidate=dual_candidate,numerical_report=numerical_report))
    for name in ('solve_first_case_spectrum_lp.py','first_case_spectrum_scope.py','test_first_case_spectrum_scope.py',
                 'raw_box_ipm.py','test_raw_box_ipm.py'): b.bind(H/name)
    b.bind(highs_core.__file__)
    proposal=dict(schema_version=1,status='PROPOSED_FIRST_CASE_FULL_SPECTRUM_LP_RUN',global_status='UNRESOLVED',
        scope=scope.to_data(),model_authority=b.bind(authority_path),model_source=authority['model_source'],
        proof=b.bind(proof_path),model_inventory=cost,result_status=result['status'],candidate=candidate,
        dual_candidate=dual_candidate,numerical_report=numerical_report,
        whole_first_case_excluded_claim=result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION',
        independent_audit='PENDING',whole_geometry_excluded=False,actual_boolean_function=False,global_goal_complete=False,
        parameters=dict(solver_seconds=seconds,memory_mib=memory_mib,presolve=False,method='direct-bundled-highs-ipm',
            run_crossover='off',scipy_version=scipy.__version__,highs_version=highs_core._Highs().version()),
        process_peak_resident_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        started_at=started,finished_at=datetime.now(timezone.utc).isoformat(),seconds=monotonic()-start,argv=sys.argv,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream: json.dump(proposal,stream,indent=2,allow_nan=False); stream.write('\n')
    print(json.dumps(dict(scope=scope.to_data(),result={k:v for k,v in result.items() if k!='certificate'},
                         process_peak_resident_kib=proposal['process_peak_resident_kib'],seconds=proposal['seconds'])),flush=True)


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__); parser.add_argument('--authority',type=Path,required=True)
    parser.add_argument('--seconds',type=float,default=60); parser.add_argument('--memory-mib',type=int,default=4096)
    parser.add_argument('--output',type=Path,required=True); a=parser.parse_args()
    run(a.authority,a.seconds,a.memory_mib,a.output)
