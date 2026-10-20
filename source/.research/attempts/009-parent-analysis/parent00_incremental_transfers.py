"""Transfer newly audited interval certificates over a previously narrowed case list."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from two_positive_four_cube_domains import CubeIndex,setup
from fixed_projection_cube_domains import projection_values
from conditional_cubic_energy import conditional_values
from variable_cubic_transfer import extract

H=Path(__file__).resolve().parent


def run(frontier_path,certificate_path,output):
    start=monotonic();b=Bindings();frontier=b.read(frontier_path);previous=b.read(frontier['pair_authority']['path'],frontier['pair_authority']['sha256']);authority=b.read(certificate_path)
    assert frontier['status']=='ACCEPTED_PARENT00_COUPLED_PROJECTION_FRONTIER' and authority['status']=='INDEPENDENTLY_VERIFIED_SAMPLED_VARIABLE_CUBIC_CERTIFICATES'
    assert authority['frontier']==b.bind(frontier_path) and authority['authority']==frontier['pair_authority']
    basis=[];seen=set()
    for r in authority['records']:
        if not r['excluded'] or r['energy']:continue
        identity=extract(read_certificate(b,r['proof']));key=json.dumps(identity.metadata(),sort_keys=True)
        if key in seen:continue
        seen.add(key);basis.append((r['proof'],identity))
    assert basis;points=sorted({x for ref,identity in basis for x in identity.points()});print(json.dumps(dict(identities=len(basis),points=len(points))),flush=True)
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];cubes=CubeIndex.build(rows);pairs,_=setup(frontier['geometry'])
    directory=output.with_suffix('');assert not directory.exists() and not output.exists();directory.mkdir();records=[]
    for record in previous['records']:
        if not record['remaining_pairs']:continue
        parent_detail=read_certificate(b,record['proof']);source=read_certificate(b,parent_detail['previous']);B=projection_values(source['spectrum']);case=[]
        for chosen in record['remaining']:
            j=chosen['pair_index'];row_pair=chosen['row_pair'];row_ids=[d['rows'][0] for d in source['input_domains']]
            for slot,row in zip(source['proof']['free_slots'],row_pair):row_ids[slot]=row
            values={x:conditional_values(pairs,x.bit_count(),(1,0,0,-1)[x&3],tuple(int(cubes.table[r,x]) for r in row_ids),3,B[x],12) for x in points};assert all(values.values())
            counts=[]
            for N in chosen['negative_counts']:
                rhs=[identity.evaluate(values,N) for ref,identity in basis];best=min(range(len(rhs)),key=lambda i:rhs[i])
                counts.append(dict(negative_count=N,basis=best,integer_rhs=rhs[best],excluded=rhs[best]<0))
            case.append(dict(pair_index=j,row_pair=row_pair,counts=counts,remaining_negative_counts=[r['negative_count'] for r in counts if not r['excluded']]))
        detail=dict(index=record['index'],projection_index=record['projection_index'],geometry=frontier['geometry'],parent=frontier['parent'],case_authority=record['proof'],previous=parent_detail['previous'],records=case)
        path=directory/f'r{record["index"]:02d}-p{record["projection_index"]:03d}.json.gz';write_certificate(path,detail)
        entry=dict(index=record['index'],projection_index=record['projection_index'],proof=b.bind(path),row_pairs=len(case),remaining_pairs=sum(bool(r['remaining_negative_counts']) for r in case),
            count_cases=sum(len(r['counts']) for r in case),remaining_count_cases=sum(len(r['remaining_negative_counts']) for r in case))
        records.append(entry);print(json.dumps({k:v for k,v in entry.items() if k!='proof'}),flush=True)
    for name in ('parent00_incremental_transfers.py','variable_cubic_transfer.py','test_variable_cubic_transfer.py'):b.bind(H/name)
    result=dict(status='PARENT00_INCREMENTAL_CUBIC_COEFFICIENT_TRANSFERS',global_status='UNRESOLVED',independent_audit='PENDING',frontier=b.bind(frontier_path),previous_authority=frontier['pair_authority'],
        certificate_authority=b.bind(certificate_path),geometry=frontier['geometry'],parent=frontier['parent'],basis=[dict(proof=ref,identity=identity.metadata()) for ref,identity in basis],records=records,elapsed_seconds=monotonic()-start,
        sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(seconds=result['elapsed_seconds'],remaining_pairs=sum(r['remaining_pairs'] for r in records),remaining_count_cases=sum(r['remaining_count_cases'] for r in records))),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--frontier',type=Path,required=True);p.add_argument('--certificates',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.frontier,a.certificates,a.output)
