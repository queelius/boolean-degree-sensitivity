import pytest
from variable_cubic_energy import build
from verify_variable_cubic_certificate import rebuild,verify


def test_independent_rows_match_small_interval_and_energy_encodings():
    values=[[-4,4] for _ in range(16)];values[0]=[-12,4];values[15]=[-4,12]
    for energy in (False,True):
        variables,rows=build(4,1,values,energy);other,exact=rebuild(4,1,values,energy)
        assert other==[v.metadata() for v in variables]
        assert exact==[(list(r.terms),r.lower,r.upper) for r in rows]


def test_integer_reader_accepts_contradiction_rejects_false_and_tampered_certificates():
    variables=[{}];rows=[([(0,1)],2,2)]
    c=dict(terms=[[0,-1,1]],box_terms=[[0,1,1]],integer_rhs=-1)
    assert verify(variables,rows,c)==-1
    with pytest.raises(AssertionError):verify(variables,[([(0,1)],1,1)],c)
    with pytest.raises(AssertionError):verify(variables,rows,dict(c,integer_rhs=-2))
