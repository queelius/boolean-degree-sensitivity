"""Independently replay fixed-row batch trees in their exact parent-index scope."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_conditioned_function_tree import verify_from

H=Path(__file__).resolve().parent


def run(source_path,output):
    assert not output.exists();start=monotonic();b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_FIXED_FIRST_ROW_COMPONENT_SEARCH_BATCH'
    residual=b.read(source['residual_authority']['path'],source['residual_authority']['sha256'])
    assert residual['status']=='INDEPENDENTLY_VERIFIED_FIRST_ROW_RESIDUAL_COVER_FROM_PARTIAL_SEARCH'
    assert source['search_authority']==residual['search_authority'] and source['quotient_authority']==residual['quotient_authority']
    authority=b.read(source['search_authority']['path'],source['search_authority']['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_COUNT_SEARCH'
    search=b.read(authority['source']['path'],authority['source']['sha256'])
    refinement=b.read(search['instance_authority']['path'],search['instance_authority']['sha256'])
    assert refinement['status']=='INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT'
    assert refinement['base_authority']==source['quotient_authority']
    quota=b.read(source['quotient_authority']['path'],source['quotient_authority']['sha256'])
    assert quota['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    assert source['geometry_index']==quota['geometry_index']==residual['geometry_index']==authority['geometry_index']
    instance=read_certificate(b,quota['instance']);extra=read_certificate(b,refinement['refinement']);tables=[]
    for j,c in enumerate(instance['components']):
        values=np.load(c['values']['path'],allow_pickle=False)
        if j==quota['component_index']:values=np.stack([values[i]for i in quota['selected_row_indices']])
        counts=np.load(extra['columns'][j]['counts']['path'],allow_pickle=False)
        tables.append(np.concatenate((values,counts[:,None]),axis=1))
    lookup={(r['weight'],r['delta']):r['tuples']for r in instance['relation_types']}
    relations=[lookup[x.bit_count(),1-(x&1)-((x>>1)&1)]for x in range(1024)]+[extra['allowed_count_tuples']]
    selected=source['parameters']['selected_first_rows'];assert len(selected)==len(set(selected))
    assert [r['first_row']for r in source['records']]==selected and set(selected)<=set(residual['residual_source_rows'])
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows']
    assert all(len(rows[first]['unit_faces'])==source['parameters']['row_family']for first in selected)
    checked=[]
    for record in source['records']:
        proof=read_certificate(b,record['proof']);first=record['first_row'];candidate=quota['selected_row_indices'].index(first);j=quota['component_index']
        assert proof['search_authority']==source['search_authority'] and proof['quotient_authority']==source['quotient_authority']
        assert proof['first_row']==first and proof['component_index']==j and proof['parent_candidate_index']==candidate==record['parent_candidate_index']
        indices=[list(range(len(t)))for t in tables];indices[j]=[candidate]
        answer=proof['answer'];status=verify_from(tables,relations,answer['tree'],indices)
        assert status==answer['status']==record['search_status']
        stack=[answer['tree']];visited=pending=0;witnesses=[]
        while stack:
            node=stack.pop()
            if node['kind']=='LIMIT':pending+=1
            else:
                visited+=1;stack.extend(node.get('children',[]))
                if 'witness'in node:witnesses.append(node['witness'])
        assert visited==record['nodes']==answer['nodes']<=answer['max_nodes']==source['parameters']['max_nodes_per_row']
        assert answer['witness']==record['witness']
        if status=='SAT':assert witnesses==[record['witness']]
        else:assert not witnesses and record['witness']is None
        if status=='UNSAT':assert pending==0
        checked.append(dict(first_row=first,parent_candidate_index=candidate,search_status=status,verified_nodes=visited,
                            unsearched_subtrees=pending,conditional_case_excluded=status=='UNSAT',necessary_component_witness=record['witness']))
        print(json.dumps(checked[-1]),flush=True)
    for name in ('verify_fixed_first_row_batch.py','verify_conditioned_function_tree.py','test_conditioned_function_search.py',
                 'verify_finite_function_csp.py','test_verify_finite_function_csp.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_FIXED_FIRST_ROW_COMPONENT_SEARCH_BATCH',global_status='UNRESOLVED',
                source=b.bind(source_path),geometry_index=quota['geometry_index'],marked_pair=quota['marked_pair'],
                quotient_authority=source['quotient_authority'],records=checked,second_row_quotient_used=False,
                producer_imported=False,bitset_kernel_imported=False,whole_geometry_excluded=False,global_goal_complete=False,
                seconds=monotonic()-start,files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(geometry=quota['geometry_index'],cases=len(checked),
                         excluded=sum(r['conditional_case_excluded']for r in checked),seconds=result['seconds'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
