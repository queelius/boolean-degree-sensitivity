"""Exact R=L+m*c join on the remaining support of a fixed marked component."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import sys
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from read_matched_cross_arrays import load
from cross_product_scope import require_cross_source
from finite_pair_products import pair_products
from product_signature_join import join_signatures
from finite_vector_sum_join import join_sums

H=Path(__file__).resolve().parent


def run(authority_path,group,output):
    directory=output.with_suffix('');assert not output.exists() and not directory.exists()
    start=monotonic();b=Bindings();authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_PRODUCT_GROUP_SEARCH'
    assert authority['complete_exact_group_cover'] is True
    accepted=authority['groups'][group];assert accepted['group_index']==group and accepted['search_status']!='UNSAT'
    source=b.read(authority['source']['path'],authority['source']['sha256'])
    record=source['records'][group];branch=read_certificate(b,record['proof'])
    join=b.read(authority['product_join_authority']['path'],authority['product_join_authority']['sha256'])
    joined_source=b.read(join['source']['path'],join['source']['sha256']);joined=read_certificate(b,joined_source['proof'])
    data=load(b,authority['refinement_authority']['path'])
    require_cross_source(join,data.authority,data.quotient_reference,b.bind(authority['refinement_authority']['path']))
    assert authority['geometry_index']==join['geometry_index'] and authority['first_row']==join['first_row']
    parent=joined['parent_domains'];marked=data.quota['component_index'];marked_row=parent[marked][0]
    assert parent[marked]==[data.quota['selected_row_indices'].index(join['first_row'])]
    support=[x for x in range(1024) if (x&3)==2 and int(data.tables[marked][marked_row,x])!=0]
    zero=[x for x in range(1024) if (x&3)==2 and int(data.tables[marked][marked_row,x])==0]
    assert support and zero==joined['points'] and len(support)+len(zero)==256
    factors=[]
    for table,domain in zip(data.tables,parent):
        raw=table[np.ix_(domain,support)];assert np.all(raw%8==0)
        factors.append((raw//8).astype(np.int16))
    m=factors[marked][0];assert np.all(np.isin(m,[-1,1]))
    complement=next(i for i in joined['safe_pair'] if i!=marked)
    c_rows=branch['parent_index_maps'][complement]
    assert c_rows==parent[complement]
    c_values=data.tables[complement][np.ix_(c_rows,support)];assert np.all(c_values%8==0)
    targets=(c_values//8).astype(np.int16)*m
    directory.mkdir()
    def array(ref):
        b.bind(ref['path'],ref['sha256']);value=np.load(ref['path'],allow_pickle=False)
        assert list(value.shape)==ref['shape'] and str(value.dtype)==ref['dtype'];return value
    def save(name,value):
        path=directory/(name+'.npy');np.save(path,value,allow_pickle=False)
        return dict(**b.bind(path),shape=list(value.shape),dtype=str(value.dtype))
    vector_refs=[];vectors=[];labels=[];selected_pairs=[];product_refs=[];label_refs=[];pair_refs=[]
    for side,(i,j) in enumerate(joined['pairs']):
        group_labels=array(joined['full_join'][('left' if side==0 else 'right')+'_groups'])
        flat=array(joined['parent_pair_indices'][side]);selected=flat[group_labels==group]
        assert len(selected)==record['pair_counts'][side]
        values=pair_products(factors[i],factors[j],selected,1 if side==0 else -1)
        unique=join_signatures(values,values)
        assert np.array_equal(unique.left_indices,np.arange(len(values)))
        vectors.append(unique.signatures);labels.append(unique.left_groups);selected_pairs.append(selected)
        product_refs.append(save(f'products-{side}',values));vector_refs.append(save(f'vectors-{side}',unique.signatures))
        label_refs.append(save(f'labels-{side}',unique.left_groups));pair_refs.append(save(f'parent-pairs-{side}',selected))
    print(json.dumps(dict(stage='support_vectors',support_points=len(support),pairs=list(map(len,selected_pairs)),
        distinct_vectors=list(map(len,vectors)),complement_candidates=len(targets),
        vector_candidate_cartesian_pairs=len(vectors[0])*len(targets),seconds=monotonic()-start)),flush=True)
    matches=join_sums(vectors[0],targets,vectors[1]);match_ref=save('matches',matches)
    retained=[list(d) for d in branch['parent_index_maps']]
    for side,(i,j) in enumerate(joined['pairs']):
        kept=set(map(int,matches[:,0 if side==0 else 2]));mask=np.isin(labels[side],list(kept))
        selected=selected_pairs[side][mask];width=len(parent[j])
        retained[i]=sorted({parent[i][int(k)//width] for k in selected})
        retained[j]=sorted({parent[j][int(k)%width] for k in selected})
    retained[complement]=[c_rows[k] for k in sorted(set(map(int,matches[:,1])))]
    counts=dict(support_points=len(support),original_pair_counts=list(map(len,selected_pairs)),
        distinct_product_vectors=list(map(len,vectors)),complement_candidates=len(targets),
        complete_vector_candidate_pairs=len(vectors[0])*len(targets),matching_triples=len(matches),
        retained_vector_counts=[len(set(map(int,matches[:,i]))) for i in (0,2)],
        initial_domain_sizes=list(map(len,branch['parent_index_maps'])),retained_domain_sizes=list(map(len,retained)))
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(group_authority=b.bind(authority_path),group_index=group,
        product_join_authority=authority['product_join_authority'],support_points=support,zero_slice_points=zero,
        normalization=8,marked_component=marked,marked_values=m.tolist(),complement_component=complement,
        complement_candidate_rows=c_rows,targets=save('complement-targets',targets),pairs=joined['pairs'],
        original_parent_domains=parent,initial_group_domains=branch['parent_index_maps'],parent_pair_indices=pair_refs,
        products=product_refs,vectors=vector_refs,labels=label_refs,matches=match_ref,retained_domains=retained,counts=counts))
    for name in ('probe_matched_support_sum.py','finite_pair_products.py','product_signature_join.py',
                 'finite_vector_sum_join.py','test_finite_vector_sum_join.py','matched_support_sum_cycle467_plan.md'):
        b.bind(H/name)
    result=dict(schema_version=1,status='PROPOSED_MATCHED_SUPPORT_SUM_JOIN',global_status='UNRESOLVED',
        geometry_index=authority['geometry_index'],first_row=authority['first_row'],group_index=group,
        group_authority=b.bind(authority_path),refinement_authority=authority['refinement_authority'],
        quotient_authority=authority['quotient_authority'],proof=b.bind(proof_path),counts=counts,
        conditional_product_group_excluded_claim=not len(matches),actual_boolean_function=False,
        whole_first_case_excluded=False,whole_geometry_excluded=False,global_goal_complete=False,
        seconds=monotonic()-start,argv=sys.argv,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(**counts,seconds=result['seconds'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--authority',type=Path,required=True)
    p.add_argument('--group',type=int,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.authority,a.group,a.output)
