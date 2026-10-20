"""Explicit parent-preserving maps among the complete surviving cubic catalogs."""
from pathlib import Path
from collections import deque
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate

H=Path(__file__).resolve().parent


def image(q,p):return sum(1<<p[i] for i in range(len(p)) if q>>i&1)


def group(generators,n):
    identity=tuple(range(n));seen={identity};queue=deque([identity])
    while queue:
        p=queue.popleft()
        for g in generators:
            new=tuple(g[p[i]] for i in range(n))
            if new not in seen:seen.add(new);queue.append(new)
        assert len(seen)<=100000
    return sorted(seen)


def signature(projection,p):
    return tuple(tuple(sorted(image(q,p) for q in projection[field])) for field in ('negative','linear','positive'))


def run():
    b=Bindings();frontier_path=H/'parent00-cubic-position-frontier-cycle112.json';frontier=b.read(frontier_path);cover=read_certificate(b,frontier['cover'])
    assert frontier['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER'
    parent=read_certificate(b,frontier['parent']);known=dict(parent['known']);g=frontier['geometry'];outside=cover['outside'];coordinates={v:i for i,v in enumerate(outside)}
    full=group(cover['full_generators'],14);local=[tuple(coordinates[p[v]] for v in outside) for p in full]
    for p in cover['full_generators']:
        assert sorted(p)==list(range(14)) and {image(q,p):k for q,k in known.items()}==known
        assert sorted(image(q,p) for q in g['positive_doubles'])==sorted(g['positive_doubles'])
        assert all(image(q,p)==q for q in g['eligible_pairs'])
    records=[]
    for catalog in frontier['complete_projection_catalogs']:
        authority=b.read(catalog['authority']['path'],catalog['authority']['sha256']);source=next(r for r in authority['records'] if r['index']==catalog['index']);projections=source['survivors']
        lookup={signature(s,range(10)):j for j,s in enumerate(projections)};assert len(lookup)==len(projections)==catalog['survivors']
        stabilizer=[(p,m) for p,m in zip(full,local) if sorted(image(q,m) for q in catalog['negative'])==catalog['negative']]
        unseen=set(range(len(projections)));representatives=[];maps=[]
        while unseen:
            representative=min(unseen);representatives.append(representative)
            for p,m in stabilizer:
                target=lookup[signature(projections[representative],m)]
                if target in unseen:
                    unseen.remove(target);maps.append(dict(projection_index=target,representative=representative,outside_map=list(m),global_map=list(p)))
        record=dict(index=catalog['index'],negative=catalog['negative'],catalog=catalog['authority'],projection_count=len(projections),representatives=representatives,maps=sorted(maps,key=lambda r:r['projection_index']))
        records.append(record);print(json.dumps(dict(index=catalog['index'],projections=len(projections),representatives=len(representatives),stabilizer_size=len(stabilizer))),flush=True)
    b.bind(H/'parent00_projection_orbits.py')
    result=dict(status='EXPLICIT_PARENT00_CUBIC_PROJECTION_ORBIT_COVERS',global_status='UNRESOLVED',independent_audit='PENDING',frontier=b.bind(frontier_path),geometry=g,parent=frontier['parent'],outside=outside,
        parent_group_size=len(full),records=records,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output=H/'parent00-projection-orbit-cover-cycle113.json';assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':run()
