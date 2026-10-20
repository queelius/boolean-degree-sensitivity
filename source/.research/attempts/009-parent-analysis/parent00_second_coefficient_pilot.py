"""Pilot coefficient consistency for the most constrained surviving row pairs."""
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


def run():
    start=monotonic();b=Bindings();authority_path=H/'parent00-joint-pairs-independent-manifest-cycle113.json';authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_PARENT00_TWO_ROW_CATALOGS_AND_SYMMETRY'
    counts_path=H/'cubic-two-negative-position-cover-independent-manifest.json';counts=b.read(counts_path,'823639dc656ba01972df0cf2dacdbf49f6e860a9815af2af56e40bdb1cdc6766')
    possibilities={tuple(r['counts']) for r in counts['actual_missing_diagonal_counts']};assert possibilities=={(1,1),(1,2)}
    selected=sorted((r for r in authority['records'] if r['surviving_pairs']),key=lambda r:(r['surviving_pairs'],r['index'],r['projection_index']))[:2]
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];cubes=CubeIndex.build(rows);pairs,_=setup(authority['geometry'])
    directory=H/'parent00-second-coefficient-pilot-cycle114';output=directory.with_suffix('.json');assert not directory.exists() and not output.exists();directory.mkdir();records=[]
    for record in selected:
        source=read_certificate(b,record['proof']);assert len(source['projection']['negative'])==2;B=projection_values(source['spectrum'])
        for j,row_pair in enumerate(source['proof']['surviving_pairs']):
            row_ids=[d['rows'][0] for d in source['input_domains']]
            for slot,row in zip(source['proof']['free_slots'],row_pair):row_ids[slot]=row
            values=[list(conditional_values(pairs,x.bit_count(),(1,0,0,-1)[x&3],tuple(int(cubes.table[r,x]) for r in row_ids),3,B[x],12)) for x in range(1024)]
            assert all(values) and values[0]==[4]
            for energy in (False,True):
                variables,inequalities=build(10,1,values,energy=energy);result=solve(inequalities,len(variables),seconds=20)
                if 'fractional_variables' in result:result['fractional_variables']=int(result['fractional_variables'])
                detail=dict(index=record['index'],projection_index=record['projection_index'],pair_index=j,row_pair=row_pair,previous=record['proof'],geometry=authority['geometry'],parent=authority['parent'],
                    negative_count=1,fixed_core_mask=3,target_core_mask=12,energy=energy,variables=[v.metadata() for v in variables],values=values,result=result)
                path=directory/f'r{record["index"]:02d}-p{record["projection_index"]:03d}-j{j:02d}-e{int(energy)}.json.gz';write_certificate(path,detail)
                entry=dict(index=record['index'],projection_index=record['projection_index'],pair_index=j,row_pair=row_pair,energy=energy,proof=b.bind(path),status=result['status'],seconds=result['elapsed_seconds'])
                records.append(entry);print(json.dumps({k:v for k,v in entry.items() if k!='proof'}),flush=True)
                if result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION':break
    for name in ('variable_cubic_energy.py','test_variable_cubic_energy.py','parent00_second_coefficient_pilot.py'):b.bind(H/name)
    result=dict(status='PARENT00_CONDITIONAL_SECOND_CUBIC_COEFFICIENT_PILOT',global_status='UNRESOLVED',independent_audit='PENDING',authority=b.bind(authority_path),actual_counts_authority=b.bind(counts_path),
        geometry=authority['geometry'],parent=authority['parent'],selection_rule='two surviving representatives with fewest joint row pairs',records=records,elapsed_seconds=monotonic()-start,
        sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':run()
