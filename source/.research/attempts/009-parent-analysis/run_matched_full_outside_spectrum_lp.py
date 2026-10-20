"""Bounded full-outside spectral and Parseval coupling on complete audited inputs."""
from argparse import ArgumentParser
from dataclasses import asdict
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
from diagnostic_box_ipm import solve

H=Path(__file__).resolve().parent


def run(authority_path,seconds,memory_mib,output):
    assert not output.exists() and seconds>0 and memory_mib>0
    start=monotonic();started=datetime.now(timezone.utc).isoformat();b=Bindings();limit=memory_mib<<20
    resource.setrlimit(resource.RLIMIT_AS,(limit,limit))
    authority=b.read(authority_path);assert authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FULL_OUTSIDE_INPUTS'
    assert not authority['empty_points']
    ref=authority['source'];source=b.read(ref['path'],ref['sha256']);p=read_certificate(b,source['proof']);blocks=[]
    for record in p['blocks']:
        ref=record['values'];b.bind(ref['path'],ref['sha256']);values=np.load(ref['path'],allow_pickle=False)
        assert list(values.shape)==ref['shape'] and str(values.dtype)==ref['dtype']
        blocks.append(PatternBlock(tuple(record['features']),values))
    coefficients=[ProjectedCoefficient(r['feature'],r['character'],r['support'],tuple(r['values'])) for r in p['projected_coefficients']]
    singletons=tuple(sorted(c.support for c in coefficients if c.support.bit_count()==1));assert len(singletons)==14
    totals=(CoefficientTotal(singletons,16),);model=prepare(p['word_pools'],blocks,coefficients,totals=totals);cost=model.inventory()
    print(json.dumps(dict(stage='full_spectrum_inventory',**cost,seconds=monotonic()-start)),flush=True)
    candidate=None;rows=None
    if cost['estimated_peak_bytes']>limit:
        result=dict(status='RESOURCE_GUARD_MODEL_ESTIMATE',estimated_peak_bytes=cost['estimated_peak_bytes'],proof_verified=False)
    else:
        try:
            rows=list(model.rows());assert len(rows)==cost['rows'] and sum(len(r.terms) for r in rows)==cost['nonzeros']
            answer=solve(rows,model.variable_count,seconds=seconds,display=True);result=answer.report
            if answer.primal is not None:
                vector=answer.primal;path=output.with_suffix('.primal.npy');assert not path.exists()
                np.save(path,vector,allow_pickle=False);by_kind={}
                for kind in sorted({v['kind'] for v in model.variables}):
                    positions=[i for i,v in enumerate(model.variables) if v['kind']==kind];values=vector[positions]
                    by_kind[kind]=dict(variables=len(positions),fractional_variables=int(np.count_nonzero(np.abs(values-np.rint(values))>1e-7)),
                        positive_variables=int(np.count_nonzero(values>1e-7)),minimum=float(np.min(values)),maximum=float(np.max(values)))
                metadata_path=output.with_suffix('.variables.json.gz');write_certificate(metadata_path,list(model.variables))
                candidate=dict(vector=dict(**b.bind(path),shape=list(vector.shape),dtype=str(vector.dtype)),
                    variables=b.bind(metadata_path),by_kind=by_kind,exact_boolean_function_verified=False)
        except MemoryError:
            rows=None;gc.collect();result=dict(status='RESOURCE_LIMIT_MEMORY',proof_verified=False)
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(input_authority=b.bind(authority_path),input_source=authority['source'],
        coefficients=model.coefficient_records(),totals=[asdict(t) for t in totals],include_moments=True,
        partitions=model.base.partition_records(),model_inventory=cost,result=result,candidate=candidate))
    for name in ('run_matched_full_outside_spectrum_lp.py','bounded_core_spectrum_lp.py','test_bounded_core_spectrum_lp.py',
                 'categorical_core_slice_lp.py','core_slice_basis_lp.py','core_slice_degree_lp.py','diagnostic_box_ipm.py',
                 'selfdual_core_projection.py','full_outside_spectrum_soundness_cycle526.md'):
        b.bind(H/name)
    proposal=dict(schema_version=1,status='PROPOSED_MATCHED_FULL_OUTSIDE_SPECTRUM_LP',global_status='UNRESOLVED',
        geometry_index=source['geometry_index'],first_row=source['first_row'],group_index=source['group_index'],
        input_authority=b.bind(authority_path),input_source=authority['source'],
        base_authority=source['base_authority'],zero_product_authority=source['zero_product_authority'],
        quotient_authority=source['quotient_authority'],refinement_authority=source['refinement_authority'],
        proof=b.bind(proof_path),model_inventory=cost,result_status=result['status'],candidate=candidate,
        conditional_product_group_excluded_claim=result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION',
        independent_audit='PENDING',whole_first_case_excluded=False,actual_boolean_function=False,
        whole_geometry_excluded=False,global_goal_complete=False,
        parameters=dict(solver_seconds=seconds,memory_mib=memory_mib,method='highs-ipm',scipy_version=scipy.__version__),
        process_peak_resident_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        started_at=started,finished_at=datetime.now(timezone.utc).isoformat(),seconds=monotonic()-start,argv=sys.argv,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(proposal,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(dict(result_status=proposal['result_status'],result={k:v for k,v in result.items() if k!='certificate'},
        candidate=candidate,process_peak_resident_kib=proposal['process_peak_resident_kib'],seconds=proposal['seconds'])),flush=True)


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__);parser.add_argument('--authority',type=Path,required=True)
    parser.add_argument('--seconds',type=float,default=60);parser.add_argument('--memory-mib',type=int,default=4096)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    run(args.authority,args.seconds,args.memory_mib,args.output)
