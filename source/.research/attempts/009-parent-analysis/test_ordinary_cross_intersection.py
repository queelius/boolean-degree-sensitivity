from itertools import combinations
import numpy as np
import pytest
from ordinary_cross_intersection import ordinary_features, cross_relations


def character(mask):
    return np.array([(-1)**((x & mask).bit_count()) for x in range(1024)], dtype=np.int16)


def test_fourier_features_ignore_apex_terms_and_detect_positive_triples():
    masks = [sum(1 << i for i in c) for c in combinations(range(2, 10), 3)]
    values = character(masks[0]) + character(masks[-1]) - 2*character(1+4+8) - character(4)
    triples, features = ordinary_features(values[None, :])
    assert triples == masks
    assert np.flatnonzero(features[0]).tolist() == [0, 55]
    with pytest.raises(AssertionError):
        ordinary_features((-character(masks[0]))[None, :])
    with pytest.raises(AssertionError):
        ordinary_features(np.zeros((1, 8), dtype=np.int8))


def test_cross_relation_forbids_disjoint_faces_but_permits_intersections():
    triples = [7, 56, 11]  # {0,1,2}; {3,4,5}; {0,1,3}
    features = [np.array([[1,0,0],[0,0,1]], dtype=np.int8), np.array([[0,1,0],[0,0,1]], dtype=np.int8)]
    columns, relations, descriptions = cross_relations(features, [3, 12], triples)
    assert len(relations) == 3 and len(descriptions) == 3
    allowed = []
    for i in range(2):
        for j in range(2):
            if all((int(columns[0][i,x]), int(columns[1][j,x])) in set(map(tuple,r)) for x,r in enumerate(relations)):
                allowed.append((i,j))
    assert allowed == [(0,1),(1,0),(1,1)]
    with pytest.raises(AssertionError):
        cross_relations(features, [3, 3], triples)
