import numpy as np
from types import SimpleNamespace
from parent00_joint_pair_catalogs import joint_pairs


def test_joint_enumeration_rejects_impossible_projection_and_preserves_literal_control(monkeypatch):
    # A small table permits an exact brute-force cross-check of the relational
    # join independently of the large catalog and the projection transform.
    table=np.zeros((3,1024),dtype=np.int8);table[1,:]=1;table[2,:]=-1
    domains=[dict(pair=p,rows=[0] if j<2 else [0,1,2]) for j,p in enumerate((5,9,6,10))]
    g={'positive_doubles':[31,47],'eligible_pairs':[5,9,6,10]}
    monkeypatch.setattr('parent00_joint_pair_catalogs.setup',lambda g:((5,9,6,10),list(range(10))))
    relation=((0,0,0,0),(0,0,1,-1),(0,0,-1,1))
    monkeypatch.setattr('parent00_joint_pair_catalogs.conditioned_relation',lambda *args:relation)
    result=joint_pairs(domains,g,SimpleNamespace(table=table),3,[])
    assert result['pairs_tested']==9 and result['surviving_pairs']==[[0,0],[1,2],[2,1]]
    monkeypatch.setattr('parent00_joint_pair_catalogs.conditioned_relation',lambda *args:())
    bad=joint_pairs(domains,g,SimpleNamespace(table=table),3,[])
    assert not bad['surviving_pairs'] and bad['steps']==[dict(point=0,before=9,after=0)]
