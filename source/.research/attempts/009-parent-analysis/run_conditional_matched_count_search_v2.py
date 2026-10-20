"""Search a fixed first row with its independently proved second-row quotient."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from restricted_function_tables import restrict_tables
from matched_component_coordinate_index import component_for_pair
from resume_function_csp import PriorityPointCSP

H=Path(__file__).resolve().parent


def run(refinement_path,cover_path,first_row,max_nodes,output):
    start=monotonic();b=Bindings();refinement=b.read(refinement_path);cover=b.read(cover_path)
    assert refinement['status']=='INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT'
    assert cover['status']=='INDEPENDENTLY_VERIFIED_MATCHED_CONDITIONAL_SECOND_ROW_COVERS'
    assert cover['quotient_authority']==refinement['base_authority'] and cover['geometry_index']==refinement['geometry_index']
    records=[r for r in cover['records']if r['first_row']==first_row];assert len(records)==1
    selected=records[0];assert selected['complete_conditional_actual_cover'] is True
    quota=b.read(refinement['base_authority']['path'],refinement['base_authority']['sha256'])
    assert quota['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    assert selected['first_pair']==quota['marked_pair']
    instance=read_certificate(b,quota['instance']);extra=read_certificate(b,refinement['refinement'])
    tables=[]
    for j,component in enumerate(instance['components']):
        values=np.load(component['values']['path'],allow_pickle=False)
        if j==quota['component_index']:values=values[quota['selected_row_indices']]
        counts=np.load(extra['columns'][j]['counts']['path'],allow_pickle=False)
        tables.append(np.column_stack((values,counts)))
    indices=[list(range(len(t)))for t in tables]
    first_index=quota['component_index'];indices[first_index]=[quota['selected_row_indices'].index(first_row)]
    second_index=component_for_pair(quota['geometry'],instance,selected['second_pair'])
    assert first_index!=second_index and instance['components'][second_index]['kind']=='safe_pair_row'
    indices[second_index]=selected['selected_second_rows'];restricted=restrict_tables(tables,indices)
    lookup={(r['weight'],r['delta']):r['tuples']for r in instance['relation_types']}
    relations=[lookup[x.bit_count(),1-(x&1)-((x>>1)&1)]for x in range(1024)]+[extra['allowed_count_tuples']]
    order=[1024]+sorted(range(1024),key=lambda x:(min(x.bit_count(),10-x.bit_count()),x))
    solver=PriorityPointCSP(restricted,relations,order,priority_point=1024);answer=solver.search(max_nodes)
    proof_path=output.with_suffix('.json.gz');assert not output.exists()and not proof_path.exists()
    write_certificate(proof_path,dict(refinement_authority=b.bind(refinement_path),cover_authority=b.bind(cover_path),
                                      first_row=first_row,parent_index_maps=indices,answer=answer))
    for name in ('run_conditional_matched_count_search_v2.py','matched_component_coordinate_index.py','test_matched_component_coordinate_index.py','restricted_function_tables.py','test_restricted_function_tables.py',
                 'resume_function_csp.py','test_resume_function_csp.py'):b.bind(H/name)
    result=dict(status='PROPOSED_CONDITIONAL_MATCHED_COUNT_SEARCH',global_status='UNRESOLVED',
                geometry_index=cover['geometry_index'],first_row=first_row,first_pair=selected['first_pair'],second_pair=selected['second_pair'],
                refinement_authority=b.bind(refinement_path),cover_authority=b.bind(cover_path),proof=b.bind(proof_path),
                search_status=answer['status'],nodes=answer['nodes'],max_nodes=max_nodes,domain_sizes=list(map(len,restricted)),
                witness=answer['witness'],necessary_components_only=True,actual_boolean_function=False,
                conditional_case_excluded=answer['status']=='UNSAT',whole_geometry_excluded=False,global_goal_complete=False,
                independent_audit='PENDING',seconds=monotonic()-start,
                files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ('geometry_index','first_row','search_status','nodes','domain_sizes','witness','seconds')}),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--refinement',type=Path,required=True);p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--first-row',type=int,required=True);p.add_argument('--max-nodes',type=int,default=10000);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.refinement,a.cover,a.first_row,a.max_nodes,a.output)
