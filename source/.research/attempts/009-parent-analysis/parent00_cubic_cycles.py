"""Complete small binary-cycle enumeration after the parent0/0 singleton reduction."""
from itertools import combinations
from collections import Counter
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from generic_parseval_envelope import permitted
from two_positive_four_cube_domains import CubeIndex

H=Path(__file__).resolve().parent


def cycle_basis(vertices):
    assert vertices==sorted(set(vertices)) and len(vertices)>=4
    triangles=[sum(1<<i for i in t) for t in combinations(vertices,3)];index={q:i for i,q in enumerate(triangles)};basis=[];anchor=vertices[0]
    for triple in combinations(vertices[1:],3):
        tetra=(anchor,)+triple;basis.append(sum(1<<index[sum(1<<i for i in t)] for t in combinations(tetra,3)))
    return triangles,basis


def gray_cycles(basis):
    code=0;yield code
    for i in range(1,1<<len(basis)):
        code^=basis[(i&-i).bit_length()-1];yield code


def stellar(base,face,center):
    assert face in base and face.bit_count()==3 and not any(q>>center&1 for q in base)
    vertices=[i for i in range(face.bit_length()) if face>>i&1]
    return (set(base)-{face})|{(1<<center)|sum(1<<i for i in pair) for pair in combinations(vertices,2)}


def run():
    start=monotonic();b=Bindings();authority_path=H/'cubic-parent-pattern-pilot-independent-manifest-cycle110.json';authority=b.read(authority_path)
    case=next(r for r in authority['records'] if (r['first_row'],r['second_row'])==(0,0));parent=read_certificate(b,case['parent']);g=authority['geometry']
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];values=permitted(g,parent['domains'],CubeIndex.build(rows),[3])[3]
    assert values[0]==[4] and [values[1<<i] for i in range(10)]==[[0,8],[0,8],[4],[4],[4],[-4],[-4],[-4],[-4],[-4]]
    vertices=[0,1,5,6,7,8,9];triangles,basis=cycle_basis(vertices);assert len(basis)==20
    incidence={v:sum(1<<i for i,q in enumerate(triangles) if q>>v&1) for v in vertices};hist=Counter();prefilter=Counter();candidates=[];seen=set()
    for code in gray_cycles(basis):
        weight=code.bit_count();hist[weight]+=1
        if weight not in (6,8,10):continue
        degrees={v:(code&incidence[v]).bit_count() for v in vertices}
        if any(degrees[v] not in (3,4,5) for v in vertices if v>=5) or any(degrees[v] not in (0,3,4,5) for v in (0,1)):continue
        prefilter[weight]+=1;must=sum(1<<v for v,d in degrees.items() if d==3);forbidden=sum(1<<v for v,d in degrees.items() if d==5)
        base=[q for i,q in enumerate(triangles) if code>>i&1]
        for face in base:
            if face&must!=must or face&forbidden or face&3==3:continue
            positive=sorted(stellar(base,face,2));linear=sorted([4]+[1<<v for v in vertices if degrees[v]+int(bool(face>>v&1))==5]);Q=len(linear)
            assert Q in (2,4,6) and len(positive)==Q+6 and 7 not in positive
            key=tuple(positive);assert key not in seen;seen.add(key)
            spectrum=sorted([(q,1) for q in positive]+[(q,-1) for q in linear]+[(7,-2)]);failure=None
            for point,allowed in enumerate(values):
                value=sum(k*(-1 if (q&point).bit_count()%2 else 1) for q,k in spectrum)
                if value not in allowed:failure=dict(point=point,value=value,allowed=allowed);break
            candidates.append(dict(base_code=code,stellar_face=face,positive=positive,linear=linear,negative=[7],linear_count=Q,first_failure=failure))
    detail=dict(geometry=g,parent=case['parent'],negative=[7],vertices=vertices,center=2,triangles=triangles,basis=basis,
        cycles_checked=1<<20,weight_histogram=dict(sorted(hist.items())),degree_prefilter_histogram=dict(sorted(prefilter.items())),candidates=candidates)
    path=H/'parent00-negative7-cycle-enumeration-cycle111.json.gz';write_certificate(path,detail)
    for name in ('parent00_cubic_cycles.py','test_parent00_cubic_cycles.py','parent00-cubic-cycle-reduction-cycle111.md'):b.bind(H/name)
    output=H/'parent00-negative7-cycle-enumeration-cycle111.json';assert not output.exists()
    result=dict(status='COMPLETE_PARENT00_NEGATIVE7_TRIANGLE_CYCLE_ENUMERATION',global_status='UNRESOLVED',independent_audit='PENDING',
        authority=b.bind(authority_path),geometry=g,parent=case['parent'],negative=[7],proof=b.bind(path),cycles_checked=1<<20,
        candidates=len(candidates),candidate_counts=dict(Counter(r['linear_count'] for r in candidates)),survivors=sum(r['first_failure'] is None for r in candidates),
        accepted_exclusion=False,elapsed_seconds=monotonic()-start,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('sources','proof','authority','geometry','parent')}),flush=True)


if __name__=='__main__':run()
