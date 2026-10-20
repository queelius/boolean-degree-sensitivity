from verify_variable_cubic_transfers import bound_rhs


def test_raw_bound_substitution_has_correct_count_interval_and_box_signs():
    certificate=dict(terms=[[0,-1,3],[1,1,2],[2,1,4],[3,-1,5]],box_terms=[[0,1,7],[1,-1,9]])
    values={0:[-2,6],1:[3,5]}
    assert bound_rhs(3,certificate,values,2)==12
    assert bound_rhs(3,certificate,values,3)==9
