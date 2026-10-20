"""Complete the three missing N=2 cubic catalogs using the low-vertex classification."""
from pathlib import Path
from time import monotonic
from collections import Counter
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from generic_parseval_envelope import permitted
from two_positive_four_cube_domains import CubeIndex
from cubic_degree_profiles import degree_options,degree_profiles
from parent00_direct_cycles import linear_for_profile
from fixed_projection_cube_domains import projection_values
from multiple_low_cycles import bounded_low_cycles

H=Path(__file__).resolve().parent


def run():
    start=monotonic();b=Bindings();frontier_path=H/'parent00-cubic-position-frontier-cycle117.json';frontier=b.read(frontier_path)
    assert frontier['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER';parent=read_certificate(b,frontier['parent']);g=frontier['geometry']
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows']
    values=permitted(g,parent['domains'],CubeIndex.build(rows),[3])[3];assert values[0]==[4];singletons=[values[1<<i] for i in range(10)]
    allowed_values=np.zeros((1024,65),dtype=bool)
    for x,possible in enumerate(values):allowed_values[x,np.array(possible)+32]=True
    selected=[r for r in frontier['remaining'] if len(r['negative'])==2];assert len(selected)==3
    directory=H/'parent00-multiple-low-cycle-catalogs-cycle119';output=directory.with_suffix('.json');assert not directory.exists() and not output.exists();directory.mkdir();records=[]
    for record in selected:
        case_start=monotonic();negative=record['negative'];options=degree_options(10,negative,singletons);profiles=degree_profiles(10,negative,singletons);maximum_faces=max(p['positive_count'] for p in profiles)
        active=[i for i,c in enumerate(options) if any(d or u for d,u in c) or any(q>>i&1 for q in negative)]
        lows=[i for i in active if {d for d,u in options[i]}=={3}];high=[i for i in active if i not in lows]
        assert len(high)==7 and len(lows) in (2,3)
        allowed={i:{d for d,u in options[i]} for i in high};maps=[dict(c) for c in options];assert all(len(m)==len(c) for m,c in zip(maps,options))
        candidates=[];families=0;seen=set();counts=Counter()
        for positive in bounded_low_cycles(high,lows,allowed,maximum_faces):
            assert positive not in seen;seen.add(positive);families+=1
            # Negative faces in the high base can be toggled away during link
            # restoration, so forbidden-face filtering is done on the final family.
            if set(positive)&set(negative):continue
            degrees=[sum(bool(q>>i&1) for q in positive) for i in range(10)]
            linear=linear_for_profile(degrees,maps,len(positive),len(negative))
            if linear is None:continue
            linear_supports=[1<<i for i,u in enumerate(linear) if u];spectrum=[(q,1) for q in positive]+[(q,-1) for q in linear_supports]+[(q,-2) for q in negative]
            evaluated=np.asarray(projection_values(spectrum),dtype=np.int16);assert np.max(np.abs(evaluated))<=32
            failures=np.flatnonzero(~allowed_values[np.arange(1024),evaluated+32]);failure=None
            if len(failures):
                x=int(failures[0]);failure=dict(point=x,value=int(evaluated[x]),allowed=values[x])
            candidates.append(dict(positive=list(positive),linear=linear_supports,linear_count=len(linear_supports),first_failure=failure));counts[len(linear_supports)]+=1
        detail=dict(index=record['index'],negative=negative,geometry=g,parent=frontier['parent'],high=high,lows=lows,degree_options=options,maximum_faces=maximum_faces,
            cycles_checked=1<<20,degree_bounded_families=families,candidates=candidates)
        path=directory/f'r{record["index"]:02d}.json.gz';write_certificate(path,detail)
        result=dict(index=record['index'],negative=negative,proof=b.bind(path),degree_bounded_families=families,candidates=len(candidates),candidate_counts=dict(counts),survivors=sum(r['first_failure'] is None for r in candidates),seconds=monotonic()-case_start)
        records.append(result);print(json.dumps({k:v for k,v in result.items() if k!='proof'}),flush=True)
    for name in ('parent00_multiple_low_cycles.py','multiple_low_cycles.py','test_multiple_low_cycles.py','multiple-low-degree-cycle-refinement-cycle118.md','multiple-low-degree-cycle-reduction-draft-cycle118.md'):b.bind(H/name)
    result=dict(status='COMPLETE_PARENT00_MULTIPLE_LOW_CUBIC_CYCLE_CATALOGS',global_status='UNRESOLVED',independent_audit='PENDING',frontier=b.bind(frontier_path),geometry=g,parent=frontier['parent'],core_mask=3,
        records=records,elapsed_seconds=monotonic()-start,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':run()
