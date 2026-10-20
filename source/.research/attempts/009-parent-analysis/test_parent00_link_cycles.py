from itertools import combinations
from parent00_link_cycles import restore_link


def even_pairs(faces):
    vertices=sorted({i for q in faces for i in range(q.bit_length()) if q>>i&1})
    return all(sum(q&edge==edge for q in faces)%2==0 for edge in (sum(1<<i for i in e) for e in combinations(vertices,2)))


def test_restoring_link_retains_tetrahedron_and_stellar_cases():
    tetra=restore_link(set(),7,3)
    assert tetra=={7,11,13,14} and even_pairs(tetra)
    stellar=restore_link(tetra,7,4)
    assert stellar=={11,13,14,19,21,22} and even_pairs(stellar)
    assert len(stellar)==len(tetra)+2
    assert restore_link({7,11,13,14},56,6)=={7,11,13,14,56,88,104,112}


def test_forced_link_peeling_recovers_genuine_projection():
    positive={11,14,25,35,49,70,76,88,98,112};center=2
    link=[q^(1<<center) for q in positive if q>>center&1]
    assert len(link)==3
    face=0
    for edge in link:face|=edge
    base=positive^({face}|{q|(1<<center) for q in link})
    assert not any(q>>center&1 for q in base) and even_pairs(base)
    assert restore_link(base,face,center)==positive
