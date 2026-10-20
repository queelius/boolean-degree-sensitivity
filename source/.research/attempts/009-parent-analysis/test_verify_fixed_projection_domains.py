import pytest
from verify_fixed_projection_domains import literal_conditioned,FixedProjectionReader


def test_literal_conditioning_has_positive_and_impossible_values():
    pairs=(5,9,6,10)
    assert literal_conditioned(pairs,5,0,3,0)
    assert not literal_conditioned(pairs,5,0,3,1)


def test_scalar_replay_rejects_false_contradiction_and_inexact_trace():
    class ConstantRows:
        def at(self,point):return (0,)
    reader=object.__new__(FixedProjectionReader);reader.checker=ConstantRows();reader.pairs=(5,9,6,10)
    reader.g={'eligible_pairs':[5,9,6,10]};domains=[dict(pair=p,rows=[0]) for p in reader.pairs]
    fixed=dict(status='NECESSARY_FIXED_PROJECTION_CUBE_FIXED_POINT',steps=[],domains=domains)
    assert not reader.replay(domains,[],3,fixed)['excluded']
    impossible=dict(status='EXACT_FIXED_PROJECTION_CUBE_CONTRADICTION',steps=[],contradiction_point=61,projection_value=1)
    assert reader.replay(domains,[(0,1)],3,impossible)['excluded']
    false=dict(impossible,projection_value=0)
    with pytest.raises(AssertionError):reader.replay(domains,[],3,false)
    bad=dict(fixed,steps=[dict(point=61,cuts=[dict(pair=5,remaining_rows=0)])])
    with pytest.raises(AssertionError):reader.replay(domains,[],3,bad)
