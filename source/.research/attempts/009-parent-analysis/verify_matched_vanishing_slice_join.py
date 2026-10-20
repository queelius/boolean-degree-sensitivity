"""Independently verify the literal zero slice, both complete joins, and projection."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
from types import SimpleNamespace
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from read_matched_cross_arrays import load
from verify_product_signature_join import verify_products,verify_join

H=Path(__file__).resolve().parent


def run(source_path,output):
    assert not output.exists();start=monotonic();b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_MATCHED_VANISHING_SLICE_PRODUCT_JOIN'
    pruning=b.read(source['pruning_authority']['path'],source['pruning_authority']['sha256'])
    assert pruning['status']=='INDEPENDENTLY_VERIFIED_MATCHED_WHOLE_FAMILY_DELETIONS'
    assert pruning['refinement_authority']==source['refinement_authority']and pruning['quotient_authority']==source['quotient_authority']
    first=source['first_row'];accepted=[r for r in pruning['records']if r['first_row']==first]
    assert len(accepted)==1 and accepted[0]['conditional_case_excluded']is False
    parent=b.read(pruning['source']['path'],pruning['source']['sha256'])
    record=next(r for r in parent['records']if r['first_row']==first);old=read_certificate(b,record['proof'])
    domains=old['final_domains'];assert list(map(len,domains))==accepted[0]['final_domain_sizes']
    data=load(b,source['refinement_authority']['path'])
    assert b.bind(source['refinement_authority']['path'])==source['refinement_authority']and data.quotient_reference==source['quotient_authority']
    instance=read_certificate(b,data.quota['instance'])
    assert source['geometry_index']==pruning['geometry_index']==instance['geometry_index']
    marked=data.quota['component_index'];assert domains[marked]==[data.quota['selected_row_indices'].index(first)]
    assert instance['components'][marked]['kind']=='safe_pair_row'
    proof=read_certificate(b,source['proof'])
    assert proof['pruning_authority']==source['pruning_authority']and proof['first_row']==first and proof['parent_domains']==domains
    core=instance['geometry']['positive_doubles'][0]&instance['geometry']['positive_doubles'][1]
    apices=sorted(v for v in range(14)if not(core>>v&1)and any(q>>v&1 for q in instance['geometry']['positive_doubles']))
    assert len(apices)==2 and instance['outside'][:2]==apices and len(instance['outside'])==10
    points=[x for x in range(1024)if (x&1)==0 and((x>>1)&1)==1 and int(data.tables[marked][domains[marked][0],x])==0]
    assert points and points==proof['points']and proof['normalization']==8
    order=instance['core_pair_order'];complementary=[]
    for i in range(6):
        for j in range(i+1,6):
            if set(v for v in range(4)if order[i]>>v&1).isdisjoint(v for v in range(4)if order[j]>>v&1):
                assert order[i]|order[j]==15;complementary.append([i,j])
    assert len(complementary)==3 and proof['complementary_pairs']==complementary
    safe=next(p for p in complementary if marked in p);pairs=[p for p in complementary if p!=safe]
    assert proof['safe_pair']==safe and proof['pairs']==pairs
    for relation in instance['relation_types']:
        if relation['delta']==0:
            for row in relation['tuples']:assert sum(int(row[i])*int(row[j])for i,j in complementary)==0
    def array(ref):
        b.bind(ref['path'],ref['sha256']);value=np.load(ref['path'],allow_pickle=False)
        assert list(value.shape)==ref['shape']and str(value.dtype)==ref['dtype'];return value
    def joined(ref):return SimpleNamespace(**{k:array(ref[k])for k in('signatures','left_indices','right_indices','left_groups','right_groups')})
    factors=list(map(array,proof['factors']));assert len(factors)==len(data.tables)
    for j,actual in enumerate(factors):
        raw=data.tables[j][np.ix_(domains[j],points)].astype(np.int64)
        assert np.all(raw%8==0)and np.array_equal(actual,raw//8)
    assert not np.any(factors[marked])
    weights=array(proof['weights']);assert weights.shape==(source['parameters']['linear_moments'],len(points))
    assert np.all(weights[0]==1)and np.all(np.isin(weights,[-1,1]))and source['parameters']['norm_moments']==1
    signatures=list(map(array,proof['moment_signatures']));assert len(signatures)==2
    pair_counts=[]
    for side,(i,j)in enumerate(pairs):
        pair_counts.append(verify_products(factors[i],factors[j],weights,signatures[side],1 if side==0 else -1))
        print(json.dumps(dict(stage='moments',side=side,verified_pairs=pair_counts[-1],seconds=monotonic()-start)),flush=True)
    approximate=joined(proof['moment_join']);verify_join(*signatures,approximate)
    products=list(map(array,proof['full_products']));assert len(products)==2
    approximate_indices=(approximate.left_indices,approximate.right_indices)
    for side,((i,j),indices)in enumerate(zip(pairs,approximate_indices)):
        assert products[side].shape==(len(indices),len(points))and products[side].dtype==np.int16
        for position,index in enumerate(indices):
            x,y=divmod(int(index),len(factors[j]))
            expected=(1 if side==0 else -1)*np.multiply(factors[i][x],factors[j][y],dtype=np.int64)
            assert np.array_equal(products[side][position],expected)
    exact=joined(proof['full_join']);verify_join(*products,exact)
    indices=list(map(array,proof['parent_pair_indices']));assert len(indices)==2
    assert np.array_equal(indices[0],approximate.left_indices[exact.left_indices])and np.array_equal(indices[1],approximate.right_indices[exact.right_indices])
    retained=[list(d)for d in domains]
    for(i,j),selected in zip(pairs,indices):
        width=len(factors[j]);retained[i]=sorted({domains[i][int(k)//width]for k in selected})
        retained[j]=sorted({domains[j][int(k)%width]for k in selected})
    assert retained==proof['retained_domains']
    zero=np.array([not any(map(int,row))for row in exact.signatures],dtype=bool)
    lc=np.bincount(exact.left_groups,minlength=len(zero));rc=np.bincount(exact.right_groups,minlength=len(zero))
    counts=dict(slice_points=len(points),complete_cartesian_pairs=pair_counts,moment_matching_groups=len(approximate.signatures),
        moment_surviving_pairs=list(map(len,products)),exact_matching_products=len(zero),zero_products=int(zero.sum()),
        exact_surviving_pairs=list(map(len,indices)),matching_quadruples=sum(int(x)*int(y)for x,y in zip(lc,rc)),
        zero_product_quadruples=sum(int(x)*int(y)for x,y in zip(lc[zero],rc[zero])),
        initial_domain_sizes=list(map(len,domains)),retained_domain_sizes=list(map(len,retained)))
    assert counts==source['counts']==proof['counts']
    assert source['conditional_case_excluded_claim']==(not len(zero))and source['all_surviving_products_zero_claim']==bool(np.all(zero))
    for name in ('verify_matched_vanishing_slice_join.py','verify_product_signature_join.py','test_verify_product_signature_join.py',
                 'read_matched_cross_arrays.py','matched_vanishing_slice_join_cycle386_plan.md'):b.bind(H/name)
    result=dict(schema_version=1,status='INDEPENDENTLY_VERIFIED_MATCHED_VANISHING_SLICE_PRODUCT_JOIN',global_status='UNRESOLVED',
        geometry_index=source['geometry_index'],first_row=first,source=b.bind(source_path),pruning_authority=source['pruning_authority'],
        quotient_authority=data.quotient_reference,refinement_authority=source['refinement_authority'],counts=counts,
        all_surviving_products_zero=bool(np.all(zero)),conditional_case_excluded=not len(zero),actual_boolean_function=False,
        whole_geometry_excluded=False,global_goal_complete=False,producer_imported=False,producer_join_imported=False,
        producer_pair_products_imported=False,seconds=monotonic()-start,
        files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(**counts,seconds=result['seconds'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
