"""Exact cycles with two/three degree-three lows and the actual high degree bounds."""
from itertools import combinations
from parent00_cubic_cycles import gray_cycles


def bounded_low_cycles(high,lows,allowed,max_faces):
    high=list(high);lows=list(lows)
    assert high==sorted(set(high)) and lows==sorted(set(lows)) and len(high)>=3 and len(lows) in (2,3)
    assert not set(high)&set(lows) and set(allowed)==set(high)
    assert all(s and set(s)<=set((0,4,5,6,7)) for s in allowed.values())
    critical=[v for v in high if any(d>=6 for d in allowed[v])];assert len(critical)==4-len(lows)
    faces=[sum(1<<v for v in t) for t in combinations(high,3)];index={q:i for i,q in enumerate(faces)};basis=[]
    for t in combinations(high[1:],3):basis.append(sum(1<<index[sum(1<<v for v in f)] for f in combinations((high[0],)+t,3)))
    incidence=[sum(1<<j for j,q in enumerate(faces) if q>>v&1) for v in high];vertices=[[i for i,v in enumerate(high) if q>>v&1] for q in faces]
    stars=[[[((1<<c)|sum(1<<high[i] for i in edge)) for edge in combinations(vs,2)] for vs in vertices] for c in lows]
    maximum=[max(allowed[v]) for v in high]
    tetra=[sum(1<<v for v in t) for t in combinations(lows+critical,3)];assert len(tetra)==4

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

    for code in gray_cycles(basis):
        count=code.bit_count()
        if count>max(max_faces-2*len(lows),max_faces-4):continue
        degree=[(code&m).bit_count() for m in incidence]
        if any(d>m for d,m in zip(degree,maximum)):continue
        if count+2*len(lows)<=max_faces:yield from restore(0,code,degree,count,[])
        if count+4<=max_faces and all(d+(3 if v in critical else 0) in allowed[v] for v,d in zip(high,degree)):
            yield tuple(sorted([q for j,q in enumerate(faces) if code>>j&1]+tetra))
