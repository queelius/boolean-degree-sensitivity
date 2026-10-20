"""Bounded fixed-first-row searches reusing one compiled exact component instance."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import write_certificate
from matched_count_frontier_io import load
from conditioned_function_search import search_from

H=Path(__file__).resolve().parent


def run(residual_path,family,count,max_nodes,output,offset=0):
    assert offset>=0 and count>0
    start=monotonic();b=Bindings();residual=b.read(residual_path)
    assert residual['status']=='INDEPENDENTLY_VERIFIED_FIRST_ROW_RESIDUAL_COVER_FROM_PARTIAL_SEARCH'
    data=load(b,residual['search_authority']['path'])
    assert b.bind(residual['search_authority']['path'])==residual['search_authority']
    quota=b.read(residual['quotient_authority']['path'],residual['quotient_authority']['sha256'])
    assert quota['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['geometry_index']==data.authority['geometry_index']
    domain=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows']
    selected=[r for r in residual['residual_source_rows']if len(domain[r]['unit_faces'])==family][offset:offset+count]
    assert selected and len(selected)<=count
    directory=output.with_suffix('');assert not directory.exists()and not output.exists();directory.mkdir()
    solver=data.solver;records=[];j=quota['component_index']
    for first in selected:
        before=monotonic();candidate=quota['selected_row_indices'].index(first)
        domains=list(solver.initial);domains[j]=1<<candidate
        answer=search_from(solver,domains,max_nodes=max_nodes)
        path=directory/f'first-{first:04d}.json.gz'
        write_certificate(path,dict(search_authority=residual['search_authority'],quotient_authority=residual['quotient_authority'],
                                    first_row=first,component_index=j,parent_candidate_index=candidate,answer=answer))
        record=dict(first_row=first,parent_candidate_index=candidate,proof=b.bind(path),search_status=answer['status'],
                    nodes=answer['nodes'],witness=answer['witness'],seconds=monotonic()-before)
        records.append(record);print(json.dumps({k:v for k,v in record.items()if k!='proof'}),flush=True)
    for name in ('matched_fixed_first_row_batch_v2.py','matched_count_frontier_io.py','conditioned_function_search.py',
                 'test_conditioned_function_search.py','verify_conditioned_function_tree.py'):b.bind(H/name)
    result=dict(status='PROPOSED_FIXED_FIRST_ROW_COMPONENT_SEARCH_BATCH',global_status='UNRESOLVED',geometry_index=quota['geometry_index'],
                residual_authority=b.bind(residual_path),search_authority=residual['search_authority'],quotient_authority=residual['quotient_authority'],
                parameters=dict(row_family=family,offset=offset,selected_first_rows=selected,max_nodes_per_row=max_nodes,split_policy='balanced_point_MRV'),
                records=records,second_row_quotient_used=False,whole_geometry_excluded=False,global_goal_complete=False,independent_audit='PENDING',
                seconds=monotonic()-start,files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(geometry=quota['geometry_index'],cases=len(records),unsat=sum(r['search_status']=='UNSAT'for r in records),
                         unknown=sum(r['search_status']=='UNKNOWN'for r in records),sat=sum(r['search_status']=='SAT'for r in records),seconds=result['seconds'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--residual',type=Path,required=True);p.add_argument('--family',type=int,required=True)
    p.add_argument('--count',type=int,default=10);p.add_argument('--offset',type=int,default=0);p.add_argument('--max-nodes',type=int,default=1000);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.residual,a.family,a.count,a.max_nodes,a.output,a.offset)
