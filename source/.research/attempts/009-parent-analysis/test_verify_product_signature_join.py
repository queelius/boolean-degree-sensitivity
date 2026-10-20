"""Controls for independent literal products and exhaustive signature membership."""
from types import SimpleNamespace
import numpy as np
import pytest
import verify_product_signature_join as reader


def test_reader_accepts_literal_opposite_and_zero_products():
    left=np.array([[1,0],[0,1]],dtype=np.int8);right=np.array([[1,1],[0,0]],dtype=np.int8)
    weights=np.array([[1,1],[1,-1]],dtype=np.int8)
    sig=np.array([[1,1,1],[0,0,0],[1,1,-1],[0,0,0]],dtype=np.int16)
    assert reader.verify_products(left,-right,weights,sig,-1)==4
    for position in ((0,0),(0,1),(2,2)):
        bad=sig.copy();bad[position]+=1
        with pytest.raises(AssertionError):reader.verify_products(left,-right,weights,bad,-1)
    with pytest.raises(AssertionError):reader.verify_products(left,right,weights,sig[:2],1)


def test_reader_rejects_missing_signature_or_matching_pair_and_wrong_group():
    left=np.array([[0,0],[1,1],[2,2],[0,0]],dtype=np.int16)
    right=np.array([[1,1],[3,3],[0,0]],dtype=np.int16)
    good=SimpleNamespace(signatures=np.array([[1,1],[0,0]],dtype=np.int16),
                         left_indices=np.array([0,1,3]),right_indices=np.array([0,2]),
                         left_groups=np.array([1,0,1]),right_groups=np.array([0,1]))
    assert reader.verify_join(left,right,good)==2
    for field,value in (('signatures',good.signatures[:1]),('left_indices',np.array([0,1])),
                        ('right_groups',np.array([1,0]))):
        bad=SimpleNamespace(**vars(good));setattr(bad,field,value)
        with pytest.raises(AssertionError):reader.verify_join(left,right,bad)


def test_reader_empty_intersection_and_seeded_join_controls():
    from product_signature_join import product_signatures,join_signatures
    rng=np.random.default_rng(362)
    for _ in range(10):
        a=rng.integers(-2,3,size=(4,7),dtype=np.int8);b=rng.integers(-2,3,size=(3,7),dtype=np.int8)
        weights=rng.choice([-1,1],size=(3,7)).astype(np.int8)
        left=product_signatures(a,b,weights);right=product_signatures(a,-b,weights)
        assert reader.verify_products(a,b,weights,left,1)==12
        joined=join_signatures(left,right)
        assert reader.verify_join(left,right,joined)==len(joined.signatures)
    empty=np.empty((0,2),dtype=np.int16)
    assert reader.verify_join(empty,empty,join_signatures(empty,empty))==0
