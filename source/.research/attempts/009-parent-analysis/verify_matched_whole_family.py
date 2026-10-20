"""Replay scoped family deletions through literal finite-relation point covers."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from read_matched_cross_arrays import load
from verify_global_pair_consistency import replay_steps,incompatible
from cached_deletion_replay import replay_cached

H=Path(__file__).resolve().parent


def run(source_path,output):
    assert not output.exists();start=monotonic();b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_MATCHED_WHOLE_FAMILY_PROPAGATION'
    data=load(b,source['refinement_authority']['path']);assert b.bind(source['refinement_authority']['path'])==source['refinement_authority']
    frontier=b.read(source['frontier_authority']['path'],source['frontier_authority']['sha256'])
    assert frontier['status']=='VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER'
    assert frontier['scope']['quotient_authority']==data.quotient_reference
    assert source['geometry_index']==data.authority['geometry_index']==frontier['scope']['geometry_index']
    firsts=source['parameters']['first_rows'];assert len(set(firsts))==len(firsts)and set(firsts)<=set(frontier['remaining_first_rows'])
    assert [r['first_row']for r in source['records']]==firsts
    checked=[]
    for record in source['records']:
        proof=read_certificate(b,record['proof']);first=record['first_row'];j=data.quota['component_index']
        candidate=data.quota['selected_row_indices'].index(first)
        assert proof['first_row']==first and proof['parent_candidate_index']==candidate
        domains=[np.arange(len(t),dtype=np.int64)for t in data.tables];domains[j]=np.array([candidate],dtype=np.int64)
        initial=proof['initial_propagation'];domains=replay_steps(data.tables,data.relations,domains,initial['steps'])
        assert list(map(len,domains))==initial['domain_sizes']==record['initial_domain_sizes']
        contradiction=initial['contradiction_point']is not None
        if contradiction:assert incompatible(data.tables,data.relations,domains,initial['contradiction_point'])
        assert len(proof['stages'])==record['rounds']<=source['parameters']['max_rounds'];deleted=0;cache_stats={}
        for stage in proof['stages']:
            assert not contradiction
            domains=replay_cached(data.tables,data.relations,domains,stage['deletions'],stats=cache_stats);deleted+=len(stage['deletions'])
            if any(not len(d)for d in domains):
                assert'point_propagation'not in stage;contradiction=True
            else:
                point=stage['point_propagation'];domains=replay_steps(data.tables,data.relations,domains,point['steps'])
                if point['contradiction_point']is not None:
                    assert incompatible(data.tables,data.relations,domains,point['contradiction_point']);contradiction=True
        assert deleted==record['deletions']and [d.tolist()for d in domains]==proof['final_domains']
        assert list(map(len,domains))==record['final_domain_sizes']
        assert proof['status']==record['propagation_status']in('CONTRADICTION','FIXED_POINT','LIMIT')
        assert contradiction==(proof['status']=='CONTRADICTION')
        checked.append(dict(first_row=first,verified_whole_family_deletions=deleted,conditional_case_excluded=contradiction,
                            initial_domain_sizes=record['initial_domain_sizes'],final_domain_sizes=list(map(len,domains)),
                            producer_propagation_status=proof['status'],cover_verification=cache_stats))
    for name in ('verify_matched_whole_family.py','read_matched_cross_arrays.py','verify_global_pair_consistency.py',
                 'test_verify_global_pair_consistency.py','matched_ordinary_cross_intersection_cycle331.md',
                 'cached_deletion_replay.py','test_cached_deletion_replay.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_MATCHED_WHOLE_FAMILY_DELETIONS',global_status='UNRESOLVED',
                source=b.bind(source_path),refinement_authority=source['refinement_authority'],quotient_authority=data.quotient_reference,
                geometry_index=source['geometry_index'],marked_pair=data.quota['marked_pair'],records=checked,
                producer_imported=False,packed_mask_kernel_imported=False,bitset_kernel_imported=False,
                fixed_point_claim_verified=False,whole_geometry_excluded=False,global_goal_complete=False,
                seconds=monotonic()-start,files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(geometry=source['geometry_index'],cases=len(checked),deletions=sum(r['verified_whole_family_deletions']for r in checked),
                         excluded=sum(r['conditional_case_excluded']for r in checked),seconds=result['seconds'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
