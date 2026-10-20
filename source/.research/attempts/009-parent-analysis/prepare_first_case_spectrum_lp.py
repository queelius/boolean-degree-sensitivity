"""Freeze every primitive integer row before independent audit and optimization."""
from argparse import ArgumentParser
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from time import monotonic
import json
import resource
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from first_case_spectrum_scope import input_scope
from core_slice_degree_lp import PatternBlock
from selfdual_core_projection import ProjectedCoefficient
from bounded_core_spectrum_lp import CoefficientTotal,prepare
from primitive_box_rows import primitive_row

H=Path(__file__).resolve().parent


def run(authority_path,output,memory_mib):
    assert not output.exists(); start=monotonic()
    resource.setrlimit(resource.RLIMIT_AS,(memory_mib<<20,memory_mib<<20))
    b=Bindings(); authority=b.read(authority_path); scope=input_scope(authority)
    ref=authority['source']; inputs=b.read(ref['path'],ref['sha256']); p=read_certificate(b,inputs['proof'])
    assert inputs['scope']==p['scope']==scope.to_data(); blocks=[]
    for record in p['blocks']:
        ref=record['values']; b.bind(ref['path'],ref['sha256']); values=np.load(ref['path'],allow_pickle=False)
        assert list(values.shape)==ref['shape'] and str(values.dtype)==ref['dtype']
        blocks.append(PatternBlock(tuple(record['features']),values))
    coefficients=[ProjectedCoefficient(c['feature'],c['character'],c['support'],tuple(c['values'])) for c in p['projected_coefficients']]
    singletons=tuple(sorted(c.support for c in coefficients if c.support.bit_count()==1))
    assert singletons==tuple(1<<i for i in range(14))
    totals=(CoefficientTotal(singletons,16),)
    model=prepare(p['word_pools'],blocks,coefficients,totals=totals,include_moments=True)
    cost=model.inventory(); matrix=[]; divisors=[]; max_old=max_new=max_old_rhs=max_new_rhs=0
    for row in model.rows():
        normalized,divisor=primitive_row(row); divisors.append(divisor)
        assert len(set(j for j,_ in normalized.terms))==len(normalized.terms)
        matrix.append([normalized.lower,normalized.upper,sorted(normalized.terms)])
        max_old=max(max_old,max((abs(a) for _,a in row.terms),default=0))
        max_new=max(max_new,max((abs(a) for _,a in normalized.terms),default=0))
        max_old_rhs=max(max_old_rhs,abs(row.lower),abs(row.upper))
        max_new_rhs=max(max_new_rhs,abs(normalized.lower),abs(normalized.upper))
    assert len(matrix)==cost['rows'] and sum(len(row[2]) for row in matrix)==cost['nonzeros']
    scaling=dict(divisor_counts=[dict(divisor=d,rows=n) for d,n in sorted(Counter(divisors).items())],
        maximum_original_coefficient=max_old,maximum_primitive_coefficient=max_new,
        maximum_original_bound=max_old_rhs,maximum_primitive_bound=max_new_rhs)
    matrix_path=output.with_suffix('.matrix.json.gz'); write_certificate(matrix_path,matrix)
    variable_path=output.with_suffix('.variables.json.gz'); write_certificate(variable_path,list(model.variables))
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(scope=scope.to_data(),input_authority=b.bind(authority_path),input_source=authority['source'],
        coefficients=model.coefficient_records(),totals=[asdict(t) for t in totals],include_moments=True,
        partitions=model.base.partition_records(),divisors=divisors,scaling_inventory=scaling,
        model_inventory=cost,primitive_matrix=b.bind(matrix_path),variables=b.bind(variable_path)))
    for name in ('prepare_first_case_spectrum_lp.py','first_case_spectrum_scope.py','test_first_case_spectrum_scope.py',
                 'bounded_core_spectrum_lp.py','test_bounded_core_spectrum_lp.py','primitive_box_rows.py',
                 'test_primitive_ipm.py','full_outside_spectrum_soundness_cycle526.md'): b.bind(H/name)
    result=dict(schema_version=1,status='PROPOSED_FIRST_CASE_FULL_SPECTRUM_MODEL',global_status='UNRESOLVED',
        scope=scope.to_data(),input_authority=b.bind(authority_path),input_source=authority['source'],proof=b.bind(proof_path),
        model_inventory=cost,scaling_inventory=scaling,result_status='MODEL_ONLY',solver_run=False,
        whole_first_case_excluded=False,actual_boolean_function=False,global_goal_complete=False,
        independent_audit='PENDING',parameters=dict(memory_mib=memory_mib),seconds=monotonic()-start,
        process_peak_resident_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream: json.dump(result,stream,indent=2); stream.write('\n')
    print(json.dumps(dict(scope=result['scope'],model_inventory=cost,scaling_inventory=scaling,seconds=result['seconds'])),flush=True)


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__); parser.add_argument('--authority',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True); parser.add_argument('--memory-mib',type=int,default=4096)
    a=parser.parse_args(); run(a.authority,a.output,a.memory_mib)
