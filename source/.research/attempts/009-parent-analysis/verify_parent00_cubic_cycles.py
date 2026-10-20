"""Independent complete binary-cycle replay and scalar candidate rejection."""
from argparse import ArgumentParser
from itertools import combinations
from collections import Counter
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from cubic_partial_scalar import PartialScalarValues

H=Path(__file__).resolve().parent


def independent_cycles(vertices,triangles):
    index={q:i for i,q in enumerate(triangles)};codes=[0];anchor=vertices[0]
    for t in combinations(vertices[1:],3):
        q=sum(1<<i for i in t);generator=1<<index[q]
        for edge in combinations(t,2):generator^=1<<index[(1<<anchor)|sum(1<<i for i in edge)]
        codes.extend([code^generator for code in codes])
    return codes


def check_value_witness(spectrum,values,failure):
    def value(x):return sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in spectrum)
    if failure is None:
        assert all(value(x) in allowed for x,allowed in enumerate(values));return True
    x=failure['point'];assert type(x) is int and 0<=x<len(values)
    assert failure['allowed']==values[x] and failure['value']==value(x) and failure['value'] not in values[x]
    return False


def run(output):
    b=Bindings();source_path=H/'parent00-negative7-cycle-enumeration-cycle111.json';source=b.read(source_path)
    assert source['status']=='COMPLETE_PARENT00_NEGATIVE7_TRIANGLE_CYCLE_ENUMERATION' and source['negative']==[7]
    authority=b.read(source['authority']['path'],source['authority']['sha256']);case=next(r for r in authority['records'] if (r['first_row'],r['second_row'])==(0,0))
    assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_TWO_FIXED_ROW_CUBIC_INTERVAL_COVERS' and case['parent']==source['parent'] and source['geometry']==authority['geometry']
    parent=read_certificate(b,source['parent']);detail=read_certificate(b,source['proof']);assert detail['parent']==source['parent'] and detail['geometry']==source['geometry'] and detail['negative']==[7] and detail['center']==2
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];values=PartialScalarValues(rows,source['geometry']).allowed(parent['domains'],3)
    assert values[0]==[4] and [values[1<<i] for i in range(10)]==[[0,8],[0,8],[4],[4],[4],[-4],[-4],[-4],[-4],[-4]]
    active=[0,1,2,5,6,7,8,9];vertices=[v for v in active if v!=2];assert detail['vertices']==vertices
    triangles=[sum(1<<v for v in t) for t in combinations(active,3)];index={q:i for i,q in enumerate(triangles)}
    base_triangles=[q for q in triangles if not q&4];assert detail['triangles']==base_triangles
    base_index={q:i for i,q in enumerate(base_triangles)};basis=[]
    for t in combinations(vertices[1:],3):basis.append(sum(1<<base_index[sum(1<<v for v in f)] for f in combinations((vertices[0],)+t,3)))
    assert detail['basis']==basis and len(basis)==20
    codes=independent_cycles(vertices,triangles);assert len(codes)==detail['cycles_checked']==source['cycles_checked']==1<<20
    hist=Counter(code.bit_count() for code in codes);assert dict(sorted(hist.items()))=={int(k):v for k,v in detail['weight_histogram'].items()}
    masks={v:sum(1<<i for i,q in enumerate(triangles) if q>>v&1) for v in active};expected={};prefilter=Counter()
    for code in codes:
        weight=code.bit_count()
        if weight not in (6,8,10):continue
        if all((code&masks[v]).bit_count() in (3,4,5) for v in active if v>=5) and all((code&masks[v]).bit_count() in (0,3,4,5) for v in (0,1)):prefilter[weight]+=1
        faces=code
        while faces:
            bit=faces&-faces;faces^=bit;face=triangles[bit.bit_length()-1];positive_code=code^bit
            vs=[v for v in active if face>>v&1]
            for a,c in combinations(vs,2):positive_code|=1<<index[4|(1<<a)|(1<<c)]
            if positive_code>>index[7]&1:continue
            degrees={v:(positive_code&masks[v]).bit_count() for v in active}
            if degrees[2]!=3 or any(degrees[v] not in (0,4,5) for v in (0,1)) or any(degrees[v] not in (4,5) for v in active if v>=5):continue
            positive=tuple(sorted(q for i,q in enumerate(triangles) if positive_code>>i&1));linear=sorted([4]+[1<<v for v in active if v!=2 and degrees[v]==5]);Q=len(linear)
            assert Q in (2,4,6) and len(positive)==Q+6
            base_code=sum(1<<base_index[q] for i,q in enumerate(triangles) if code>>i&1)
            assert positive not in expected;expected[positive]=dict(base_code=base_code,stellar_face=face,linear=linear,linear_count=Q)
    assert dict(sorted(prefilter.items()))=={int(k):v for k,v in detail['degree_prefilter_histogram'].items()}
    actual={tuple(r['positive']):r for r in detail['candidates']};assert len(actual)==len(detail['candidates'])==source['candidates'] and set(actual)==set(expected)
    counts=Counter();survivors=[]
    for positive,parameters in expected.items():
        record=actual[positive];assert all(record[k]==v for k,v in parameters.items()) and record['negative']==[7]
        spectrum=[(q,1) for q in positive]+[(q,-1) for q in parameters['linear']]+[(7,-2)]
        if check_value_witness(spectrum,values,record['first_failure']):survivors.append(record)
        counts[parameters['linear_count']]+=1
    assert dict(counts)=={int(k):v for k,v in source['candidate_counts'].items()} and len(survivors)==source['survivors']
    for name in ('verify_parent00_cubic_cycles.py','test_verify_parent00_cubic_cycles.py','parent00-cubic-cycle-reduction-cycle111.md','signed-divisibility-criterion-cycle107.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_PARENT00_NEGATIVE7_CYCLE_ENUMERATION',global_status='UNRESOLVED',source=b.bind(source_path),
        authority=source['authority'],geometry=source['geometry'],parent=source['parent'],negative=[7],cycles_checked=len(codes),
        candidates=len(expected),candidate_counts=dict(counts),survivors=survivors,negative_position_excluded=not survivors,
        whole_parent_excluded=False,solver_imported=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(cycles=len(codes),candidates=len(expected),counts=dict(counts),survivors=len(survivors))),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
