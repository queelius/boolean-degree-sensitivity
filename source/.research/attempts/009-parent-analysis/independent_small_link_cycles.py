"""Independent even-edge-link reconstruction using opposite cones and unpacked bits."""
from itertools import combinations
import numpy as np


def literal_bounded_high_cycles(high,anchor,maximum,max_faces,ambient_triangles):
    assert high==sorted(set(high)) and 3<=len(high)<=8 and anchor in high
    assert len(maximum)==len(high) and all(type(c) is int and c>=0 for c in maximum)
    limit=maximum[high.index(anchor)];assert limit<=5 and max_faces>=0
    faces=list(combinations(high,3));face_index={frozenset(t):j for j,t in enumerate(faces)}
    other=[v for v in high if v!=anchor];cone=other[-1];numbers=[0]
    for triple in combinations(other[:-1],3):
        toggle=sum(1<<face_index[frozenset(t)] for t in combinations(triple+(cone,),3))
        numbers.extend([number^toggle for number in numbers])
    codes=np.asarray(numbers,dtype='<u8');del numbers
    bits=np.unpackbits(codes.view(np.uint8).reshape(-1,8),axis=1,bitorder='little')[:,:len(faces)]
    weights=bits.sum(axis=1,dtype=np.int16)
    incidence=[[j for j,t in enumerate(faces) if v in t] for v in high]
    degrees=[bits[:,columns].sum(axis=1,dtype=np.int16) for columns in incidence]
    global_index={q:i for i,q in enumerate(ambient_triangles)}
    image=[1<<global_index[sum(1<<v for v in t)] for t in faces]
    all_edges=list(combinations(other,2))
    for size in range(limit+1):
        for edges in combinations(all_edges,size):
            if any(sum(v in e for e in edges)%2 for v in other):continue
            filling=[face_index[frozenset((cone,)+edge)] for edge in edges if cone not in edge]
            star=[face_index[frozenset((anchor,)+edge)] for edge in edges]
            overlap=bits[:,filling].sum(axis=1,dtype=np.int16) if filling else 0
            valid=weights+len(filling)+len(star)-2*overlap<=max_faces
            for i,v in enumerate(high):
                columns=[j for j in filling if v in faces[j]]
                shared=bits[:,columns].sum(axis=1,dtype=np.int16) if columns else 0
                added=sum(v in faces[j] for j in filling+star)
                valid &= degrees[i]+added-2*shared<=maximum[i]
            toggle=sum(1<<j for j in filling+star)
            for index in np.flatnonzero(valid):
                local=int(codes[index])^toggle;full=0
                while local:
                    bit=local&-local;full |= image[bit.bit_length()-1];local-=bit
                yield full
