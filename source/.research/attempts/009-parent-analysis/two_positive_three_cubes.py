"""Exact batch test of shared-endpoint pair derivatives on Boolean three-cubes."""
from functools import lru_cache
import numpy as np


def signature(truth):
    assert len(truth)==8 and set(truth)<={0,1}
    return (truth[3]-truth[1]-truth[2]+truth[0],
            truth[7]-truth[5]-truth[6]+truth[4],
            truth[5]-truth[1]-truth[4]+truth[0],
            truth[7]-truth[3]-truth[6]+truth[2])


def encode(values):
    result=0
    for value in values:
        result=result*5+np.asarray(value,dtype=np.int16)+2
    return result


@lru_cache(None)
def allowed_signatures():
    result=np.zeros((12,625),dtype=bool)
    for word in range(256):
        truth=[word>>i&1 for i in range(8)];code=int(encode(signature(truth)))
        for outside in range(12):
            allowed=True
            for point,value in enumerate(truth):
                weight=outside+point.bit_count()
                if weight in (0,12,13) and value!=0:allowed=False
                if weight in (1,2,14) and value!=1:allowed=False
            if allowed:result[outside,code]=True
    return result


def walsh_rows(rows):
    values=np.zeros((len(rows),4096),dtype=np.int16)
    for i,row in enumerate(rows):
        assert not {13,14}&set(row['unit_faces'])
        values[i,row['unit_faces']]=1
        values[i,[1<<v for v in range(12)]]=row['linear_numerators']
        values[i,[13,14]]=2
    step=1
    while step<4096:
        block=values.reshape(len(rows),-1,2,step)
        left=block[:,:,0,:].copy();right=block[:,:,1,:].copy()
        block[:,:,0,:]=left+right;block[:,:,1,:]=left-right
        step*=2
    assert np.all(values%8==0) and np.max(np.abs(values))<=16
    return (-values//8).astype(np.int8)


def coordinates(geometry,pair):
    p,r=geometry['positive_doubles'];u=p&r
    def vs(mask):return [v for v in range(14) if mask>>v&1]
    image=vs(p^u)+vs(r^u)+vs(u^pair)
    image+=sorted(set(range(14))-set(vs(pair))-set(image))
    assert len(image)==len(set(image))==12
    return image


def filter_rows(table,geometry,first_pair,first_row,second_pair,candidates):
    assert (first_pair&second_pair).bit_count()==1 and (first_pair|second_pair).bit_count()==3
    core=first_pair|second_pair
    outside=[v for v in range(14) if not core>>v&1]
    points=np.arange(2048,dtype=np.uint16)
    global_points=np.zeros(2048,dtype=np.uint16)
    for i,v in enumerate(outside):global_points|=((points>>i)&1)<<v
    weights=np.array([int(x).bit_count() for x in points],dtype=np.int8)
    indices=[];opposites=[]
    for pair,other in ((first_pair,second_pair),(second_pair,first_pair)):
        image=coordinates(geometry,pair);projected=np.zeros(2048,dtype=np.uint16)
        for i,v in enumerate(image):projected|=((global_points>>v)&1)<<i
        opposite=(other^pair)&other
        assert opposite.bit_count()==1
        opposites.append(1<<image.index(opposite.bit_length()-1));indices.append(projected)
    selected=np.array(candidates,dtype=np.int32)
    a0=table[first_row,indices[0]];a1=table[first_row,indices[0]|opposites[0]]
    b0=table[selected[:,None],indices[1][None,:]]
    b1=table[selected[:,None],(indices[1]|opposites[1])[None,:]]
    codes=encode((a0[None,:],a1[None,:],b0,b1))
    allowed=allowed_signatures()[weights[None,:],codes]
    passes=np.all(allowed,axis=1);first_bad=np.argmax(~allowed,axis=1)
    rejected=[]
    for i,row_id in enumerate(candidates):
        if passes[i]:continue
        j=int(first_bad[i])
        rejected.append(dict(row=row_id,outside_point=int(global_points[j]),outside_weight=int(weights[j]),
                             pair_values=[[int(a0[j]),int(a1[j])],[int(b0[i,j]),int(b1[i,j])]]))
    return dict(status='COMPLETE_NECESSARY_THREE_CUBE_FILTER',first_pair=first_pair,first_row=first_row,
                second_pair=second_pair,input_rows=list(candidates),rejections=rejected,
                remaining_rows=[row for row,passed in zip(candidates,passes) if passed],
                outside_inputs_per_row=2048)
