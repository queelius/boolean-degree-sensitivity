"""Exact finite-value Parseval lift for a fixed cubic negative pattern and count."""
from baseline_full_truth_model import Row
from unspecified_negative_envelope import Variable,Role
from fixed_cubic_box import build as fixed_box
from generic_parseval_envelope import lift_block


def build(negative,values,linear_count):
    assert linear_count in range(0,11,2) and len(values)==1024 and values[0]==[4]
    local,base_rows=fixed_box(10,negative,values)
    # A virtual core occupies bits0..3, its missing pair is3, and the ten
    # outside coordinates occupy bits4..13. Only this block is modeled.
    base=[Variable(3|(q<<4),Role.CUBIC_NEGATIVE if sign==-1 else Role.QUINTIC_POSITIVE) for q,sign in local]
    base_rows=[Row(r.terms,r.lower,r.upper,dict(kind='core_fourier_envelope',core_mask=3,outside_point=x)) for x,r in enumerate(base_rows)]
    known={3|(q<<4):-2 for q in negative};variables,rows=lift_block(base,base_rows,values,known,15,3,3)
    rows.append(Row(tuple((i,1) for i,(q,sign) in enumerate(local) if sign==-1),linear_count,linear_count,dict(kind='linear_count')))
    positive_count=linear_count+4+2*len(negative)
    rows.append(Row(tuple((i,1) for i,(q,sign) in enumerate(local) if sign==1),positive_count,positive_count,dict(kind='positive_cubic_count')))
    return variables,rows
