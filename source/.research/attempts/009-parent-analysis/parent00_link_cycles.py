"""Complete cubic catalogs by removing one forced degree-three vertex."""
from collections import Counter
from itertools import combinations
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from generic_parseval_envelope import permitted
from two_positive_four_cube_domains import CubeIndex
from cubic_degree_profiles import degree_options,degree_profiles
from parent00_cubic_cycles import cycle_basis,gray_cycles
from parent00_direct_cycles import linear_for_profile

H=Path(__file__).resolve().parent


def restore_link(base,face,center):
    """Toggle the tetrahedron boundary; retain both possible base-face states."""
    assert face.bit_count()==3 and not face>>center&1 and not any(q>>center&1 for q in base)
    vertices=[i for i in range(face.bit_length()) if face>>i&1]
    tetra={face}|{(1<<center)|sum(1<<v for v in edge) for edge in combinations(vertices,2)}
    return set(base)^tetra


def run():
    start=monotonic();b=Bindings();frontier_path=H/'parent00-cubic-position-frontier-cycle111.json';frontier=b.read(frontier_path)
    assert frontier['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER'
    parent=read_certificate(b,frontier['parent']);g=frontier['geometry']
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows']
    values=permitted(g,parent['domains'],CubeIndex.build(rows),[3])[3];assert values[0]==[4]
    singletons=[values[1<<i] for i in range(10)];selected=[r for r in frontier['remaining'] if r['negative'] in ([37],[37,194])];assert len(selected)==2
    cases=[]
    for record in selected:
        options=degree_options(10,record['negative'],singletons);profiles=degree_profiles(10,record['negative'],singletons)
        active=[i for i,c in enumerate(options) if any(d or u for d,u in c) or any(q>>i&1 for q in record['negative'])]
        forced=[i for i in active if {d for d,u in options[i]}=={3}]
        cases.append(dict(index=record['index'],negative=record['negative'],degree_options=options,maps=[dict(c) for c in options],
            active=active,forced=forced,face_counts=sorted({p['positive_count'] for p in profiles}),candidates=[]))
    centers=set(cases[0]['forced']).intersection(*(c['forced'] for c in cases[1:]));assert centers;center=min(centers)
    active=cases[0]['active'];assert len(active)==8 and all(c['active']==active for c in cases)
    vertices=[i for i in active if i!=center];triangles,basis=cycle_basis(vertices)
    incidence=[sum(1<<j for j,q in enumerate(triangles) if q>>i&1) for i in range(10)]
    for c in cases:
        c['base_counts']={p-shift for p in c['face_counts'] for shift in (2,4)}
        c['base_degrees']=[{d-shift for d,u in choices for shift in (0,1,3) if d-shift>=0} for choices in c['degree_options']]
        c['seen']=set()
    hist=Counter()
    for code in gray_cycles(basis):
        weight=code.bit_count();hist[weight]+=1
        if not any(weight in c['base_counts'] for c in cases):continue
        degrees=[(code&m).bit_count() for m in incidence]
        for c in cases:
            if weight not in c['base_counts'] or any(degrees[i] not in c['base_degrees'][i] for i in vertices):continue
            base=None
            for j,face in enumerate(triangles):
                present=bool(code>>j&1);shift=1 if present else 3;count=weight+(2 if present else 4)
                if count not in c['face_counts']:continue
                final_degrees=[3 if i==center else d+shift*int(bool(face>>i&1)) for i,d in enumerate(degrees)]
                linear=linear_for_profile(final_degrees,c['maps'],count,len(c['negative']))
                if linear is None:continue
                if base is None:base={q for k,q in enumerate(triangles) if code>>k&1}
                positive=sorted(restore_link(base,face,center))
                if set(positive)&set(c['negative']):continue
                assert len(positive)==count and tuple(positive) not in c['seen'];c['seen'].add(tuple(positive))
                linear_supports=[1<<i for i,u in enumerate(linear) if u]
                spectrum=[(q,1) for q in positive]+[(q,-1) for q in linear_supports]+[(q,-2) for q in c['negative']];failure=None
                for x,allowed in enumerate(values):
                    value=sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in spectrum)
                    if value not in allowed:failure=dict(point=x,value=value,allowed=allowed);break
                c['candidates'].append(dict(base_code=code,link_face=face,face_in_base=present,positive=positive,linear=linear_supports,
                    linear_count=sum(linear),first_failure=failure))
    directory=H/'parent00-link-cycle-catalogs-cycle112';output=directory.with_suffix('.json');assert not output.exists() and not directory.exists();directory.mkdir();records=[]
    for c in cases:
        detail=dict(geometry=g,parent=frontier['parent'],index=c['index'],negative=c['negative'],active=active,center=center,vertices=vertices,
            triangles=triangles,basis=basis,cycles_checked=1<<len(basis),weight_histogram=dict(sorted(hist.items())),degree_options=c['degree_options'],candidates=c['candidates'])
        path=directory/f'r{c["index"]:02d}.json.gz';write_certificate(path,detail)
        record=dict(index=c['index'],negative=c['negative'],proof=b.bind(path),candidates=len(c['candidates']),
            candidate_counts=dict(Counter(r['linear_count'] for r in c['candidates'])),tetrahedron_candidates=sum(not r['face_in_base'] for r in c['candidates']),
            survivors=sum(r['first_failure'] is None for r in c['candidates']))
        records.append(record);print(json.dumps({k:v for k,v in record.items() if k!='proof'}),flush=True)
    for name in ('parent00_link_cycles.py','test_parent00_link_cycles.py','parent00_cubic_cycles.py','parent00_direct_cycles.py','cubic_degree_profiles.py'):b.bind(H/name)
    result=dict(status='COMPLETE_PARENT00_ONE_LINK_CUBIC_CYCLE_CATALOGS',global_status='UNRESOLVED',independent_audit='PENDING',frontier=b.bind(frontier_path),
        geometry=g,parent=frontier['parent'],core_mask=3,records=records,elapsed_seconds=monotonic()-start,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':run()
