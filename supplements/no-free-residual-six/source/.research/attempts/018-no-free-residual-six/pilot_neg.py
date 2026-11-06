"""Pilot (exploration, not evidence): one derivative with negative quartics.

p = Delta_u f on 13 coordinates, 16p = c + sum_A k_A chi_A + sum_D l_D chi_D,
with p ternary, p(0) = 1, p(e_v) = 0 and ordinary quadratic coefficients
m_A in {0,1} (the empty-pair representative: f = 1 on weights 1 and 2).
Ordinary expansion: m_A = (k_A + L_A)/4, cubic -t_T with t_T = L_T/2
(integer, any sign here), quartic l_D, so p(1_X) = 1 - |X| + sum m - sum t
+ sum l. Coefficient domains are given per run: baseline means k_A in
{-1,0}, l_D in {0,1}, c in {1,2}; departures are fixed explicitly.

  pilot_neg.py SECONDS JSON_SPEC
  spec: {"c": [1,2], "negative": [[[0,1,2,3], -2]], "pairs": {"0,1": [-2]}, "workers": 8}
"""
import itertools
import json
import sys
import time

from ortools.sat.python import cp_model

N = 13


def solve(spec, seconds):
    n = spec.get('n', N)
    V = range(n)
    pairs = [tuple(p) for p in itertools.combinations(V, 2)]
    triples = [tuple(t) for t in itertools.combinations(V, 3)]
    quads = [tuple(q) for q in itertools.combinations(V, 4)]
    fixed_l = {tuple(sorted(q)): v for q, v in spec.get('negative', [])}
    fixed_l.update({tuple(sorted(q)): v for q, v in spec.get('quartics', [])})
    pair_dom = {tuple(sorted(map(int, k.split(',')))): v for k, v in spec.get('pairs', {}).items()}
    if 'explicit' in spec:      # positive control: every coefficient fixed
        ex = spec['explicit']
        spec = dict(spec, c=[ex['constant']])
        pair_dom = {a: [0] for a in pairs}
        pair_dom.update({tuple(p): [v] for p, v in ex['pairs']})
        fixed_l = {q: 0 for q in quads}
        fixed_l.update({tuple(q): v for q, v in ex['quartics']})
    cp = cp_model.CpModel()
    budget = spec.get('budget')
    z = {v: cp.NewBoolVar(f'z{v}') for v in V}       # some departure touches v (budget mode)
    if budget is None:
        c = cp.NewIntVarFromDomain(cp_model.Domain.FromValues(spec.get('c', [1, 2])), 'c')
        l = {q: (fixed_l[q] if q in fixed_l else cp.NewBoolVar(f'l{q}')) for q in quads}
        k = {a: cp.NewIntVarFromDomain(cp_model.Domain.FromValues(pair_dom.get(a, [-1, 0])), f'k{a}') for a in pairs}
    else:
        # incident departures chosen by the solver, each of cost 2, total <= budget
        s0, s3, y = cp.NewBoolVar('s0'), cp.NewBoolVar('s3'), cp.NewBoolVar('y')
        cp.Add(s0 + s3 + y <= 1)
        c = 1 + y - s0 + s3
        cost = [2 * s0, 2 * s3]
        dep_pairs, dep_quads = [], []
        k = {}
        for a in pairs:
            kap, nu, pi = cp.NewBoolVar(''), cp.NewBoolVar(''), cp.NewBoolVar('')
            cp.Add(nu <= kap)
            cp.Add(pi + kap <= 1)
            k[a] = pi - kap - nu
            cost += [2 * nu, 2 * pi]
            dep_pairs.append((a, nu, pi))
            for v in a:
                cp.Add(z[v] >= nu + pi)
        l = {}
        for q in quads:
            if q in fixed_l:
                l[q] = fixed_l[q]
                continue
            lam, dlt = cp.NewBoolVar(''), cp.NewBoolVar('')
            cp.Add(dlt <= lam)
            l[q] = lam + dlt
            cost.append(2 * dlt)
            dep_quads.append((q, dlt))
            for v in q:
                cp.Add(z[v] >= dlt)
        allow = set(spec.get('allow', ['s0', 's3', 'pm', 'pp', 'q2']))
        Qset = set(map(tuple, (sorted(q) for q, _ in spec.get('negative', []))))
        Qv = set().union(*[set(q) for q in Qset]) if Qset else set()
        if 's0' not in allow: cp.Add(s0 == 0)
        if 's3' not in allow: cp.Add(s3 == 0)
        meet = spec.get('meet')          # restrict the departure's intersection size with Q
        for a, nu, pi in dep_pairs:
            ok_meet = meet is None or len(set(a) & Qv) == meet
            if 'pm' not in allow or not ok_meet: cp.Add(nu == 0)
            if 'pp' not in allow or not ok_meet: cp.Add(pi == 0)
        for q, dlt in dep_quads:
            if 'q2' not in allow or not (meet is None or len(set(q) & Qv) == meet): cp.Add(dlt == 0)
        cp.Add(sum(cost) <= budget)
        cp.Add(z[0] == 0)                              # the root is ordinary
    m = {a: cp.NewBoolVar(f'm{a}') for a in pairs}
    t = {T: cp.NewIntVar(-3, 6, f't{T}') for T in triples}
    for a in pairs:
        cp.Add(4 * m[a] == k[a] + sum(l[q] for q in quads if set(a) <= set(q)))
    for T in triples:
        cp.Add(2 * t[T] == sum(l[q] for q in quads if set(T) <= set(q)))
    for v in V:
        cp.Add(sum(k[a] for a in pairs if v in a) + sum(l[q] for q in quads if v in q) == 8)
    cp.Add(c + sum(k.values()) + sum(l.values()) == 16)
    # exploration only: assumed (not yet proved) structure
    if 'root_faces' in spec:      # root 0 with the given link
        faces = {tuple(sorted(f)) for f in spec['root_faces']}
        nb = {x for f in faces for x in f}
        for a in pairs:
            if 0 in a:
                cp.Add(m[a] == int(a[1] in nb))
        for q in quads:
            if q[0] == 0 and not isinstance(l[q], int):
                cp.Add(l[q] == int(q[1:] in faces))
    for v in spec.get('flag', []):
        for a, b, d in itertools.combinations([x for x in V if x != v], 3):
            tri = [t[tuple(sorted((v, x, y)))] for x, y in ((a, b), (b, d), (a, d))]
            cp.Add(sum(tri) - l[tuple(sorted((v, a, b, d)))] <= 2 + (3 * z[v] if budget is not None else 0))
    for size in range(2, n + 1):
        for X in itertools.combinations(V, size):
            xs = set(X)
            e = (-sum(m[a] for a in pairs if set(a) <= xs) + sum(t[T] for T in triples if set(T) <= xs)
                 - sum(l[q] for q in quads if set(q) <= xs))
            cp.Add(e >= -size)
            cp.Add(e <= 2 - size)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = seconds
    s.parameters.num_workers = spec.get('workers', 8)
    t0 = time.time()
    st = s.StatusName(s.Solve(cp))
    return dict(status=st, sec=round(time.time() - t0, 1))


if __name__ == '__main__':
    print(json.dumps(solve(json.loads(sys.argv[2]), float(sys.argv[1]))))
