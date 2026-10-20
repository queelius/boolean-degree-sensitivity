"""Assemble conditional UNSAT authorities into one exact first-row frontier."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from merge_first_row_exclusions import merge_rows
from matched_first_row_authorities import closed_batch_rows

H=Path(__file__).resolve().parent


def run(base_path,closures,output,batches=()):
    b=Bindings();base=b.read(base_path)
    assert base['status']=='INDEPENDENTLY_VERIFIED_FIRST_ROW_RESIDUAL_COVER_FROM_PARTIAL_SEARCH'
    quota=b.read(base['quotient_authority']['path'],base['quotient_authority']['sha256'])
    assert quota['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    universe=quota['selected_row_indices']
    assert len(universe)==base['first_row_total']
    assert set(base['excluded_source_rows']).isdisjoint(base['residual_source_rows'])
    assert sorted(base['excluded_source_rows']+base['residual_source_rows'])==sorted(universe)
    records=[]
    for path in closures:
        closure=b.read(path)
        assert closure['status']=='INDEPENDENTLY_VERIFIED_CONDITIONAL_MATCHED_COUNT_SEARCH'
        assert closure['search_status']=='UNSAT' and closure['conditional_case_excluded'] is True
        assert closure['unsearched_subtrees']==0 and closure['necessary_component_witness'] is None
        assert closure['geometry_index']==base['geometry_index']==quota['geometry_index']
        assert closure['first_pair']==quota['marked_pair']
        cover=b.read(closure['cover_authority']['path'],closure['cover_authority']['sha256'])
        assert cover['status']=='INDEPENDENTLY_VERIFIED_MATCHED_CONDITIONAL_SECOND_ROW_COVERS'
        assert cover['quotient_authority']==base['quotient_authority']
        records.append(dict(first_row=closure['first_row'],authority=b.bind(path),verified_nodes=closure['verified_search_nodes']))
    for path in batches:
        batch=b.read(path)
        for index,first,nodes in closed_batch_rows(batch,base['geometry_index'],quota['marked_pair'],base['quotient_authority']):
            records.append(dict(first_row=first,authority=b.bind(path),record_index=index,verified_nodes=nodes,kind='fixed_first_row_batch'))
    merged=merge_rows(universe,base['excluded_source_rows'],[r['first_row']for r in records])
    for name in ('assemble_matched_first_row_exclusions_v2.py','matched_first_row_authorities.py','test_matched_first_row_authorities.py','merge_first_row_exclusions.py','test_merge_first_row_exclusions.py',
                 'matched_first_row_residual_cover_cycle306.md','matched_conditional_second_cover_soundness_cycle307.md'):b.bind(H/name)
    result=dict(schema_version=1,status='VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER',global_status='UNRESOLVED',
                scope=dict(geometry_index=base['geometry_index'],marked_pair=quota['marked_pair'],quotient_authority=base['quotient_authority']),
                base_residual_authority=b.bind(base_path),conditional_exclusion_authorities=records,
                total_first_rows=len(universe),excluded_first_rows=merged['excluded'],remaining_first_rows=merged['remaining'],
                newly_excluded_first_rows=merged['newly_excluded'],whole_geometry_excluded=merged['whole_geometry_excluded'],
                global_goal_complete=False,bookkeeping_replays_mathematics=False,
                files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(geometry=base['geometry_index'],excluded=len(merged['excluded']),remaining=len(merged['remaining']),
                         newly_excluded=merged['newly_excluded'],whole_geometry_excluded=merged['whole_geometry_excluded'])))


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--closures',type=Path,nargs='*',default=[]);p.add_argument('--batches',type=Path,nargs='*',default=[])
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.base,a.closures,a.output,a.batches)
