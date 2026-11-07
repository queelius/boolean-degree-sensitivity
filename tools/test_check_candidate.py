"""Tests for check_candidate.py; run in normal and -O mode:  python -m unittest discover -s tools"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import check_candidate as C  # noqa: E402

# Kushilevitz's function as given by Amano (2010), variables renumbered from 0.
S6 = [(1, 2, 3), (1, 2, 4), (3, 4, 5), (3, 4, 6), (1, 5, 6), (2, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
KUSHILEVITZ = dict(n=6, terms=[dict(vars=[i], coef=1) for i in range(6)]
                   + [dict(vars=[i, j], coef=-1) for i in range(6) for j in range(i + 1, 6)]
                   + [dict(vars=[a - 1, b - 1, c - 1], coef=1) for a, b, c in S6])


def table(n, f):
    return ''.join(str(int(f([(k >> i) & 1 for i in range(n)]))) for k in range(1 << n))


class CheckTests(unittest.TestCase):
    def test_kushilevitz_is_boolean_degree3_full_sensitive_on_boundary(self):
        r = C.check(KUSHILEVITZ)
        self.assertEqual((r['boolean'], r['degree'], r['f_at_origin'], r['origin_sensitivity']), (True, 3, 0, 6))
        self.assertFalse(r['beats_kushilevitz_exponent'])  # 6 = 3**(log 6/log 3) exactly
        self.assertFalse(r['meets_degree5_target'])

    def test_terms_and_truth_table_agree(self):
        vals = C.values_from_terms(6, KUSHILEVITZ['terms'])
        r = C.check(dict(n=6, truth_table=''.join(map(str, vals))))
        self.assertEqual((r['degree'], r['origin_sensitivity']), (3, 6))

    def test_e2_degree2_sensitivity3(self):
        r = C.check(dict(n=3, truth_table=table(3, lambda x: sum(x) in (1, 2))))
        self.assertEqual((r['degree'], r['origin_sensitivity']), (2, 3))
        self.assertFalse(r['beats_kushilevitz_exponent'])  # 3 < 2**1.63 = 3.10

    def test_or14_has_full_degree(self):
        r = C.check(dict(n=14, truth_table=table(14, any)))
        self.assertEqual((r['degree'], r['f_at_origin'], r['origin_sensitivity']), (14, 0, 14))
        self.assertFalse(r['meets_degree5_target'])

    def test_degree_is_exact_after_cancellation(self):
        r = C.check(dict(n=3, terms=[dict(vars=[0, 1, 2], coef=1), dict(vars=[2, 1, 0], coef=-1), dict(vars=[0], coef=1)]))
        self.assertEqual((r['boolean'], r['degree']), (True, 1))

    def test_non_boolean_is_reported(self):
        r = C.check(dict(n=2, terms=[dict(vars=[0], coef=1), dict(vars=[1], coef=1)]))
        self.assertFalse(r['boolean'])
        self.assertEqual((r['first_non_boolean_input'], r['value_there']), ([1, 1], 2))
        self.assertFalse(r['meets_degree5_target'])

    def test_constant_zero(self):
        r = C.check(dict(n=4, terms=[]))
        self.assertEqual((r['degree'], r['origin_sensitivity'], r['beats_kushilevitz_exponent']), (0, 0, False))

    def test_invalid_inputs(self):
        bad = [dict(n=0, terms=[]), dict(n=21, terms=[]), dict(n=True, terms=[]), [1], dict(n=2),
               dict(n=2, terms=[], truth_table='0000'), dict(n=2, terms=[dict(vars=[0, 0], coef=1)]),
               dict(n=2, terms=[dict(vars=[2], coef=1)]), dict(n=2, terms=[dict(vars=[0], coef=True)]),
               dict(n=2, terms=[dict(vars=[0], coef=1.0)]), dict(n=2, terms=[dict(vars=[0], coef=1, x=1)]),
               dict(n=2, truth_table='012'), dict(n=2, truth_table='0102'), dict(n=2, terms=None),
               dict(n=2, terms={}), dict(n=2, terms='x'), dict(n=2, terms=[[0]]), dict(n=2, terms=[dict(vars=0, coef=1)])]
        for c in bad:
            with self.subTest(c=c), self.assertRaises(C.InvalidCandidate):
                C.check(c)

    def test_beats_exponent_boundaries(self):
        cases = {(6, 3): False, (7, 3): True, (36, 9): False, (37, 9): True, (216, 27): False,
                 (14, 5): True, (13, 5): False, (4, 2): True, (3, 2): False, (5, 1): False, (0, 4): False}
        for (s, d), want in cases.items():
            with self.subTest(s=s, d=d):
                self.assertIs(C.beats_exponent(s, d), want)

    def test_cli_exit_codes(self):
        script = os.path.join(os.path.dirname(__file__), 'check_candidate.py')
        with tempfile.TemporaryDirectory() as d:
            good, bad = os.path.join(d, 'k.json'), os.path.join(d, 'bad.json')
            with open(good, 'w') as f:
                json.dump(KUSHILEVITZ, f)
            with open(bad, 'w') as f:
                f.write('{')
            with open(os.path.join(d, 'null.json'), 'w') as f:
                json.dump(dict(n=2, terms=None), f)
            flags = ['-O'] * sys.flags.optimize  # the CLI runs in the same mode as the tests
            run = lambda p: subprocess.run([sys.executable, *flags, script, p], capture_output=True, text=True)
            r = run(good)
            self.assertEqual(r.returncode, 1)
            self.assertEqual(json.loads(r.stdout)['degree'], 3)
            self.assertEqual(run(bad).returncode, 2)
            self.assertEqual(run(os.path.join(d, 'missing.json')).returncode, 2)
            null = run(os.path.join(d, 'null.json'))
            self.assertEqual(null.returncode, 2)
            self.assertIn('terms must be a list', null.stdout)


    def test_main_in_process(self):
        import contextlib, io
        with tempfile.TemporaryDirectory() as d:
            good = os.path.join(d, 'k.json')
            with open(good, 'w') as f:
                json.dump(KUSHILEVITZ, f)
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                self.assertEqual(C.main(['x', good]), 1)
                self.assertEqual(C.main(['x']), 2)
                self.assertEqual(C.main(['x', os.path.join(d, 'missing.json')]), 2)
            self.assertIn('"degree": 3', out.getvalue())
            self.assertIn('Check a candidate', err.getvalue())

if __name__ == '__main__':
    unittest.main()
