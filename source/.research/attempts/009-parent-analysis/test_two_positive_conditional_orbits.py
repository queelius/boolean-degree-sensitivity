from two_positive_conditional_orbits import coordinate_generators, move


def test_generators_preserve_zero_coefficients_and_ordered_marks():
    known={1:1,2:1,4:0};marks=(3,)
    generators=coordinate_generators(known,marks,n=3)
    assert any(p[0]==1 and p[1]==0 for p in generators)
    for p in generators:
        assert sorted(p)==[0,1,2]
        assert {move(q,p):k for q,k in known.items()}==known
        assert tuple(move(m,p) for m in marks)==marks


def test_distinguishing_mark_removes_coordinate_swap():
    generators=coordinate_generators({1:1,2:1,4:0},(1,2),n=3)
    assert all(p==[0,1,2] for p in generators)
