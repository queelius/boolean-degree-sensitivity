"""Complete degree-only cubic families for canonical ordinary singleton partitions."""
from argparse import ArgumentParser
from itertools import combinations
from pathlib import Path
from time import monotonic
from collections import Counter
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import write_certificate
from center_negative_placement_cover import orbit_cover
from verify_cubic_negative_pair_cover import signature
from cubic_degree_profiles import degree_options,degree_profiles
from parent00_direct_cycles import linear_for_profile
from forced_link_cycles_v2 import bounded_forced_cycles

H=Path(__file__).resolve().parent


def run(low_counts,output):
    assert low_counts==sorted(set(low_counts)) and all(2<=k<=6 for k in low_counts)
    b=Bindings();start=monotonic()
    singleton_path=H/'cubic-N1-interval-transfers-independent-manifest-cycle109.json';single=b.read(singleton_path)
    pair_path=H/'cubic-two-negative-position-cover-independent-manifest.json';pair=b.read(pair_path,'823639dc656ba01972df0cf2dacdbf49f6e860a9815af2af56e40bdb1cdc6766')
    assert single['frames_authority']==pair['frames_authority'] and single['allowed_apex_counts']==[1,2] and pair['allowed_signatures']==[[1,2,0]]
    triples=[q for q in range(1024) if q.bit_count()==3]
    patterns=[(q,) for q in triples if q&3]+[p for p in combinations(triples,2) if signature(p,[0,1])==(1,2,0)]
    directory=output.with_suffix('');assert not output.exists() and not directory.exists();directory.mkdir();covers=[];records=[]
    for low_count in low_counts:
        groups=[list(range(2)),list(range(2,2+low_count)),list(range(2+low_count,10))];generators=[]
        for group in groups:
            for i,j in zip(group,group[1:]):
                permutation=list(range(10));permutation[i],permutation[j]=j,i;generators.append(permutation)
        representatives,maps=orbit_cover(patterns,generators,10)
        cover=dict(low_count=low_count,coordinate_groups=groups,generators=generators,
            representatives=[dict(index=i,pattern=list(p)) for i,p in enumerate(representatives)],maps=maps)
        covers.append(cover)
        singletons=[[0,8],[0,8]]+[[4] for _ in groups[1]]+[[-4] for _ in groups[2]]
        for orbit_index,negative in enumerate(representatives):
            case_start=monotonic();negative=list(negative);options=degree_options(10,negative,singletons);profiles=degree_profiles(10,negative,singletons)
            active=[i for i,c in enumerate(options) if any(d or u for d,u in c) or any(q>>i&1 for q in negative)]
            lows=[i for i in active if {d for d,u in options[i]}=={3}];high=[i for i in active if i not in lows]
            assert len(high)<=8 and len(lows)<=4
            allowed={i:{d for d,u in options[i]} for i in high};maps_by_degree=[dict(c) for c in options]
            assert all(len(m)==len(c) for m,c in zip(maps_by_degree,options))
            maximum=max((p['positive_count'] for p in profiles),default=0);families=0;candidates=[];seen=set()
            if profiles:
                for positive in bounded_forced_cycles(high,lows,allowed,maximum):
                    assert positive not in seen;seen.add(positive);families+=1
                    if set(positive)&set(negative):continue
                    degrees=[sum(bool(q>>i&1) for q in positive) for i in range(10)]
                    linear=linear_for_profile(degrees,maps_by_degree,len(positive),len(negative))
                    if linear is None:continue
                    candidates.append(dict(positive=list(positive),linear=[1<<i for i,u in enumerate(linear) if u]))
            candidates.sort(key=lambda r:tuple(r['positive']))
            detail=dict(low_count=low_count,index=orbit_index,negative=negative,singletons=singletons,degree_options=options,
                profiles=len(profiles),high=high,lows=lows,maximum_faces=maximum,degree_bounded_families=families,candidates=candidates)
            path=directory/f'L{low_count}-r{orbit_index:03d}.json.gz';write_certificate(path,detail)
            record=dict(low_count=low_count,index=orbit_index,negative=negative,proof=b.bind(path),profiles=len(profiles),
                degree_bounded_families=families,candidates=len(candidates),candidate_counts=dict(Counter(len(r['linear']) for r in candidates)),seconds=monotonic()-case_start)
            records.append(record);print(json.dumps({k:v for k,v in record.items() if k!='proof'}),flush=True)
    for name in ('singleton_stratified_cubic_catalogs_v2.py','forced_link_cycles_v2.py','test_forced_link_cycles_v2.py','small_link_high_cycles.py','test_small_link_high_cycles.py','eight_vertex_small_link_plan_cycle138.md'):b.bind(H/name)
    result=dict(status='COMPLETE_SINGLETON_STRATIFIED_CUBIC_CATALOGS',global_status='UNRESOLVED',independent_audit='PENDING',
        actual_singleton_authority=b.bind(singleton_path),actual_pair_authority=b.bind(pair_path),low_counts=low_counts,covers=covers,records=records,
        parent_specific_scalar_filter_applied=False,parent_exclusion_claimed=False,elapsed_seconds=monotonic()-start,
        sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(seconds=result['elapsed_seconds'],cases=len(records),candidates=sum(r['candidates'] for r in records))),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--low-counts',type=int,nargs='+',required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.low_counts,a.output)
