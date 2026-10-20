"""Reconstruct exact candidate-pair lists and replay the mixed-constraint proof."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from read_matched_cross_arrays import load
from cross_product_scope import require_cross_source
from binary_row_relation import BinaryRelation
from verify_binary_function_csp import verify_tree

H=Path(__file__).resolve().parent


def run(source_path,output):
    assert not output.exists();start=monotonic();b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_MATCHED_BINARY_SUPPORT_SEARCH'
    support=b.read(source['support_sum_authority']['path'],source['support_sum_authority']['sha256'])
    assert support['status']=='INDEPENDENTLY_VERIFIED_MATCHED_SUPPORT_SUM_JOIN' and support['complete_sum_cover'] is True
    assert support['conditional_product_group_excluded'] is False
    previous=b.read(support['source']['path'],support['source']['sha256']);p=read_certificate(b,previous['proof'])
    groups=b.read(source['product_group_authority']['path'],source['product_group_authority']['sha256'])
    assert source['product_group_authority']==support['group_authority']
    assert groups['status']=='INDEPENDENTLY_VERIFIED_MATCHED_PRODUCT_GROUP_SEARCH' and groups['complete_exact_group_cover'] is True
    g=source['group_index'];assert g==support['group_index'] and groups['groups'][g]['group_index']==g
    assert groups['groups'][g]['search_status']!='UNSAT'
    old=b.read(groups['source']['path'],groups['source']['sha256']);old_proof=read_certificate(b,old['proof'])
    branch=read_certificate(b,old_proof['records'][g]['proof'])
    join=b.read(groups['product_join_authority']['path'],groups['product_join_authority']['sha256'])
    data=load(b,source['refinement_authority']['path']);ref=b.bind(source['refinement_authority']['path'])
    require_cross_source(join,data.authority,data.quotient_reference,ref)
    assert ref==source['refinement_authority']==support['refinement_authority']
    assert source['quotient_authority']==support['quotient_authority']==data.quotient_reference
    assert source['geometry_index']==groups['geometry_index']==support['geometry_index']
    assert source['first_row']==groups['first_row']==support['first_row']
    proof=read_certificate(b,source['proof'])
    assert proof['support_sum_authority']==source['support_sum_authority'] and proof['product_group_authority']==source['product_group_authority']
    assert proof['group_index']==g and proof['refinement_authority']==ref
    domains=p['retained_domains'];assert proof['parent_index_maps']==domains and source['domain_sizes']==list(map(len,domains))
    assert p['initial_group_domains']==branch['parent_index_maps']
    points=p['zero_slice_points'];vector=branch['normalized_product'];pairs=p['pairs']
    assert points==proof['zero_slice_points']==old_proof['points'] and len(points)==source['added_point_count']
    assert vector==proof['normalized_zero_slice_product'] and pairs==proof['product_pairs']==old_proof['pairs']
    assert len(data.relations)==proof['old_point_count']==source['old_point_count']
    def array(ref):
        b.bind(ref['path'],ref['sha256']);a=np.load(ref['path'],allow_pickle=False)
        assert list(a.shape)==ref['shape'] and str(a.dtype)==ref['dtype'];return a
    matches=array(p['matches']);assert len(matches)>0
    assert [r['components'] for r in proof['binary_relations']]==pairs
    binary=[]
    for side,record in enumerate(proof['binary_relations']):
        i,j=record['components'];allowed=array(record['allowed_pairs'])
        assert allowed.dtype==np.int64 and allowed.ndim==2 and allowed.shape[1]==2
        original=p['original_parent_domains'];flat=array(p['parent_pair_indices'][side]);labels=array(p['labels'][side])
        keep={int(row[0 if side==0 else 2]) for row in matches}
        left={row:k for k,row in enumerate(domains[i])};right={row:k for k,row in enumerate(domains[j])}
        assert len(left)==len(domains[i]) and len(right)==len(domains[j])
        expected=[]
        for index,label in zip(flat,labels):
            if int(label) not in keep:continue
            a,c=divmod(int(index),len(original[j]));assert 0<=a<len(original[i])
            u,v=original[i][a],original[j][c];assert u in left and v in right
            expected.append([left[u],right[v]])
        assert allowed.tolist()==expected
        assert set(allowed[:,0].tolist())==set(range(len(left))) and set(allowed[:,1].tolist())==set(range(len(right)))
        binary.append(BinaryRelation(i,j,allowed))
        print(json.dumps(dict(stage='binary_relation',components=[i,j],verified_pairs=len(allowed),seconds=monotonic()-start)),flush=True)
    assert [len(r.allowed) for r in binary]==source['binary_pair_counts']
    tables=[]
    for table,domain in zip(data.tables,domains):
        assert domain==sorted(set(domain)) and all(0<=i<len(table) for i in domain)
        subset=table[np.asarray(domain,dtype=np.int64)]
        tables.append(np.hstack((subset,subset[:,np.asarray(points,dtype=np.int64)])))
    relations=list(data.relations)
    for x,v in zip(points,vector):
        allowed=[]
        for row in data.relations[x]:
            a=int(row[pairs[0][0]])*int(row[pairs[0][1]])
            c=int(row[pairs[1][0]])*int(row[pairs[1][1]])
            if a==64*int(v) and c==-64*int(v):allowed.append(tuple(row))
        relations.append(allowed)
    answer=proof['answer'];assert answer['proof_schema']=='point_and_binary_v1'
    status=verify_tree(tables,relations,binary,answer['tree'])
    assert status==answer['status']==source['search_status'] and answer['witness']==source['witness']
    nodes=pending=pair_events=0;found=[];stack=[answer['tree']]
    while stack:
        node=stack.pop()
        if node['kind']=='LIMIT':pending+=1;continue
        nodes+=1;pair_events+=sum(e['kind']=='binary' for e in node['propagation']);stack.extend(node.get('children',[]))
        if 'witness' in node:found.append(node['witness'])
    assert nodes==answer['nodes']==source['nodes']<=answer['max_nodes']==source['max_nodes']
    if status=='SAT':assert found==[source['witness']]
    else:assert not found and source['witness'] is None
    if status=='UNSAT':assert pending==0
    original=None if source['witness'] is None else [domains[j][i] for j,i in enumerate(source['witness'])]
    assert original==source['witness_original_rows'] and source['conditional_product_group_excluded_claim']==(status=='UNSAT')
    for name in ('verify_matched_binary_support_search.py','verify_binary_function_csp.py','binary_row_relation.py',
                 'test_binary_function_csp.py','test_project_binary_candidate_pairs.py','read_matched_cross_arrays.py',
                 'matched_binary_pair_search_cycle481_plan.md'):b.bind(H/name)
    result=dict(schema_version=1,status='INDEPENDENTLY_VERIFIED_MATCHED_BINARY_SUPPORT_SEARCH',global_status='UNRESOLVED',
        geometry_index=source['geometry_index'],first_row=source['first_row'],group_index=g,source=b.bind(source_path),
        support_sum_authority=source['support_sum_authority'],product_group_authority=source['product_group_authority'],
        refinement_authority=ref,quotient_authority=source['quotient_authority'],search_status=status,
        verified_search_nodes=nodes,unsearched_subtrees=pending,binary_propagation_events=pair_events,
        domain_sizes=source['domain_sizes'],binary_pair_counts=source['binary_pair_counts'],
        necessary_component_witness=original,conditional_product_group_excluded=status=='UNSAT',
        whole_first_case_excluded=False,actual_boolean_function=False,whole_geometry_excluded=False,global_goal_complete=False,
        producer_imported=False,producer_pair_projection_imported=False,bitset_propagation_imported=False,
        seconds=monotonic()-start,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('first_row','group_index','search_status','verified_search_nodes','unsearched_subtrees',
        'binary_propagation_events','seconds')}),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
