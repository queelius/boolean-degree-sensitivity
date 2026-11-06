"""model018 rows against real derivatives (exact evaluation, no solver)."""
import itertools
import json
import unittest
from pathlib import Path

import model018 as M

HERE = Path(__file__).resolve().parent
CONTROLS = json.loads((HERE / 'controls-n13.json').read_text())['controls']


def assignment(ex, n):
    """Model for a real derivative: every non-baseline coefficient an exception or a weight."""
    pairs = {tuple(p): v for p, v in ex['pairs']}
    quads = {tuple(q): v for q, v in ex['quartics']}
    exc = {p: v for p, v in pairs.items() if v not in (-1, 0)}
    weights = {q: v for q, v in quads.items() if v not in (0, 1)}
    L = lambda S: sum(v for q, v in quads.items() if set(S) <= set(q))
    ints = [T for T in itertools.combinations(range(n), 3) if L(T) // 2 not in (0, 1)]
    model = M.build(exc, ex['constant'], ex['constant'], weights=weights, int_triples=ints, n=n)
    val = {}
    for q in itertools.combinations(range(n), 4):
        val[('l', frozenset(q))] = 1 if q in weights else quads.get(q, 0)
    for a in itertools.combinations(range(n), 2):
        k = pairs.get(a, 0)
        val[('m', frozenset(a))] = (k + L(a)) // 4
        if a not in exc:
            val[('kappa', frozenset(a))] = -k
    for T in itertools.combinations(range(n), 3):
        t = L(T) // 2
        if T in ints:
            b = t + 1
            val[('t', frozenset(T))], val[('t2', frozenset(T))], val[('t4', frozenset(T))] = b & 1, b >> 1 & 1, b >> 2 & 1
        else:
            val[('t', frozenset(T))] = t
    x = [val[nm] for nm in model['variables']]
    return model, x


def violated(model, x):
    return [key for terms, lo, hi, key in model['rows'] if not lo <= sum(c * x[v] for v, c in terms) <= hi]


class TestModel018(unittest.TestCase):
    def test_real_derivatives_satisfy_every_row(self):
        for r in CONTROLS:
            model, x = assignment(r['explicit'], 12)
            self.assertEqual(violated(model, x), [], r['witness'])

    def test_perturbed_derivative_fails(self):
        ex = dict(CONTROLS[0]['explicit'])
        ex['constant'] += 1
        model, x = assignment(ex, 12)
        self.assertNotEqual(violated(model, x), [])

    def test_case_model_shapes(self):
        cover = json.loads((HERE / 'l1-cover.json').read_text())['rows']
        case = next(r for r in cover if r['part'] == 'B-exc')
        model, fixed = M.case_model(case, 2)
        names = set(model['variables'])
        self.assertTrue(all(nm in names for nm in fixed))
        self.assertIn(('t4', frozenset(case['Q'][:3])), names)


if __name__ == '__main__':
    unittest.main()
