"""Complete degree-(3,5^6,7^3) triangle cycles via an audited eight-vertex catalog."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import write_certificate
from fan_cycle_extension import ResidualCatalog,permute_face_codes
from small_link_high_cycles import small_even_links

H=Path(__file__).resolve().parent


def run():
    start=monotonic();b=Bindings();authority_path=H/'eight-vertex-residual-independent-manifest-cycle148.json'
    authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_EIGHT_VERTEX_RESIDUAL_CATALOG'
    assert authority['maximum']==[7,7,7,6,5,5,5,5] and authority['maximum_faces']==14
    data=Path(authority['data']['path']);assert b.bind(data)==authority['data']
    base=np.load(data,allow_pickle=False);assert len(base)==authority['cycles'] and base.dtype==np.uint64
    low=2;critical=[3,4,5];high=[v for v in range(10) if v!=low]
    ordinary=[v for v in high if v not in critical];anchor=ordinary[0];other=[v for v in high if v!=anchor]
    target=np.array([7 if v in critical else 5 for v in other],dtype=np.int16)
    contracted=np.array([4 if v in critical else 5 for v in other],dtype=np.int16)
    catalogs={};found=set();links=[];cases=Counter();critical_face=sum(1<<v for v in critical)
    for link in small_even_links(other,5):
        if len(link) not in (4,5):continue
        neighbors={v for e in link for v in e};fan=min(neighbors-set(critical))
        if fan not in catalogs:
            image=critical+[fan]+[v for v in other if v not in critical and v!=fan]
            catalogs[fan]=ResidualCatalog(permute_face_codes(base,image,other),other)
        catalog=catalogs[fan];remaining,weights,degrees=catalog.extend(link,fan)
        sixteen=(weights==16)&np.all((degrees==target)|(degrees==target-1),axis=1)
        fourteen=(weights==14)&np.all(degrees==contracted,axis=1) if len(link)==5 else np.zeros(len(base),dtype=bool)
        selected=np.flatnonzero(sixteen|fourteen);accepted=0
        for j in selected:
            code=int(remaining[j]);faces={sum(1<<v for v in t) for k,t in enumerate(catalog.faces) if code>>k&1}
            faces.update((1<<anchor)|(1<<a)|(1<<c) for a,c in link)
            if fourteen[j]:
                triangle=critical_face
                if triangle in faces:continue
                assert len(faces)==14;cases['absent_triangle']+=1
            else:
                deficient=[v for v,d,t in zip(other,degrees[j],target) if d==t-1]
                if len(link)==4:deficient.append(anchor)
                assert len(deficient)==3;triangle=sum(1<<v for v in deficient)
                if triangle not in faces:continue
                assert len(faces)==16;cases['present_triangle']+=1
            vertices=[v for v in high if triangle>>v&1]
            faces.symmetric_difference_update({triangle}|{(1<<low)|(1<<a)|(1<<c) for a,c in combinations(vertices,2)})
            full=tuple(sorted(faces));assert len(full)==18 and full not in found
            assert [sum(bool(q>>v&1) for q in full) for v in range(10)]==[3 if v==low else 7 if v in critical else 5 for v in range(10)]
            assert all(sum(q&e==e for q in full)%2==0 for e in [sum(1<<v for v in e) for e in combinations(range(10),2)])
            found.add(full);accepted+=1
        links.append(dict(edges=[list(e) for e in link],fan=fan,degree_filtered=len(selected),cycles=accepted))
    assert len(links)==882
    proof=H/'hard-low-one-positive-cycles-cycle148.json.gz'
    write_certificate(proof,dict(low=low,critical=critical,anchor=anchor,positive_cycles=[list(c) for c in sorted(found)],links=links))
    for name in ('hard_low_one_cubic_cycles.py','fan_cycle_extension.py','test_fan_cycle_extension.py','small_link_high_cycles.py',
                 'nine_vertex_reconstruction_plan_cycle148.md'):b.bind(H/name)
    result=dict(status='COMPLETE_HARD_LOW_ONE_POSITIVE_CYCLE_CATALOG',global_status='UNRESOLVED',independent_audit='PENDING',
        residual_authority=b.bind(authority_path),proof=b.bind(proof),low=low,critical=critical,anchor=anchor,
        links=len(links),cycles=len(found),contraction_cases=dict(cases),seconds=monotonic()-start,
        forbidden_negative_faces_filtered=False,accepted_parent_exclusions=0,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output=H/'hard-low-one-positive-cycles-cycle148.json';assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='sources'}),flush=True)


if __name__=='__main__':run()
