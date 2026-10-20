"""Complete bounded cycles when degree-three vertices have at most four partners."""
from itertools import combinations
from parent00_cubic_cycles import gray_cycles
from small_link_high_cycles import bounded_high_codes


def bounded_forced_cycles(high,lows,allowed,max_faces):
    high=list(high);lows=list(lows)
    assert high==sorted(set(high)) and lows==sorted(set(lows)) and high and len(lows)<=4
    assert not set(high)&set(lows) and set(allowed)==set(high) and max_faces>=0
    assert all(s and set(s)<=set((0,4,5,6,7)) for s in allowed.values())
    critical=[v for v in high if max(allowed[v])>=6];assert len(lows)+len(critical)<=4
    faces=[sum(1<<v for v in t) for t in combinations(high,3)];index={q:i for i,q in enumerate(faces)}
    basis=[sum(1<<index[sum(1<<v for v in f)] for f in combinations((high[0],)+t,3)) for t in combinations(high[1:],3)]
    incidence=[sum(1<<j for j,q in enumerate(faces) if q>>v&1) for v in high]
    vertices=[[i for i,v in enumerate(high) if q>>v&1] for q in faces]
    stars=[[[((1<<c)|sum(1<<high[i] for i in edge)) for edge in combinations(vs,2)] for vs in vertices] for c in lows]
    maximum=[max(allowed[v]) for v in high]
    exceptional=len(lows)>=2 and len(lows)+len(critical)==4
    tetra=[sum(1<<v for v in t) for t in combinations(lows+critical,3)] if exceptional else []

    def restore(stage,code,degree,count,low_faces):
        remaining=len(lows)-stage
        if count+2*remaining>max_faces:return
        if any(not any(d<=a<=d+3*remaining for a in allowed[v]) for v,d in zip(high,degree)):return
        if not remaining:
            yield tuple(sorted([q for j,q in enumerate(faces) if code>>j&1]+low_faces));return
        for j,vs in enumerate(vertices):
            present=bool(code>>j&1);increment=1 if present else 3
            if any(degree[i]+increment>maximum[i] for i in vs):continue
            updated=degree.copy()
            for i in vs:updated[i]+=increment
            yield from restore(stage+1,code^(1<<j),updated,count+(2 if present else 4),low_faces+stars[stage][j])

    base_cap=max(max_faces-2*len(lows),max_faces-4 if exceptional else -1)
    if len(high)<=7:
        base=((code,code.bit_count(),[(code&m).bit_count() for m in incidence]) for code in gray_cycles(basis))
    else:
        assert len(high)==8
        anchor=next(v for v,m in zip(high,maximum) if m<=5)
        base=bounded_high_codes(high,anchor,maximum,max(0,base_cap))
    for code,count,degree in base:
        if count>max(max_faces-2*len(lows),max_faces-4 if exceptional else -1):continue
        if any(d>m for d,m in zip(degree,maximum)):continue
        if count+2*len(lows)<=max_faces:yield from restore(0,code,degree,count,[])
        if exceptional and count+4<=max_faces and all(d+(3 if v in critical else 0) in allowed[v] for v,d in zip(high,degree)):
            yield tuple(sorted([q for j,q in enumerate(faces) if code>>j&1]+tetra))
