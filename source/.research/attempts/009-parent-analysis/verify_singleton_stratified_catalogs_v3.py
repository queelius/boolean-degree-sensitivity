"""Independent complete reconstruction of degree-only singleton-stratified catalogs."""
from argparse import ArgumentParser
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_cubic_target_covers import verify_maps
from verify_cubic_negative_pair_cover import signature
from verify_parent00_cubic_cycles import independent_cycles
from verify_forced_link_cycles_v2 import independent_forced_cycles
from independent_small_link_cycles import literal_bounded_high_cycles

H=Path(__file__).resolve().parent


def compare_old_degree_catalogs(b,records):
    current={tuple(r['negative']):r for r in records if r['low_count']==3}
    if not current:return 0
    old=[]
    for name in ('parent00-direct-cycle-catalogs-independent-manifest-cycle112.json',
                 'parent00-link-cycle-catalogs-independent-manifest-cycle112.json',
                 'parent00-multiple-low-cycle-catalogs-independent-manifest-cycle119.json'):
        authority=b.read(H/name)
        old.extend((r['negative'],r['proof']) for r in authority['records'])
    a=b.read(H/'parent00-negative7-cycle-independent-manifest-cycle111.json')
    producer=b.read(a['source']['path'],a['source']['sha256']);old.append((a['negative'],producer['proof']))
    checked=set()
    for negative,ref in old:
        previous=read_certificate(b,ref);now=read_certificate(b,current[tuple(negative)]['proof'])
        first={(tuple(r['positive']),tuple(r['linear'])) for r in previous['candidates']}
        second={(tuple(r['positive']),tuple(r['linear'])) for r in now['candidates']}
        assert first==second,(negative,len(first),len(second));checked.add(tuple(negative))
    euler=b.read(H/'parent00-negative13-euler-independent-manifest-cycle112.json')
    assert euler['negative_position_excluded']
    assert read_certificate(b,current[tuple(euler['negative'])]['proof'])['candidates']==[]
    checked.add(tuple(euler['negative']));assert checked==set(current)
    return len(checked)


def run(source_path,output):
    b=Bindings();source=b.read(source_path);assert source['status']=='COMPLETE_SINGLETON_STRATIFIED_CUBIC_CATALOGS'
    single=b.read(source['actual_singleton_authority']['path'],source['actual_singleton_authority']['sha256'])
    pair=b.read(source['actual_pair_authority']['path'],source['actual_pair_authority']['sha256'])
    assert single['allowed_apex_counts']==[1,2] and pair['allowed_signatures']==[[1,2,0]] and single['frames_authority']==pair['frames_authority']
    triples=[q for q in range(1024) if q.bit_count()==3]
    patterns={(q,) for q in triples if q&3}|{p for p in combinations(triples,2) if signature(p,[0,1])==(1,2,0)}
    assert source['low_counts']==sorted(set(source['low_counts'])) and all(2<=L<=6 for L in source['low_counts'])
    assert [c['low_count'] for c in source['covers']]==source['low_counts'];expected={}
    for cover in source['covers']:
        L=cover['low_count'];groups=[list(range(2)),list(range(2,2+L)),list(range(2+L,10))]
        assert cover['coordinate_groups']==groups
        verify_maps(10,patterns,cover['representatives'],cover['maps'])
        for m in cover['maps']:
            assert all({m['map'][i] for i in group}==set(group) for group in groups)
        for r in cover['representatives']:expected[L,r['index']]=r['pattern']
    assert len(source['records'])==len(expected) and {(r['low_count'],r['index']) for r in source['records']}==set(expected)
    triangles=[sum(1<<v for v in t) for t in combinations(range(10),3)];cache={};results=[]
    for record in source['records']:
        L=record['low_count'];key=L,record['index'];negative=expected[key];detail=read_certificate(b,record['proof'])
        assert record['negative']==negative and detail['negative']==negative and (detail['low_count'],detail['index'])==key
        singletons=[[0,8],[0,8]]+[[4] for _ in range(L)]+[[-4] for _ in range(8-L)]
        assert detail['singletons']==singletons
        incident=[sum(bool(q>>i&1) for q in negative) for i in range(10)]
        options=[[[d,u] for d in range(37) if d==0 or d>=3 for u in (0,1) if 4-2*(d-2*incident[i]-u) in singletons[i]] for i in range(10)]
        assert detail['degree_options']==options
        profiles=[p for p in product(*options) if sum(u for d,u in p)%2==0 and sum(d for d,u in p)==3*(sum(u for d,u in p)+4+2*len(negative))]
        maximum=max((sum(u for d,u in p)+4+2*len(negative) for p in profiles),default=0)
        assert detail['profiles']==record['profiles']==len(profiles) and detail['maximum_faces']==maximum
        active=[i for i in range(10) if incident[i] or any(d or u for d,u in options[i])]
        lows=[i for i in active if {d for d,u in options[i]}=={3}];high=[i for i in active if i not in lows]
        assert detail['high']==high and detail['lows']==lows and len(high)<=8
        allowed={i:{d for d,u in options[i]} for i in high};families=set();candidates={}
        if profiles:
            if len(high)<=7:
                if tuple(high) not in cache:cache[tuple(high)]=independent_cycles(high,triangles)
                base=cache[tuple(high)]
            else:
                assert len(high)==8
                caps=[max(allowed[v]) for v in high]
                anchor=next(v for v in reversed(high) if max(allowed[v])<=5)
                critical=[v for v in high if max(allowed[v])>=6]
                exceptional=len(lows)>=2 and len(lows)+len(critical)==4
                cap=max(maximum-2*len(lows),maximum-4 if exceptional else -1)
                base=literal_bounded_high_cycles(high,anchor,caps,max(0,cap),triangles)
            for code in independent_forced_cycles(high,lows,allowed,maximum,triangles,base):
                assert code not in families;families.add(code)
                positive=tuple(sorted(q for j,q in enumerate(triangles) if code>>j&1))
                if set(positive)&set(negative):continue
                degrees=[sum(bool(q>>i&1) for q in positive) for i in range(10)]
                assert all(degrees[i]==3 for i in lows);linear=[]
                for i,d in enumerate(degrees):
                    choices=[u for u in (0,1) if 4-2*(d-2*incident[i]-u) in singletons[i]]
                    if not choices:break
                    assert len(choices)==1;linear.append(choices[0])
                if len(linear)!=10 or sum(linear)%2 or len(positive)!=sum(linear)+4+2*len(negative):continue
                candidates[positive]=[1<<i for i,u in enumerate(linear) if u]
        assert len(families)==detail['degree_bounded_families']==record['degree_bounded_families']
        actual={tuple(r['positive']):r['linear'] for r in detail['candidates']}
        assert len(actual)==len(detail['candidates'])==record['candidates'] and actual==candidates
        counts=dict(Counter(map(len,candidates.values())));assert counts=={int(k):v for k,v in record['candidate_counts'].items()}
        result=dict(low_count=L,index=record['index'],negative=negative,proof=record['proof'],profiles=len(profiles),
            degree_bounded_families=len(families),candidates=len(candidates),candidate_counts=counts)
        results.append(result);print(json.dumps({k:v for k,v in result.items() if k!='proof'}),flush=True)
    regressions=compare_old_degree_catalogs(b,results)
    for name in ('verify_singleton_stratified_catalogs_v3.py','verify_forced_link_cycles_v2.py','test_verify_forced_link_cycles_v2.py','independent_small_link_cycles.py','test_independent_small_link_cycles.py','eight_vertex_small_link_plan_cycle138.md','small_link_completeness_cycle139.md','forced_link_reader_reachability_cycle140.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_SINGLETON_STRATIFIED_CUBIC_CATALOGS',global_status='UNRESOLVED',source=b.bind(source_path),
        low_counts=source['low_counts'],covers=source['covers'],records=results,old_complete_degree_catalog_regressions=regressions,
        parent_specific_scalar_filter_applied=False,parent_exclusion_claimed=False,solver_imported=False,canonicalizer_imported=False,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(cases=len(results),candidates=sum(r['candidates'] for r in results),old_catalog_regressions=regressions)),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
