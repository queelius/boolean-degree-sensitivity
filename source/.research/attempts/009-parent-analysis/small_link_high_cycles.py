"""Exact bounded high cycles via an anchor link with at most five edges."""
from itertools import combinations,permutations
import numpy as np


def small_even_links(vertices,maximum):
    assert vertices==sorted(set(vertices)) and 0<=maximum<=5
    yield ()
    for size in range(3,maximum+1):
        for chosen in combinations(vertices,size):
            for tail in permutations(chosen[1:]):
                if tail[0]>tail[-1]:continue
                cycle=(chosen[0],)+tail
                yield tuple(sorted(tuple(sorted((cycle[i],cycle[(i+1)%size]))) for i in range(size)))


def bounded_high_codes(vertices,anchor,maximum,max_faces):
    """Yield (face bitset, face count, degrees), with faces in combination order."""
    assert vertices==sorted(set(vertices)) and 3<=len(vertices)<=8 and anchor in vertices
    assert len(maximum)==len(vertices) and all(type(v) is int and v>=0 for v in maximum)
    anchor_index=vertices.index(anchor);assert maximum[anchor_index]<=5 and max_faces>=0
    faces=list(combinations(vertices,3));lookup={face:i for i,face in enumerate(faces)}
    other=[v for v in vertices if v!=anchor];cone=other[0]
    basis=[sum(1<<lookup[face] for face in combinations((cone,)+t,3)) for t in combinations(other[1:],3)]
    codes=np.array([0],dtype=np.uint64)
    for vector in basis:codes=np.concatenate((codes,codes^np.uint64(vector)))
    byte_counts=np.array([i.bit_count() for i in range(256)],dtype=np.int16)

    def population(array):
        result=np.zeros(len(array),dtype=np.int16)
        for shift in range(0,len(faces),8):result+=byte_counts[((array>>np.uint64(shift))&np.uint64(255)).astype(np.uint8)]
        return result

    weights=population(codes);degree=np.empty((len(vertices),len(codes)),dtype=np.int16)
    for i,v in enumerate(vertices):
        mask=sum(1<<j for j,face in enumerate(faces) if v in face);degree[i]=population(codes&np.uint64(mask))
    for edges in small_even_links(other,maximum[anchor_index]):
        filling=[lookup[tuple(sorted((cone,)+edge))] for edge in edges if cone not in edge]
        star=[lookup[tuple(sorted((anchor,)+edge))] for edge in edges]
        changed=degree.copy();count=weights.copy()
        for j in filling:
            delta=1-2*((codes>>np.uint64(j))&np.uint64(1)).astype(np.int16);count+=delta
            for v in faces[j]:changed[vertices.index(v)]+=delta
        for j in star:
            count+=1
            for v in faces[j]:changed[vertices.index(v)]+=1
        valid=count<=max_faces
        for i,cap in enumerate(maximum):valid &= changed[i]<=cap
        toggle=np.uint64(sum(1<<j for j in filling+star))
        for j in np.flatnonzero(valid):
            yield int(codes[j]^toggle),int(count[j]),[int(d) for d in changed[:,j]]
