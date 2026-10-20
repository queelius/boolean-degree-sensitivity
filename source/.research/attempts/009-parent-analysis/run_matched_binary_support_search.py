"""Search one product group while retaining its exact whole-row pair cover."""
from argparse import ArgumentParser
from datetime import datetime,timezone
from pathlib import Path
from time import monotonic
import json
import sys
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from read_matched_cross_arrays import load
from cross_product_scope import require_cross_source
from project_binary_candidate_pairs import project_pairs
from binary_row_relation import BinaryRelation
from binary_function_csp import BinaryFunctionCSP
from append_product_value_relations import append_product_values

H=Path(__file__).resolve().parent


def run(support_path,max_nodes,output):
    directory=output.with_suffix('');assert not output.exists() and not directory.exists() and max_nodes>0
    start=monotonic();started=datetime.now(timezone.utc).isoformat();b=Bindings();support=b.read(support_path)
    assert support['status']=='INDEPENDENTLY_VERIFIED_MATCHED_SUPPORT_SUM_JOIN' and support['complete_sum_cover'] is True
    assert support['conditional_product_group_excluded'] is False
    source=b.read(support['source']['path'],support['source']['sha256']);p=read_certificate(b,source['proof'])
    groups=b.read(support['group_authority']['path'],support['group_authority']['sha256']);g=support['group_index']
    assert groups['status']=='INDEPENDENTLY_VERIFIED_MATCHED_PRODUCT_GROUP_SEARCH' and groups['complete_exact_group_cover'] is True
    assert groups['groups'][g]['group_index']==g and groups['groups'][g]['search_status']!='UNSAT'
    old=b.read(groups['source']['path'],groups['source']['sha256']);old_proof=read_certificate(b,old['proof'])
    branch=read_certificate(b,old_proof['records'][g]['proof'])
    assert branch['group_index']==g and p['initial_group_domains']==branch['parent_index_maps']
    join=b.read(groups['product_join_authority']['path'],groups['product_join_authority']['sha256'])
    data=load(b,support['refinement_authority']['path'])
    require_cross_source(join,data.authority,data.quotient_reference,b.bind(support['refinement_authority']['path']))
    assert groups['geometry_index']==support['geometry_index']==join['geometry_index']
    assert groups['first_row']==support['first_row']==join['first_row']
    assert support['quotient_authority']==groups['quotient_authority']==data.quotient_reference
    def array(ref):
        b.bind(ref['path'],ref['sha256']);a=np.load(ref['path'],allow_pickle=False)
        assert list(a.shape)==ref['shape'] and str(a.dtype)==ref['dtype'];return a
    domains=p['retained_domains'];parent=p['original_parent_domains'];pairs=p['pairs'];matches=array(p['matches'])
    assert len(matches)>0 and list(map(len,domains))==support['counts']['retained_domain_sizes']
    points=p['zero_slice_points'];vector=branch['normalized_product']
    assert points==old_proof['points'] and pairs==old_proof['pairs'] and len(points)==len(vector)
    binary=[];records=[];directory.mkdir()
    for side,(i,j) in enumerate(pairs):
        indices=array(p['parent_pair_indices'][side]);labels=array(p['labels'][side])
        kept=set(map(int,matches[:,0 if side==0 else 2]))
        allowed=project_pairs(parent[i],parent[j],indices,labels,kept,domains[i],domains[j])
        path=directory/f'allowed-pairs-{side}.npy';np.save(path,allowed,allow_pickle=False)
        records.append(dict(components=[i,j],allowed_pairs=dict(**b.bind(path),shape=list(allowed.shape),dtype=str(allowed.dtype))))
        binary.append(BinaryRelation(i,j,allowed))
    base=[table[np.asarray(domain,dtype=np.int64)] for table,domain in zip(data.tables,domains)]
    targets=[[sign*64*int(v) for v in vector] for sign in (1,-1)]
    tables,relations=append_product_values(base,data.relations,points,pairs,targets);old_points=len(data.relations)
    instance=read_certificate(b,data.quota['instance']);raw=1<<len(instance['outside'])
    order=[raw+1,raw]+list(range(old_points,len(relations)))+list(range(raw+2,old_points))
    order+=sorted(range(raw),key=lambda x:(min(x.bit_count(),len(instance['outside'])-x.bit_count()),x))
    print(json.dumps(dict(stage='model_ready',domain_sizes=list(map(len,domains)),binary_pair_counts=[len(r.allowed) for r in binary],
        old_points=old_points,added_points=len(points),max_nodes=max_nodes,seconds=monotonic()-start)),flush=True)
    solver=BinaryFunctionCSP(tables,relations,binary,order,priority_point=raw+1);answer=solver.search(max_nodes)
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(support_sum_authority=b.bind(support_path),product_group_authority=support['group_authority'],
        group_index=g,refinement_authority=support['refinement_authority'],parent_index_maps=domains,
        zero_slice_points=points,normalized_zero_slice_product=vector,product_pairs=pairs,binary_relations=records,
        old_point_count=old_points,answer=answer))
    for name in ('run_matched_binary_support_search.py','binary_row_relation.py','binary_function_csp.py',
                 'finite_function_csp.py','resume_function_csp.py','project_binary_candidate_pairs.py',
                 'test_project_binary_candidate_pairs.py','test_binary_function_csp.py','append_product_value_relations.py',
                 'test_append_product_value_relations.py','read_matched_cross_arrays.py','matched_binary_pair_search_cycle481_plan.md'):
        b.bind(H/name)
    original=None if answer['witness'] is None else [domains[j][i] for j,i in enumerate(answer['witness'])]
    result=dict(schema_version=1,status='PROPOSED_MATCHED_BINARY_SUPPORT_SEARCH',global_status='UNRESOLVED',
        geometry_index=support['geometry_index'],first_row=support['first_row'],group_index=g,
        support_sum_authority=b.bind(support_path),product_group_authority=support['group_authority'],
        refinement_authority=support['refinement_authority'],quotient_authority=support['quotient_authority'],
        proof=b.bind(proof_path),domain_sizes=list(map(len,domains)),binary_pair_counts=[len(r.allowed) for r in binary],
        old_point_count=old_points,added_point_count=len(points),search_status=answer['status'],nodes=answer['nodes'],
        max_nodes=max_nodes,witness=answer['witness'],witness_original_rows=original,
        conditional_product_group_excluded_claim=answer['status']=='UNSAT',whole_first_case_excluded=False,
        actual_boolean_function=False,whole_geometry_excluded=False,global_goal_complete=False,
        started_at=started,finished_at=datetime.now(timezone.utc).isoformat(),seconds=monotonic()-start,argv=sys.argv,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('first_row','group_index','search_status','nodes','binary_pair_counts','seconds')}),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--support',type=Path,required=True)
    p.add_argument('--max-nodes',type=int,default=1000);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.support,a.max_nodes,a.output)
