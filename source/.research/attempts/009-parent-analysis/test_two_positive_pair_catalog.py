from collections import Counter
import pytest

from two_positive_pair_catalog import eligible_pairs, make_row, pair_rows, signed_range


def test_literal_pair_guard():
    # The two positives have common quartet 0,1,2,3. One negative covers
    # exactly the pairs on 0,1,2 within that quartet.
    negatives = [sum(1 << v for v in (0,1,2,6,7))]
    p = sum(1 << v for v in (0,1,2,3,4))
    q = sum(1 << v for v in (0,1,2,3,5))
    assert eligible_pairs(negatives, [p,q]) == [9,10,12]


def test_catalog_has_three_surface_types():
    rows = pair_rows()
    assert [r['surface_order'] for r in rows] == [5,6,8]
    for r in rows:
        assert len(r['linear_numerators']) == 12
        assert r['range']['status'] == 'NECESSARY_RANGE_VALID'
        assert sum(r['range']['value_histogram'].values()) == 4096
        assert (r['double_faces'][0]&r['double_faces'][1]).bit_count() == 2


def test_bipyramid_exact_positive_control():
    # Two cone apices a,b on a triangular rim; the two doubled faces have
    # shared vertices u,v outside the sphere.
    faces = [sum(1<<v for v in (a,c,d)) for a in (0,1)
             for c,d in ((2,3),(2,4),(3,4))]
    row = make_row(5, faces)
    assert row['range']['value_histogram'] == {-8:512,0:3072,8:512}
    assert row['linear_numerators'][:5] == [-1,-1,0,0,0]


def test_corrupted_surface_and_range_are_rejected():
    faces = [13,14,21,22,25,26]
    with pytest.raises(AssertionError):
        make_row(5, faces[:-1])
    row = make_row(5, faces)
    changed = dict(row)
    changed['linear_numerators'] = [0]*12
    assert signed_range(changed)['status'] == 'EXACT_RANGE_CONTRADICTION'


def test_euler_two_does_not_by_itself_make_a_valid_row():
    # A tetrahedron has four degree-three vertices, violating the required
    # two exclusive doubled-tail vertices.
    with pytest.raises(AssertionError):
        make_row(4, [7,11,13,14])
