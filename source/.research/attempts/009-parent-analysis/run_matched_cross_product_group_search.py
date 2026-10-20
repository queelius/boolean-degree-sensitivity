"""Search a complete product partition using the join's ordinary-cross instance."""
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
from append_product_value_relations import append_product_values
from resume_function_csp import PriorityPointCSP

H=Path(__file__).resolve().parent


def run(join_path,max_nodes,output):
    assert not output.exists() and max_nodes>0
    start=monotonic();started=datetime.now(timezone.utc).isoformat();b=Bindings();join=b.read(join_path)
    source=b.read(join['source']['path'],join['source']['sha256']);joined=read_certificate(b,source['proof'])
    refinement=join['refinement_authority'];data=load(b,refinement['path'])
    require_cross_source(join,data.authority,data.quotient_reference,b.bind(refinement['path']))
    def array(ref):
        b.bind(ref['path'],ref['sha256']);value=np.load(ref['path'],allow_pickle=False)
        assert list(value.shape)==ref['shape'] and str(value.dtype)==ref['dtype'];return value
    vectors=array(joined['full_join']['signatures'])
    labels=[array(joined['full_join'][side+'_groups']) for side in ('left','right')]
    flat=[array(ref) for ref in joined['parent_pair_indices']]
    parent=joined['parent_domains'];pairs=joined['pairs'];points=joined['points'];marked=data.quota['component_index']
    assert len(pairs)==2 and len(vectors)==join['counts']['exact_matching_products']>0
    assert vectors.shape[1]==len(points) and joined['normalization']==8
    scale=int(joined['normalization'])**2;old=len(data.relations)
    instance=read_certificate(b,data.quota['instance']);raw=1<<len(instance['outside'])
    assert raw==1024 and data.authority['old_point_count']==raw+2
    order=[raw+1,raw]+list(range(old,old+len(points)))+list(range(raw+2,old))
    order+=sorted(range(raw),key=lambda x:(min(x.bit_count(),len(instance['outside'])-x.bit_count()),x))
    assert sorted(order)==list(range(old+len(points)))
    records=[]
    for group,vector in enumerate(vectors):
        begin=monotonic();domains=[list(d) for d in parent];counts=[]
        for side,(i,j) in enumerate(pairs):
            selected=flat[side][labels[side]==group];assert len(selected);counts.append(len(selected))
            width=len(parent[j]);domains[i]=sorted({parent[i][int(k)//width] for k in selected})
            domains[j]=sorted({parent[j][int(k)%width] for k in selected})
        assert domains[marked]==[data.quota['selected_row_indices'].index(join['first_row'])]
        targets=[[sign*scale*int(v) for v in vector] for sign in (1,-1)]
        base=[table[np.asarray(d,dtype=np.int64)] for table,d in zip(data.tables,domains)]
        tables,relations=append_product_values(base,data.relations,points,pairs,targets)
        answer=PriorityPointCSP(tables,relations,order,priority_point=raw+1).search(max_nodes)
        proof_path=output.with_name(output.stem+f'-group{group}.json.gz')
        write_certificate(proof_path,dict(group_index=group,parent_index_maps=domains,
            normalized_product=vector.tolist(),pair_counts=counts,answer=answer))
        record=dict(group_index=group,zero_product=not bool(np.any(vector)),pair_counts=counts,
            domain_sizes=list(map(len,domains)),search_status=answer['status'],nodes=answer['nodes'],
            witness=answer['witness'],proof=b.bind(proof_path),seconds=monotonic()-begin)
        records.append(record);print(json.dumps(dict(first_row=join['first_row'],**record)),flush=True)
    statuses=[r['search_status'] for r in records]
    status='UNSAT' if all(s=='UNSAT' for s in statuses) else ('SAT' if 'SAT' in statuses else 'UNKNOWN')
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(product_join_authority=b.bind(join_path),instance_authority=refinement,
        points=points,pairs=pairs,normalization=joined['normalization'],old_point_count=old,
        group_count=len(vectors),records=records))
    for name in ('run_matched_cross_product_group_search.py','cross_product_scope.py','test_cross_product_scope.py',
                 'append_product_value_relations.py','test_append_product_value_relations.py','read_matched_cross_arrays.py',
                 'finite_function_csp.py','resume_function_csp.py','matched_cross_product_groups_cycle463.md'):
        b.bind(H/name)
    result=dict(schema_version=1,status='PROPOSED_MATCHED_CROSS_PRODUCT_GROUP_SEARCH',global_status='UNRESOLVED',
        geometry_index=join['geometry_index'],first_row=join['first_row'],product_join_authority=b.bind(join_path),
        instance_authority=refinement,proof=b.bind(proof_path),old_point_count=old,added_point_count=len(points),
        group_count=len(vectors),records=records,search_status=status,nodes=sum(r['nodes'] for r in records),
        max_nodes_per_group=max_nodes,conditional_case_excluded_claim=status=='UNSAT',actual_boolean_function=False,
        whole_geometry_excluded=False,global_goal_complete=False,started_at=started,
        finished_at=datetime.now(timezone.utc).isoformat(),seconds=monotonic()-start,
        environment=dict(python=sys.version,numpy=np.__version__),argv=sys.argv,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('first_row','search_status','nodes','group_count','seconds')}),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--join',type=Path,required=True)
    p.add_argument('--max-nodes',type=int,default=3000);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.join,a.max_nodes,a.output)
