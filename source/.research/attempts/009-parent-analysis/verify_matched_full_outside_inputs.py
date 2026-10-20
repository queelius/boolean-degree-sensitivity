"""Literal full-cube pool enumeration and independent global-support projection."""
from argparse import ArgumentParser
from collections import Counter
from itertools import combinations
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from read_matched_cross_arrays import load

H=Path(__file__).resolve().parent


def run(source_path,output):
    assert not output.exists();start=monotonic();b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_MATCHED_FULL_OUTSIDE_INPUTS';proof=read_certificate(b,source['proof'])
    base=b.read(source['base_authority']['path'],source['base_authority']['sha256'])
    zero=b.read(source['zero_product_authority']['path'],source['zero_product_authority']['sha256'])
    assert base['status']=='INDEPENDENTLY_VERIFIED_MATCHED_BINARY_SUPPORT_SEARCH'
    assert zero['status']=='INDEPENDENTLY_VERIFIED_FIRST_CASE_SELECTED_SLICE_ZERO_PRODUCTS'
    assert zero['all_complementary_products_zero_on_selected_slice'] and zero['selected_apex_bits']==[0,1]
    assert source['geometry_index']==base['geometry_index']==zero['geometry_index']
    assert source['first_row']==base['first_row']==zero['first_row'] and source['group_index']==base['group_index']
    assert proof['base_authority']==source['base_authority'] and proof['zero_product_authority']==source['zero_product_authority']
    assert source['refinement_authority']==base['refinement_authority']
    assert source['quotient_authority']==base['quotient_authority']==zero['quotient_authority']
    data=load(b,source['refinement_authority']['path']);instance=read_certificate(b,data.quota['instance'])
    geometry=instance['geometry'];assert proof['geometry']==geometry
    core_mask=geometry['positive_doubles'][0]&geometry['positive_doubles'][1]
    core=[i for i in range(14) if core_mask>>i&1]
    apices=sorted(i for i in range(14) if not core_mask>>i&1 and any(p>>i&1 for p in geometry['positive_doubles']))
    outside=apices+[i for i in range(14) if i not in core and i not in apices]
    assert len(core)==4 and len(apices)==2 and len(outside)==10
    assert proof['core']==core and proof['outside']==outside==instance['outside']
    assert proof['face_points']==list(range(512)) and proof['fixed_outside_coordinate']==outside[-1]
    assert proof['all_component_rows_complement_odd'] is True
    features=instance['core_pair_order'];assert features==sorted(sum(1<<i for i in c) for c in combinations(range(4),2))
    safe={c['local_core_pair'] for c in instance['components'] if c['kind']=='safe_pair_row'}
    matching=proof['safe_matching'];assert len(matching)==2 and matching[0] in safe and matching[1] in safe
    assert not matching[0]&matching[1] and matching[0]|matching[1]==15
    old=b.read(base['source']['path'],base['source']['sha256']);previous=read_certificate(b,old['proof'])
    domains=previous['parent_index_maps'];tables=[t[d,:1024] for t,d in zip(data.tables,domains)]
    assert source['original_pattern_counts']==list(map(len,tables)) and len(proof['blocks'])==6
    parity_checks=0
    for j,(table,record) in enumerate(zip(tables,proof['blocks'])):
        assert record['components']==[j] and record['features']==[features[j]] and record['original_domain']==domains[j]
        ref=record['values'];b.bind(ref['path'],ref['sha256']);values=np.load(ref['path'],allow_pickle=False)
        assert list(values.shape)==ref['shape'] and str(values.dtype)==ref['dtype'] and np.issubdtype(values.dtype,np.integer)
        assert values.shape==(len(table),512,1)
        for k in range(len(table)):
            for point in range(512):
                assert int(values[k,point,0])==int(table[k,point])==-int(table[k,1023^point]);parity_checks+=1
    assert proof['complete_binary_relations']==previous['binary_relations'];binary=[]
    for record in previous['binary_relations']:
        ref=record['allowed_pairs'];b.bind(ref['path'],ref['sha256']);pairs=np.load(ref['path'],allow_pickle=False)
        assert list(pairs.shape)==ref['shape'] and str(pairs.dtype)==ref['dtype'];binary.append((record['components'],pairs))
    negative_masks=[sum(1<<z for z in range(16) if (q&z).bit_count()%2) for q in range(16)]
    catalog=[];delta_counts=Counter();triple_masks=[q for q in range(16) if q.bit_count()==3]
    for word in range(65536):
        count=word.bit_count();spectrum=(16-2*count,)+tuple(4*(word&negative_masks[q]).bit_count()-2*count for q in range(1,16))
        if any(spectrum[q] for q in triple_masks) or spectrum[15] not in (-4,0,4):continue
        delta=spectrum[15]//4;catalog.append((word,spectrum,delta));delta_counts[delta]+=1
    assert dict(delta_counts)=={-1:152,0:222,1:152}
    print(json.dumps(dict(stage='complete_full_patterns_and_catalog',patterns=list(map(len,tables)),
        parity_checks=parity_checks,core_tables_checked=65536,seconds=monotonic()-start)),flush=True)
    actual_pools=[];complements=[(q,15^q) for q in features if q<(15^q)]
    for point in range(512):
        delta=1-(point&1)-((point>>1)&1);unary=[set(map(int,t[:,point])) for t in tables];allowed=[]
        for (i,j),pairs in binary:
            left=tables[i][pairs[:,0],point];right=tables[j][pairs[:,1],point];pairs_here=set()
            for value in set(map(int,left)):pairs_here.update((value,int(v)) for v in np.unique(right[left==value]))
            allowed.append((i,j,pairs_here))
        zeros=sum(1<<z for z in range(16) if point.bit_count()+z.bit_count() in (0,12,13))
        ones=sum(1<<z for z in range(16) if point.bit_count()+z.bit_count() in (1,2,14))
        pool=sorted(spectrum for word,spectrum,d in catalog if d==delta and not word&zeros and word&ones==ones
            and all(spectrum[q] in unary[j] for j,q in enumerate(features))
            and (delta!=0 or all(spectrum[q]*spectrum[r]==0 for q,r in complements))
            and all((spectrum[features[i]],spectrum[features[j]]) in values for i,j,values in allowed))
        assert proof['word_pools'][point]==[list(row) for row in pool];actual_pools.append(pool)
    assert len(proof['word_pools'])==512 and source['word_pool_sizes']==list(map(len,actual_pools))
    assert source['word_variables']==sum(map(len,actual_pools))
    assert source['empty_points']==[x for x,pool in enumerate(actual_pools) if not pool]
    negatives=set(geometry['negative_supports']);positives=set(geometry['positive_doubles'])
    assert len(negatives)==4 and len(positives)==2 and not negatives&positives
    projected=[]
    for support in range(1<<14):
        degree=support.bit_count()
        if degree not in (1,3,5) or (support&core_mask).bit_count()>1:continue
        feature=sum(1<<i for i,v in enumerate(core) if support>>v&1)
        character=sum(1<<i for i,v in enumerate(outside[:-1]) if support>>v&1)
        if support in negatives:values=[-2]
        elif support in positives:values=[2]
        elif degree==1:values=[1,2]
        elif degree==3:values=[-1,0]
        else:values=[0,1]
        projected.append(dict(feature=feature,character=character,support=support,values=values))
    projected.sort(key=lambda r:(r['feature'],r['character']))
    assert proof['projected_coefficients']==projected
    assert len({(r['feature'],r['character']) for r in projected})==len(projected)==source['projected_coefficients']
    assert source['free_coefficient_flags']==sum(len(r['values'])==2 for r in projected)
    assert source['conditional_product_group_excluded_claim'] is False and not source['global_goal_complete']
    for name in ('verify_matched_full_outside_inputs.py','read_matched_cross_arrays.py','full_outside_spectrum_soundness_cycle526.md',
                 'parity_face_extension_cycle514.md','matching_core_word_lemma_cycle224.md','selfdualization.md'):b.bind(H/name)
    accepted=dict(schema_version=1,status='INDEPENDENTLY_VERIFIED_MATCHED_FULL_OUTSIDE_INPUTS',global_status='UNRESOLVED',
        geometry_index=source['geometry_index'],first_row=source['first_row'],group_index=source['group_index'],
        source=b.bind(source_path),base_authority=source['base_authority'],zero_product_authority=source['zero_product_authority'],
        refinement_authority=source['refinement_authority'],quotient_authority=source['quotient_authority'],
        complete_original_pattern_cover=True,complete_word_pool_cover=True,complete_projected_coefficient_cover=True,
        odd_component_entries_checked=parity_checks,core_truth_tables_checked=65536,
        word_variables=sum(map(len,actual_pools)),pattern_variables=sum(map(len,tables)),projected_coefficients=len(projected),
        free_coefficient_flags=source['free_coefficient_flags'],empty_points=source['empty_points'],
        producer_imported=False,producer_word_filter_imported=False,producer_coefficient_mapper_imported=False,
        conditional_product_group_excluded=False,whole_first_case_excluded=False,global_goal_complete=False,
        seconds=monotonic()-start,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(accepted,stream,indent=2);stream.write('\n')
    print(json.dumps({k:accepted[k] for k in ('word_variables','pattern_variables','projected_coefficients',
        'free_coefficient_flags','empty_points','seconds')}),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
