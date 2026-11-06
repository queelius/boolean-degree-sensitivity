"""Check a candidate for the degree-sensitivity question exactly (Python standard library only).

A candidate is a JSON file in one of two forms:

  {"n": 14, "terms": [{"vars": [0, 3, 7], "coef": 1}, ...]}
      a multilinear polynomial with integer coefficients; repeated monomials are summed.
  {"n": 14, "truth_table": "0110..."}
      2**n characters '0'/'1'; character k is f(x) where x_i is bit i of k.

The checker evaluates the function on all 2**n inputs, recomputes its unique multilinear
representation by the Moebius transform (so the reported degree is exact), and reports:
Boolean values on the cube, exact degree, f(0), the origin sensitivity s(f, 0) = #{i : f(e_i) != f(0)},
and whether the instance meets the d = 5 target (n = 14, degree <= 5, f(0) = 0, f(e_i) = 1 for all i)
and Epoch's exponent condition s(f, 0) > deg(f)**(log 6 / log 3) with deg(f) > 1.

    python tools/check_candidate.py candidate.json

Exit status 0 means the d = 5 target holds; 1 means it does not; 2 means invalid input.
Checks never use assert, so they also run under python -O.
"""
import decimal
import json
import sys

MAX_N = 20


class InvalidCandidate(ValueError):
    pass


def values_from_terms(n, terms):
    coeffs = {}
    for t in terms:
        if not isinstance(t, dict) or set(t) != {'vars', 'coef'}:
            raise InvalidCandidate('each term needs exactly "vars" and "coef"')
        vs, c = t['vars'], t['coef']
        if not isinstance(c, int) or isinstance(c, bool):
            raise InvalidCandidate('coefficients must be integers')
        if not isinstance(vs, list) or any(not isinstance(v, int) or isinstance(v, bool) or not 0 <= v < n for v in vs):
            raise InvalidCandidate(f'variables must be integers in [0, {n})')
        if len(set(vs)) != len(vs):
            raise InvalidCandidate('a monomial repeats a variable (the polynomial must be multilinear)')
        mask = sum(1 << v for v in vs)
        coeffs[mask] = coeffs.get(mask, 0) + c
    vals = [0] * (1 << n)
    for mask, c in coeffs.items():
        vals[mask] += c
    zeta(vals, n)
    return vals


def values_from_table(n, table):
    if not isinstance(table, str) or len(table) != 1 << n or set(table) - {'0', '1'}:
        raise InvalidCandidate(f'truth_table must be a string of {1 << n} characters 0/1')
    return [int(ch) for ch in table]


def zeta(a, n):
    """In place: a[x] <- sum of a[s] over subsets s of x."""
    for i in range(n):
        bit = 1 << i
        for x in range(1 << n):
            if x & bit:
                a[x] += a[x ^ bit]


def moebius(a, n):
    """In place: inverse of zeta, giving multilinear coefficients from cube values."""
    for i in range(n):
        bit = 1 << i
        for x in range(1 << n):
            if x & bit:
                a[x] -= a[x ^ bit]


def beats_exponent(s, d):
    """s > d**(log 6 / log 3) with d > 1, i.e. log s * log 3 > log 6 * log d.

    Floats can misjudge the boundary s = 6**k, d = 3**k (Kushilevitz composition), where the two sides
    are equal. The comparison uses 80-digit decimals, and differences below 1e-60 count as equality
    (not beating); for s, d <= 2**20 any genuine difference is far larger.
    """
    if d <= 1 or s <= 0:
        return False
    with decimal.localcontext() as ctx:
        ctx.prec = 80
        lhs = decimal.Decimal(s).ln() * decimal.Decimal(3).ln()
        rhs = decimal.Decimal(6).ln() * decimal.Decimal(d).ln()
        return lhs - rhs > decimal.Decimal('1e-60')


def check(candidate):
    if not isinstance(candidate, dict):
        raise InvalidCandidate('candidate must be a JSON object')
    n = candidate.get('n')
    if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= MAX_N:
        raise InvalidCandidate(f'n must be an integer in [1, {MAX_N}]')
    if ('terms' in candidate) == ('truth_table' in candidate):
        raise InvalidCandidate('give exactly one of "terms" or "truth_table"')
    vals = (values_from_terms(n, candidate['terms']) if 'terms' in candidate
            else values_from_table(n, candidate['truth_table']))
    bad = next((x for x, v in enumerate(vals) if v not in (0, 1)), None)
    report = dict(n=n, boolean=bad is None)
    if bad is not None:
        report['first_non_boolean_input'] = [(bad >> i) & 1 for i in range(n)]
        report['value_there'] = vals[bad]
        report['meets_degree5_target'] = False
        return report
    coeffs = list(vals)
    moebius(coeffs, n)
    degree = max((bin(x).count('1') for x, c in enumerate(coeffs) if c), default=0)
    f0 = vals[0]
    s0 = sum(vals[1 << i] != f0 for i in range(n))
    report.update(degree=degree, f_at_origin=f0, origin_sensitivity=s0,
                  meets_degree5_target=(n == 14 and degree <= 5 and f0 == 0 and s0 == 14))
    report['beats_kushilevitz_exponent'] = beats_exponent(s0, degree)
    return report


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding='utf-8') as f:
            report = check(json.load(f))
    except (InvalidCandidate, json.JSONDecodeError, OSError) as e:
        print(json.dumps(dict(error=str(e))))
        return 2
    print(json.dumps(report, indent=1))
    return 0 if report['meets_degree5_target'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
