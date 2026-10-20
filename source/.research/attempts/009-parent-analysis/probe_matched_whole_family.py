"""Bounded whole-family propagation with explicit point-cover deletion proofs."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from load_matched_safe_count_instance import load
from finite_function_csp import FunctionCSP
from whole_family_cross import family_masks,forbidden_masks,filter_pair,cover_features

H=Path(__file__).resolve().parent


def indices(bits,size):
    raw=np.frombuffer(bits.to_bytes((size+7)//8,'little'),dtype=np.uint8)
    return np.flatnonzero(np.unpackbits(raw,bitorder='little')[:size])


def bitset(rows,size):
    values=np.zeros(size,dtype=np.uint8);values[rows]=1
    return int.from_bytes(np.packbits(values,bitorder='little').tobytes(),'little')


def run(authority_path,frontier_path,first_rows,max_rounds,output):
    assert max_rounds>=1
    directory=output.with_suffix('');assert not directory.exists()and not output.exists()
    start=monotonic();b=Bindings();authority=b.read(authority_path);frontier=b.read(frontier_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_ORDINARY_CROSS_REFINEMENT'and authority['complete_actual_cover']is True
    assert frontier['status']=='VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER'
    base,quota,tables,relations=load(b,Path(authority['base_refinement']['path']))
    assert b.bind(authority['base_refinement']['path'])==authority['base_refinement']
    original=b.read(base['base_refinement']['path'],base['base_refinement']['sha256'])
    assert frontier['scope']['quotient_authority']==original['base_authority']
    assert authority['geometry_index']==base['geometry_index']==frontier['scope']['geometry_index']
    assert len(set(first_rows))==len(first_rows)and set(first_rows)<=set(frontier['remaining_first_rows'])
    extra=read_certificate(b,authority['refinement']);offset=len(relations);assert offset==extra['old_point_count']
    tables=[np.concatenate((t,np.load(c['columns']['path'],allow_pickle=False)),axis=1)for t,c in zip(tables,extra['components'])]
    relations=relations+extra['relations']
    order=list(range(offset,len(relations)))+[1025,1024]+sorted(range(1024),key=lambda x:(min(x.bit_count(),10-x.bit_count()),x))
    solver=FunctionCSP(tables,relations,order)
    features=[np.load(c['features']['path'],allow_pickle=False)for c in extra['components']]
    present=[family_masks(f)for f in features];forbidden=[forbidden_masks(f,extra['ordinary_triples'])for f in features]
    points={}
    for x,d in enumerate(extra['descriptions']):points.setdefault((d['left'],d['right']),{})[d['triple']]=offset+x
    point_lists={pair:[mapping[t]for t in extra['ordinary_triples']]for pair,mapping in points.items()}
    sizes=list(map(len,tables));directory.mkdir();records=[]
    for first in first_rows:
        before=monotonic();candidate=quota['selected_row_indices'].index(first);j=quota['component_index']
        initial=list(solver.initial);initial[j]=1<<candidate
        reduced,steps,bad=solver.propagate(tuple(initial))
        domains=[indices(d,n)for d,n in zip(reduced,sizes)];initial_sizes=list(map(len,domains))
        initial_propagation=dict(steps=steps,contradiction_point=bad,domain_sizes=initial_sizes)
        status='CONTRADICTION'if bad is not None else'LIMIT';stages=[];deleted=0
        if bad is None:
            for _ in range(max_rounds):
                deletions=[]
                for (left,right),local_points in sorted(point_lists.items()):
                    a,c=filter_pair(present[left],forbidden[right],domains[left],domains[right])
                    for i in sorted(set(map(int,domains[left]))-set(map(int,a))):
                        cover=cover_features(present[left][i],forbidden[right][domains[right]])
                        deletions.append(dict(variable=left,candidate=i,partner=right,points=[local_points[x]for x in cover]))
                    domains[left]=a
                    if not len(a):break
                    for i in sorted(set(map(int,domains[right]))-set(map(int,c))):
                        cover=cover_features(forbidden[right][i],present[left][domains[left]])
                        deletions.append(dict(variable=right,candidate=i,partner=left,points=[local_points[x]for x in cover]))
                    domains[right]=c
                    if not len(c):break
                deleted+=len(deletions);stage=dict(deletions=deletions)
                if any(not len(d)for d in domains):
                    status='CONTRADICTION';stages.append(stage);break
                reduced,steps,bad=solver.propagate(tuple(bitset(d,n)for d,n in zip(domains,sizes)))
                domains=[indices(d,n)for d,n in zip(reduced,sizes)]
                stage['point_propagation']=dict(steps=steps,contradiction_point=bad);stages.append(stage)
                if bad is not None:status='CONTRADICTION';break
                if not deletions and not steps:status='FIXED_POINT';break
        pp=directory/f'first-{first:04d}.json.gz'
        write_certificate(pp,dict(first_row=first,parent_candidate_index=candidate,initial_propagation=initial_propagation,
                                  stages=stages,final_domains=[d.tolist()for d in domains],status=status))
        record=dict(first_row=first,proof=b.bind(pp),propagation_status=status,deletions=deleted,
                    initial_domain_sizes=initial_sizes,final_domain_sizes=list(map(len,domains)),rounds=len(stages),seconds=monotonic()-before)
        records.append(record);print(json.dumps({k:v for k,v in record.items()if k!='proof'}),flush=True)
    for name in ('probe_matched_whole_family.py','whole_family_cross.py','test_whole_family_cross.py','finite_function_csp.py',
                 'load_matched_safe_count_instance.py','matched_ordinary_cross_intersection_cycle331.md'):b.bind(H/name)
    result=dict(status='PROPOSED_MATCHED_WHOLE_FAMILY_PROPAGATION',global_status='UNRESOLVED',
                refinement_authority=b.bind(authority_path),frontier_authority=b.bind(frontier_path),geometry_index=authority['geometry_index'],
                parameters=dict(first_rows=first_rows,max_rounds=max_rounds),records=records,global_goal_complete=False,
                seconds=monotonic()-start,files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--refinement',type=Path,required=True);p.add_argument('--frontier',type=Path,required=True)
    p.add_argument('--first-rows',type=int,nargs='+',required=True);p.add_argument('--max-rounds',type=int,default=5);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.refinement,a.frontier,a.first_rows,a.max_rounds,a.output)
