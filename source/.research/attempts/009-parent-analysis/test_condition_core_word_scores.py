import pytest
from condition_core_word_scores import minima_by_feature


def test_complete_unary_filter_preserves_each_marked_value_minimum():
    words=[(0,1),(1,0),(1,1),(2,1)];costs=[4,3,-2,-100]
    assert minima_by_feature(words,costs,{0:{0,1},1:{0,1}},0)=={0:4,1:-2}


def test_fixed_value_and_empty_domains_are_handled_without_representative_loss():
    words=[(0,1),(1,0),(1,1)];costs=[4,3,-2]
    assert minima_by_feature(words,costs,{0:{1},1:{0}},0)=={1:3}
    assert minima_by_feature(words,costs,{0:set()},0)=={}


def test_enlarging_the_word_pool_can_lower_a_conditional_bound():
    assert minima_by_feature([(1,0)],[3],{},0)=={1:3}
    assert minima_by_feature([(1,0),(1,1)],[3,-2],{},0)=={1:-2}


@pytest.mark.parametrize('words,costs,marked', [([(1,)],[],0), ([(1,)],[.5],0), ([(1,)],[0],1)])
def test_malformed_inputs_are_rejected(words,costs,marked):
    with pytest.raises(ValueError):minima_by_feature(words,costs,{},marked)
