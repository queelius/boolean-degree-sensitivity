"""Independent complete sum-cover check using Python integers and tuple keys."""
import numpy as np


def verify_sums(left,middle,right,matches):
    assert all(a.ndim==2 and np.issubdtype(a.dtype,np.integer) for a in (left,middle,right))
    assert left.shape[1]==middle.shape[1]==right.shape[1]
    assert matches.ndim==2 and matches.shape[1]==3 and matches.dtype==np.dtype('int64')
    right_rows={}
    for k,row in enumerate(right.tolist()):right_rows.setdefault(tuple(map(int,row)),[]).append(k)
    expected=[];middle_rows=middle.tolist()
    for i,row in enumerate(left.tolist()):
        for j,term in enumerate(middle_rows):
            value=tuple(int(a)+int(c) for a,c in zip(row,term))
            for k in right_rows.get(value,()):expected.append([i,j,k])
    assert matches.tolist()==expected
    return dict(cartesian_pairs_checked=len(left)*len(middle),matching_triples=len(expected))
