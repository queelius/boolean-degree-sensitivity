"""Literal full-core truth tables and global supports verify a complete first case."""
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
from first_case_spectrum_scope import CaseScope

H=Path(__file__).resolve().parent


def run(source_path,output):
    assert not output.exists(); start=monotonic(); b=Bindings(); source=b.read(source_path)
    assert source['status']=='PROPOSED_FIRST_CASE_FULL_SPECTRUM_INPUTS'
    scope=CaseScope.from_data(source['scope']); proof=read_certificate(b,source['proof'])
    assert proof['scope']==scope.to_data() and proof['domain_authority']==source['domain_authority']
    ref=source['domain_authority']; authority=b.read(ref['path'],ref['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_WHOLE_FAMILY_DELETIONS'
    assert authority['geometry_index']==scope.geometry_index and authority['quotient_authority']==source['scope']['quotient_authority']
    records=[r for r in authority['records'] if r['first_row']==scope.first_row]; assert len(records)==1
    accepted=records[0]; assert not accepted['conditional_case_excluded']
    ref=authority['source']; original=b.read(ref['path'],ref['sha256'])
    records=[r for r in original['records'] if r['first_row']==scope.first_row]; assert len(records)==1
    assert records[0]['proof']==proof['domain_proof']
    previous=read_certificate(b,records[0]['proof'])
    assert source['refinement_authority']==authority['refinement_authority']==original['refinement_authority']
    data=load(b,source['refinement_authority']['path'])
    assert b.bind(source['refinement_authority']['path'])==source['refinement_authority']
    assert data.quotient_reference==source['scope']['quotient_authority']
    candidate=data.quota['selected_row_indices'].index(scope.first_row)
    assert previous['first_row']==scope.first_row and previous['parent_candidate_index']==candidate
    domains=previous['final_domains']; assert list(map(len,domains))==accepted['final_domain_sizes']
    assert domains[data.quota['component_index']]==[candidate]
    instance=read_certificate(b,data.quota['instance']); geometry=instance['geometry']; assert proof['geometry']==geometry
    negatives=set(geometry['negative_supports']); positives=set(geometry['positive_doubles'])
    assert len(negatives)==4 and len(positives)==2 and not negatives&positives
    assert all(s.bit_count()==5 for s in negatives|positives)
    core_mask=geometry['positive_doubles'][0]&geometry['positive_doubles'][1]
    core=[i for i in range(14) if core_mask>>i&1]
    apices=sorted(i for i in range(14) if not core_mask>>i&1 and any(p>>i&1 for p in positives))
    outside=apices+[i for i in range(14) if i not in core and i not in apices]
    assert len(core)==4 and len(apices)==2 and len(outside)==10
    assert proof['core']==core and proof['outside']==outside==instance['outside']
    assert proof['face_points']==list(range(512)) and proof['fixed_outside_coordinate']==outside[-1]
    assert proof['all_component_rows_complement_odd'] is True and proof['additional_word_filters']==[]
    features=instance['core_pair_order']
    assert features==sorted(sum(1<<i for i in c) for c in combinations(range(4),2))
    safe={c['local_core_pair'] for c in instance['components'] if c['kind']=='safe_pair_row'}
    matching=proof['safe_matching']; assert len(matching)==2 and all(q in safe for q in matching)
    assert not matching[0]&matching[1] and matching[0]|matching[1]==15
    tables=[t[d,:1024] for t,d in zip(data.tables,domains)]
    assert source['original_pattern_counts']==list(map(len,tables)) and len(proof['blocks'])==6
    parity_checks=0
    for j,(table,record) in enumerate(zip(tables,proof['blocks'])):
        assert record['components']==[j] and record['features']==[features[j]] and record['original_domain']==domains[j]
        ref=record['values']; b.bind(ref['path'],ref['sha256']); values=np.load(ref['path'],allow_pickle=False)
        assert list(values.shape)==ref['shape'] and str(values.dtype)==ref['dtype'] and np.issubdtype(values.dtype,np.integer)
        assert values.shape==(len(table),512,1)
        for k in range(len(table)):
            for point in range(512):
                assert int(values[k,point,0])==int(table[k,point])==-int(table[k,1023^point]); parity_checks+=1
    negative_masks=[sum(1<<z for z in range(16) if (q&z).bit_count()%2) for q in range(16)]
    catalog=[]; delta_counts=Counter(); triples=[q for q in range(16) if q.bit_count()==3]
    for word in range(65536):
        count=word.bit_count()
        spectrum=(16-2*count,)+tuple(4*(word&negative_masks[q]).bit_count()-2*count for q in range(1,16))
        if any(spectrum[q] for q in triples) or spectrum[15] not in (-4,0,4): continue
        delta=spectrum[15]//4; catalog.append((word,spectrum,delta)); delta_counts[delta]+=1
    assert dict(delta_counts)=={-1:152,0:222,1:152}
    print(json.dumps(dict(stage='complete_patterns_and_catalog',patterns=list(map(len,tables)),parity_checks=parity_checks,
                         core_tables_checked=65536,seconds=monotonic()-start)),flush=True)
    actual_pools=[]
    for point in range(512):
        delta=1-(point&1)-((point>>1)&1); unary=[set(map(int,t[:,point])) for t in tables]
        zeros=sum(1<<z for z in range(16) if point.bit_count()+z.bit_count() in (0,12,13))
        ones=sum(1<<z for z in range(16) if point.bit_count()+z.bit_count() in (1,2,14))
        pool=sorted(spectrum for word,spectrum,d in catalog if d==delta and not word&zeros and word&ones==ones
                    and all(spectrum[q] in unary[j] for j,q in enumerate(features)))
        assert proof['word_pools'][point]==[list(row) for row in pool]; actual_pools.append(pool)
    assert len(proof['word_pools'])==512 and source['word_pool_sizes']==list(map(len,actual_pools))
    assert source['word_variables']==sum(map(len,actual_pools))
    assert source['empty_points']==[x for x,pool in enumerate(actual_pools) if not pool]
    projected=[]
    for support in range(1<<14):
        degree=support.bit_count()
        if degree not in (1,3,5) or (support&core_mask).bit_count()>1: continue
        feature=sum(1<<i for i,v in enumerate(core) if support>>v&1)
        character=sum(1<<i for i,v in enumerate(outside[:-1]) if support>>v&1)
        if support in negatives: values=[-2]
        elif support in positives: values=[2]
        elif degree==1: values=[1,2]
        elif degree==3: values=[-1,0]
        else: values=[0,1]
        projected.append(dict(feature=feature,character=character,support=support,values=values))
    projected.sort(key=lambda r:(r['feature'],r['character']))
    assert proof['projected_coefficients']==projected
    assert len({(r['feature'],r['character']) for r in projected})==len(projected)==source['projected_coefficients']
    assert source['free_coefficient_flags']==sum(len(r['values'])==2 for r in projected)
    assert source['whole_first_case_necessary_cover_claim'] is True and not source['global_goal_complete']
    assert not source['whole_first_case_excluded']
    for name in ('verify_first_case_full_spectrum_inputs.py','first_case_spectrum_scope.py','test_first_case_spectrum_scope.py',
                 'read_matched_cross_arrays.py','full_outside_spectrum_soundness_cycle526.md','parity_face_extension_cycle514.md',
                 'matching_core_word_lemma_cycle224.md','selfdualization.md'): b.bind(H/name)
    result=dict(schema_version=1,status='INDEPENDENTLY_VERIFIED_FIRST_CASE_FULL_SPECTRUM_INPUTS',global_status='UNRESOLVED',
        scope=scope.to_data(),source=b.bind(source_path),domain_authority=source['domain_authority'],
        refinement_authority=source['refinement_authority'],complete_original_pattern_cover=True,
        complete_word_pool_cover=True,complete_projected_coefficient_cover=True,whole_first_case_necessary_cover=True,
        odd_component_entries_checked=parity_checks,core_truth_tables_checked=65536,
        word_variables=sum(map(len,actual_pools)),pattern_variables=sum(map(len,tables)),projected_coefficients=len(projected),
        free_coefficient_flags=source['free_coefficient_flags'],empty_points=source['empty_points'],
        producer_imported=False,producer_word_filter_imported=False,producer_coefficient_mapper_imported=False,
        domain_deletions_replayed_in_this_run=False,domain_deletion_independent_authority_referenced=True,
        whole_first_case_excluded=False,global_goal_complete=False,seconds=monotonic()-start,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream: json.dump(result,stream,indent=2); stream.write('\n')
    print(json.dumps({k:result[k] for k in ('scope','word_variables','pattern_variables','projected_coefficients',
                                          'free_coefficient_flags','empty_points','seconds')}),flush=True)


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__); parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True); a=parser.parse_args(); run(a.source,a.output)
