from verify_parent00_joint_pairs import literal_join,map_mask


def test_scalar_join_preserves_known_relation_and_rejects_empty_relation(monkeypatch):
    class Checker:
        def at(self,x):return (0,1,-1)
        def coordinates(self,g):return (5,9,6,10),list(range(10))
    domains=[dict(pair=p,rows=[0] if j<2 else [0,1,2]) for j,p in enumerate((5,9,6,10))]
    monkeypatch.setattr('verify_parent00_joint_pairs.literal_conditioned',lambda *args:{(0,0,0,0),(0,0,1,-1),(0,0,-1,1)})
    assert literal_join(domains,{},[],3,Checker())==[[0,0],[1,2],[2,1]]
    monkeypatch.setattr('verify_parent00_joint_pairs.literal_conditioned',lambda *args:set())
    assert literal_join(domains,{},[],3,Checker())==[]


def test_explicit_coordinate_image_uses_forward_map():
    assert map_mask(3,[1,2,0,3])==6
    assert map_mask(6,[2,0,1,3])==3
