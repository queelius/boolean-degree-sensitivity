"""Exact pair-domain consistency conditioned on a specified core projection."""
from functools import lru_cache
import numpy as np
from core_fourier_envelope import core_words
from two_positive_four_cube_domains import setup,supported_values


@lru_cache(None)
def conditioned_relation(pairs,weight,delta,mask,value):
    assert 0<=weight<=10 and delta in (-1,0,1) and 0<=mask<16
    words,truth,deltas,ts,sums=core_words(pairs)
    live=(deltas==delta)&(sums[:,mask]==value)
    for y in range(16):
        if weight+y.bit_count() in (0,12,13):live&=truth[:,y]==0
        elif weight+y.bit_count() in (1,2,14):live&=truth[:,y]==1
    return tuple(sorted(set(map(tuple,ts[live].astype(int).tolist()))))


def projection_values(spectrum,n=10):
    assert len({q for q,k in spectrum})==len(spectrum) and all(0<=q<1<<n and type(k) is int for q,k in spectrum)
    values=np.zeros(1<<n,dtype=np.int64)
    for q,k in spectrum:values[q]=k
    step=1
    while step<1<<n:
        blocks=values.reshape(-1,2,step);left=blocks[:,0,:].copy();right=blocks[:,1,:].copy()
        blocks[:,0,:]=left+right;blocks[:,1,:]=left-right;step*=2
    return values.tolist()


def propagate(domains,g,cubes,mask,spectrum):
    assert [d['pair'] for d in domains]==g['eligible_pairs']
    assert all(d['rows'] and d['rows']==sorted(set(d['rows'])) for d in domains)
    pairs,outside=setup(g);values=projection_values(spectrum);live=[sum(1<<r for r in d['rows']) for d in domains];steps=[]
    points=sorted(range(1024),key=lambda x:(min(x.bit_count(),10-x.bit_count()),x))
    while True:
        changed=False
        for point in points:
            partitions=cubes.partitions(point);available=tuple(sum(1<<i for i,part in enumerate(partitions) if part&rows) for rows in live)
            allowed=conditioned_relation(pairs,point.bit_count(),(1,0,0,-1)[point&3],mask,values[point])
            supports=supported_values(allowed,available)
            if not all(supports):
                return dict(status='EXACT_FIXED_PROJECTION_CUBE_CONTRADICTION',steps=steps,contradiction_point=point,projection_value=values[point])
            cuts=[]
            for j,(support,possible) in enumerate(zip(supports,available)):
                if support==possible:continue
                keep=0
                for i,part in enumerate(partitions):
                    if support>>i&1:keep|=part
                live[j]&=keep;cuts.append(dict(pair=domains[j]['pair'],remaining_rows=live[j].bit_count()))
            if cuts:steps.append(dict(point=point,cuts=cuts));changed=True
        if not changed:
            return dict(status='NECESSARY_FIXED_PROJECTION_CUBE_FIXED_POINT',steps=steps,
                domains=[dict(pair=d['pair'],rows=[i for i in range(len(cubes.table)) if live[j]>>i&1]) for j,d in enumerate(domains)])
