"""Disconnected ordinary link: exact cross-degree search per shape (PLAN.md step 4).

At an ordinary w whose link is two six-vertex projective planes on A and B,
every other vertex v lies in A or B, D_v = 6 + cross(v), 0 <= cross(v) <= 6,
and the number of cross edges is M = sum over A of cross = sum over B of
cross = 7 + c. Necessary conditions used (CROSS-EDGES.md):

- an exceptional vertex has D_v in the orders allowed by vertex_types.py
  (for the triangle --- shape, which Lemma 2 does not cover, only D_v >= 8);
- an ordinary vertex has cross >= 1 (cross 0 forces two degree-3 link
  vertices);
- cross 0 only at a vertex of type (0,0,2), with both +1 partners on its
  side;
- cross 1 at a vertex with a sphere link and no +1 partner on its own
  side forces a vertex on the other side with cross 6 (otherwise the disk
  left by w's star has a chord cutting off a degree-3 ear).

The search is exact over side assignments of the exceptional vertices and
over all cross values; it reports the shapes and constants that survive.
"""
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
GRAPHS = {'triangle': [(0, 1), (1, 2), (0, 2)], 'star': [(0, 1), (0, 2), (0, 3)],
          'P4': [(0, 1), (1, 2), (2, 3)], 'P3+K2': [(0, 1), (1, 2), (3, 4)], '3K2': [(0, 1), (2, 3), (4, 5)]}


def allowed_orders():
    doc = json.loads((HERE / 'vertex-types-result.json').read_text())
    return {(r['c6'], r['plus1']): sorted({cf[0][1] for cf in r['component_patterns']})
            for r in doc['rows'] if r['split'] == 0}


def shapes():
    seen, out = set(), []
    for g, edges in GRAPHS.items():
        for signs in itertools.product('-+', repeat=3):
            if g == 'star' and signs == ('+', '+', '+'):
                continue
            verts = sorted({v for e in edges for v in e})
            canon = min(tuple(sorted((s, tuple(sorted((p[a], p[b])))) for (a, b), s in zip(edges, signs)))
                        for p in itertools.permutations(range(6)))
            if canon not in seen:
                seen.add(canon)
                out.append((g, ''.join(signs), edges, signs, verts))
    return out


def cross_options(g, signs, edges, verts, orders):
    """For each exceptional vertex: allowed cross values."""
    signs = tuple(signs)
    out = {}
    for v in verts:
        minus = sum(1 for e, s in zip(edges, signs) if v in e and s == '-')
        plus = sum(1 for e, s in zip(edges, signs) if v in e and s == '+')
        if g == 'triangle' and signs == ('-', '-', '-'):
            vals = range(2, 7)
        else:
            vals = [n - 6 for n in orders.get((minus, plus), []) if 6 <= n <= 12]
        out[v] = (list(vals), (minus, plus))
    return out


def feasible(g, signs, edges, verts, orders, c, universal=True, zero_rule=True):
    M = 7 + c
    signs = tuple(signs)
    opts = cross_options(g, signs, edges, verts, orders)
    for sides in itertools.product((0, 1), repeat=len(verts)):
        side = dict(zip(verts, sides))
        if any(sum(1 for v in verts if side[v] == t) > 6 for t in (0, 1)):
            continue
        for vals in itertools.product(*[opts[v][0] for v in verts]):
            cross = dict(zip(verts, vals))
            # cross 0: type (0,0,2) with both +1 partners on its side
            bad = False
            for v in verts:
                if cross[v] == 0 and zero_rule:
                    partners = [b if a == v else a for (a, b), s in zip(edges, signs) if v in (a, b)]
                    if opts[v][1] != (0, 2) or any(side[r] != side[v] for r in partners):
                        bad = True
            if bad:
                continue
            exc = [[cross[v] for v in verts if side[v] == t] for t in (0, 1)]
            # exceptional cross-1 vertices that force a universal neighbour
            forcing = [False, False]
            for v in verts:
                if cross[v] == 1:
                    plus_same = any(s == '+' and v in e and side[e[0] if e[1] == v else e[1]] == side[v]
                                    for e, s in zip(edges, signs))
                    forcing[side[v]] |= not plus_same
            k = [6 - len(e) for e in exc]
            # ordinary cross values per side: any multiset from 1..6
            choices = [list(itertools.combinations_with_replacement(range(1, 7), k[t])) for t in (0, 1)]
            for oa in choices[0]:
                sa = exc[0] + list(oa)
                if sum(sa) != M:
                    continue
                for ob in choices[1]:
                    sb = exc[1] + list(ob)
                    if sum(sb) != M:
                        continue
                    fa = forcing[0] or 1 in oa
                    fb = forcing[1] or 1 in ob
                    if universal and ((fa and 6 not in sb) or (fb and 6 not in sa)):
                        continue
                    return dict(sides=side, cross=cross, A=sorted(sa), B=sorted(sb))
    return None


def main():
    orders = allowed_orders()
    rows = []
    for g, sg, edges, signs, verts in shapes():
        for c in (1, 2):
            w = feasible(g, sg, edges, verts, orders, c)
            rows.append(dict(graph=g, signs=sg, c=c, survives=w is not None,
                             witness=None if w is None else dict(A=w['A'], B=w['B'])))
    doc = dict(status='STEP4_CROSS_DEGREE_SEARCH', shapes=len(rows) // 2,
               surviving=[(r['graph'], r['signs'], r['c']) for r in rows if r['survives']], rows=rows)
    print(json.dumps(doc, indent=1))
    return doc


if __name__ == '__main__':
    main()
