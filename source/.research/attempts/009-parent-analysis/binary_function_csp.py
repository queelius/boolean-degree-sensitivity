"""Pointwise function search augmented by exact whole-row binary relations."""
import numpy as np
from binary_row_relation import BinaryRelation
from resume_function_csp import PriorityPointCSP


def bit_indices(mask):
    while mask:
        bit=mask & -mask
        yield bit.bit_length()-1
        mask^=bit


class BinaryFunctionCSP(PriorityPointCSP):
    def __init__(self,tables,relations,binary_relations,point_order=None,*,priority_point):
        super().__init__(tables,relations,point_order,priority_point=priority_point)
        self.binary=tuple(binary_relations);self.adjacency=[];self.binary_queries=0;self.binary_deletions=0
        for relation in self.binary:
            i,j=relation.left,relation.right
            assert type(i) is int and type(j) is int and 0<=i<len(tables) and 0<=j<len(tables) and i!=j
            a=relation.allowed
            assert a.ndim==2 and a.shape[1]==2 and np.issubdtype(a.dtype,np.integer)
            assert np.all(a>=0) and np.all(a[:,0]<len(tables[i])) and np.all(a[:,1]<len(tables[j]))
            left=[0]*len(tables[i]);right=[0]*len(tables[j])
            for u,v in a:
                u,v=int(u),int(v);left[u]|=1<<v;right[v]|=1<<u
            self.adjacency.append((left,right))

    def propagate(self,domains):
        domains=list(domains);steps=[]
        if any(not d for d in domains):return tuple(domains),steps,dict(kind='empty')
        while True:
            reduced,point_steps,bad=super().propagate(tuple(domains))
            steps.extend(dict(kind='point',point=x) for x in point_steps);domains=list(reduced)
            if bad is not None:return tuple(domains),steps,dict(kind='point',point=bad)
            changed=False
            for k,(relation,(left,right)) in enumerate(zip(self.binary,self.adjacency)):
                self.binary_queries+=1;i,j=relation.left,relation.right
                old_left,old_right=domains[i],domains[j]
                keep_left=sum(1<<u for u in bit_indices(old_left) if left[u]&old_right)
                keep_right=sum(1<<v for v in bit_indices(old_right) if right[v]&old_left)
                if not keep_left or not keep_right:return tuple(domains),steps,dict(kind='binary',relation=k)
                if (keep_left,keep_right)!=(old_left,old_right):
                    self.binary_deletions+=old_left.bit_count()+old_right.bit_count()-keep_left.bit_count()-keep_right.bit_count()
                    domains[i]=keep_left;domains[j]=keep_right
                    steps.append(dict(kind='binary',relation=k));changed=True
            if not changed:return tuple(domains),steps,None

    def search(self,max_nodes=1000):
        answer=super().search(max_nodes)
        if answer['witness'] is not None:
            witness=answer['witness']
            for relation,(left,_) in zip(self.binary,self.adjacency):
                assert left[witness[relation.left]] & (1<<witness[relation.right])
        answer.update(proof_schema='point_and_binary_v1',binary_queries=self.binary_queries,
                      binary_candidate_deletions=self.binary_deletions,binary_relation_count=len(self.binary))
        return answer
