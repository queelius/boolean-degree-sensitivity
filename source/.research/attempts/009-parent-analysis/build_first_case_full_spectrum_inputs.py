"""Complete whole-first-case inputs from independently verified family deletions."""
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
from first_case_spectrum_scope import CaseScope

H=Path(__file__).resolve().parent


def run(authority_path,first,output):
    directory=output.with_suffix(''); assert not output.exists() and not directory.exists()
    start=monotonic(); b=Bindings(); authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_WHOLE_FAMILY_DELETIONS'
    selected=[r for r in authority['records'] if r['first_row']==first]; assert len(selected)==1
    accepted=selected[0]; assert not accepted['conditional_case_excluded']
    ref=authority['source']; old=b.read(ref['path'],ref['sha256'])
    selected=[r for r in old['records'] if r['first_row']==first]; assert len(selected)==1
    record=selected[0]; previous=read_certificate(b,record['proof'])
    assert old['refinement_authority']==authority['refinement_authority']
    data=load(b,authority['refinement_authority']['path'])
    assert b.bind(authority['refinement_authority']['path'])==authority['refinement_authority']
    assert data.quotient_reference==authority['quotient_authority']
    assert data.authority['geometry_index']==authority['geometry_index']
    candidate=data.quota['selected_row_indices'].index(first)
    domains=previous['final_domains']; assert previous['first_row']==first and previous['parent_candidate_index']==candidate
    assert domains[data.quota['component_index']]==[candidate]
    assert list(map(len,domains))==accepted['final_domain_sizes'] and all(domains)
    instance=read_certificate(b,data.quota['instance']); geometry=instance['geometry']
    core_mask=geometry['positive_doubles'][0]&geometry['positive_doubles'][1]
    core=[i for i in range(14) if core_mask>>i&1]; outside=instance['outside']; features=instance['core_pair_order']
    assert len(core)==4 and len(outside)==10
    safe={c['local_core_pair'] for c in instance['components'] if c['kind']=='safe_pair_row'}
    matching=next(([q,15^q] for q in sorted(safe) if q<(15^q) and (15^q) in safe),None)
    assert matching is not None
    tables=[t[d,:1024].astype(np.int16) for t,d in zip(data.tables,domains)]
    assert all(np.array_equal(t,-t[:,np.arange(1024)^1023]) for t in tables)
    pools=[]
    for x in range(512):
        words=guarded_words(x.bit_count(),1-(x&1)-((x>>1)&1)); live=np.ones(len(words),dtype=bool)
        for j,feature in enumerate(features): live &= np.isin(words[:,feature],tables[j][:,x])
        pools.append(sorted(set(tuple(map(int,row)) for row in words[live])))
    directory.mkdir(); blocks=[]
    for j,table in enumerate(tables):
        values=table[:,:512,None]; path=directory/f'component-{j}.npy'; np.save(path,values,allow_pickle=False)
        blocks.append(dict(components=[j],features=[features[j]],original_domain=domains[j],
                           values=dict(**b.bind(path),shape=list(values.shape),dtype=str(values.dtype))))
    fixed={s:-2 for s in geometry['negative_supports']}; fixed.update({s:2 for s in geometry['positive_doubles']})
    assert len(geometry['negative_supports'])==4 and len(geometry['positive_doubles'])==2 and len(fixed)==6
    coefficients=projected_coefficients(core,outside,5,fixed,{1:(1,2),3:(-1,0),5:(0,1)})
    ref=data.quotient_reference; scope=CaseScope(authority['geometry_index'],first,ref['path'],ref['sha256']).to_data()
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(scope=scope,domain_authority=b.bind(authority_path),domain_proof=record['proof'],
        geometry=geometry,core=core,outside=outside,face_points=list(range(512)),fixed_outside_coordinate=outside[-1],
        all_component_rows_complement_odd=True,safe_matching=matching,word_pools=pools,blocks=blocks,
        additional_word_filters=[],projected_coefficients=[asdict(c) for c in coefficients]))
    for name in ('build_first_case_full_spectrum_inputs.py','first_case_spectrum_scope.py','test_first_case_spectrum_scope.py',
                 'selfdual_core_projection.py','test_selfdual_core_projection.py','read_matched_cross_arrays.py',
                 'matched_component_frontier.py','matching_core_word_lemma_cycle224.md',
                 'full_outside_spectrum_soundness_cycle526.md','parity_face_extension_cycle514.md','selfdualization.md'):
        b.bind(H/name)
    result=dict(schema_version=1,status='PROPOSED_FIRST_CASE_FULL_SPECTRUM_INPUTS',global_status='UNRESOLVED',scope=scope,
        domain_authority=b.bind(authority_path),refinement_authority=authority['refinement_authority'],proof=b.bind(proof_path),
        original_pattern_counts=list(map(len,tables)),word_pool_sizes=list(map(len,pools)),word_variables=sum(map(len,pools)),
        projected_coefficients=len(coefficients),free_coefficient_flags=sum(len(c.values)==2 for c in coefficients),
        empty_points=[x for x,pool in enumerate(pools) if not pool],independent_audit='PENDING',
        whole_first_case_necessary_cover_claim=True,whole_first_case_excluded=False,
        actual_boolean_function=False,global_goal_complete=False,seconds=monotonic()-start,
        process_peak_resident_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream: json.dump(result,stream,indent=2); stream.write('\n')
    print(json.dumps({k:result[k] for k in ('scope','original_pattern_counts','word_variables','projected_coefficients',
                                          'free_coefficient_flags','empty_points','seconds')}),flush=True)


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__); parser.add_argument('--authority',type=Path,required=True)
    parser.add_argument('--first-row',type=int,required=True); parser.add_argument('--output',type=Path,required=True)
    a=parser.parse_args(); run(a.authority,a.first_row,a.output)
