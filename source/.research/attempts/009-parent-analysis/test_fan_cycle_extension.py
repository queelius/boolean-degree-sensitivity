from itertools import combinations,permutations
import numpy as np
from verify_parent00_cubic_cycles import independent_cycles
from fan_cycle_extension import ResidualCatalog,permute_face_codes


def face_list(vertices):
    return [sum(1<<v for v in t) for t in combinations(vertices,3)]


def test_all_six_vertex_extensions_with_anchor_degree_at_most_five():
    other=list(range(5));anchor=5;local=face_list(other);ambient=face_list(other+[anchor])
    codes=independent_cycles(other,local);catalog=ResidualCatalog(codes,other)
    edge_list=list(combinations(other,2));seen=set()
    for count in range(6):
        for link in combinations(edge_list,count):
            degrees=[sum(v in e for e in link) for v in other]
            if any(d%2 for d in degrees):continue
            w=min((v for v,d in zip(other,degrees) if d),default=None)
            remaining,weights,actual_degrees=catalog.extend(link,w)
            for j,code in enumerate(remaining):
                faces=[q for i,q in enumerate(local) if int(code)>>i&1]
                faces += [(1<<anchor)|(1<<a)|(1<<b) for a,b in link]
                full=sum(1<<ambient.index(q) for q in faces)
                assert full not in seen;seen.add(full)
                assert weights[j]==len(faces)
                assert actual_degrees[j].tolist()==[sum(bool(q>>v&1) for q in faces) for v in other]
                assert all(sum(q&e==e for q in faces)%2==0 for e in [sum(1<<v for v in e) for e in combinations(range(6),2)])
    expected={c for c in independent_cycles(list(range(6)),ambient)
              if sum(bool(q>>anchor&1) and bool(c>>j&1) for j,q in enumerate(ambient))<=5}
    assert seen==expected


def test_every_five_coordinate_permutation_against_literal_face_transport():
    vertices=list(range(5));faces=face_list(vertices);codes=independent_cycles(vertices,faces)
    for image in permutations(vertices):
        actual=permute_face_codes(codes,list(image),vertices)
        expected=[]
        for code in codes:
            moved=[sum(1<<image[v] for v in range(5) if q>>v&1) for j,q in enumerate(faces) if code>>j&1]
            expected.append(sum(1<<faces.index(q) for q in moved))
        assert actual.tolist()==expected
