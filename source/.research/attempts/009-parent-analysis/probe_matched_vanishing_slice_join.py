"""Complete two-stage product join on a fixed component's literal zero slice."""
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
from finite_pair_products import pair_products,opposite_zero_points
from product_signature_join import product_signatures,join_signatures

H=Path(__file__).resolve().parent
JOIN_FIELDS=('signatures','left_indices','right_indices','left_groups','right_groups')


def run(pruning_path,first,seed,moments,output):
    assert not output.exists()and not output.with_suffix('').exists()and moments>=1
    start=monotonic();started=datetime.now(timezone.utc).isoformat();b=Bindings();pruning=b.read(pruning_path)
    assert pruning['status']=='INDEPENDENTLY_VERIFIED_MATCHED_WHOLE_FAMILY_DELETIONS'
    records=[r for r in pruning['records']if r['first_row']==first];assert len(records)==1 and not records[0]['conditional_case_excluded']
    parent=b.read(pruning['source']['path'],pruning['source']['sha256'])
    record=next(r for r in parent['records']if r['first_row']==first);old_proof=read_certificate(b,record['proof'])
    domains=old_proof['final_domains'];assert list(map(len,domains))==records[0]['final_domain_sizes']
    data=load(b,pruning['refinement_authority']['path']);assert b.bind(pruning['refinement_authority']['path'])==pruning['refinement_authority']
    assert data.quotient_reference==pruning['quotient_authority'];instance=read_certificate(b,data.quota['instance'])
    marked=data.quota['component_index'];assert domains[marked]==[data.quota['selected_row_indices'].index(first)]
    assert instance['components'][marked]['kind']=='safe_pair_row'
    order=instance['core_pair_order'];complementary=[[i,j]for i in range(6)for j in range(i+1,6)if order[i]&order[j]==0 and order[i]|order[j]==15]
    safe=next(p for p in complementary if marked in p);pairs=[p for p in complementary if p!=safe];assert len(pairs)==2
    geometry=instance['geometry'];core=geometry['positive_doubles'][0]&geometry['positive_doubles'][1]
    apices=sorted(v for v in range(14)if any(q>>v&1 for q in geometry['positive_doubles'])and not(core>>v&1))
    assert instance['outside'][:2]==apices and len(apices)==2 and len(instance['outside'])==10
    points=opposite_zero_points(data.tables[marked][domains[marked][0],:1024]);assert len(points)>0
    factors=[]
    for table,domain in zip(data.tables,domains):
        raw=table[np.ix_(domain,points)];assert np.all(raw%8==0);scaled=raw//8
        assert np.all((scaled>=-2)&(scaled<=2));factors.append(scaled.astype(np.int8))
    assert not np.any(factors[marked])
    for relation in instance['relation_types']:
        if relation['delta']==0:assert all(sum(int(row[i])*int(row[j])for i,j in complementary)==0 for row in relation['tuples'])
    rng=np.random.default_rng(seed)
    weights=np.vstack((np.ones((1,len(points)),dtype=np.int8),rng.choice([-1,1],size=(moments-1,len(points))).astype(np.int8)))
    directory=output.with_suffix('');directory.mkdir()
    def save(name,value):
        path=directory/(name+'.npy');np.save(path,value,allow_pickle=False)
        return dict(**b.bind(path),shape=list(value.shape),dtype=str(value.dtype))
    def save_join(name,join):return {field:save(name+'-'+field,getattr(join,field))for field in JOIN_FIELDS}
    factor_refs=[save(f'factor-{j}',v)for j,v in enumerate(factors)];weight_ref=save('weights',weights)
    signatures=[];sig_refs=[]
    for side,(i,j)in enumerate(pairs):
        sig=product_signatures(factors[i],factors[j],weights,product_sign=1 if side==0 else -1)
        signatures.append(sig);sig_refs.append(save(f'moment-signatures-{side}',sig))
        print(json.dumps(dict(stage='moments',side=side,pairs=len(sig),points=len(points),seconds=monotonic()-start)),flush=True)
    approximate=join_signatures(*signatures);approx_ref=save_join('moment-join',approximate)
    approx_indices=(approximate.left_indices,approximate.right_indices)
    products=[pair_products(factors[i],factors[j],indices,1 if side==0 else -1)
              for side,((i,j),indices)in enumerate(zip(pairs,approx_indices))]
    full_refs=[save(f'full-products-{side}',v)for side,v in enumerate(products)]
    exact=join_signatures(*products);exact_ref=save_join('full-join',exact)
    indices=[approximate.left_indices[exact.left_indices],approximate.right_indices[exact.right_indices]]
    index_refs=[save(f'parent-pair-indices-{side}',v)for side,v in enumerate(indices)]
    retained=[list(d)for d in domains]
    for(i,j),selected in zip(pairs,indices):
        width=len(factors[j]);retained[i]=np.asarray(domains[i])[np.unique(selected//width)].tolist()
        retained[j]=np.asarray(domains[j])[np.unique(selected%width)].tolist()
    zero=~np.any(exact.signatures,axis=1);lc=np.bincount(exact.left_groups,minlength=len(zero));rc=np.bincount(exact.right_groups,minlength=len(zero))
    counts=dict(slice_points=len(points),complete_cartesian_pairs=list(map(len,signatures)),moment_matching_groups=len(approximate.signatures),
        moment_surviving_pairs=list(map(len,products)),exact_matching_products=len(zero),zero_products=int(zero.sum()),
        exact_surviving_pairs=list(map(len,indices)),matching_quadruples=sum(int(x)*int(y)for x,y in zip(lc,rc)),
        zero_product_quadruples=sum(int(x)*int(y)for x,y in zip(lc[zero],rc[zero])),
        initial_domain_sizes=list(map(len,domains)),retained_domain_sizes=list(map(len,retained)))
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(pruning_authority=b.bind(pruning_path),first_row=first,parent_domains=domains,
        points=points.tolist(),normalization=8,complementary_pairs=complementary,safe_pair=safe,pairs=pairs,
        factors=factor_refs,weights=weight_ref,moment_signatures=sig_refs,moment_join=approx_ref,full_products=full_refs,
        full_join=exact_ref,parent_pair_indices=index_refs,retained_domains=retained,counts=counts))
    for name in ('probe_matched_vanishing_slice_join.py','finite_pair_products.py','test_finite_pair_products.py',
                 'product_signature_join.py','test_product_signature_join.py','cycle386-tests-green.log','cycle386-pair-products-coverage.txt',
                 'matched_vanishing_slice_join_cycle386_plan.md','matched_ordinary_cross_intersection_cycle331.md'):b.bind(H/name)
    result=dict(schema_version=1,status='PROPOSED_MATCHED_VANISHING_SLICE_PRODUCT_JOIN',global_status='UNRESOLVED',
        geometry_index=instance['geometry_index'],first_row=first,pruning_authority=b.bind(pruning_path),
        quotient_authority=data.quotient_reference,refinement_authority=pruning['refinement_authority'],proof=b.bind(proof_path),counts=counts,
        parameters=dict(seed=seed,linear_moments=moments,norm_moments=1,arithmetic='exact_integer',argv=sys.argv),
        environment=dict(python=sys.version,numpy=np.__version__),started_at=started,finished_at=datetime.now(timezone.utc).isoformat(),
        seconds=monotonic()-start,conditional_case_excluded_claim=not len(zero),all_surviving_products_zero_claim=bool(np.all(zero)),
        independent_verification='PENDING',actual_boolean_function=False,whole_geometry_excluded=False,global_goal_complete=False,
        files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(**counts,seconds=result['seconds'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--pruning',type=Path,required=True);p.add_argument('--first-row',type=int,required=True)
    p.add_argument('--seed',type=int,default=388);p.add_argument('--linear-moments',type=int,default=7);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.pruning,a.first_row,a.seed,a.linear_moments,a.output)
