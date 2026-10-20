"""Independent exhaustive link restoration in the full ambient face coordinates."""
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
    b=Bindings();source_path=H/'parent00-link-cycle-catalogs-cycle112.json';source=b.read(source_path)
    assert source['status']=='COMPLETE_PARENT00_ONE_LINK_CUBIC_CYCLE_CATALOGS' and source['core_mask']==3
    frontier=b.read(source['frontier']['path'],source['frontier']['sha256']);assert frontier['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER'
    assert source['geometry']==frontier['geometry'] and source['parent']==frontier['parent'];parent=read_certificate(b,source['parent'])
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows']
    values=PartialScalarValues(rows,source['geometry']).allowed(parent['domains'],3);assert values[0]==[4]
    singletons=[values[1<<i] for i in range(10)];expected_cases=[r for r in frontier['remaining'] if r['negative'] in ([37],[37,194])]
    assert [(r['index'],r['negative']) for r in source['records']]==[(r['index'],r['negative']) for r in expected_cases]
    tables=[];common=None
    for record in source['records']:
        detail=read_certificate(b,record['proof']);negative=record['negative']
        assert detail['index']==record['index'] and detail['negative']==negative and detail['parent']==source['parent'] and detail['geometry']==source['geometry']
        incidences=[sum(bool(q>>i&1) for q in negative) for i in range(10)]
        options=[[[d,u] for d in range(37) if d==0 or d>=3 for u in (0,1) if 4-2*(d-2*incidences[i]-u) in singletons[i]] for i in range(10)]
        assert detail['degree_options']==options
        active=[i for i in range(10) if incidences[i] or any(d or u for d,u in options[i])]
        center=detail['center'];assert len(active)==8 and active==detail['active'] and {d for d,u in options[center]}=={3}
        vertices=[i for i in active if i!=center];assert detail['vertices']==vertices
        if common is None:common=(active,center,vertices)
        assert common==(active,center,vertices)
        actual={tuple(r['positive']):r for r in detail['candidates']};assert len(actual)==len(detail['candidates'])==record['candidates']
        tables.append(dict(record=record,detail=detail,negative=negative,incidences=incidences,options=options,actual=actual,expected={}))
    active,center,vertices=common
    triangles=[sum(1<<v for v in t) for t in combinations(active,3)];index={q:i for i,q in enumerate(triangles)}
    base_triangles=[q for q in triangles if not q>>center&1];base_index={q:i for i,q in enumerate(base_triangles)}
    basis=[]
    for t in combinations(vertices[1:],3):basis.append(sum(1<<base_index[sum(1<<v for v in f)] for f in combinations((vertices[0],)+t,3)))
    for t in tables:assert t['detail']['triangles']==base_triangles and t['detail']['basis']==basis and t['detail']['cycles_checked']==1<<20
    masks=[sum(1<<j for j,q in enumerate(triangles) if q>>i&1) for i in range(10)]
    tetrahedra=[]
    for face in base_triangles:
        vs=[v for v in vertices if face>>v&1];tetra=(1<<index[face])
        for edge in combinations(vs,2):tetra^=1<<index[(1<<center)|sum(1<<v for v in edge)]
        tetrahedra.append((face,tetra))
    codes=independent_cycles(vertices,triangles);assert len(codes)==1<<20;hist=Counter(code.bit_count() for code in codes)
    for code in codes:
        weight=code.bit_count();base_degrees=[(code&m).bit_count() for m in masks]
        for table in tables:
            # Restoration only increases degrees of vertices other than the center.
            if any(base_degrees[i]>max(d for d,u in table['options'][i]) for i in vertices):continue
            if weight+2>10+4+2*len(table['negative']):continue
            for face,tetra in tetrahedra:
                final=code^tetra;P=final.bit_count()
                if any(final>>index[q]&1 for q in table['negative']):continue
                linear=[]
                for i,m in enumerate(masks):
                    d=(final&m).bit_count();choices=[u for u in (0,1) if 4-2*(d-2*table['incidences'][i]-u) in singletons[i]]
                    if not choices:break
                    assert len(choices)==1;linear.append(choices[0])
                if len(linear)!=10 or P!=sum(linear)+4+2*len(table['negative']):continue
                assert sum(linear)%2==0
                positive=tuple(sorted(q for j,q in enumerate(triangles) if final>>j&1));assert positive not in table['expected']
                table['expected'][positive]=dict(base_code=sum(1<<base_index[q] for j,q in enumerate(triangles) if code>>j&1),link_face=face,
                    face_in_base=bool(code>>index[face]&1),linear=[1<<i for i,u in enumerate(linear) if u],linear_count=sum(linear))
    results=[]
    for table in tables:
        detail=table['detail'];record=table['record'];assert {int(k):v for k,v in detail['weight_histogram'].items()}==dict(hist)
        assert set(table['actual'])==set(table['expected']);counts=Counter();survivors=[];tetra_count=0
        for positive,parameters in table['expected'].items():
            candidate=table['actual'][positive];assert all(candidate[k]==v for k,v in parameters.items())
            spectrum=[(q,1) for q in positive]+[(q,-1) for q in parameters['linear']]+[(q,-2) for q in table['negative']]
            if check_value_witness(spectrum,values,candidate['first_failure']):
                evaluations=[sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in spectrum) for x in range(1024)]
                norm=len(positive)+len(parameters['linear'])+4*len(table['negative']);assert sum(v*v for v in evaluations)==1024*norm
                survivors.append(dict(positive=list(positive),linear=parameters['linear'],negative=table['negative'],coefficient_norm=norm,inputs_checked=1024))
            counts[parameters['linear_count']]+=1;tetra_count+=not parameters['face_in_base']
        assert len(survivors)==record['survivors'] and dict(counts)=={int(k):v for k,v in record['candidate_counts'].items()} and tetra_count==record['tetrahedron_candidates']
        result=dict(index=record['index'],negative=record['negative'],proof=record['proof'],candidates=len(table['expected']),candidate_counts=dict(counts),
            tetrahedron_candidates=tetra_count,survivors=survivors,negative_position_excluded=not survivors)
        results.append(result);print(json.dumps({k:v for k,v in result.items() if k not in ('proof','survivors')}|dict(survivors=len(survivors))),flush=True)
    for name in ('verify_parent00_link_cycles.py','test_parent00_link_cycles.py','verify_parent00_cubic_cycles.py','test_verify_parent00_cubic_cycles.py','signed-divisibility-criterion-cycle107.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_COMPLETE_PARENT00_ONE_LINK_CUBIC_CATALOGS',global_status='UNRESOLVED',source=b.bind(source_path),frontier=source['frontier'],
        geometry=source['geometry'],parent=source['parent'],core_mask=3,cycles_checked_per_case=1<<20,records=results,
        whole_parent_excluded=False,boolean_function_on14_constructed=False,solver_imported=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
