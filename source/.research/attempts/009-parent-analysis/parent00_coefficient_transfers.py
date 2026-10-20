"""Apply sparse coefficient certificates to every remaining joint pair and count."""
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


def run():
    start=monotonic();b=Bindings();frontier_path=H/'parent00-coupled-projection-frontier-cycle114.json';frontier=b.read(frontier_path)
    assert frontier['status']=='ACCEPTED_PARENT00_COUPLED_PROJECTION_FRONTIER'
    joint=b.read(frontier['joint_authority']['path'],frontier['joint_authority']['sha256']);authority=b.read(frontier['coefficient_authority']['path'],frontier['coefficient_authority']['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_CONDITIONAL_SECOND_CUBIC_COEFFICIENT_EXCLUSIONS'
    count_authority=b.read(authority['actual_counts_authority']['path'],authority['actual_counts_authority']['sha256']);count_pairs=set()
    for r in count_authority['actual_missing_diagonal_counts']:
        a,c=r['counts'];count_pairs.update(((a,c),(c,a)))
    basis=[];seen=set()
    for r in authority['records']:
        certificate=read_certificate(b,r['proof']);identity=extract(certificate);key=json.dumps(identity.metadata(),sort_keys=True)
        if key in seen:continue
        seen.add(key);basis.append((r['proof'],identity))
    points=sorted({x for ref,identity in basis for x in identity.points()});print(json.dumps(dict(distinct_identities=len(basis),outside_points=len(points))),flush=True)
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];cubes=CubeIndex.build(rows);pairs,_=setup(frontier['geometry'])
    remaining={(r['index'],j) for r in frontier['records'] for j in r['remaining_representatives']}
    directory=H/'parent00-coefficient-transfers-cycle115';output=directory.with_suffix('.json');assert not directory.exists() and not output.exists();directory.mkdir();records=[]
    for record in joint['records']:
        if (record['index'],record['projection_index']) not in remaining:continue
        source=read_certificate(b,record['proof']);B=projection_values(source['spectrum']);n=len(source['projection']['negative']);counts=sorted(c for a,c in count_pairs if a==n);case=[]
        for j,row_pair in enumerate(source['proof']['surviving_pairs']):
            row_ids=[d['rows'][0] for d in source['input_domains']]
            for slot,row in zip(source['proof']['free_slots'],row_pair):row_ids[slot]=row
            values={x:conditional_values(pairs,x.bit_count(),(1,0,0,-1)[x&3],tuple(int(cubes.table[r,x]) for r in row_ids),3,B[x],12) for x in points};assert all(values.values())
            attempts=[]
            for N in counts:
                rhs=[identity.evaluate(values,N) for ref,identity in basis];best=min(range(len(rhs)),key=lambda i:rhs[i])
                attempts.append(dict(negative_count=N,basis=best,integer_rhs=rhs[best],excluded=rhs[best]<0))
            case.append(dict(pair_index=j,row_pair=row_pair,counts=attempts,remaining_negative_counts=[r['negative_count'] for r in attempts if not r['excluded']]))
        detail=dict(index=record['index'],projection_index=record['projection_index'],geometry=frontier['geometry'],parent=frontier['parent'],previous=record['proof'],allowed_negative_counts=counts,records=case)
        path=directory/f'r{record["index"]:02d}-p{record["projection_index"]:03d}.json.gz';write_certificate(path,detail)
        result=dict(index=record['index'],projection_index=record['projection_index'],proof=b.bind(path),row_pairs=len(case),remaining_pairs=sum(bool(r['remaining_negative_counts']) for r in case),
            count_cases=sum(len(r['counts']) for r in case),remaining_count_cases=sum(len(r['remaining_negative_counts']) for r in case))
        records.append(result);print(json.dumps({k:v for k,v in result.items() if k!='proof'}),flush=True)
    for name in ('variable_cubic_transfer.py','test_variable_cubic_transfer.py','parent00_coefficient_transfers.py'):b.bind(H/name)
    result=dict(status='PARENT00_SPARSE_COEFFICIENT_CERTIFICATE_TRANSFERS',global_status='UNRESOLVED',independent_audit='PENDING',frontier=b.bind(frontier_path),
        geometry=frontier['geometry'],parent=frontier['parent'],basis=[dict(proof=ref,identity=identity.metadata()) for ref,identity in basis],records=records,elapsed_seconds=monotonic()-start,
        sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(seconds=result['elapsed_seconds'],remaining_pairs=sum(r['remaining_pairs'] for r in records),remaining_count_cases=sum(r['remaining_count_cases'] for r in records))),flush=True)


if __name__=='__main__':run()
