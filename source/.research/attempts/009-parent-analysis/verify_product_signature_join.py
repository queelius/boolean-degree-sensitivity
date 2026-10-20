"""Independent literal arithmetic and complete set membership verification."""
import numpy as np


def verify_products(left, right, weights, signatures, product_sign):
    assert product_sign in (-1,1)
    assert all(a.ndim == 2 and np.issubdtype(a.dtype,np.integer) for a in (left,right,weights,signatures))
    assert left.shape[1] == right.shape[1] == weights.shape[1]
    assert signatures.shape == (len(left)*len(right),len(weights)+1)
    assert np.all(np.isin(weights,[-1,1]))
    assert all(np.all((a>=-2)&(a<=2)) for a in (left,right))
    assert left.shape[1]*16 < 2**31
    right = right.astype(np.int64)
    for i,row in enumerate(left):
        product = row.astype(np.int64)*right
        actual = signatures[i*len(right):(i+1)*len(right)]
        assert np.array_equal(actual[:,0],np.sum(product*product,axis=1,dtype=np.int64))
        for k,weight in enumerate(weights):
            assert np.array_equal(actual[:,k+1],product_sign*np.sum(product*weight,axis=1,dtype=np.int64))
    return len(left)*len(right)


def verify_join(left, right, joined):
    assert left.ndim == right.ndim == joined.signatures.ndim == 2
    assert left.shape[1] == right.shape[1] == joined.signatures.shape[1]
    assert left.dtype == right.dtype == joined.signatures.dtype == np.dtype('int16')
    # Independent Python sets, not the producer's sorted NumPy row join.
    left_keys = {row.tobytes() for row in left}
    common = set()
    for row in right:
        key = row.tobytes()
        if key in left_keys: common.add(key)
    groups = {row.tobytes():i for i,row in enumerate(joined.signatures)}
    assert len(groups) == len(joined.signatures) and set(groups) == common
    del left_keys
    for values,indices,labels in ((left,joined.left_indices,joined.left_groups),
                                  (right,joined.right_indices,joined.right_groups)):
        expected_indices = []; expected_labels = []
        for i,row in enumerate(values):
            label = groups.get(row.tobytes())
            if label is not None:
                expected_indices.append(i); expected_labels.append(label)
        assert np.array_equal(indices,np.asarray(expected_indices,dtype=np.int64))
        assert np.array_equal(labels,np.asarray(expected_labels,dtype=np.int64))
    return len(groups)
