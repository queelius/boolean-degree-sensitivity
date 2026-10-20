"""Controls catch sign reversal, overflow, lost pairs, and false exclusions."""
import numpy as np
import pytest
import product_signature_join as subject


def test_identical_opposite_and_zero_products_survive():
    a = np.array([[1, 0], [0, 1]], dtype=np.int8)
    b = np.array([[1, 1], [0, 0]], dtype=np.int8)
    weights = np.array([[1, 1], [1, -1]], dtype=np.int8)
    plus = subject.product_signatures(a, b, weights)
    minus = subject.product_signatures(a, -b, weights, product_sign=-1)
    assert plus.tolist() == [[1, 1, 1], [0, 0, 0], [1, 1, -1], [0, 0, 0]]
    assert np.array_equal(plus, minus)
    joined = subject.join_signatures(plus, minus)
    assert joined.left_indices.tolist() == [0, 1, 2, 3]
    assert joined.right_indices.tolist() == [0, 1, 2, 3]
    assert sorted(zip(np.bincount(joined.left_groups), np.bincount(joined.right_groups))) == [(1, 1), (1, 1), (2, 2)]


def test_constant_moment_rejects_opposite_nonzero_products():
    v = np.array([[1, 1]], dtype=np.int16); w = np.ones((1, 2), dtype=np.int16)
    left = subject.product_signatures(v, v, w)
    right = subject.product_signatures(v, v, w, product_sign=-1)
    joined = subject.join_signatures(left, right)
    assert joined.signatures.shape == (0, 2)
    assert len(joined.left_indices) == len(joined.right_indices) == 0


def test_seeded_products_match_python_integer_enumeration_and_join():
    rng = np.random.default_rng(361)
    for _ in range(35):
        a = rng.integers(-2, 3, size=(4, 9), dtype=np.int16)
        b = rng.integers(-2, 3, size=(5, 9), dtype=np.int16)
        weights = rng.choice([-1, 1], size=(3, 9)).astype(np.int16)
        expected = []
        for x in a.tolist():
            for y in b.tolist():
                product = [p*q for p,q in zip(x,y)]
                expected.append([sum(p*p for p in product)]+[-sum(p*w for p,w in zip(product,row)) for row in weights.tolist()])
        actual = subject.product_signatures(a, b, weights, product_sign=-1)
        assert actual.tolist() == expected
        other = actual[rng.permutation(len(actual))[:7]]
        joined = subject.join_signatures(actual, other)
        matches = {(i,j) for i,x in enumerate(expected) for j,y in enumerate(other.tolist()) if x == y}
        reconstructed = {(int(i),int(j)) for i,g in zip(joined.left_indices,joined.left_groups)
                         for j,h in zip(joined.right_indices,joined.right_groups) if g == h}
        assert reconstructed == matches
        # Every real product equality must survive even if the moments collide.
        for i,j in matches: assert np.array_equal(actual[i], other[j])


def test_exact_range_empty_domain_and_invalid_inputs():
    full = np.full((1,256), 2, dtype=np.int8); weights = np.ones((1,256), dtype=np.int8)
    assert subject.product_signatures(full, full, weights).tolist() == [[4096,1024]]
    empty = subject.product_signatures(full[:0], full, weights)
    assert empty.shape == (0,2)
    assert len(subject.join_signatures(empty, empty).left_indices) == 0
    with pytest.raises(ValueError): subject.product_signatures(full.astype(float),full,weights)
    with pytest.raises(ValueError): subject.product_signatures(full,full,weights,product_sign=0)
    with pytest.raises(ValueError): subject.product_signatures(full,full,np.zeros_like(weights))
    with pytest.raises(ValueError): subject.product_signatures(full,full,np.ones((1,255),dtype=int))
    with pytest.raises(ValueError): subject.product_signatures(full*10,full*10,weights)
    with pytest.raises(ValueError): subject.join_signatures(np.ones((1,2),dtype=int),np.ones((1,3),dtype=int))


def test_input_extrema_cannot_wrap_the_precast_bound():
    small = np.ones((1,1),dtype=np.int16)
    for extreme in (np.array([[2**64-1]],dtype=np.uint64),np.array([[-2**63]],dtype=np.int64)):
        with pytest.raises(ValueError): subject.product_signatures(extreme,small,small)
