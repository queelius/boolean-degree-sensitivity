"""Genuine and gap controls for the fixed scheduling adapter, no native query."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time
from types import SimpleNamespace

import context_first_rows_cycle1438 as adapter
import gap_transcript_reader_cycle1436 as reader
import signed_star_rows_independent_cycle1431 as builder

H=Path(__file__).resolve().parent
GAP=H.parent/'006-solver-resume/exact_binary_gap_propagation.py'


def ref(path):
    path=Path(path).resolve();body=path.read_bytes()
    return dict(path=str(path),sha256=hashlib.sha256(body).hexdigest(),bytes=len(body))


def load_generator():
    if ref(GAP)['sha256']!='eb423a01a7bba42767e88493465e0594f9f0210dd1e8496af1ff764e55f2ec76':raise ValueError('frozen gap generator changed')
    if ref(H/'exact_binary_row_propagation.py')['sha256']!='6f01e230b88384aa0142798639aeae602d74e0473cd26c6e1df54cc2d183e491':raise ValueError('frozen interval dependency changed')
    spec=importlib.util.spec_from_file_location('unchanged_gap_cycle1438',GAP);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def main():
    if not __debug__:raise ValueError('normal Python required before I/O')
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    if args.output.exists():raise ValueError('fresh output required')
    resource.setrlimit(resource.RLIMIT_CPU,(10,15));resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
    start=time.process_time();generator=load_generator();records=[]
    def run(label,model,common_count,assignment=None):
        order,inverse=adapter.context_first(common_count,len(model['rows'])-common_count)
        rows=[SimpleNamespace(terms=tuple(map(tuple,r['terms'])),lower=r['lower'],upper=r['upper']) for r in model['rows']]
        before=time.process_time();raw=generator.propagate([rows[i] for i in order]);generation=time.process_time()-before
        translated=adapter.translate(raw,order);binding=reader.binding(model);before=time.process_time()
        checked=reader.verify(model,dict(schema_version=1,model_binding=binding,certificate=translated),binding);replay=time.process_time()-before
        if assignment is not None:
            if not reader.check_assignment(model,assignment) or checked['status']!='VALID_PREFIX_INCONCLUSIVE':raise ValueError('genuine positive failed')
        records.append(dict(label=label,generator_to_native=order,native_to_generator=inverse,model_binding=binding,raw_certificate=raw,native_certificate=translated,independent_replay=checked,generation_CPU_seconds=generation,replay_CPU_seconds=replay,known_assignment_checked=assignment is not None))
    specifications=[([[1,-1],[2,1]],0,0),([[2,-1],[3,1]],0,0),([[3,1]],0,0),([[1,1]],1,1)]
    toy=dict(schema_version=1,header=dict(kind='NONINVOLUTIVE_ROW_CONTROL'),variables=[1,2,3],rows=[dict(key=dict(family='CONTROL',subject=i,detail=0),terms=t,lower=l,upper=u) for i,(t,l,u) in enumerate(specifications)])
    run('noninvolutive-four-row-contradiction',toy,3)
    gap=dict(schema_version=1,header=dict(kind='TWO_X_EQUALS_ONE_CONTROL'),variables=[1],rows=[dict(key=dict(family='CONTROL',subject=0,detail=0),terms=[[1,2]],lower=1,upper=1)])
    run('2x=1',gap,0)
    for a,b in [(4,4),(5,5)]:
        n=a+b;facets=builder.cycle_join(a,b);faces=builder.face_assignment(facets);constant=16-4*n+len(facets)
        layout=builder.context(n,constant,0,[f^1 for f in facets if f&1],False)
        common=list(builder.common_rows(n));contexts=list(builder.context_rows(layout))
        model=dict(schema_version=1,header=dict(kind='GENUINE_CYCLE_JOIN_CONTROL',n=n,constant=constant,cycles=[a,b]),variables=list(builder.variables(n)),rows=[r.record() for r in common+contexts])
        run('C'+str(a)+'*C'+str(b),model,len(common),{v:int(v in faces) for v in model['variables']})
        records[-1]['cube_and_direct_Walsh_control']=builder.positive_control(a,b)
    before=time.process_time();order,inverse=adapter.context_first(12130,382);permutation_CPU=time.process_time()-before
    sources=[ref(p) for p in [__file__,H/'context_first_rows_cycle1438.py',H/'gap_transcript_reader_cycle1436.py',H/'signed_star_rows_independent_cycle1431.py',GAP,H/'exact_binary_row_propagation.py']]
    report=dict(schema_version=1,status='CONTEXT_FIRST_CONTROLS_PASS_NO_NATIVE_QUERY',sources=sources,records=records,
                target_permutation_length=len(order),target_permutation_only_CPU_seconds=permutation_CPU,
                CPU_seconds=time.process_time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                native_queries=0,new_engine=False,full_target_generation_runtime_unknown=True,global_goal_complete=False)
    with args.output.open('x') as stream:json.dump(report,stream,indent=2);stream.write('\n')
    print(json.dumps({k:report[k] for k in ['status','CPU_seconds','peak_RSS_bytes','native_queries']}))


if __name__=='__main__':main()
