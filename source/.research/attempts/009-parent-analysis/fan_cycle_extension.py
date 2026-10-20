"""Exact vectorized fan toggles on complete finite catalogs of binary cycles."""
from itertools import combinations
import numpy as np


def permute_face_codes(codes,image,target):
    assert len(image)==len(target) and sorted(image)==target==sorted(set(target))
    local=list(combinations(range(len(image)),3));faces=list(combinations(target,3))
    index={t:j for j,t in enumerate(faces)};source=np.asarray(codes,dtype=np.uint64)
    result=np.zeros(len(source),dtype=np.uint64)
    for j,t in enumerate(local):
        moved=tuple(sorted(image[v] for v in t))
        result |= ((source>>j)&1)<<index[moved]
    return result


class ResidualCatalog:
    def __init__(self,codes,vertices):
        assert vertices==sorted(set(vertices)) and 3<=len(vertices)<=8
        self.vertices=vertices;self.faces=list(combinations(vertices,3))
        self.index={t:j for j,t in enumerate(self.faces)}
        self.codes=np.asarray(codes,dtype='<u8')
        assert all(int(q)<1<<len(self.faces) for q in self.codes)
        self.bits=np.unpackbits(self.codes.view(np.uint8).reshape(-1,8),axis=1,bitorder='little')[:,:len(self.faces)]
        self.weights=self.bits.sum(axis=1,dtype=np.int16)
        self.degrees=np.stack([self.bits[:,[j for j,t in enumerate(self.faces) if v in t]].sum(axis=1,dtype=np.int16)
                               for v in vertices],axis=1)

    def extend(self,link,fan_apex):
        link=list(link);assert len(link)==len(set(link)) and len(link)<=5
        assert all(len(e)==2 and tuple(sorted(e))==tuple(e) and set(e)<=set(self.vertices) for e in link)
        link_degrees=[sum(v in e for e in link) for v in self.vertices]
        assert all(d in (0,2) for d in link_degrees)
        assert (not link and fan_apex is None) or (link and fan_apex in self.vertices and link_degrees[self.vertices.index(fan_apex)]==2)
        filling=[self.index[tuple(sorted((fan_apex,)+tuple(e)))] for e in link if fan_apex not in e]
        toggle=sum(1<<j for j in filling)
        weights=self.weights+len(link)+len(filling)
        if filling:weights=weights-2*self.bits[:,filling].sum(axis=1,dtype=np.int16)
        degrees=self.degrees+np.asarray(link_degrees,dtype=np.int16)
        for i,v in enumerate(self.vertices):
            columns=[j for j in filling if v in self.faces[j]]
            if columns:degrees[:,i]+=len(columns)-2*self.bits[:,columns].sum(axis=1,dtype=np.int16)
        return self.codes^toggle,weights,degrees
