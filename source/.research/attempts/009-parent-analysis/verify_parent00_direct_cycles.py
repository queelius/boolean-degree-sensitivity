"""Independent full-space replay of the three direct cubic-cycle catalogs."""
from argparse import ArgumentParser
from itertools import combinations
from collections import Counter
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from cubic_partial_scalar import PartialScalarValues
from verify_parent00_cubic_cycles import independent_cycles,check_value_witness

H=Path(__file__).resolve().parent


def run(output):
    b=Bindings();source_path=H/'parent00-direct-cycle-catalogs-cycle112.json';source=b.read(source_path)
    assert source['status']=='COMPLETE_PARENT00_DIRECT_CUBIC_CYCLE_CATALOGS' and source['core_mask']==3
    frontier=b.read(source['frontier']['path'],source['frontier']['sha256']);assert frontier['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER'
    assert source['geometry']==frontier['geometry'] and source['parent']==frontier['parent'];parent=read_certificate(b,source['parent'])
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];values=PartialScalarValues(rows,source['geometry']).allowed(parent['domains'],3)
    assert values[0]==[4];singletons=[values[1<<i] for i in range(10)];expected_cases=[r for r in frontier['remaining'] if r['negative'] in ([35],[97],[97,386])]
    assert [(r['index'],r['negative']) for r in source['records']]==[(r['index'],r['negative']) for r in expected_cases]
    tables=[];common=None
    for record in source['records']:
        detail=read_certificate(b,record['proof']);negative=record['negative'];assert detail['index']==record['index'] and detail['negative']==negative and detail['parent']==source['parent'] and detail['geometry']==source['geometry']
        incidences=[sum(bool(q>>i&1) for q in negative) for i in range(10)];options=[]
        for i in range(10):
            options.append([[d,u] for d in range(37) if d==0 or d>=3 for u in (0,1) if 4-2*(d-2*incidences[i]-u) in singletons[i]])
        assert detail['degree_options']==options
        vertices=[i for i in range(10) if incidences[i] or any(d or u for d,u in options[i])];assert len(vertices)==7 and detail['vertices']==vertices
        if common is None:common=vertices
        assert vertices==common
        triangles=[sum(1<<v for v in t) for t in combinations(vertices,3)];assert detail['triangles']==triangles
        index={q:i for i,q in enumerate(triangles)};basis=[]
        for t in combinations(vertices[1:],3):basis.append(sum(1<<index[sum(1<<v for v in f)] for f in combinations((vertices[0],)+t,3)))
        assert detail['basis']==basis and detail['cycles_checked']==1<<20
        actual={r['code']:r for r in detail['candidates']};assert len(actual)==len(detail['candidates'])==record['candidates']
        tables.append(dict(record=record,detail=detail,negative=negative,incidences=incidences,actual=actual,expected={},forbidden=sum(1<<index[q] for q in negative)))
    codes=independent_cycles(common,triangles);assert len(codes)==1<<20;hist=Counter(code.bit_count() for code in codes)
    masks=[sum(1<<j for j,q in enumerate(triangles) if q>>i&1) for i in range(10)]
    for code in codes:
        degrees=[(code&m).bit_count() for m in masks];P=code.bit_count()
        for table in tables:
            if code&table['forbidden']:continue
            linear=[]
            for i,d in enumerate(degrees):
                choices=[u for u in (0,1) if 4-2*(d-2*table['incidences'][i]-u) in singletons[i]]
                if not choices:break
                assert len(choices)==1;linear.append(choices[0])
            if len(linear)!=10 or P!=sum(linear)+4+2*len(table['negative']):continue
            assert sum(linear)%2==0 and all(d==0 or d>=3 for d in degrees)
            table['expected'][code]=[1<<i for i,u in enumerate(linear) if u]
    results=[]
    for table in tables:
        detail=table['detail'];record=table['record'];assert {int(k):v for k,v in detail['weight_histogram'].items()}==dict(hist)
        assert set(table['actual'])==set(table['expected']);counts=Counter();survivors=[]
        for code,linear in table['expected'].items():
            candidate=table['actual'][code];positive=sorted(q for j,q in enumerate(triangles) if code>>j&1)
            assert candidate['positive']==positive and candidate['linear']==linear and candidate['linear_count']==len(linear)
            spectrum=[(q,1) for q in positive]+[(q,-1) for q in linear]+[(q,-2) for q in table['negative']]
            if check_value_witness(spectrum,values,candidate['first_failure']):
                evaluations=[sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in spectrum) for x in range(1024)]
                norm=len(positive)+len(linear)+4*len(table['negative']);assert sum(v*v for v in evaluations)==1024*norm
                survivors.append(dict(positive=positive,linear=linear,negative=table['negative'],coefficient_norm=norm,inputs_checked=1024))
            counts[len(linear)]+=1
        assert len(survivors)==record['survivors'] and dict(counts)=={int(k):v for k,v in record['candidate_counts'].items()}
        result=dict(index=record['index'],negative=record['negative'],proof=record['proof'],candidates=len(table['expected']),candidate_counts=dict(counts),survivors=survivors,negative_position_excluded=not survivors)
        results.append(result);print(json.dumps({k:v for k,v in result.items() if k not in ('proof','survivors')}|dict(survivors=len(survivors))),flush=True)
    for name in ('verify_parent00_direct_cycles.py','test_parent00_direct_cycles.py','verify_parent00_cubic_cycles.py','test_verify_parent00_cubic_cycles.py','parent00-degree-catalog-roadmap-cycle112.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_COMPLETE_PARENT00_DIRECT_CUBIC_CATALOGS',global_status='UNRESOLVED',source=b.bind(source_path),
        frontier=source['frontier'],geometry=source['geometry'],parent=source['parent'],core_mask=3,cycles_checked_per_case=1<<20,records=results,
        whole_parent_excluded=False,boolean_function_on14_constructed=False,solver_imported=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
