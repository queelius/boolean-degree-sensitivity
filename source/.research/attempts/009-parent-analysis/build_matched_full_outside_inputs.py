"""Complete half-cube words and original component patterns for full spectral coupling."""
from argparse import ArgumentParser
from dataclasses import asdict
from pathlib import Path
from time import monotonic
import json
import resource
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from read_matched_cross_arrays import load
from matched_component_frontier import guarded_words
from selfdual_core_projection import projected_coefficients

H=Path(__file__).resolve().parent


def run(base_path,zero_path,output):
    directory=output.with_suffix('');assert not output.exists() and not directory.exists();directory.mkdir()
    start=monotonic();b=Bindings();base=b.read(base_path);zero=b.read(zero_path)
    assert base['status']=='INDEPENDENTLY_VERIFIED_MATCHED_BINARY_SUPPORT_SEARCH'
    assert zero['status']=='INDEPENDENTLY_VERIFIED_FIRST_CASE_SELECTED_SLICE_ZERO_PRODUCTS'
    assert zero['all_complementary_products_zero_on_selected_slice'] and zero['selected_apex_bits']==[0,1]
    assert base['geometry_index']==zero['geometry_index'] and base['first_row']==zero['first_row']
    assert base['quotient_authority']==zero['quotient_authority']
    data=load(b,base['refinement_authority']['path']);instance=read_certificate(b,data.quota['instance'])
    geometry=instance['geometry'];core_mask=geometry['positive_doubles'][0]&geometry['positive_doubles'][1]
    core=[i for i in range(14) if core_mask>>i&1];outside=instance['outside'];features=instance['core_pair_order']
    assert len(core)==4 and len(outside)==10 and outside[:2]==[i for i in outside if any(p==core_mask|(1<<i) for p in geometry['positive_doubles'])]
    safe={c['local_core_pair'] for c in instance['components'] if c['kind']=='safe_pair_row'}
    matching=next(([q,15^q] for q in sorted(safe) if q<(15^q) and (15^q) in safe),None);assert matching is not None
    previous_source=b.read(base['source']['path'],base['source']['sha256']);previous=read_certificate(b,previous_source['proof'])
    domains=previous['parent_index_maps'];tables=[t[d,:1024].astype(np.int16) for t,d in zip(data.tables,domains)]
    assert all(np.array_equal(t,-t[:,np.arange(1024)^1023]) for t in tables)
    binary=[]
    for record in previous['binary_relations']:
        ref=record['allowed_pairs'];b.bind(ref['path'],ref['sha256']);pairs=np.load(ref['path'],allow_pickle=False)
        assert list(pairs.shape)==ref['shape'] and str(pairs.dtype)==ref['dtype']
        binary.append((record['components'],pairs))
    points=list(range(512));pools=[]
    for x in points:
        delta=1-(x&1)-((x>>1)&1);words=guarded_words(x.bit_count(),delta);live=np.ones(len(words),dtype=bool)
        for j,feature in enumerate(features):live&=np.isin(words[:,feature],tables[j][:,x])
        if delta==0:
            for i,j in zero['complementary_component_pairs']:
                assert features[i]&features[j]==0 and features[i]|features[j]==15
                live&=words[:,features[i]]*words[:,features[j]]==0
        for (i,j),pairs in binary:
            lo_a=int(tables[i][:,x].min());lo_b=int(tables[j][:,x].min());width=int(tables[j][:,x].max())-lo_b+1
            codes=(tables[i][pairs[:,0],x].astype(np.int64)-lo_a)*width+tables[j][pairs[:,1],x]-lo_b
            allowed=np.zeros((int(tables[i][:,x].max())-lo_a+1)*width,dtype=bool);allowed[codes]=True
            candidate=(words[:,features[i]].astype(np.int64)-lo_a)*width+words[:,features[j]]-lo_b
            live&=np.isin(candidate,np.flatnonzero(allowed))
        pools.append(sorted(set(tuple(map(int,row)) for row in words[live])))
    records=[]
    for j,table in enumerate(tables):
        values=table[:,points,None];path=directory/f'component-{j}.npy';np.save(path,values,allow_pickle=False)
        records.append(dict(components=[j],features=[features[j]],original_domain=domains[j],
            values=dict(**b.bind(path),shape=list(values.shape),dtype=str(values.dtype))))
    fixed={n:-2 for n in geometry['negative_supports']};fixed.update({p:2 for p in geometry['positive_doubles']})
    assert len(geometry['negative_supports'])==4 and len(geometry['positive_doubles'])==2 and len(fixed)==6
    coefficients=projected_coefficients(core,outside,5,fixed,{1:(1,2),3:(-1,0),5:(0,1)})
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(base_authority=b.bind(base_path),zero_product_authority=b.bind(zero_path),
        geometry=geometry,core=core,outside=outside,face_points=points,fixed_outside_coordinate=outside[-1],
        all_component_rows_complement_odd=True,safe_matching=matching,word_pools=pools,blocks=records,
        complete_binary_relations=previous['binary_relations'],projected_coefficients=[asdict(c) for c in coefficients]))
    for name in ('build_matched_full_outside_inputs.py','selfdual_core_projection.py','test_selfdual_core_projection.py',
                 'read_matched_cross_arrays.py','matched_component_frontier.py','matching_core_word_lemma_cycle224.md',
                 'full_outside_spectrum_soundness_cycle526.md','parity_face_extension_cycle514.md','selfdualization.md'):
        b.bind(H/name)
    result=dict(schema_version=1,status='PROPOSED_MATCHED_FULL_OUTSIDE_INPUTS',global_status='UNRESOLVED',
        geometry_index=base['geometry_index'],first_row=base['first_row'],group_index=base['group_index'],
        base_authority=b.bind(base_path),zero_product_authority=b.bind(zero_path),refinement_authority=base['refinement_authority'],
        quotient_authority=base['quotient_authority'],proof=b.bind(proof_path),
        original_pattern_counts=list(map(len,tables)),word_pool_sizes=list(map(len,pools)),word_variables=sum(map(len,pools)),
        projected_coefficients=len(coefficients),free_coefficient_flags=sum(len(c.values)==2 for c in coefficients),
        empty_points=[x for x,pool in enumerate(pools) if not pool],independent_audit='PENDING',
        conditional_product_group_excluded_claim=False,actual_boolean_function=False,global_goal_complete=False,
        seconds=monotonic()-start,process_peak_resident_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('word_variables','original_pattern_counts','projected_coefficients',
        'free_coefficient_flags','empty_points','seconds','process_peak_resident_kib')}),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__)
    for flag in ('base','zero','output'):p.add_argument('--'+flag,type=Path,required=True)
    a=p.parse_args();run(a.base,a.zero,a.output)
