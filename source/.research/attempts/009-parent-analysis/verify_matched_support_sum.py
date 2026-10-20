"""Independently recalculate a complete support-product and vector-sum cover."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from read_matched_cross_arrays import load
from cross_product_scope import require_cross_source
from verify_vector_sum_join import verify_sums

H=Path(__file__).resolve().parent


def run(source_path,output):
    assert not output.exists();start=monotonic();b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_MATCHED_SUPPORT_SUM_JOIN'
    authority=b.read(source['group_authority']['path'],source['group_authority']['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_PRODUCT_GROUP_SEARCH' and authority['complete_exact_group_cover'] is True
    group=source['group_index'];assert authority['groups'][group]['group_index']==group
    assert authority['groups'][group]['search_status']!='UNSAT'
    previous=b.read(authority['source']['path'],authority['source']['sha256'])
    branch=read_certificate(b,previous['records'][group]['proof'])
    join=b.read(authority['product_join_authority']['path'],authority['product_join_authority']['sha256'])
    old=b.read(join['source']['path'],join['source']['sha256']);joined=read_certificate(b,old['proof'])
    data=load(b,source['refinement_authority']['path']);ref=b.bind(source['refinement_authority']['path'])
    require_cross_source(join,data.authority,data.quotient_reference,ref)
    assert ref==source['refinement_authority']==authority['refinement_authority']
    assert source['quotient_authority']==authority['quotient_authority']==data.quotient_reference
    assert source['geometry_index']==authority['geometry_index']==join['geometry_index']
    assert source['first_row']==authority['first_row']==join['first_row']
    proof=read_certificate(b,source['proof']);assert proof['group_authority']==source['group_authority'] and proof['group_index']==group
    assert proof['product_join_authority']==authority['product_join_authority']
    parent=joined['parent_domains'];marked=data.quota['component_index']
    assert parent[marked]==[data.quota['selected_row_indices'].index(source['first_row'])]
    support=[];zero=[]
    for x in range(1024):
        if (x&1)!=0 or ((x>>1)&1)!=1:continue
        (support if int(data.tables[marked][parent[marked][0],x]) else zero).append(x)
    assert support and support==proof['support_points'] and zero==proof['zero_slice_points']==joined['points']
    assert proof['normalization']==8 and proof['marked_component']==marked and proof['original_parent_domains']==parent
    assert proof['initial_group_domains']==branch['parent_index_maps']
    instance=read_certificate(b,data.quota['instance']);order=instance['core_pair_order']
    complementary=[[i,j] for i in range(6) for j in range(i+1,6) if order[i]&order[j]==0 and order[i]|order[j]==15]
    assert len(complementary)==3
    paired=next(p for p in complementary if marked in p);complement=next(i for i in paired if i!=marked)
    pairs=[p for p in complementary if p!=paired]
    assert pairs==proof['pairs']==joined['pairs'] and complement==proof['complement_component']
    for relation in instance['relation_types']:
        if relation['delta']==0:
            assert all(sum(int(row[i])*int(row[j]) for i,j in complementary)==0 for row in relation['tuples'])
    m=[]
    for x in support:
        value=int(data.tables[marked][parent[marked][0],x]);assert value%8==0 and value//8 in (-1,1);m.append(value//8)
    assert m==proof['marked_values']
    c_rows=branch['parent_index_maps'][complement]
    assert c_rows==proof['complement_candidate_rows']==parent[complement]
    def array(ref):
        b.bind(ref['path'],ref['sha256']);value=np.load(ref['path'],allow_pickle=False)
        assert list(value.shape)==ref['shape'] and str(value.dtype)==ref['dtype'];return value
    targets=array(proof['targets']);assert targets.shape==(len(c_rows),len(support)) and targets.dtype==np.int16
    for k,row in enumerate(c_rows):
        expected=[]
        for mark,x in zip(m,support):
            value=int(data.tables[complement][row,x]);assert value%8==0;expected.append(mark*(value//8))
        assert targets[k].tolist()==expected
    vectors=[];labels=[];flat_indices=[];verified_pairs=[]
    for side,(i,j) in enumerate(pairs):
        old_labels=array(joined['full_join'][('left' if side==0 else 'right')+'_groups'])
        old_indices=array(joined['parent_pair_indices'][side])
        expected=[int(k) for label,k in zip(old_labels,old_indices) if int(label)==group]
        flat=array(proof['parent_pair_indices'][side]);assert flat.tolist()==expected
        products=array(proof['products'][side]);values=array(proof['vectors'][side]);lab=array(proof['labels'][side])
        assert products.dtype==values.dtype==np.int16 and products.shape==(len(flat),len(support))
        assert values.ndim==2 and values.shape[1]==len(support) and lab.shape==(len(flat),) and lab.dtype==np.int64
        assert len({row.tobytes() for row in values})==len(values) and set(map(int,lab))==set(range(len(values)))
        left=data.tables[i][np.ix_(parent[i],support)].astype(np.int64)
        right=data.tables[j][np.ix_(parent[j],support)].astype(np.int64)
        assert np.all(left%8==0) and np.all(right%8==0);left//=8;right//=8
        for position,flat_index in enumerate(flat):
            a,c=divmod(int(flat_index),len(parent[j]));assert 0<=a<len(parent[i])
            expected_product=(1 if side==0 else -1)*left[a]*right[c]
            assert np.array_equal(products[position],expected_product)
            assert np.array_equal(values[int(lab[position])],products[position])
        vectors.append(values);labels.append(lab);flat_indices.append(flat);verified_pairs.append(len(flat))
        print(json.dumps(dict(stage='literal_support_products',side=side,checked=len(flat),vectors=len(values),seconds=monotonic()-start)),flush=True)
    matches=array(proof['matches']);cover=verify_sums(vectors[0],targets,vectors[1],matches)
    kept=[set(),set()];c_kept=set()
    for a,c,r in matches.tolist():kept[0].add(a);c_kept.add(c);kept[1].add(r)
    retained=[list(d) for d in branch['parent_index_maps']]
    for side,(i,j) in enumerate(pairs):
        left,right=set(),set()
        for label,flat in zip(labels[side],flat_indices[side]):
            if int(label) not in kept[side]:continue
            a,c=divmod(int(flat),len(parent[j]));left.add(parent[i][a]);right.add(parent[j][c])
        retained[i]=sorted(left);retained[j]=sorted(right)
    retained[complement]=[c_rows[k] for k in sorted(c_kept)]
    assert retained==proof['retained_domains']
    counts=dict(support_points=len(support),original_pair_counts=verified_pairs,distinct_product_vectors=list(map(len,vectors)),
        complement_candidates=len(targets),complete_vector_candidate_pairs=cover['cartesian_pairs_checked'],
        matching_triples=cover['matching_triples'],retained_vector_counts=list(map(len,kept)),
        initial_domain_sizes=list(map(len,branch['parent_index_maps'])),retained_domain_sizes=list(map(len,retained)))
    assert counts==proof['counts']==source['counts']
    assert source['conditional_product_group_excluded_claim']==(not len(matches))
    for name in ('verify_matched_support_sum.py','verify_vector_sum_join.py','test_finite_vector_sum_join.py',
                 'read_matched_cross_arrays.py','matched_support_sum_cycle467_plan.md'):b.bind(H/name)
    result=dict(schema_version=1,status='INDEPENDENTLY_VERIFIED_MATCHED_SUPPORT_SUM_JOIN',global_status='UNRESOLVED',
        geometry_index=source['geometry_index'],first_row=source['first_row'],group_index=group,source=b.bind(source_path),
        group_authority=source['group_authority'],refinement_authority=ref,quotient_authority=source['quotient_authority'],
        counts=counts,complete_sum_cover=True,conditional_product_group_excluded=not len(matches),
        actual_boolean_function=False,whole_first_case_excluded=False,whole_geometry_excluded=False,global_goal_complete=False,
        producer_imported=False,producer_sum_lookup_imported=False,producer_pair_products_imported=False,
        seconds=monotonic()-start,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(**counts,seconds=result['seconds'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
