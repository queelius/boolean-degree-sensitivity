from itertools import combinations
from cubic_degree_profiles import degree_profiles,low_degree_cycle_bound


def tetra(vertices):return [sum(1<<i for i in t) for t in combinations(vertices,3)]


def degrees(faces,n):return [sum(bool(q>>i&1) for q in faces) for i in range(n)]


def test_tetrahedra_controls_and_high_degree_scope_guard():
    assert not low_degree_cycle_bound(degrees(tetra([0,1,2,3]),4))['excluded']
    disjoint=tetra([0,1,2,3])+tetra([4,5,6,7]);assert not low_degree_cycle_bound(degrees(disjoint,8))['excluded']
    # Two tetrahedral spheres sharing a vertex have chi3 with only eight faces.
    # The shared degree6 vertex makes the degree<=5 theorem inapplicable.
    wedge=tetra([0,1,2,3])+tetra([0,4,5,6]);assert low_degree_cycle_bound(degrees(wedge,7)) is None


def test_parent13_all_profiles_have_chi3_and_too_few_faces():
    values=[[0,8],[0,8],[4],[4],[4],[-4],[-4],[-4],[-4],[-4]];profiles=degree_profiles(10,[13],values)
    assert len(profiles)==25 and {p['linear_count'] for p in profiles}=={4,6}
    assert all(low_degree_cycle_bound(p['degrees'])['excluded'] for p in profiles)
