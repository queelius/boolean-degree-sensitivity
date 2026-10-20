"""Small exact-row LP relaxations obtained by projecting Boolean core cubes."""
from functools import lru_cache
from itertools import combinations
import numpy as np
from baseline_full_truth_model import Row,Variable,Kind,affine
from two_positive_four_cube_domains import setup


def character_sums(truth):
    values=(1-2*np.asarray(truth,dtype=np.int16)).copy()
    assert values.ndim==2 and values.shape[1]==16
    step=1
    while step<16:
        blocks=values.reshape(len(values),-1,2,step)
        left=blocks[:,:,0,:].copy();right=blocks[:,:,1,:].copy()
        blocks[:,:,0,:]=left+right;blocks[:,:,1,:]=left-right
        step*=2
    return values


@lru_cache(None)
def core_words(pairs):
    words=np.arange(65536,dtype=np.uint32)
    truth=((words[:,None]>>np.arange(16))&1).astype(np.int8)
    valid=np.ones(65536,dtype=bool);ts=[];delta=None
    for pair in pairs:
        i,j=[v for v in range(4) if pair>>v&1];rest=[v for v in range(4) if not pair>>v&1]
        values=[]
        for point in range(4):
            base=sum(1<<v for k,v in enumerate(rest) if point>>k&1)
            values.append(truth[:,base|pair]+truth[:,base]-truth[:,base|(1<<i)]-truth[:,base|(1<<j)])
        this=values[1]-values[0]
        valid&=(values[0]==values[3])&(values[1]==values[2])&(this>=-1)&(this<=1)
        if delta is None:delta=this
        else:valid&=this==delta
        ts.append(values[0])
    return words[valid],truth[valid],delta[valid],np.stack(ts,axis=1)[valid],character_sums(truth[valid])


def envelopes(geometry,domains,cubes):
    assert [d['pair'] for d in domains]==geometry['eligible_pairs']
    pairs,outside=setup(geometry);words,truth,delta,ts,sums=core_words(pairs)
    row_sets=[sum(1<<r for r in d['rows']) for d in domains]
    lower=[];upper=[];retained=[]
    for point in range(1024):
        live=delta==(1,0,0,-1)[point&3]
        partitions=cubes.partitions(point)
        for j,rows in enumerate(row_sets):
            available=[v-2 for v,mask in enumerate(partitions) if mask&rows]
            live&=np.isin(ts[:,j],available)
        for core_point in range(16):
            weight=point.bit_count()+core_point.bit_count()
            if weight in (0,12,13):live&=truth[:,core_point]==0
            elif weight in (1,2,14):live&=truth[:,core_point]==1
        assert np.any(live),'already contradictory Boolean core domain'
        lower.append(np.min(sums[live],axis=0).astype(int).tolist())
        upper.append(np.max(sums[live],axis=0).astype(int).tolist())
        retained.append(int(np.sum(live)))
    return dict(outside=outside,lower=lower,upper=upper,retained_cubes=retained)


def build_projection(geometry,known,envelope,core_mask):
    assert 0<=core_mask<16
    core=geometry['positive_doubles'][0]&geometry['positive_doubles'][1]
    core_vertices=[v for v in range(14) if core>>v&1]
    global_core=sum(1<<v for i,v in enumerate(core_vertices) if core_mask>>i&1)
    outside=envelope['outside'];supports=[]
    for size in range(6-global_core.bit_count()):
        degree=size+global_core.bit_count()
        if degree%2==0:continue
        for vs in combinations(range(10),size):
            local=sum(1<<v for v in vs)
            support=global_core|sum(1<<outside[v] for v in vs)
            supports.append((support,local))
    free=[q for q,_ in supports if q not in known];positions={q:i for i,q in enumerate(free)}
    rows=[]
    for point in range(1024):
        constant=0;terms=[]
        for q,local in supports:
            character=-1 if (local&point).bit_count()%2 else 1
            if q in known:constant+=character*known[q]
            else:
                offset,sign=affine(q.bit_count());constant+=character*offset
                terms.append((positions[q],character*sign))
        rows.append(Row(tuple(terms),envelope['lower'][point][core_mask]-constant,
                        envelope['upper'][point][core_mask]-constant,
                        dict(kind='core_fourier_envelope',core_mask=core_mask,outside_point=point)))
    return free,rows
