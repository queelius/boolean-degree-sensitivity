"""Case cover for the one-incident-departure lemma (L1) at a delta = 1 coordinate.

A derivative p = Delta_u f on 13 coordinates with one negative quartic Q
(l_Q = -m, m in {1,2}) and at most one incident cost-2 departure:
none (constant in {1,2}); constant 0; constant 3; or a pair numerator -2 or
+1 (constant in {1,2}). (+2 quartic departures are excluded by the private
-vertex lemma, NOTES.md.) Ordinary vertex: outside Q and the departure pair.

Parts (root always labelled 0, never in Q):
  B-ord  all ordinary links are spheres; root an ordinary vertex, link a
         deltahedron (1..n), non-neighbours n+1..12. Types: none, c0, c3,
         and pairs inside Q.
  B-exc  all ordinary links are spheres; the pair has an endpoint x outside
         Q; root x, link the type (1,0) sphere (-2) or the type (0,1) sphere
         (+1) from the 017 catalog, partner y its degree-6 or degree-3 vertex.
         Types: pairs meeting Q in 0 or 1 vertex (y in Q or not).
  A      some ordinary vertex has a disconnected link: root there, link two
         six-vertex projective planes on 1..6 and 7..12. Every type.
Reductions: automorphisms of the root link fixing the special structure, and
relabelling of non-neighbours; each orbit is generated explicitly and its
least member kept. Soundness does not rest on that exactness:
cover_reader018.py checks only that every labelled placement is matched by
a listed case, so a redundant listing is harmless.
"""
import itertools
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C017 = HERE.parent / '017-type-ii-three-exception'
sys.path.insert(0, str(C017))
import cases as c017  # noqa: E402

N = 13
LABELS = list(range(1, N))


def deltahedra():
    return json.loads((C017 / 'deltahedra.json').read_text())['spheres']


def rp2_pair():
    import surfaces
    (rp,) = surfaces.brute(6, 1).values()
    rp = sorted(sorted(f) for f in rp)
    return rp, [[x + 1 for x in f] for f in rp] + [[x + 7 for x in f] for f in rp]


def auts_rp2_pair(rp):
    one = c017.automorphisms([[x + 1 for x in f] for f in rp])
    out = []
    for a, b in itertools.product(one, one):
        mp = {**a, **{x + 6: b[x] + 6 for x in b}}
        out.append(mp)
        out.append({x: (mp[x] + 6 if mp[x] <= 6 else mp[x] - 6) for x in mp})
    return out


def normal(Q, P, order):
    """Relabel non-neighbours (> order) by first use in (sorted Q, sorted P)."""
    ren, nxt = {}, order + 1
    for x in sorted(Q) + sorted(P):
        if x > order and x not in ren:
            ren[x] = nxt
            nxt += 1
    return tuple(sorted(ren.get(x, x) for x in Q)), tuple(sorted(ren.get(x, x) for x in P))


def orbits(placements, auts, order):
    """Least member of each orbit; every orbit generated explicitly."""
    seen, reps = set(), []
    for Q, P in placements:
        key = normal(Q, P, order)
        if key in seen:
            continue
        orbit = {normal([a.get(x, x) for x in key[0]], [a.get(x, x) for x in key[1]], order) for a in auts}
        seen |= orbit
        reps.append(min(orbit))
    return sorted(reps)


def placements_B_ord(order, meet):
    for Q in itertools.combinations(LABELS, 4):
        if meet is None:
            yield Q, ()
        else:
            for P in itertools.combinations(Q, 2):
                yield Q, P


def cover():
    rows = []
    for li, d in enumerate(deltahedra()):
        auts = c017.automorphisms(d['faces'])
        for t, meet in (('none', None), ('c0', None), ('c3', None), ('pm', 2), ('pp', 2)):
            for Q, P in orbits(list(placements_B_ord(d['order'], meet)), auts, d['order']):
                rows.append(dict(part='B-ord', root=dict(kind='deltahedron', index=li), order=d['order'],
                                 faces=d['faces'], type=t, Q=list(Q), pair=list(P)))
    cat = json.loads((C017 / 'roots-catalog.json').read_text())['catalog']
    for t, key, deg in (('pm', '1,0', 6), ('pp', '0,1', 3)):
        for li, r in enumerate(cat[key]):
            faces, order = r['faces'], r['order']
            dg = c017.degrees(faces)
            (y,) = [v for v in dg if dg[v] == deg]
            auts = [a for a in c017.automorphisms(faces) if a[y] == y]
            for meet in (0, 1):
                pl = [(Q, ()) for Q in itertools.combinations(LABELS, 4) if (y in Q) == (meet == 1)]
                for Q, _ in orbits(pl, auts, order):
                    rows.append(dict(part='B-exc', root=dict(kind='catalog-' + key, index=li), order=order,
                                     faces=faces, type=t, Q=list(Q), pair=[0, y]))
    rp, faces = rp2_pair()
    auts = auts_rp2_pair(rp)
    for t, meet in (('none', None), ('c0', None), ('c3', None)) + tuple((k, j) for k in ('pm', 'pp') for j in (0, 1, 2)):
        pl = []
        for Q in itertools.combinations(LABELS, 4):
            if meet is None:
                pl.append((Q, ()))
                continue
            for P in itertools.combinations(LABELS, 2):
                if len(set(P) & set(Q)) == meet:
                    pl.append((Q, P))
        for Q, P in orbits(pl, auts, 12):
            rows.append(dict(part='A', root=dict(kind='rp2-pair', index=0), order=12, faces=faces, type=t,
                             Q=list(Q), pair=list(P)))
    return dict(status='L1_CASE_COVER', rows=rows)


def main(out):
    doc = cover()
    Path(out).write_text(json.dumps(doc) + '\n')
    from collections import Counter
    print(json.dumps(Counter((r['part'], r['type']) for r in doc['rows']).most_common()), len(doc['rows']))


if __name__ == '__main__':
    main(sys.argv[1])
