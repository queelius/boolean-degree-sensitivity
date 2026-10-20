"""Independent opposite-anchor reconstruction of the hard ten-vertex cycle family."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate

H=Path(__file__).resolve().parent


def literal_cycle_links(vertices):
    edges=list(combinations(vertices,2))
    for size in (4,5):
        for link in combinations(edges,size):
            if all(sum(v in e for e in link) in (0,2) for v in vertices):yield link


def run():
    start=monotonic();b=Bindings();source_path=H/'hard-low-one-positive-cycles-cycle148.json';source=b.read(source_path)
    assert source['status']=='COMPLETE_HARD_LOW_ONE_POSITIVE_CYCLE_CATALOG'
    assert source['low']==2 and source['critical']==[3,4,5] and source['anchor']==0
    authority=b.read(source['residual_authority']['path'],source['residual_authority']['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_EIGHT_VERTEX_RESIDUAL_CATALOG'
    assert authority['maximum']==[7,7,7,6,5,5,5,5] and authority['maximum_faces']==14
    data=Path(authority['data']['path']);assert b.bind(data)==authority['data']
    codes=np.load(data,allow_pickle=False);assert codes.dtype==np.uint64 and len(codes)==authority['cycles']
    raw_bits=np.unpackbits(codes.view(np.uint8).reshape(-1,8),axis=1,bitorder='little')[:,:56]
    low=source['low'];critical=source['critical'];high=[v for v in range(10) if v!=low]
    anchor=max(v for v in high if v not in critical);other=[v for v in high if v!=anchor]
    faces=list(combinations(other,3));positions={t:j for j,t in enumerate(faces)}
    canonical=list(combinations(range(8),3));local_positions={t:j for j,t in enumerate(canonical)}
    incidence=[[j for j,t in enumerate(faces) if v in t] for v in other]
    target=np.array([7 if v in critical else 5 for v in other],dtype=np.int16)
    tables={};found=set();links=0;cases=Counter()
    for link in literal_cycle_links(other):
        links+=1;fan=max(v for e in link for v in e if v not in critical)
        if fan not in tables:
            image=list(reversed(critical))+[fan]+list(reversed([v for v in other if v not in critical and v!=fan]))
            inverse={v:i for i,v in enumerate(image)}
            columns=[local_positions[tuple(sorted(inverse[v] for v in t))] for t in faces]
            table=raw_bits[:,columns]
            weights=table.sum(axis=1,dtype=np.int16)
            degrees=np.stack([table[:,cols].sum(axis=1,dtype=np.int16) for cols in incidence],axis=1)
            tables[fan]=table,weights,degrees
        table,base_weights,base_degrees=tables[fan]
        filling=[positions[tuple(sorted((fan,)+e))] for e in link if fan not in e]
        flips=1-2*table[:,filling].astype(np.int16)
        weights=base_weights+len(link)+flips.sum(axis=1,dtype=np.int16)
        degrees=base_degrees+np.array([sum(v in e for e in link) for v in other],dtype=np.int16)
        for i,v in enumerate(other):
            cols=[j for j,k in enumerate(filling) if v in faces[k]]
            if cols:degrees[:,i]+=flips[:,cols].sum(axis=1,dtype=np.int16)
        delta=target-degrees;anchor_delta=5-len(link)
        for weight,increment in ((14,3),(16,1)):
            if anchor_delta not in (0,increment):continue
            valid=(weights==weight)&np.all((delta==0)|(delta==increment),axis=1)
            valid &= np.count_nonzero(delta,axis=1)+(anchor_delta>0)==3
            for j in np.flatnonzero(valid):
                selected=[v for v,d in zip(other,delta[j]) if d]
                if anchor_delta:selected.append(anchor)
                triangle=sum(1<<v for v in selected);assert len(selected)==3
                present={sum(1<<v for v in t) for k,t in enumerate(faces) if bool(table[j,k])^(k in filling)}
                present.update((1<<anchor)|sum(1<<v for v in e) for e in link)
                if (triangle in present)!=(weight==16):continue
                if triangle in present:present.remove(triangle)
                else:present.add(triangle)
                present.update((1<<low)|sum(1<<v for v in e) for e in combinations(selected,2))
                full=tuple(sorted(present));assert len(full)==18 and full not in found
                assert [sum(v in [i for i in range(10) if q>>i&1] for q in full) for v in range(10)]==[3 if v==low else 7 if v in critical else 5 for v in range(10)]
                for edge in combinations(range(10),2):
                    assert sum(all(q>>v&1 for v in edge) for q in full)%2==0
                found.add(full);cases['present_triangle' if weight==16 else 'absent_triangle']+=1
    detail=read_certificate(b,source['proof'])
    assert detail['low']==low and detail['critical']==critical and detail['anchor']==source['anchor']
    assert detail['positive_cycles']==[list(c) for c in sorted(found)]
    assert links==source['links']==882 and len(found)==source['cycles'] and dict(cases)==source['contraction_cases']
    for name in ('verify_hard_low_one_cubic_cycles.py','test_literal_cycle_links.py','nine_vertex_reconstruction_plan_cycle148.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_HARD_LOW_ONE_POSITIVE_CYCLE_CATALOG',global_status='UNRESOLVED',
        source=b.bind(source_path),residual_authority=source['residual_authority'],proof=source['proof'],low=low,critical=critical,
        independent_anchor=anchor,links=links,cycles=len(found),contraction_cases=dict(cases),seconds=monotonic()-start,
        forbidden_negative_faces_filtered=False,accepted_parent_exclusions=0,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output=H/'hard-low-one-positive-cycles-independent-manifest-cycle148.json';assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='files'}),flush=True)


if __name__=='__main__':run()
