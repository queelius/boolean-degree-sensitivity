"""Exhaust all two-row combinations under one fully specified cubic projection."""
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from two_positive_four_cube_domains import CubeIndex,setup
from fixed_projection_cube_domains import conditioned_relation,projection_values

H=Path(__file__).resolve().parent


def joint_pairs(domains,g,cubes,mask,spectrum):
    fixed=[i for i,d in enumerate(domains) if len(d['rows'])==1];free=[i for i,d in enumerate(domains) if len(d['rows'])>1]
    assert len(free)==2
    pairs,_=setup(g);values=projection_values(spectrum);left,right=[domains[j]['rows'] for j in free]
    live=np.ones((len(left),len(right)),dtype=bool);steps=[]
    for x in sorted(range(1024),key=lambda x:(min(x.bit_count(),10-x.bit_count()),x)):
        allowed=conditioned_relation(pairs,x.bit_count(),(1,0,0,-1)[x&3],mask,values[x]);table=np.zeros((5,5),dtype=bool)
        for ts in allowed:
            if all(ts[j]==int(cubes.table[domains[j]['rows'][0],x]) for j in fixed):table[ts[free[0]]+2,ts[free[1]]+2]=True
        before=int(live.sum());live&=table[cubes.table[left,x,None]+2,cubes.table[right,x][None,:]+2];after=int(live.sum())
        if after!=before:steps.append(dict(point=x,before=before,after=after))
        if not after:break
    surviving=[[left[i],right[j]] for i,j in zip(*np.nonzero(live))]
    return dict(status='COMPLETE_FIXED_PROJECTION_TWO_ROW_CATALOG',free_slots=free,pairs_tested=len(left)*len(right),steps=steps,surviving_pairs=surviving)


def run():
    start=monotonic();b=Bindings();orbit_path=H/'parent00-projection-orbit-cover-cycle113.json';orbits=b.read(orbit_path)
    assert orbits['status']=='EXPLICIT_PARENT00_CUBIC_PROJECTION_ORBIT_COVERS'
    domain_path=H/'parent00-fixed-projection-independent-manifest-cycle113.json';authority=b.read(domain_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_PARENT00_FIXED_PROJECTION_PROPAGATION' and authority['frontier']==orbits['frontier']
    records={(r['index'],r['projection_index']):r for r in authority['records']}
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];cubes=CubeIndex.build(rows)
    directory=H/'parent00-joint-pair-catalogs-cycle113';output=directory.with_suffix('.json');assert not directory.exists() and not output.exists();directory.mkdir();results=[]
    for case in orbits['records']:
        for representative in case['representatives']:
            previous=records[case['index'],representative];assert not previous['excluded'];source=read_certificate(b,previous['proof']);domains=source['proof']['domains']
            proof=joint_pairs(domains,orbits['geometry'],cubes,3,source['spectrum'])
            detail=dict(geometry=orbits['geometry'],parent=orbits['parent'],index=case['index'],projection_index=representative,previous=previous['proof'],
                projection=source['projection'],spectrum=source['spectrum'],input_domains=domains,core_mask=3,proof=proof)
            path=directory/f'r{case["index"]:02d}-p{representative:03d}.json.gz';write_certificate(path,detail)
            result=dict(index=case['index'],projection_index=representative,proof=b.bind(path),pairs_tested=proof['pairs_tested'],surviving_pairs=len(proof['surviving_pairs']))
            results.append(result);print(json.dumps({k:v for k,v in result.items() if k!='proof'}),flush=True)
    for name in ('parent00_joint_pair_catalogs.py','test_parent00_joint_pair_catalogs.py','fixed_projection_cube_domains.py'):b.bind(H/name)
    result=dict(status='COMPLETE_PARENT00_FIXED_PROJECTION_TWO_ROW_CATALOGS',global_status='UNRESOLVED',independent_audit='PENDING',orbit_cover=b.bind(orbit_path),domain_authority=b.bind(domain_path),
        geometry=orbits['geometry'],parent=orbits['parent'],records=results,elapsed_seconds=monotonic()-start,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(seconds=result['elapsed_seconds'],surviving_pairs=sum(r['surviving_pairs'] for r in results))),flush=True)


if __name__=='__main__':run()
