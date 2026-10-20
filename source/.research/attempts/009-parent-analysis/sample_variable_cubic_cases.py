"""Sample coefficient LPs from the exact current pair/count frontier."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from two_positive_four_cube_domains import CubeIndex,setup
from fixed_projection_cube_domains import projection_values
from conditional_cubic_energy import conditional_values
from variable_cubic_energy import build
from exact_box_row_lp import solve

H=Path(__file__).resolve().parent


def run(frontier_path,output,limit,seconds):
    assert limit>0 and seconds>0;start=monotonic();b=Bindings();frontier=b.read(frontier_path)
    assert frontier['status']=='ACCEPTED_PARENT00_COUPLED_PROJECTION_FRONTIER'
    authority=b.read(frontier['pair_authority']['path'],frontier['pair_authority']['sha256'])
    assert authority['status'] in ('INDEPENDENTLY_VERIFIED_PARENT00_VARIABLE_CUBIC_CERTIFICATE_TRANSFERS','INDEPENDENTLY_VERIFIED_INCREMENTAL_CUBIC_COEFFICIENT_TRANSFERS')
    selected=sorted((r for r in authority['records'] if r['remaining_pairs']),key=lambda r:(r['remaining_count_cases'],r['index'],r['projection_index']))[:limit]
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];cubes=CubeIndex.build(rows);pairs,_=setup(frontier['geometry'])
    directory=output.with_suffix('');assert not directory.exists() and not output.exists();directory.mkdir();records=[]
    for record in selected:
        previous=read_certificate(b,record['proof']);source=read_certificate(b,previous['previous']);B=projection_values(source['spectrum'])
        chosen=min(record['remaining'],key=lambda r:r['pair_index']);j=chosen['pair_index'];N=min(chosen['negative_counts']);row_pair=chosen['row_pair']
        row_ids=[d['rows'][0] for d in source['input_domains']]
        for slot,row in zip(source['proof']['free_slots'],row_pair):row_ids[slot]=row
        values=[list(conditional_values(pairs,x.bit_count(),(1,0,0,-1)[x&3],tuple(int(cubes.table[r,x]) for r in row_ids),3,B[x],12)) for x in range(1024)]
        assert all(values) and values[0]==[4]
        for energy in (False,True):
            variables,inequalities=build(10,N,values,energy=energy);result=solve(inequalities,len(variables),seconds=seconds)
            if 'fractional_variables' in result:result['fractional_variables']=int(result['fractional_variables'])
            detail=dict(index=record['index'],projection_index=record['projection_index'],pair_index=j,row_pair=row_pair,case_authority=record['proof'],previous=previous['previous'],geometry=frontier['geometry'],parent=frontier['parent'],
                negative_count=N,fixed_core_mask=3,target_core_mask=12,energy=energy,variables=[v.metadata() for v in variables],values=values,result=result)
            path=directory/f'r{record["index"]:02d}-p{record["projection_index"]:03d}-j{j:04d}-n{N}-e{int(energy)}.json.gz';write_certificate(path,detail)
            entry=dict(index=record['index'],projection_index=record['projection_index'],pair_index=j,row_pair=row_pair,negative_count=N,energy=energy,proof=b.bind(path),status=result['status'],seconds=result['elapsed_seconds'])
            records.append(entry);print(json.dumps({k:v for k,v in entry.items() if k!='proof'}),flush=True)
            if result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION':break
    for name in ('sample_variable_cubic_cases.py','variable_cubic_energy.py','test_variable_cubic_energy.py'):b.bind(H/name)
    result=dict(status='SAMPLED_VARIABLE_CUBIC_COEFFICIENT_CASES',global_status='UNRESOLVED',independent_audit='PENDING',frontier=b.bind(frontier_path),authority=frontier['pair_authority'],
        geometry=frontier['geometry'],parent=frontier['parent'],parameters=dict(limit=limit,seconds=seconds),records=records,elapsed_seconds=monotonic()-start,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--frontier',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--limit',type=int,default=3);p.add_argument('--seconds',type=float,default=20);a=p.parse_args();run(a.frontier,a.output,a.limit,a.seconds)
