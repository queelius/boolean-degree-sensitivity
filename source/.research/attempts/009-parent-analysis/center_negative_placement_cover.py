"""Explicit complete placement cover under partial-spectrum automorphisms."""
from collections import deque
from pathlib import Path
import json
import pynauty
from compose_class40_same_b_acceptance import Bindings
from safe_star_triple_orbits import triple_known
from verify_four_cube_pair_domains import LiteralCubeChecker

H=Path(__file__).resolve().parent


def move(q,image):return sum(1<<image[i] for i in range(len(image)) if q>>i&1)


def orbit_cover(patterns,generators,n):
    patterns={tuple(sorted(p)) for p in patterns}
    assert patterns and all(sorted(g)==list(range(n)) for g in generators)
    remaining=set(patterns);representatives=[];maps=[]
    while remaining:
        representative=min(remaining);index=len(representatives);representatives.append(representative)
        images={representative:tuple(range(n))};queue=deque([representative])
        while queue:
            current=queue.popleft();image=images[current]
            for generator in generators:
                target=tuple(sorted(move(q,generator) for q in current));assert target in patterns
                if target not in images:
                    images[target]=tuple(generator[v] for v in image);queue.append(target)
        for pattern,image in sorted(images.items()):
            assert pattern in remaining;remaining.remove(pattern)
            inverse=[None]*n
            for i,v in enumerate(image):inverse[v]=i
            assert tuple(sorted(move(q,inverse) for q in pattern))==representative
            maps.append(dict(pattern=list(pattern),representative=index,map=inverse))
    return representatives,sorted(maps,key=lambda r:r['pattern'])


def automorphisms(known,center,n=14):
    terms=sorted(known.items());adj={i:[] for i in range(n+len(terms))}
    colors=[{center.bit_length()-1},set(range(n))-{center.bit_length()-1}]
    colors += [{n+i for i,(_,v) in enumerate(terms) if v==k} for k in sorted({v for _,v in terms})]
    for i,(q,_) in enumerate(terms):
        for v in range(n):
            if q>>v&1:adj[v].append(n+i);adj[n+i].append(v)
    graph=pynauty.Graph(n+len(terms),adjacency_dict=adj,vertex_coloring=colors)
    generators,size,exponent,_,_=pynauty.autgrp(graph)
    result=[tuple(p[:n]) for p in generators]
    for p in result:
        assert sorted(p)==list(range(n)) and move(center,p)==center
        assert {move(q,p):k for q,k in known.items()}==known
    return result,dict(mantissa=size,exponent=exponent)


def run():
    b=Bindings();frontier_path=H/'center-pattern-family-independent-manifest.json';frontier=b.read(frontier_path)
    assert frontier['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_CENTER_PATTERN_FAMILY_SPLIT'
    authority=b.read(frontier['pattern_authority']['path'],frontier['pattern_authority']['sha256'])
    patterns=b.read(authority['source']['path'],authority['source']['sha256'])
    families={p['index']:p for p in patterns['patterns']}
    data=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')
    rows=data['domain']['rows'];g=frontier['geometry'];_,outside=LiteralCubeChecker.coordinates(g)
    center=g['eligible_pairs'][0]&g['eligible_pairs'][1]&g['eligible_pairs'][2]
    def global_support(q):return center|sum(1<<v for i,v in enumerate(outside) if q>>i&1)
    def local_support(q):return sum(1<<i for i,v in enumerate(outside) if q>>v&1)
    records=[]
    for case in frontier['remaining']:
        known=triple_known(rows,g,case['triple']);generators,order=automorphisms(known,center)
        for p in generators:
            assert sorted(move(q,p) for q in g['positive_doubles'])==g['positive_doubles']
            assert sorted(move(q,p) for q in g['eligible_pairs'])==g['eligible_pairs']
            assert {p[v] for v in outside}==set(outside)
        for family_id in case['remaining_pattern_indices']:
            family=families[family_id]
            actual=[tuple(sorted(global_support(q) for q in pattern)) for pattern in family['literal_patterns']]
            reps,maps=orbit_cover(actual,generators,14)
            for record in maps:record['pattern']=sorted(local_support(q) for q in record['pattern'])
            record=dict(class_index=case['index'],triple=case['triple'],negative_pattern_index=family_id,
                outside=outside,generators=generators,reported_group_order=order,
                representatives=[dict(index=i,pattern=sorted(local_support(q) for q in p)) for i,p in enumerate(reps)],
                maps=sorted(maps,key=lambda r:r['pattern']))
            records.append(record)
            print(json.dumps(dict(class_index=case['index'],family=family_id,literals=len(maps),representatives=len(reps))),flush=True)
    for name in ('center_negative_placement_cover.py','test_center_negative_placement_cover.py','safe_star_triple_orbits.py'):b.bind(H/name)
    output=H/'center-negative-placement-cover-cycle104.json';assert not output.exists()
    output.write_text(json.dumps(dict(status='PROPOSED_COMPLETE_CENTER_NEGATIVE_PLACEMENT_COVER',global_status='UNRESOLVED',
        frontier_authority=b.bind(frontier_path),pattern_authority=frontier['pattern_authority'],geometry=g,records=records,
        sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]),indent=2)+'\n')


if __name__=='__main__':run()
