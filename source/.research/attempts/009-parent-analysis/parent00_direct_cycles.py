"""Complete direct seven-coordinate cubic-cycle catalogs for three0/0 patterns."""
from collections import Counter
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from generic_parseval_envelope import permitted
from two_positive_four_cube_domains import CubeIndex
from cubic_degree_profiles import degree_options
from parent00_cubic_cycles import cycle_basis,gray_cycles

H=Path(__file__).resolve().parent


def linear_for_profile(degrees,maps,positive_count,negative_count):
    if any(d not in choices for d,choices in zip(degrees,maps)):return None
    linear=[choices[d] for d,choices in zip(degrees,maps)];Q=sum(linear)
    if Q%2 or positive_count!=Q+4+2*negative_count:return None
    return linear


def run():
    start=monotonic();b=Bindings();frontier_path=H/'parent00-cubic-position-frontier-cycle111.json';frontier=b.read(frontier_path)
    assert frontier['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER'
    parent=read_certificate(b,frontier['parent']);g=frontier['geometry'];rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows']
    values=permitted(g,parent['domains'],CubeIndex.build(rows),[3])[3];assert values[0]==[4]
    singletons=[values[1<<i] for i in range(10)];selected=[r for r in frontier['remaining'] if r['negative'] in ([35],[97],[97,386])];assert len(selected)==3
    cases=[]
    for case in selected:
        options=degree_options(10,case['negative'],singletons);maps=[dict(c) for c in options];assert all(len(m)==len(c) for m,c in zip(maps,options))
        active=[i for i,choices in enumerate(options) if any(d or u for d,u in choices) or any(q>>i&1 for q in case['negative'])]
        cases.append(dict(index=case['index'],negative=case['negative'],degree_options=options,maps=maps,vertices=active,candidates=[]))
    vertices=cases[0]['vertices'];assert len(vertices)==7 and all(c['vertices']==vertices for c in cases)
    triangles,basis=cycle_basis(vertices);incidence=[sum(1<<j for j,q in enumerate(triangles) if q>>i&1) for i in range(10)];position={q:i for i,q in enumerate(triangles)}
    for case in cases:case['forbidden']=sum(1<<position[q] for q in case['negative'])
    minimum_faces=4+2*min(len(c['negative']) for c in cases);maximum_faces=len(singletons)+4+2*max(len(c['negative']) for c in cases)
    hist=Counter()
    for code in gray_cycles(basis):
        count=code.bit_count();hist[count]+=1
        if count<minimum_faces or count>maximum_faces:continue
        degrees=[(code&m).bit_count() for m in incidence]
        for case in cases:
            if code&case['forbidden']:continue
            linear=linear_for_profile(degrees,case['maps'],count,len(case['negative']))
            if linear is None:continue
            positive=[q for i,q in enumerate(triangles) if code>>i&1];linear_supports=[1<<i for i,u in enumerate(linear) if u]
            spectrum=sorted([(q,1) for q in positive]+[(q,-1) for q in linear_supports]+[(q,-2) for q in case['negative']]);failure=None
            for x,allowed in enumerate(values):
                value=sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in spectrum)
                if value not in allowed:failure=dict(point=x,value=value,allowed=allowed);break
            case['candidates'].append(dict(code=code,positive=sorted(positive),linear=linear_supports,linear_count=sum(linear),first_failure=failure))
    directory=H/'parent00-direct-cycle-catalogs-cycle112';output=directory.with_suffix('.json');assert not output.exists() and not directory.exists();directory.mkdir();records=[]
    for case in cases:
        detail=dict(geometry=g,parent=frontier['parent'],index=case['index'],negative=case['negative'],vertices=vertices,triangles=triangles,basis=basis,
            cycles_checked=1<<20,weight_histogram=dict(sorted(hist.items())),degree_options=case['degree_options'],candidates=case['candidates'])
        path=directory/f'r{case["index"]:02d}.json.gz';write_certificate(path,detail)
        record=dict(index=case['index'],negative=case['negative'],proof=b.bind(path),candidates=len(case['candidates']),
            candidate_counts=dict(Counter(r['linear_count'] for r in case['candidates'])),survivors=sum(r['first_failure'] is None for r in case['candidates']))
        records.append(record);print(json.dumps({k:v for k,v in record.items() if k!='proof'}),flush=True)
    for name in ('parent00_direct_cycles.py','test_parent00_direct_cycles.py','cubic_degree_profiles.py','parent00-degree-catalog-roadmap-cycle112.md'):b.bind(H/name)
    result=dict(status='COMPLETE_PARENT00_DIRECT_CUBIC_CYCLE_CATALOGS',global_status='UNRESOLVED',independent_audit='PENDING',frontier=b.bind(frontier_path),geometry=g,parent=frontier['parent'],core_mask=3,
        records=records,elapsed_seconds=monotonic()-start,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':run()
