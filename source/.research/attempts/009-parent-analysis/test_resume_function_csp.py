from itertools import product
import random
import numpy as np
from finite_function_csp import FunctionCSP
from verify_finite_function_csp import verify_tree
from resume_function_csp import PriorityPointCSP, resume_search


def test_resume_with_added_constraint_agrees_with_exhaustion():
    rng = random.Random(290); tested = 0
    for _ in range(40):
        tables = [np.array(rng.sample(list(product(range(2), repeat=4)), 4)) for _ in range(3)]
        relations = [set(rng.sample(list(product(range(2), repeat=3)), rng.randrange(2, 9))) for _ in range(4)]
        old = FunctionCSP(tables, relations).search(2)
        if old['status'] == 'SAT': continue
        extended = [np.column_stack((t, np.array([0, 1, 0, 1]))) for t in tables]
        extra = set(rng.sample(list(product(range(2), repeat=3)), rng.randrange(0, 9)))
        all_relations = relations+[extra]
        feasible = [c for c in product(range(4), repeat=3)
                    if all(tuple(int(t[i, x]) for t, i in zip(extended, c)) in all_relations[x] for x in range(5))]
        solver = PriorityPointCSP(extended, all_relations, priority_point=4)
        result = resume_search(solver, old['tree'], max_new_nodes=1000, added_point=4)
        assert verify_tree(extended, all_relations, result['tree']) == result['status'] == ('SAT' if feasible else 'UNSAT')
        assert result['nodes'] <= old['nodes']+result['new_nodes_explored']
        tested += 1
    assert tested >= 20


def test_zero_allowance_preserves_partial_tree_and_empty_added_relation_closes_it():
    tables = [np.array([[0, 1], [1, 0]]), np.array([[0, 0], [1, 1]])]
    relations = [set(product(range(2), repeat=2))]*2
    old = FunctionCSP(tables, relations).search(1)
    result = resume_search(PriorityPointCSP(tables, relations, priority_point=1), old['tree'], max_new_nodes=0)
    assert result['status'] == 'UNKNOWN' and result['tree'] == old['tree']
    extended = [np.column_stack((t, np.zeros(len(t), dtype=int))) for t in tables]
    bad = PriorityPointCSP(extended, relations+[set()], priority_point=2)
    result = resume_search(bad, old['tree'], max_new_nodes=0, added_point=2)
    assert result['status'] == 'UNSAT' and verify_tree(extended, relations+[set()], result['tree']) == 'UNSAT'
