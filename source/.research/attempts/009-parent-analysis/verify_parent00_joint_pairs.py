"""Independent explicit symmetry checks and scalar bitset joins of two row catalogs."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_fixed_projection_domains import literal_conditioned
from verify_four_cube_pair_domains import LiteralCubeChecker

H=Path(__file__).resolve().parent


def map_mask(mask,permutation):
    result=0
    for i,new in enumerate(permutation):
        if mask&(1<<i):result|=1<<new
    return result


def verify_orbits(b,source):
    assert source['status']=='EXPLICIT_PARENT00_CUBIC_PROJECTION_ORBIT_COVERS'
    frontier=b.read(source['frontier']['path'],source['frontier']['sha256']);parent=read_certificate(b,source['parent']);known=dict(parent['known'])
    assert source['geometry']==frontier['geometry'] and source['parent']==frontier['parent'];g=source['geometry'];outside=source['outside']
    assert outside==LiteralCubeChecker.coordinates(g)[1]
    catalogs={c['index']:c for c in frontier['complete_projection_catalogs']};assert {r['index'] for r in source['records']}==set(catalogs)
    for record in source['records']:
        c=catalogs[record['index']];assert record['catalog']==c['authority'] and record['negative']==c['negative']
        a=b.read(c['authority']['path'],c['authority']['sha256']);projections=next(r for r in a['records'] if r['index']==c['index'])['survivors']
        assert record['projection_count']==len(projections)==c['survivors']
        assert len(record['maps'])==len(projections) and {m['projection_index'] for m in record['maps']}==set(range(len(projections)))
        assert record['representatives']==sorted({m['representative'] for m in record['maps']})
        for m in record['maps']:
            p=m['global_map'];local=m['outside_map'];assert sorted(p)==list(range(14)) and sorted(local)==list(range(10))
            assert all(p[v]==outside[local[i]] for i,v in enumerate(outside))
            assert {map_mask(q,p):k for q,k in known.items()}==known
            assert sorted(map_mask(q,p) for q in g['positive_doubles'])==sorted(g['positive_doubles'])
            assert all(map_mask(q,p)==q for q in g['eligible_pairs'])
            core=g['positive_doubles'][0]&g['positive_doubles'][1];assert all(p[i]==i for i in range(14) if core>>i&1)
            left=projections[m['representative']];right=projections[m['projection_index']]
            assert all(sorted(map_mask(q,local) for q in left[k])==right[k] for k in ('negative','linear','positive'))
    return frontier


def literal_join(domains,g,spectrum,mask,checker):
    free=[j for j,d in enumerate(domains) if len(d['rows'])>1];fixed=[j for j,d in enumerate(domains) if len(d['rows'])==1];assert len(free)==2
    left,right=[domains[j]['rows'] for j in free];edges=[(1<<len(right))-1 for _ in left];pairs,_=checker.coordinates(g)
    for x in range(1024):
        values=checker.at(x);B=sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in spectrum)
        relation=literal_conditioned(pairs,x.bit_count(),1-(x&1)-((x>>1)&1),mask,B)
        parts={v:0 for v in range(-2,3)}
        for i,r in enumerate(right):parts[values[r]]|=1<<i
        keep={v:0 for v in range(-2,3)}
        for ts in relation:
            if all(ts[j]==values[domains[j]['rows'][0]] for j in fixed):keep[ts[free[0]]]|=parts[ts[free[1]]]
        for i,r in enumerate(left):edges[i]&=keep[values[r]]
        if not any(edges):break
    result=[]
    for r,code in zip(left,edges):
        while code:
            bit=code&-code;code^=bit;result.append([r,right[bit.bit_length()-1]])
    return result


def run(output):
    b=Bindings();source_path=H/'parent00-joint-pair-catalogs-cycle113.json';source=b.read(source_path)
    assert source['status']=='COMPLETE_PARENT00_FIXED_PROJECTION_TWO_ROW_CATALOGS'
    orbits=b.read(source['orbit_cover']['path'],source['orbit_cover']['sha256']);frontier=verify_orbits(b,orbits)
    authority=b.read(source['domain_authority']['path'],source['domain_authority']['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_PARENT00_FIXED_PROJECTION_PROPAGATION' and authority['frontier']==orbits['frontier']
    assert source['geometry']==orbits['geometry'] and source['parent']==orbits['parent']
    previous={(r['index'],r['projection_index']):r for r in authority['records']}
    expected={(r['index'],j) for r in orbits['records'] for j in r['representatives']}
    assert len(source['records'])==len(expected) and {(r['index'],r['projection_index']) for r in source['records']}==expected
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];checker=LiteralCubeChecker(rows);results=[]
    for record in source['records']:
        key=record['index'],record['projection_index'];detail=read_certificate(b,record['proof']);prior=previous[key]
        assert not prior['excluded'] and detail['previous']==prior['proof'];old=read_certificate(b,prior['proof'])
        assert (detail['index'],detail['projection_index'])==key and detail['geometry']==source['geometry'] and detail['parent']==source['parent'] and detail['core_mask']==3
        assert detail['input_domains']==old['proof']['domains'] and detail['spectrum']==old['spectrum'] and detail['projection']==old['projection']
        proof=detail['proof'];assert proof['status']=='COMPLETE_FIXED_PROJECTION_TWO_ROW_CATALOG'
        free=[j for j,d in enumerate(detail['input_domains']) if len(d['rows'])>1];assert len(free)==2 and free==proof['free_slots']
        count=1
        for j in free:count*=len(detail['input_domains'][j]['rows'])
        assert count==proof['pairs_tested']==record['pairs_tested']
        surviving=literal_join(detail['input_domains'],source['geometry'],detail['spectrum'],3,checker)
        assert surviving==proof['surviving_pairs'] and len(surviving)==record['surviving_pairs']
        result=dict(index=key[0],projection_index=key[1],proof=record['proof'],pairs_checked=count,surviving_pairs=len(surviving),projection_excluded=not surviving)
        results.append(result);print(json.dumps({k:v for k,v in result.items() if k!='proof'}),flush=True)
    summaries=[]
    for orbit in orbits['records']:
        excluded={r['projection_index'] for r in results if r['index']==orbit['index'] and r['projection_excluded']}
        literal=[m['projection_index'] for m in orbit['maps'] if m['representative'] in excluded]
        summaries.append(dict(index=orbit['index'],catalog_size=orbit['projection_count'],representatives=len(orbit['representatives']),excluded_representatives=sorted(excluded),
            excluded_projection_indices=literal,remaining_projection_indices=sorted(set(range(orbit['projection_count']))-set(literal)),negative_position_excluded=len(literal)==orbit['projection_count']))
    for name in ('verify_parent00_joint_pairs.py','test_verify_parent00_joint_pairs.py','verify_fixed_projection_domains.py','verify_four_cube_pair_domains.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_PARENT00_TWO_ROW_CATALOGS_AND_SYMMETRY',global_status='UNRESOLVED',source=b.bind(source_path),frontier=orbits['frontier'],orbit_cover=source['orbit_cover'],
        geometry=source['geometry'],parent=source['parent'],core_mask=3,records=results,summaries=summaries,whole_parent_excluded=False,boolean_function_on14_constructed=False,
        group_maximality_required=False,solver_imported=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(representatives=len(results),excluded_representatives=sum(r['projection_excluded'] for r in results),excluded_projections=sum(len(s['excluded_projection_indices']) for s in summaries),surviving_row_pairs=sum(r['surviving_pairs'] for r in results))),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
