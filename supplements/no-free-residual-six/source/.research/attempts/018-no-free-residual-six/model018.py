"""Exact row model of one derivative with a negative quartic (lemma L1).

p = Delta_u f on N = 13 coordinates, 16p = c + sum_A k_A chi_A + sum_D l_D chi_D.
Baseline: k_A = -kappa_A in {-1,0}, l_D in {0,1}. Fixed exceptions: pair
numerators given in `exceptions`; quartics with fixed weight w (l_D = w, a
variable fixed to 1 carrying coefficient w); the constant c in [c_lo, c_hi].
Ordinary expansion (as in 017 model.py): m_A = (k_A + L_A)/4 in {0,1},
cubic -t_T with t_T = L_T / 2, quartic l_D, hence the rows

  pair      4 m_A - L_A - k_A = 0
  triple    L_T - 2 t_T = 0
  vertex    K_v + P_v = 8                    (p(e_v) = 0)
  constant  16 - c_hi <= K + L <= 16 - c_lo  (p(0) = 1)
  value     0 <= |X| - sum m + sum t - sum l <= 2, every X with |X| >= 2

where L_S = sum over D containing S of l_D (weights included). t_T is
binary (incidence 0 or 2) except on `int_triples`, where
t_T = b0 + 2 b1 + 4 b2 - 1 in [-1, 6] (names t, t2, t4). Flag rows at
`flag_vertices`: t_vab + t_vbd + t_vad - l_vabd <= 2. Implied rows: the
linear consequences P_v = 2 D_v - 4 and K_v = 12 - 2 D_v.
Rows are (terms, lo, hi, key) over variable indices, as in 014 and 017.
"""
import itertools
import sys

sys.dont_write_bytecode = True
N = 13


def build(exceptions, c_lo, c_hi, weights=(), int_triples=(), flag_vertices=(), implied=True, n=N, degree_cap=None):
    V = range(n)
    pairs = [frozenset(p) for p in itertools.combinations(V, 2)]
    triples = [frozenset(t) for t in itertools.combinations(V, 3)]
    quads = [frozenset(q) for q in itertools.combinations(V, 4)]
    weights = {frozenset(q): w for q, w in dict(weights).items()}
    ints = {frozenset(t) for t in int_triples}
    exc = {frozenset(p): k for p, k in dict(exceptions).items()}
    names = ([('l', q) for q in quads] + [('m', a) for a in pairs] + [('t', t) for t in triples]
             + [('kappa', a) for a in pairs if a not in exc]
             + [(nm, t) for t in sorted(ints, key=sorted) for nm in ('t2', 't4')])
    index = {v: i for i, v in enumerate(names)}
    rows = []

    def emit(acc, const, lo, hi, key):
        terms = sorted((index[nm], co) for nm, co in acc.items() if co)
        rows.append((terms, lo - const, hi - const, key))

    def add(acc, nm, co):
        acc[nm] = acc.get(nm, 0) + co

    def add_l(acc, q, co):
        add(acc, ('l', q), co * weights.get(q, 1))

    def add_k(acc, a, co):
        """Add co * k_a; return the constant part."""
        if a in exc:
            return co * exc[a]
        add(acc, ('kappa', a), -co)
        return 0

    def add_t(acc, T, co):
        """Add co * t_T; return the constant part."""
        add(acc, ('t', T), co)
        if T in ints:
            add(acc, ('t2', T), 2 * co)
            add(acc, ('t4', T), 4 * co)
            return -co
        return 0

    for a in pairs:
        acc = {('m', a): 4}
        for q in quads:
            if a <= q:
                add_l(acc, q, -1)
        const = add_k(acc, a, -1)
        emit(acc, const, 0, 0, ('pair', tuple(sorted(a))))
    for T in triples:
        acc = {}
        for q in quads:
            if T <= q:
                add_l(acc, q, 1)
        const = add_t(acc, T, -2)
        emit(acc, const, 0, 0, ('triple', tuple(sorted(T))))
    for v in V:
        acc, const = {}, 0
        for a in pairs:
            if v in a:
                const += add_k(acc, a, 1)
        for q in quads:
            if v in q:
                add_l(acc, q, 1)
        emit(acc, const, 8, 8, ('vertex', v))
    acc, const = {}, 0
    for a in pairs:
        const += add_k(acc, a, 1)
    for q in quads:
        add_l(acc, q, 1)
    emit(acc, const, 16 - c_hi, 16 - c_lo, ('constant',))
    for size in range(2, n + 1):
        for X in itertools.combinations(V, size):
            xs = frozenset(X)
            acc, const = {}, 0
            for a in pairs:
                if a <= xs:
                    add(acc, ('m', a), -1)
            for T in triples:
                if T <= xs:
                    const += add_t(acc, T, 1)
            for q in quads:
                if q <= xs:
                    add_l(acc, q, -1)
            emit(acc, const, -size, 2 - size, ('value', X))
    for v in sorted(flag_vertices):
        for a, b, d in itertools.combinations([x for x in V if x != v], 3):
            acc, const = {}, 0
            for x, y in ((a, b), (b, d), (a, d)):
                const += add_t(acc, frozenset((v, x, y)), 1)
            add_l(acc, frozenset((v, a, b, d)), -1)
            emit(acc, const, -10 ** 6, 2, ('flag', v, (a, b, d)))
    if degree_cap is not None:                     # (bound, vertices): D_v <= bound
        bound, cap_vertices = degree_cap
        for v in sorted(cap_vertices):
            acc = {('m', a): 1 for a in pairs if v in a}
            emit(acc, 0, -10 ** 6, bound, ('degcap', v))
    if implied:
        for v in V:
            acc = {}
            for q in quads:
                if v in q:
                    add_l(acc, q, 1)
            for a in pairs:
                if v in a:
                    add(acc, ('m', a), -2)
            emit(acc, 0, -4, -4, ('implied_P', v))
            acc, const = {}, 0
            for a in pairs:
                if v in a:
                    const += add_k(acc, a, 1)
                    add(acc, ('m', a), 2)
            emit(acc, const, 12, 12, ('implied_k', v))
    return dict(variables=names, rows=rows)


def root_fixings(root, link_faces, n=N):
    nbrs = set().union(*[set(f) for f in link_faces])
    out = {('m', frozenset((root, v))): int(v in nbrs) for v in range(n) if v != root}
    faces = {frozenset(f) for f in link_faces}
    for f in itertools.combinations([v for v in range(n) if v != root], 3):
        out[('l', frozenset(f) | {root})] = int(frozenset(f) in faces)
    return out


def case_model(case, m):
    """Model and fixings for one cover case at negative magnitude m."""
    Q = frozenset(case['Q'])
    t = case['type']
    exc = {}
    if t in ('pm', 'pp'):
        exc[frozenset(case['pair'])] = -2 if t == 'pm' else 1
    c_lo, c_hi = {'none': (1, 2), 'c0': (0, 0), 'c3': (3, 3)}.get(t, (1, 2))
    special = set(Q) | set(case['pair'])
    flags = [] if case['part'] == 'A' else [v for v in range(1, N) if v not in special]
    # in part B-ord the root is an ordinary vertex of maximum degree (L1.md), so every
    # other ordinary vertex has degree at most the root link's order
    cap = (case['order'], flags) if case['part'] == 'B-ord' else None
    model = build(exc, c_lo, c_hi, weights={Q: -m}, flag_vertices=flags, degree_cap=cap,
                  int_triples=[frozenset(T) for T in itertools.combinations(sorted(Q), 3)])
    fixed = root_fixings(0, case['faces'])
    fixed[('l', Q)] = 1
    return model, fixed
