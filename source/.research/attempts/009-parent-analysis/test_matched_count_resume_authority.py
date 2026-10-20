import pytest
from matched_count_resume_authority import validate_previous


def test_supported_prior_instance_types():
    refinement = dict(geometry_index=19, base_authority=dict(path='quota', sha256='q'))
    reference = dict(path='refinement', sha256='r')
    for status, instance in [('INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_SEARCH', refinement['base_authority']),
                             ('INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_COUNT_SEARCH', reference)]:
        previous = dict(status=status, search_status='UNKNOWN', geometry_index=19)
        source = dict(instance_authority=instance, geometry_index=19)
        validate_previous(previous, source, refinement, reference)
        with pytest.raises(AssertionError): validate_previous(previous, dict(source,instance_authority=dict(path='wrong',sha256='r')),refinement,reference)
    with pytest.raises(AssertionError): validate_previous(dict(previous,status='UNVERIFIED'),source,refinement,reference)
    with pytest.raises(AssertionError): validate_previous(dict(previous,search_status='SAT'),source,refinement,reference)


def test_repeated_resumption_preserves_exact_search_tree():
    import numpy as np
    from finite_function_csp import FunctionCSP
    from resume_function_csp import resume_search
    from verify_finite_function_csp import verify_tree
    tables=[np.array([[0,0],[0,1],[1,0],[1,1]])]*2
    relations=[[(0,0),(1,1)]]*2
    solver=FunctionCSP(tables,relations)
    first=solver.search(1)
    second=resume_search(solver,first['tree'],max_new_nodes=1,added_point=1)
    assert verify_tree(tables,relations,second['tree'])=='UNKNOWN'
    third=resume_search(solver,second['tree'],max_new_nodes=20,added_point=1)
    assert verify_tree(tables,relations,third['tree'])==third['status']=='SAT'
