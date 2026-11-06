import itertools, random
import pytest
from pysat.solvers import Cadical153
from encode import CNF


def sat_under(cnf, assumption):
    with Cadical153(bootstrap_with=[c for c in cnf.clauses]) as s:
        if any(len(c) == 0 for c in cnf.clauses):
            return False
        return s.solve(assumptions=assumption)


@pytest.mark.parametrize('seed', range(40))
def test_projection_equals_row(seed):
    r = random.Random(seed)
    n = r.randint(1, 8)
    terms = [(i + 1, r.choice([-3, -2, -1, 1, 2, 3])) for i in range(n)]
    total = sum(abs(c) for _, c in terms)
    lo = r.randint(-total - 1, total + 1); hi = lo + r.randint(-1, 4)
    cnf = CNF(n); cnf.add_row(terms, lo, hi)
    for bits in itertools.product([0, 1], repeat=n):
        s = sum(c * b for (_, c), b in zip(terms, bits))
        want = lo <= s <= hi
        got = sat_under(cnf, [(i + 1) if b else -(i + 1) for i, b in enumerate(bits)])
        assert got == want, (terms, lo, hi, bits)


def test_conjunction_unsat_control():
    # x1 + x2 = 1 and x1 - x2 = 0 has no 0/1 solution; x1 + x2 = 2 makes it sat
    cnf = CNF(2); cnf.add_row([(1, 1), (2, 1)], 1, 1); cnf.add_row([(1, 1), (2, -1)], 0, 0)
    assert not sat_under(cnf, [])
    cnf = CNF(2); cnf.add_row([(1, 1), (2, 1)], 2, 2); cnf.add_row([(1, 1), (2, -1)], 0, 0)
    assert sat_under(cnf, [])


def test_trivial_rows():
    cnf = CNF(2); assert cnf.add_row([(1, 1), (2, 1)], 0, 2) == 0 and cnf.clauses == []
    cnf = CNF(2); cnf.add_row([(1, 1)], 2, 3); assert cnf.clauses == [[]]
