"""Independent full-tree replay with explicit conditional quotient scope."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_finite_function_csp import verify_tree

H=Path(__file__).resolve().parent


def run(source_path,output):
    assert not output.exists();start=monotonic();b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_CONDITIONAL_MATCHED_COUNT_SEARCH'
    refinement=b.read(source['refinement_authority']['path'],source['refinement_authority']['sha256'])
    cover=b.read(source['cover_authority']['path'],source['cover_authority']['sha256'])
    assert refinement['status']=='INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT'
    assert cover['status']=='INDEPENDENTLY_VERIFIED_MATCHED_CONDITIONAL_SECOND_ROW_COVERS'
    assert cover['quotient_authority']==refinement['base_authority']
    quota=b.read(refinement['base_authority']['path'],refinement['base_authority']['sha256'])
    assert quota['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    assert source['geometry_index']==cover['geometry_index']==refinement['geometry_index']==quota['geometry_index']
    records=[r for r in cover['records']if r['first_row']==source['first_row']];assert len(records)==1
    record=records[0];assert record['complete_conditional_actual_cover'] is True
    assert record['first_pair']==source['first_pair']==quota['marked_pair'] and record['second_pair']==source['second_pair']
    instance=read_certificate(b,quota['instance']);extra=read_certificate(b,refinement['refinement'])
    proof=read_certificate(b,source['proof'])
    assert proof['refinement_authority']==source['refinement_authority'] and proof['cover_authority']==source['cover_authority']
    assert proof['first_row']==source['first_row']
    base=[]
    for j,c in enumerate(instance['components']):
        values=np.load(c['values']['path'],allow_pickle=False)
        if j==quota['component_index']:values=np.stack([values[i]for i in quota['selected_row_indices']])
        counts=np.load(extra['columns'][j]['counts']['path'],allow_pickle=False)
        base.append(np.concatenate((values,counts[:,None]),axis=1))
    core=quota['geometry']['positive_doubles'][0]&quota['geometry']['positive_doubles'][1]
    vertices=[v for v in range(14)if core>>v&1]
    global_pairs=[sum(1<<v for i,v in enumerate(vertices)if local>>i&1)for local in instance['core_pair_order']]
    first=global_pairs.index(record['first_pair']);second=global_pairs.index(record['second_pair'])
    assert first==quota['component_index'] and first!=second and instance['components'][second]['kind']=='safe_pair_row'
    maps=[list(range(len(t)))for t in base]
    maps[first]=[quota['selected_row_indices'].index(record['first_row'])];maps[second]=record['selected_second_rows']
    assert maps==proof['parent_index_maps']
    tables=[np.stack([table[i]for i in indices])for table,indices in zip(base,maps)]
    assert list(map(len,tables))==source['domain_sizes']
    lookup={(r['weight'],r['delta']):r['tuples']for r in instance['relation_types']}
    relations=[lookup[x.bit_count(),1-(x&1)-((x>>1)&1)]for x in range(1024)]+[extra['allowed_count_tuples']]
    answer=proof['answer'];status=verify_tree(tables,relations,answer['tree'])
    assert status==answer['status']==source['search_status']
    stack=[answer['tree']];visited=pending=0;witnesses=[]
    while stack:
        node=stack.pop()
        if node['kind']=='LIMIT':pending+=1
        else:
            visited+=1;stack.extend(node.get('children',[]))
            if 'witness'in node:witnesses.append(node['witness'])
    assert visited==answer['nodes']==source['nodes']<=answer['max_nodes']==source['max_nodes']
    assert answer['witness']==source['witness']
    if status=='SAT':assert witnesses==[source['witness']]
    else:assert not witnesses and source['witness'] is None
    if status=='UNSAT':assert pending==0
    for name in ('verify_conditional_matched_count_search.py','verify_finite_function_csp.py','test_verify_finite_function_csp.py',
                 'matched_conditional_second_cover_soundness_cycle307.md','test_restricted_function_tables.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_CONDITIONAL_MATCHED_COUNT_SEARCH',global_status='UNRESOLVED',
                source=b.bind(source_path),refinement_authority=source['refinement_authority'],cover_authority=source['cover_authority'],
                geometry_index=source['geometry_index'],first_row=source['first_row'],first_pair=source['first_pair'],second_pair=source['second_pair'],
                search_status=status,verified_search_nodes=visited,unsearched_subtrees=pending,
                conditional_case_excluded=status=='UNSAT',whole_geometry_excluded=False,global_goal_complete=False,
                necessary_component_witness=source['witness'],actual_boolean_function=False,
                parent_candidate_witness=None if source['witness']is None else [maps[j][i]for j,i in enumerate(source['witness'])],
                producer_imported=False,bitset_kernel_imported=False,seconds=monotonic()-start,
                files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ('geometry_index','first_row','search_status','verified_search_nodes','unsearched_subtrees','seconds')}),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
