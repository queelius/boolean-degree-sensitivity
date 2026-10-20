"""Independently check conditional second-row maps with the first spectrum fixed."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_coupled_two_positive import literal_embedding
from verify_matched_first_row_cover import row_map_coverage
from verify_parent_coordinate_cover import check_map
from verify_two_positive_conditional_orbits import relabel

H=Path(__file__).resolve().parent


def check_condition(image,known,first_pair,second_pair):
    assert sorted(image)==list(range(14))
    assert relabel(first_pair,image)==first_pair and relabel(second_pair,image)==second_pair
    assert {relabel(q,image):k for q,k in known.items()}==known


def run(source_path,output):
    b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_MATCHED_CONDITIONAL_SECOND_ROW_COVER_PILOT'
    quota=b.read(source['quotient_authority']['path'],source['quotient_authority']['sha256'])
    assert quota['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    residual=b.read(source['residual_cover']['path'],source['residual_cover']['sha256'])
    assert residual['status']=='INDEPENDENTLY_VERIFIED_FIRST_ROW_RESIDUAL_COVER_FROM_PARTIAL_SEARCH'
    assert residual['quotient_authority']==source['quotient_authority']
    assert source['geometry_index']==quota['geometry_index']==residual['geometry_index']
    proof=read_certificate(b,source['proof'])
    assert proof['quotient_authority']==source['quotient_authority'] and proof['residual_cover']==source['residual_cover']
    geometry=dict(quota['geometry']);geometry['selected_pair']=quota['marked_pair']
    assert proof['geometry']==geometry
    data=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')
    rows=data['domain']['rows'];accepted=[];seen_first=set()
    for record in proof['records']:
        first=record['first_row'];pair=record['second_pair']
        assert first not in seen_first and first in residual['residual_source_rows'] and first in quota['selected_row_indices'];seen_first.add(first)
        assert pair in geometry['eligible_pairs'] and pair!=geometry['selected_pair']
        known=literal_embedding(rows[first],geometry,geometry['selected_pair'])
        assert record['known']==[list(r)for r in sorted(known.items())] and record['row_family']==len(rows[first]['unit_faces'])
        selected=row_map_coverage(record['maps'],record['representatives'],len(rows))
        assert record['raw_rows']==len(rows) and record['representative_count']==len(selected)
        targets={r['index']:literal_embedding(rows[r['row']],geometry,pair)for r in record['representatives']}
        checked=set()
        for mapping in record['maps']:
            image=tuple(mapping['map'])
            if image not in checked:
                check_condition(image,known,geometry['selected_pair'],pair);checked.add(image)
            embedded=literal_embedding(rows[mapping['source_row']],geometry,pair)
            check_map(mapping['map'],embedded,targets[mapping['representative']],geometry)
        accepted.append(dict(first_row=first,first_pair=geometry['selected_pair'],second_pair=pair,
                             selected_second_rows=selected,full_second_row_count=len(rows),maps_checked=len(record['maps']),
                             distinct_maps=len(checked),complete_conditional_actual_cover=True,whole_geometry_covered=False))
    assert sorted(seen_first)==sorted(source['sampled_first_rows'])
    for name in ('verify_matched_conditional_second_cover.py','test_verify_matched_conditional_second_cover.py',
                 'matched_conditional_second_cover_soundness_cycle307.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_MATCHED_CONDITIONAL_SECOND_ROW_COVERS',global_status='UNRESOLVED',
                source=b.bind(source_path),quotient_authority=source['quotient_authority'],geometry_index=quota['geometry_index'],records=accepted,
                conditional_first_spectrum_preserved=True,canonicalizer_imported=False,no_function_symmetry_imposed=True,
                covered_all_first_rows=False,geometry_exclusions=0,global_goal_complete=False,
                files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(geometry=quota['geometry_index'],conditional_covers=len(accepted),
                         maps_checked=sum(r['maps_checked']for r in accepted),
                         representatives=[len(r['selected_second_rows'])for r in accepted])))


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
