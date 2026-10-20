"""Independent full-face-bitmask enumeration of the multiple-low cubic catalogs."""
from argparse import ArgumentParser
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from cubic_partial_scalar import PartialScalarValues
from verify_parent00_cubic_cycles import independent_cycles,check_value_witness

H=Path(__file__).resolve().parent


def independent_low_families(high,lows,allowed,max_faces,triangles,codes):
    index={q:i for i,q in enumerate(triangles)};masks={v:sum(1<<j for j,q in enumerate(triangles) if q>>v&1) for v in high}
    critical=[v for v in high if max(allowed[v])>=6]
    assert len(lows) in (2,3) and len(critical)==4-len(lows) and all(set(s)<=set((0,4,5,6,7)) for s in allowed.values())
    high_triples=list(combinations(high,3));tetra=[]
    for c in reversed(lows):tetra.append([sum(1<<index[sum(1<<v for v in face)] for face in combinations((c,)+t,3)) for t in high_triples])
    exceptional=sum(1<<index[sum(1<<v for v in face)] for face in combinations(tuple(lows)+tuple(critical),3))

    def extend(stage,code):
        if code.bit_count()+2*(len(lows)-stage)>max_faces:return
        if any((code&masks[v]).bit_count()>max(allowed[v]) for v in high):return
        if stage==len(lows):
            if all((code&masks[v]).bit_count() in allowed[v] for v in high):yield code
            return
        for toggle in tetra[stage]:yield from extend(stage+1,code^toggle)

    for code in codes:
        weight=code.bit_count()
        if weight+2*len(lows)<=max_faces:yield from extend(0,code)
        if weight+4<=max_faces:
            full=code^exceptional
            if all((full&masks[v]).bit_count() in allowed[v] for v in high):yield full


def run(output):
    b=Bindings();source_path=H/'parent00-multiple-low-cycle-catalogs-cycle119.json';source=b.read(source_path)
    assert source['status']=='COMPLETE_PARENT00_MULTIPLE_LOW_CUBIC_CYCLE_CATALOGS' and source['core_mask']==3
    frontier=b.read(source['frontier']['path'],source['frontier']['sha256']);assert frontier['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER'
    assert source['parent']==frontier['parent'] and source['geometry']==frontier['geometry'];parent=read_certificate(b,source['parent'])
    expected_cases=[r for r in frontier['remaining'] if len(r['negative'])==2];assert [(r['index'],r['negative']) for r in source['records']]==[(r['index'],r['negative']) for r in expected_cases]
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];values=PartialScalarValues(rows,source['geometry']).allowed(parent['domains'],3)
    assert values[0]==[4];singletons=[values[1<<i] for i in range(10)];cases=[];groups={}
    for record in source['records']:
        detail=read_certificate(b,record['proof']);negative=record['negative'];assert detail['index']==record['index'] and detail['negative']==negative and detail['parent']==source['parent'] and detail['geometry']==source['geometry']
        incidences=[sum(bool(q>>i&1) for q in negative) for i in range(10)]
        options=[[[d,u] for d in range(37) if d==0 or d>=3 for u in (0,1) if 4-2*(d-2*incidences[i]-u) in singletons[i]] for i in range(10)]
        assert detail['degree_options']==options
        active=[i for i in range(10) if incidences[i] or any(d or u for d,u in options[i])];lows=[i for i in active if {d for d,u in options[i]}=={3}];high=[i for i in active if i not in lows]
        assert len(high)==7 and detail['high']==high and detail['lows']==lows and len(lows) in (2,3) and detail['cycles_checked']==1<<20
        face_counts=[]
        for profile in product(*options):
            Q=sum(u for d,u in profile);P=Q+8
            if Q%2==0 and sum(d for d,u in profile)==3*P:face_counts.append(P)
        maximum=max(face_counts);assert detail['maximum_faces']==maximum
        allowed={i:{d for d,u in options[i]} for i in high};key=(tuple(high),tuple(lows),tuple(tuple(sorted(allowed[i])) for i in high),maximum)
        actual={tuple(r['positive']):r for r in detail['candidates']};assert len(actual)==len(detail['candidates'])==record['candidates']
        case=dict(record=record,detail=detail,negative=negative,incidences=incidences,actual=actual,expected={});cases.append(case)
        groups.setdefault(key,[]).append(case)
    triangles=[sum(1<<v for v in t) for t in combinations(range(10),3)];code_cache={}
    for (high,lows,options,maximum),group in groups.items():
        if high not in code_cache:code_cache[high]=independent_cycles(high,triangles)
        codes=code_cache[high];assert len(codes)==1<<20;allowed={v:set(s) for v,s in zip(high,options)};families=set()
        for code in independent_low_families(high,lows,allowed,maximum,triangles,codes):
            positive=tuple(sorted(q for j,q in enumerate(triangles) if code>>j&1));assert positive not in families;families.add(positive)
            degrees=[sum(bool(q>>i&1) for q in positive) for i in range(10)];assert all(degrees[i]==3 for i in lows)
            for case in group:
                if set(positive)&set(case['negative']):continue
                linear=[]
                for i,d in enumerate(degrees):
                    choices=[u for u in (0,1) if 4-2*(d-2*case['incidences'][i]-u) in singletons[i]]
                    if not choices:break
                    assert len(choices)==1;linear.append(choices[0])
                if len(linear)!=10 or len(positive)!=sum(linear)+8:continue
                assert sum(linear)%2==0;case['expected'][positive]=[1<<i for i,u in enumerate(linear) if u]
        for case in group:assert len(families)==case['detail']['degree_bounded_families']==case['record']['degree_bounded_families']
        print(json.dumps(dict(lows=list(lows),bounded_families=len(families),cases=[c['record']['index'] for c in group])),flush=True)
    results=[]
    for case in cases:
        record=case['record'];assert set(case['actual'])==set(case['expected']);counts=Counter();survivors=[]
        for positive,linear in case['expected'].items():
            candidate=case['actual'][positive];assert candidate['linear']==linear and candidate['linear_count']==len(linear)
            spectrum=[(q,1) for q in positive]+[(q,-1) for q in linear]+[(q,-2) for q in case['negative']]
            if check_value_witness(spectrum,values,candidate['first_failure']):
                evaluations=[sum(k*(1-2*((q&x).bit_count()%2)) for q,k in spectrum) for x in range(1024)]
                norm=len(positive)+len(linear)+8;assert sum(v*v for v in evaluations)==1024*norm
                survivors.append(dict(positive=list(positive),linear=linear,negative=case['negative'],coefficient_norm=norm,inputs_checked=1024))
            counts[len(linear)]+=1
        assert len(survivors)==record['survivors'] and dict(counts)=={int(k):v for k,v in record['candidate_counts'].items()}
        result=dict(index=record['index'],negative=case['negative'],proof=record['proof'],candidates=len(case['expected']),candidate_counts=dict(counts),survivors=survivors,negative_position_excluded=not survivors)
        results.append(result);print(json.dumps({k:v for k,v in result.items() if k not in ('proof','survivors')}|dict(survivors=len(survivors))),flush=True)
    for name in ('verify_multiple_low_cycles.py','test_verify_multiple_low_cycles.py','test_multiple_low_cycles.py','multiple-low-degree-cycle-proof-cycle119.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_COMPLETE_PARENT00_MULTIPLE_LOW_CUBIC_CATALOGS',global_status='UNRESOLVED',source=b.bind(source_path),frontier=source['frontier'],geometry=source['geometry'],parent=source['parent'],core_mask=3,
        cycles_checked_per_profile=1<<20,records=results,whole_parent_excluded=False,boolean_function_on14_constructed=False,solver_imported=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
