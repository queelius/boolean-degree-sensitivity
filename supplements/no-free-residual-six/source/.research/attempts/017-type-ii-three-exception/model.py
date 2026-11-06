"""Exact row model of a three-exception Type II derivative (PLAN.md step 6).

p on N = 13 coordinates with 16p = c + sum_A k_A chi_A + sum_D l_D chi_D,
l_D in {0,1}, baseline k_A in {-1,0} (k_A = -kappa_A), exceptional k_A
fixed. Writing m_A = (k_A + sum_{D > A} l_D)/4 and t_T = sum_{D > T} l_D / 2,
the ordinary expansion of p has constant (c + sum k + sum l)/16, linear
coefficients -(sum_{A ni v} k_A + sum_{D ni v} l_D)/8, quadratic m_A, cubic
-t_T and quartic l_D. Hence, with the rows

  pair      4 m_A - sum_{D > A} l_D - k_A = 0        (m_A binary: coefficient 0/1)
  triple    sum_{D > T} l_D - 2 t_T = 0              (t_T binary; see below)
  vertex    sum_{A ni v} k_A + sum_{D ni v} l_D = 8  (p(e_v) = 0)
  constant  sum k + sum l = 16 - c                   (p(0) = 1)
  value     0 <= |X| - sum_{A < X} m_A + sum_{T < X} t_T - sum_{D < X} l_D <= 2
            for every X with |X| >= 2               (p(1_X) = 1 - chi in {-1,0,1})

a 0/1 solution is exactly such a derivative. t_T binary encodes triangle
incidence 0 or 2, which VERTEX-TYPES.md Lemma 1 proves outside the triangle
--- shape; `wide_triples` allows incidence 4 on named triples through a
second binary t2_T: sum_{D > T} l_D = 2 (t_T + t2_T) and the cubic
coefficient is -(t_T + t2_T), so t2 has coefficient 1 in the value rows. Optional
fixings (a root link) are unit rows and must be justified by a cover.

The model is a dict: variables (names) and rows (terms, lo, hi, key), the
format of the 014 pipeline.
"""
import itertools
import sys

sys.dont_write_bytecode = True
N = 13


def build(exceptions, c, fixed=(), wide_triples=(), n=N, flag_vertices=(), implied=False, doubled=()):
    """exceptions: {frozenset pair: k}; fixed: iterable of (name, value).

    doubled: quartics with l_D = 2, encoded by a variable fixed to 1 with
    coefficient 2 wherever l_D appears (the caller fixes it).

    flag_vertices: {v: +1 partners of v} for vertices whose link is proved
    near-flag: every 3-cycle of the link that is not a face is the
    neighbourhood of a degree-3 vertex, i.e. of a +1 partner y. Row
    t_vab + t_vbd + t_vad - l_vabd - sum_y l_vyab <= 2 (y not in abd). implied: add the
    linear consequences P_v = 2 D_v - 4 and sum_r k_vr = 12 - 2 D_v (sums of rows).
    """
    verts = range(n)
    pairs = [frozenset(p) for p in itertools.combinations(verts, 2)]
    triples = [frozenset(t) for t in itertools.combinations(verts, 3)]
    quads = [frozenset(q) for q in itertools.combinations(verts, 4)]
    names = ([('l', q) for q in quads] + [('m', a) for a in pairs] + [('t', t) for t in triples]
             + [('kappa', a) for a in pairs if a not in exceptions]
             + [('t2', t) for t in wide_triples])
    index = {v: i for i, v in enumerate(names)}
    rows = []
    doubled = {frozenset(q) for q in doubled}

    def w(q):
        return 2 if q in doubled else 1

    def k_terms(a):
        """k_A as (terms, constant)."""
        return ([], exceptions[a]) if a in exceptions else ([(index[('kappa', a)], -1)], 0)

    for a in pairs:
        kt, kc = k_terms(a)
        terms = [(index[('m', a)], 4)] + [(index[('l', q)], -w(q)) for q in quads if a <= q] + [(v, -c_) for v, c_ in kt]
        rows.append((terms, kc, kc, ('pair', tuple(sorted(a)))))
    for t in triples:
        terms = [(index[('l', q)], w(q)) for q in quads if t <= q] + [(index[('t', t)], -2)]
        if t in wide_triples:
            terms.append((index[('t2', t)], -2))
        rows.append((terms, 0, 0, ('triple', tuple(sorted(t)))))
    const_terms, const = {}, 0
    for v in verts:
        terms, rhs = {}, 8
        for a in pairs:
            if v in a:
                kt, kc = k_terms(a)
                rhs -= kc
                for x, co in kt:
                    terms[x] = terms.get(x, 0) + co
        for q in quads:
            if v in q:
                terms[index[('l', q)]] = w(q)
        rows.append((sorted(terms.items()), rhs, rhs, ('vertex', v)))
    for a in pairs:
        kt, kc = k_terms(a)
        const += kc
        for x, co in kt:
            const_terms[x] = const_terms.get(x, 0) + co
    for q in quads:
        const_terms[index[('l', q)]] = w(q)
    rows.append((sorted(const_terms.items()), 16 - c - const, 16 - c - const, ('constant',)))
    for size in range(2, n + 1):
        for X in itertools.combinations(verts, size):
            xs = frozenset(X)
            terms = ([(index[('m', a)], -1) for a in pairs if a <= xs]
                     + [(index[('t', t)], 1) for t in triples if t <= xs]
                     + [(index[('t2', t)], 1) for t in wide_triples if t <= xs]
                     + [(index[('l', q)], -w(q)) for q in quads if q <= xs])
            rows.append((terms, -size, 2 - size, ('value', X)))
    for v in sorted(dict(flag_vertices)):
        plus = dict(flag_vertices)[v]
        others = [x for x in verts if x != v]
        for a, b, d in itertools.combinations(others, 3):
            tri = [index[('t', frozenset((v, x, y)))] for x, y in ((a, b), (b, d), (a, d))]
            relax = [(index[('l', frozenset((v, y, a, b)))], -1) for y in plus if y not in (a, b, d)]
            rows.append(([(x, 1) for x in tri] + [(index[('l', frozenset((v, a, b, d)))], -1)] + relax,
                         -3 - len(relax), 2, ('flag', v, (a, b, d))))
    if implied:
        for v in verts:
            mt = [(index[('m', a)], -2) for a in pairs if v in a]
            lt = [(index[('l', q)], w(q)) for q in quads if v in q]
            rows.append((lt + mt, -4, -4, ('implied_P', v)))
            kt, kc = [], 0
            for a in pairs:
                if v in a:
                    t_, c_ = k_terms(a)
                    kt += t_
                    kc += c_
            rows.append((kt + [(index[('m', a)], 2) for a in pairs if v in a], 12 - kc, 12 - kc, ('implied_k', v)))
    for name, value in fixed:
        rows.append(([(index[name], 1)], value, value, ('fix',) + tuple(sorted(name[1])) + (name[0],)))
    return dict(variables=names, rows=rows, c=c, exceptions={tuple(sorted(a)): k for a, k in exceptions.items()})


def root_fixings(root, link_faces, n=N):
    """Unit rows fixing everything at the root: its edges and the quartics through it."""
    nbrs = set().union(*link_faces)
    out = [(('m', frozenset((root, v))), int(v in nbrs)) for v in range(n) if v != root]
    faces = {frozenset(f) for f in link_faces}
    for f in itertools.combinations([v for v in range(n) if v != root], 3):
        out.append((('l', frozenset(f) | {root}), int(frozenset(f) in faces)))
    return out


def check(model, values):
    """Indices of rows a 0/1 vector violates."""
    return [i for i, (terms, lo, hi, _) in enumerate(model['rows']) if not lo <= sum(c * values[v] for v, c in terms) <= hi]
