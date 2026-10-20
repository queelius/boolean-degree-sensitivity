"""Extract a necessary first-row residual cover by independently replaying open spines."""
from argparse import ArgumentParser
from pathlib import Path
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_global_pair_consistency import frontier_domains

H=Path(__file__).resolve().parent


def run(authority_path,output):
    b=Bindings();authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_COUNT_SEARCH' and authority['search_status']=='UNKNOWN'
    source=b.read(authority['source']['path'],authority['source']['sha256']);proof=read_certificate(b,source['proof'])
    refinement=b.read(source['instance_authority']['path'],source['instance_authority']['sha256'])
    assert refinement['status']=='INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT'
    quota=b.read(refinement['base_authority']['path'],refinement['base_authority']['sha256'])
    assert quota['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    instance=read_certificate(b,quota['instance']);extra=read_certificate(b,refinement['refinement'])
    assert authority['geometry_index']==quota['geometry_index']==instance['geometry_index']
    tables=[]
    for j,c in enumerate(instance['components']):
        values=np.load(c['values']['path'],allow_pickle=False)
        if j==quota['component_index']:values=np.stack([values[i]for i in quota['selected_row_indices']])
        counts=np.load(extra['columns'][j]['counts']['path'],allow_pickle=False)
        tables.append(np.concatenate((values,counts[:,None]),axis=1))
    lookup={(r['weight'],r['delta']):r['tuples']for r in instance['relation_types']}
    relations=[lookup[x.bit_count(),1-(x&1)-((x>>1)&1)]for x in range(1024)]+[extra['allowed_count_tuples']]
    paths=[]
    def visit(node,path):
        if node['kind']=='UNSAT':return
        if node['kind']=='LIMIT':paths.append(path);return
        assert node['kind']=='UNKNOWN' and len(node['children'])==2
        for direction,child in enumerate(node['children']):visit(child,path+[direction])
    visit(proof['answer']['tree'],[]);assert len(paths)==authority['unsearched_subtrees']
    records=[];residual=set();j=quota['component_index']
    for path in paths:
        domains=frontier_domains(tables,relations,proof['answer']['tree'],path)
        rows=list(map(int,domains[j]));residual.update(rows)
        records.append(dict(path=path,first_row_candidate_indices=rows,domain_sizes=list(map(len,domains))))
    excluded=sorted(set(range(len(tables[j])))-residual);residual=sorted(residual)
    for name in ('matched_first_row_search_progress_cycle306.py','verify_global_pair_consistency.py',
                 'test_verify_global_pair_consistency.py','matched_first_row_residual_cover_cycle306.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_FIRST_ROW_RESIDUAL_COVER_FROM_PARTIAL_SEARCH',global_status='UNRESOLVED',
                search_authority=b.bind(authority_path),quotient_authority=refinement['base_authority'],
                geometry_index=authority['geometry_index'],marked_component_index=j,records=records,
                first_row_total=len(tables[j]),excluded_candidate_indices=excluded,residual_candidate_indices=residual,
                excluded_source_rows=[quota['selected_row_indices'][i]for i in excluded],
                residual_source_rows=[quota['selected_row_indices'][i]for i in residual],
                independent_array_spine_replay=True,producer_imported=False,geometry_exclusions=0,global_goal_complete=False,
                files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(geometry=authority['geometry_index'],first_row_total=len(tables[j]),
                         excluded_first_rows=len(excluded),remaining_first_rows=len(residual),pending_paths=len(paths))))


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--authority',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.authority,a.output)
