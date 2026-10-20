"""Small joint core-word moment relaxations, with exact coefficient norms."""
from collections import Counter
from fractions import Fraction
import numpy as np
from baseline_full_truth_model import Row
from core_fourier_envelope import core_words
from two_positive_four_cube_domains import setup


def singleton_norm(c,neighbor_sum,negative_count):
    return c*c+3*c-Fraction(neighbor_sum,2)+6*negative_count


def pair_norm(n,origin,neighbor_sum,negative_count):
    return Fraction((n-4)*origin-neighbor_sum,2)+6*negative_count


def joint_hull(pools):
    variables=[];rows=[];features=[]
    assert pools and all(pool for pool in pools)
    width=len(pools[0][0]);assert width and all(len(v)==width for pool in pools for v in pool)
    for point,pool in enumerate(pools):
        states=sorted(set(tuple(v) for v in pool));start=len(variables)
        variables.extend(dict(kind='joint_core_value_state',outside_point=point,features=list(v)) for v in states)
        rows.append(Row(tuple((start+j,1) for j in range(len(states))),1,1,dict(kind='joint_word_normalization',outside_point=point)))
        features.append([tuple((start+j,v[k]) for j,v in enumerate(states) if v[k]) for k in range(width)])
    return variables,rows,features


def fixed_word_pools(g,domains,cubes,masks):
    assert [d['pair'] for d in domains]==g['eligible_pairs'] and all(len(d['rows'])==1 for d in domains)
    pairs,_=setup(g);words,truth,delta,ts,sums=core_words(pairs);pools=[]
    for point in range(512):
        live=delta==(1,0,0,-1)[point&3]
        for j,d in enumerate(domains):live&=ts[:,j]==cubes.table[d['rows'][0],point]
        for y in range(16):
            weight=point.bit_count()+y.bit_count()
            if weight in (0,12,13):live&=truth[:,y]==0
            elif weight in (1,2,14):live&=truth[:,y]==1
        assert np.any(live)
        pools.append([tuple(map(int,v))+tuple(int(t)**2 for t in v) for v in sums[live][:,masks]])
    return pools


def build(pools,masks):
    assert len(pools)==512 and masks[:4]==[1,2,4,8] and len(masks)==6
    assert all(m.bit_count()==2 for m in masks[4:]) and masks[4]&masks[5]==0
    assert all(v[:4]==(0,0,0,0) and v[4:6]==(4,4) for v in pools[0])
    variables,rows,features=joint_hull(pools)
    extras=list(range(len(variables),len(variables)+4));variables.extend(dict(kind='singleton_extra',core_mask=m) for m in masks[:4])
    negatives=list(range(len(variables),len(variables)+6));variables.extend(dict(kind='quarter_negative_count',core_mask=m) for m in masks)
    def terms(parts):
        result=Counter()
        for factor,part in parts:
            for i,k in part:result[i]+=factor*k
        return tuple(sorted((i,k) for i,k in result.items() if k))
    for j,mask in enumerate(masks):
        parts=[(1,features[x][j+6]) for x in range(512)]
        for v in range(10):
            point=1<<v;sign=1
            if point>=512:
                point^=1023
                if mask.bit_count()==2:sign=-1
            parts.append((256*sign,features[point][j]))
        parts.append((-12288,((negatives[j],1),)))
        if j<4:
            parts.append((-3072,((extras[j],1),)));target=2048
            mean=terms([(1,features[x][j]) for x in range(512)]+[(-512,((extras[j],1),))])
            rows.append(Row(mean,512,512,dict(kind='singleton_mean',core_mask=mask)))
        else:target=6144
        rows.append(Row(terms(parts),target,target,dict(kind='core_norm_identity',core_mask=mask)))
        rows.append(Row(((negatives[j],4),),0 if j<4 else 1,2 if j<4 else 4,dict(kind='negative_count_range',core_mask=mask)))
    rows.append(Row(tuple((i,1) for i in extras),0,2,dict(kind='singleton_extras_budget')))
    rows.append(Row(tuple((i,4) for i in negatives[:4]),0,2,dict(kind='single_core_negative_budget')))
    rows.append(Row(tuple((i,4) for i in negatives),0,4,dict(kind='total_negative_budget')))
    return variables,rows
