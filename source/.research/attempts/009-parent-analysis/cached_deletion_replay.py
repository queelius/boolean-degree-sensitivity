"""Literal array verification, caching identical covers in identical contexts."""
import numpy as np


def replay_cached(tables,relations,domains,deletions,*,stats=None):
    assert len(tables)==len(domains)
    original=[np.asarray(d,dtype=np.int64)for d in domains]
    assert all(len(set(map(int,d)))==len(d)and np.all((d>=0)&(d<len(t)))for t,d in zip(tables,original))
    active=[np.zeros(len(t),dtype=bool)for t in tables]
    for a,d in zip(active,original):a[d]=True
    counts=[len(d)for d in original];versions=[0]*len(tables);cache=set()
    if stats is None:stats={}
    stats.setdefault('cover_replays',0);stats.setdefault('cached_covers',0)
    for record in deletions:
        a,i,c=record['variable'],record['candidate'],record['partner'];points=record['points']
        assert all(type(x)is int for x in (a,i,c))and 0<=a<len(tables)and 0<=c<len(tables)and a!=c
        assert 0<=i<len(tables[a])and active[a][i]and counts[c]>0
        assert all(type(x)is int and 0<=x<len(relations)for x in points)
        values=tuple(int(tables[a][i,x])for x in points)
        key=a,c,versions[c],tuple(points),values
        if key in cache:stats['cached_covers']+=1
        else:
            possible=original[c][active[c][original[c]]]
            for x,value in zip(points,values):
                allowed=sorted({r[c]for r in relations[x]if r[a]==value})
                reduced=possible[np.isin(tables[c][possible,x],allowed)]
                assert len(reduced)<len(possible);possible=reduced
            assert not len(possible);cache.add(key);stats['cover_replays']+=1
        active[a][i]=False;counts[a]-=1;versions[a]+=1
    return [d[a[d]]for d,a in zip(original,active)]
