"""Independently turn a complete row-family exclusion into transported Q<=4 rules."""
from argparse import ArgumentParser
from pathlib import Path
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate

H=Path(__file__).resolve().parent


def check_family(universe,excluded,rows):
    family=[i for i in universe if len(rows[i]['unit_faces'])==12]
    assert family and set(family)<=set(excluded)
    return family


def check_transport(known,source_pair,target_pair,image):
    assert sorted(image)==list(range(14))
    def moved(q):return sum(1<<image[v]for v in range(14)if q>>v&1)
    assert moved(source_pair)==target_pair and {moved(q):k for q,k in known.items()}==known


def run(proposal_path,refinement_path,output):
    assert not output.exists();b=Bindings();proposal=b.read(proposal_path);refinement=b.read(refinement_path)
    assert proposal['status']=='PROPOSED_SIGNED_GEOMETRY_SAFE_PAIR_TRANSPORTS'
    assert refinement['status']=='INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT'
    frontier=b.read(proposal['frontier']['path'],proposal['frontier']['sha256'])
    assert frontier['status']=='VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER'
    assert frontier['scope']['quotient_authority']==proposal['quotient_authority']==refinement['base_authority']
    quota=b.read(proposal['quotient_authority']['path'],proposal['quotient_authority']['sha256'])
    assert quota['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    full=b.read(quota['base_instance_authority']['path'],quota['base_instance_authority']['sha256'])
    assert full['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_MATCHED_CORE_COMPONENT_INSTANCE' and full['complete_component_domains'] is True
    assert full['instance']==quota['instance']
    geometry=quota['geometry'];marked=quota['marked_pair']
    assert proposal['geometry_index']==refinement['geometry_index']==frontier['scope']['geometry_index']==geometry['index']
    assert proposal['marked_pair']==frontier['scope']['marked_pair']==marked
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows']
    family=check_family(quota['selected_row_indices'],frontier['excluded_first_rows'],rows)
    known={q:-2 for q in geometry['negative_supports']}|{q:2 for q in geometry['positive_doubles']}
    targets={marked}
    for record in proposal['transports']:
        assert record['source_pair']==marked and record['target_pair'] in geometry['eligible_pairs']
        check_transport(known,marked,record['target_pair'],record['map']);targets.add(record['target_pair'])
    instance=read_certificate(b,quota['instance']);extra=read_certificate(b,refinement['refinement'])
    core=geometry['positive_doubles'][0]&geometry['positive_doubles'][1];vertices=[v for v in range(14)if core>>v&1]
    weights=np.array([10-2*x.bit_count()for x in range(1024)],dtype=np.int64)
    expected=np.array([len(row['unit_faces'])-4 for row in rows],dtype=np.int64)
    indices=[];checked=0
    for j,component in enumerate(instance['components']):
        if component['kind']!='safe_pair_row':continue
        pair=sum(1<<v for i,v in enumerate(vertices)if component['local_core_pair']>>i&1)
        assert pair in geometry['eligible_pairs'] and component['row_count']==len(rows)
        values=np.load(component['values']['path'],allow_pickle=False)
        linear_sum=-(values.astype(np.int64)@weights)
        assert np.all(linear_sum%1024==0);counts=linear_sum//1024
        assert np.array_equal(counts,expected) and set(map(int,counts))=={2,4,8}
        actual_counts=counts[quota['selected_row_indices']]if j==quota['component_index']else counts
        stored=np.load(extra['columns'][j]['counts']['path'],allow_pickle=False)
        assert np.array_equal(actual_counts,stored);checked+=len(values)
        if pair in targets:indices.append(j)
    assert len(indices)==len(targets) and quota['component_index'] in indices
    for name in ('verify_matched_safe_count_exclusion.py','test_verify_matched_safe_count_exclusion.py',
                 'matched_safe_eight_exclusion_cycle323.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_MATCHED_SAFE_LINEAR_COUNT_EXCLUSIONS',global_status='UNRESOLVED',
                proposal=b.bind(proposal_path),frontier=proposal['frontier'],base_refinement=b.bind(refinement_path),
                quotient_authority=proposal['quotient_authority'],geometry_index=geometry['index'],
                marked_pair=marked,excluded_quotient_rows=family,safe_pairs_restricted=sorted(targets),
                component_indices_restricted=indices,excluded_linear_count=8,remaining_linear_counts=[2,4],
                safe_catalog_rows_checked=checked,transport_maps_checked=len(proposal['transports']),
                canonicalizer_imported=False,actual_function_scope=True,whole_geometry_excluded=False,global_goal_complete=False,
                files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ('geometry_index','safe_pairs_restricted','component_indices_restricted','safe_catalog_rows_checked','transport_maps_checked')}))


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--proposal',type=Path,required=True);p.add_argument('--refinement',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.proposal,a.refinement,a.output)
