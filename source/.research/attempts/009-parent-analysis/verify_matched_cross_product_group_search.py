"""Independently replay a complete product cover over an ordinary-cross instance."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from read_matched_cross_arrays import load
from cross_product_scope import require_cross_source
from verify_cross_product_branch import verify_branch

H=Path(__file__).resolve().parent


def run(source_path,output):
    assert not output.exists();start=monotonic();b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_MATCHED_CROSS_PRODUCT_GROUP_SEARCH'
    join=b.read(source['product_join_authority']['path'],source['product_join_authority']['sha256'])
    prior=b.read(join['source']['path'],join['source']['sha256']);joined=read_certificate(b,prior['proof'])
    data=load(b,source['instance_authority']['path'])
    reference=b.bind(source['instance_authority']['path']);assert reference==source['instance_authority']
    require_cross_source(join,data.authority,data.quotient_reference,reference)
    assert source['geometry_index']==join['geometry_index'] and source['first_row']==join['first_row']
    proof=read_certificate(b,source['proof'])
    assert proof['product_join_authority']==source['product_join_authority'] and proof['instance_authority']==reference
    parent=joined['parent_domains'];marked=data.quota['component_index']
    assert parent[marked]==[data.quota['selected_row_indices'].index(source['first_row'])]
    points=[x for x in range(1024) if (x&3)==2 and int(data.tables[marked][parent[marked][0],x])==0]
    assert points==joined['points']==proof['points'] and len(points)==source['added_point_count']
    instance=read_certificate(b,data.quota['instance']);order=instance['core_pair_order']
    complements=[[i,j] for i in range(6) for j in range(i+1,6) if order[i]&order[j]==0 and order[i]|order[j]==15]
    pairs=[pair for pair in complements if marked not in pair]
    assert len(pairs)==2 and pairs==joined['pairs']==proof['pairs']
    assert joined['normalization']==proof['normalization']==8
    assert len(data.relations)==proof['old_point_count']==source['old_point_count']
    def array(ref):
        b.bind(ref['path'],ref['sha256']);value=np.load(ref['path'],allow_pickle=False)
        assert list(value.shape)==ref['shape'] and str(value.dtype)==ref['dtype'];return value
    vectors=array(joined['full_join']['signatures'])
    labels=[array(joined['full_join'][side+'_groups']) for side in ('left','right')]
    indices=[array(ref) for ref in joined['parent_pair_indices']]
    groups=len(vectors)
    assert groups>0 and groups==proof['group_count']==source['group_count']==join['counts']['exact_matching_products']
    assert vectors.shape[1]==len(points) and proof['records']==source['records']
    assert [r['group_index'] for r in proof['records']]==list(range(groups))
    buckets=[]
    for label,flat in zip(labels,indices):
        assert len(label)==len(flat) and set(map(int,label))==set(range(groups))
        by_group=[[] for _ in range(groups)]
        for g,k in zip(label,flat):by_group[int(g)].append(int(k))
        assert sum(map(len,by_group))==len(flat);buckets.append(by_group)
    verified=[];total_nodes=total_pending=0;witnesses=[]
    for group,record in enumerate(proof['records']):
        branch=read_certificate(b,record['proof']);domains=[list(d) for d in parent];counts=[]
        for side,(i,j) in enumerate(pairs):
            left,right=set(),set();selected=buckets[side][group];assert selected
            for flat in selected:
                x,y=divmod(flat,len(parent[j]));assert 0<=x<len(parent[i])
                left.add(parent[i][x]);right.add(parent[j][y])
            domains[i]=sorted(left);domains[j]=sorted(right);counts.append(len(selected))
        assert branch['group_index']==group and branch['parent_index_maps']==domains
        assert branch['pair_counts']==record['pair_counts']==counts
        assert record['domain_sizes']==list(map(len,domains))
        vector=list(map(int,vectors[group]));assert branch['normalized_product']==vector
        assert record['zero_product']==(not any(vector))
        answer=branch['answer']
        status=verify_branch(data.tables,data.relations,domains,points,pairs,vector,answer['tree'],8)
        assert status==answer['status']==record['search_status'] and record['witness']==answer['witness']
        nodes=pending=0;found=[];stack=[answer['tree']]
        while stack:
            node=stack.pop()
            if node['kind']=='LIMIT':pending+=1
            else:
                nodes+=1;stack.extend(node.get('children',[]))
                if 'witness' in node:found.append(node['witness'])
        assert nodes==record['nodes']==answer['nodes']<=answer['max_nodes']==source['max_nodes_per_group']
        if status=='SAT':
            assert found==[record['witness']];witnesses.append(dict(group_index=group,witness=record['witness']))
        else:assert not found and record['witness'] is None
        if status=='UNSAT':assert pending==0
        total_nodes+=nodes;total_pending+=pending
        accepted=dict(group_index=group,search_status=status,verified_search_nodes=nodes,unsearched_subtrees=pending,
                      domain_sizes=record['domain_sizes'],zero_product=record['zero_product'])
        verified.append(accepted);print(json.dumps(dict(first_row=source['first_row'],**accepted)),flush=True)
    statuses=[r['search_status'] for r in verified]
    status='UNSAT' if set(statuses)=={'UNSAT'} else ('SAT' if 'SAT' in statuses else 'UNKNOWN')
    assert source['search_status']==status and source['nodes']==total_nodes
    assert source['conditional_case_excluded_claim']==(status=='UNSAT')
    for name in ('verify_matched_cross_product_group_search.py','verify_cross_product_branch.py','test_cross_product_branch.py',
                 'cross_product_scope.py','test_cross_product_scope.py','verify_finite_function_csp.py',
                 'read_matched_cross_arrays.py','matched_cross_product_groups_cycle463.md'):
        b.bind(H/name)
    result=dict(schema_version=1,status='INDEPENDENTLY_VERIFIED_MATCHED_PRODUCT_GROUP_SEARCH',global_status='UNRESOLVED',
        encoding='accepted_ordinary_cross_plus_fixed_products',geometry_index=source['geometry_index'],first_row=source['first_row'],
        source=b.bind(source_path),product_join_authority=source['product_join_authority'],refinement_authority=reference,
        quotient_authority=data.quotient_reference,search_status=status,verified_search_nodes=total_nodes,
        unsearched_subtrees=total_pending,group_count=groups,complete_exact_group_cover=True,groups=verified,
        conditional_case_excluded=status=='UNSAT',necessary_component_witnesses=witnesses,actual_boolean_function=False,
        whole_geometry_excluded=False,global_goal_complete=False,producer_imported=False,
        product_relation_builder_imported=False,bitset_kernel_imported=False,seconds=monotonic()-start,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('first_row','search_status','verified_search_nodes','unsearched_subtrees','group_count','seconds')}),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
