"""Independent full ambient face-bitmask reconstruction of forced-link cycles."""
from itertools import combinations


def independent_forced_cycles(high,lows,allowed,max_faces,triangles,codes):
    assert len(set(high))==len(high) and len(set(lows))==len(lows) and not set(high)&set(lows)
    assert high and len(lows)<=4 and max_faces>=0 and set(allowed)==set(high)
    assert all(s and set(s)<=set((0,4,5,6,7)) for s in allowed.values())
    critical=[v for v in high if max(allowed[v])>=6];assert len(lows)+len(critical)<=4
    index={q:i for i,q in enumerate(triangles)}
    masks={v:sum(1<<j for j,q in enumerate(triangles) if q>>v&1) for v in high}
    high_triples=list(combinations(high,3));toggles=[]
    for c in reversed(lows):
        toggles.append([sum(1<<index[sum(1<<v for v in f)] for f in combinations((c,)+t,3)) for t in high_triples])
    exceptional=None
    if len(lows)>=2 and len(lows)+len(critical)==4:
        exceptional=sum(1<<index[sum(1<<v for v in f)] for f in combinations(tuple(lows)+tuple(critical),3))

    def extend(stage,code):
        if code.bit_count()+2*(len(lows)-stage)>max_faces:return
        remaining=len(lows)-stage
        degrees={v:(code&masks[v]).bit_count() for v in high}
        if any(not any(degrees[v]<=target<=degrees[v]+3*remaining for target in allowed[v]) for v in high):return
        if stage==len(lows):
            if all((code&masks[v]).bit_count() in allowed[v] for v in high):yield code
            return
        for toggle in toggles[stage]:yield from extend(stage+1,code^toggle)

    for code in codes:
        weight=code.bit_count()
        if weight+2*len(lows)<=max_faces:yield from extend(0,code)
        if exceptional is not None and weight+4<=max_faces:
            full=code^exceptional
            if all((full&masks[v]).bit_count() in allowed[v] for v in high):yield full
