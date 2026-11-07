"""Case cover for the pair-only shapes (PLAN.md step 5).

A shape is three signed pairs on abstract vertices. Choose a root r of the
shape (the vertex meeting the most exceptions, -2 counted first). Outside
triangle ---, the unit link of r is a sphere L in roots-catalog.json for the
type of r (VERTEX-TYPES.md), with the -2 partners of r exactly its degree-6
vertices and the +1 partners exactly its degree-3 vertices. Label r as 0,
the link vertices 1..|L| as in the catalog and the non-neighbours of r as
|L|+1..12. A case maps every shape vertex to a label:

- r to 0, the partners of r bijectively onto the special vertices of L of
  the right degree;
- every other shape vertex injectively to a non-special link vertex or a
  non-neighbour label.

Cases are reduced only by (a) relabelling non-neighbours, which are
interchangeable (nothing about them is fixed), so new ones take the least
unused label in order of first use; and (b) automorphisms of L, computed by
flag extension and each checked on the full face set; two cases related by an
automorphism (extended by the identity on 0 and the non-neighbours) are the
same up to relabelling, since the model is invariant under relabelling and
the fixings are those of L itself. The kept case is the lexicographically
least image.
"""
import itertools
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
N = 13


class CoverError(Exception):
    pass


def require(cond, detail):
    if not cond:
        raise CoverError(detail)


def automorphisms(faces):
    """All vertex permutations of a closed surface L mapping its face set onto itself.

    An automorphism is fixed by the image of one ordered face: propagate across
    edges (each edge lies in exactly two faces), then verify bijectivity and
    the full face set.
    """
    fs = {frozenset(f) for f in faces}
    vs = sorted(set().union(*fs))
    by_edge = {}
    for f in fs:
        for e in itertools.combinations(sorted(f), 2):
            by_edge.setdefault(frozenset(e), []).append(f)
    require(all(len(x) == 2 for x in by_edge.values()), 'not a closed surface')

    def other(e, f):
        a, b = by_edge[e]
        return b if a == f else a

    f0 = min(fs, key=sorted)
    out = []
    for g in fs:
        for img in itertools.permutations(sorted(g)):
            m = dict(zip(sorted(f0), img))
            queue, done, ok = [(f0, g)], set(), True
            while queue and ok:
                f, h = queue.pop()
                if f in done:
                    continue
                done.add(f)
                for e in itertools.combinations(sorted(f), 2):
                    e = frozenset(e)
                    eh = frozenset(m[v] for v in e)
                    if eh not in by_edge:
                        ok = False
                        break
                    f2, h2 = other(e, f), other(eh, h)
                    (c,) = f2 - e
                    (c2,) = h2 - eh
                    if m.setdefault(c, c2) != c2:
                        ok = False
                        break
                    queue.append((f2, h2))
            if ok and len(m) == len(vs) and len(set(m.values())) == len(vs) \
                    and {frozenset(m[v] for v in f) for f in fs} == fs:
                out.append(m)
    return out


def degrees(faces):
    d = {}
    for f in faces:
        for v in f:
            d[v] = d.get(v, 0) + 1   # faces at v = degree on a closed surface
    return d


def root_of(edges, signs):
    verts = sorted({v for e in edges for v in e})
    score = {v: (sum(1 for e, s in zip(edges, signs) if v in e and s == '-'),
                 sum(1 for e, s in zip(edges, signs) if v in e)) for v in verts}
    return max(verts, key=lambda v: (score[v][1], score[v][0], -v))


def cases(edges, signs, catalog):
    r = root_of(edges, signs)
    minus = [b if a == r else a for (a, b), s in zip(edges, signs) if r in (a, b) and s == '-']
    plus = [b if a == r else a for (a, b), s in zip(edges, signs) if r in (a, b) and s == '+']
    others = sorted({v for e in edges for v in e} - {r} - set(minus) - set(plus))
    out = []
    for li, root in enumerate(catalog[f'{len(minus)},{len(plus)}']):
        faces = [tuple(f) for f in root['faces']]
        order = root['order']
        deg = degrees(faces)
        six = [v for v in sorted(deg) if deg[v] == 6]
        three = [v for v in sorted(deg) if deg[v] == 3]
        plain = [v for v in sorted(deg) if deg[v] in (4, 5)]
        auts = automorphisms(faces)
        require(all({tuple(sorted(a[v] for v in f)) for f in faces} == {tuple(sorted(f)) for f in faces}
                    for a in auts), 'automorphism check')
        seen = set()
        for pm in itertools.permutations(six):
            for pp in itertools.permutations(three):
                base = {r: 0, **dict(zip(minus, pm)), **dict(zip(plus, pp))}
                for targets in itertools.product(plain + ['new'], repeat=len(others)):
                    lab = dict(base)
                    nxt = order + 1
                    ok = True
                    for v, t in zip(others, targets):
                        if t == 'new':
                            if nxt > N - 1:
                                ok = False
                                break
                            lab[v] = nxt
                            nxt += 1
                        else:
                            lab[v] = t
                    if not ok or len(set(lab.values())) != len(lab):
                        continue
                    key = canonical(edges, signs, lab, auts, order)
                    if key not in seen:
                        seen.add(key)
                        out.append(dict(root_index=li, order=order, faces=[list(f) for f in faces],
                                        exceptions=[[list(p), k] for p, k in key]))
    return r, out


def ordinary_cases(edges, signs, deltahedra, anchor):
    """Root at an ordinary neighbour w of the shape vertex `anchor`.

    Used for triangle ---, whose exceptional links may split or pinch. w has
    a sphere link with degrees 4 and 5 (CROSS-EDGES.md), one of the six
    deltahedra; anchor is a link vertex, every other shape vertex a link
    vertex or a non-neighbour.
    """
    verts = sorted({v for e in edges for v in e})
    out = []
    for li, root in enumerate(deltahedra):
        faces = [tuple(f) for f in root['faces']]
        order = root['order']
        auts = automorphisms(faces)
        link = list(range(1, order + 1))
        seen = set()
        for targets in itertools.product(link + ['new'], repeat=len(verts)):
            if targets[verts.index(anchor)] == 'new':
                continue
            lab, nxt, ok = {}, order + 1, True
            for v, t in zip(verts, targets):
                if t == 'new':
                    if nxt > N - 1:
                        ok = False
                        break
                    lab[v] = nxt
                    nxt += 1
                else:
                    lab[v] = t
            if not ok or len(set(lab.values())) != len(lab):
                continue
            key = canonical(edges, signs, lab, auts, order)
            if key not in seen:
                seen.add(key)
                out.append(dict(root_index=li, order=order, faces=[list(f) for f in faces], root_kind='ordinary',
                                exceptions=[[list(p), k] for p, k in key]))
    return out


def canonical(edges, signs, lab, auts, order):
    """Least image of the labelled exception set under Aut(L) and non-neighbour relabelling."""
    best = None
    for a in auts:
        img = {v: (a[x] if 1 <= x <= order else x) for v, x in lab.items()}
        # relabel non-neighbours by first use in the sorted exception list
        exc = sorted((tuple(sorted((img[p], img[q]))), -2 if s == '-' else 1) for (p, q), s in zip(edges, signs))
        ren, nxt = {}, order + 1
        for (p, q), _ in exc:
            for x in (p, q):
                if x > order and x not in ren:
                    ren[x] = nxt
                    nxt += 1
        exc = tuple(sorted((tuple(sorted(ren.get(x, x) for x in pq)), k) for pq, k in exc))
        best = exc if best is None or exc < best else best
    return best


def cover(cat):
    sys.path.insert(0, str(HERE))
    import step4_count
    shapes = []
    for g, sg, edges, signs, verts in step4_count.shapes():
        if g == 'triangle' and sg == '---':
            continue
        r, cs = cases(edges, signs, cat)
        shapes.append(dict(graph=g, signs=sg, edges=[list(e) for e in edges], root=r, cases=cs))
    return dict(status='CASE_COVER', excluded_shapes=['triangle ---', 'doubled-quartic shape 1'], shapes=shapes)


def triangle_cover():
    import step4_count
    deltahedra = json.loads((HERE / 'deltahedra.json').read_text())['spheres']
    g, sg, edges, signs, verts = next(x for x in step4_count.shapes() if x[:2] == ('triangle', '---'))
    cs = ordinary_cases(edges, signs, deltahedra, anchor=verts[0])
    return dict(status='CASE_COVER_ORDINARY_ROOT', shapes=[dict(graph=g, signs=sg, edges=[list(e) for e in edges],
                                                                 root=None, anchor=verts[0], cases=cs)])


def main(out=None):
    cat = json.loads((HERE / 'roots-catalog.json').read_text())['catalog']
    doc = cover(cat)
    if out:
        Path(out).write_text(json.dumps(doc) + '\n')
    summary = [dict(graph=s['graph'], signs=s['signs'], root=s['root'], cases=len(s['cases'])) for s in doc['shapes']]
    print(json.dumps(summary))
    return summary


def shape1_cover():
    """Shape 1: -2 on {0,1} and {2,3}, doubled quartic {0,1,2,3}; root an ordinary neighbour of 0 (SHAPE1.md)."""
    deltahedra = json.loads((HERE / 'deltahedra.json').read_text())['spheres']
    edges, signs = [(0, 1), (2, 3)], ('-', '-')
    cs = ordinary_cases(edges, signs, deltahedra, anchor=0)
    for case in cs:
        (p, _), (q, _) = case['exceptions']
        case['doubled'] = [sorted(set(p) | set(q))]
    return dict(status='CASE_COVER_ORDINARY_ROOT', shapes=[dict(graph='shape1', signs='--Q2', edges=[list(e) for e in edges],
                                                                 root=None, anchor=0, doubled=True, cases=cs)])


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--shape1':
        doc = shape1_cover()
        Path(sys.argv[2]).write_text(json.dumps(doc) + '\n')
        print(json.dumps([len(s['cases']) for s in doc['shapes']]))
    elif len(sys.argv) > 2 and sys.argv[1] == '--triangle':
        sys.path.insert(0, str(HERE))
        doc = triangle_cover()
        Path(sys.argv[2]).write_text(json.dumps(doc) + '\n')
        print(json.dumps([len(s['cases']) for s in doc['shapes']]))
    else:
        main(sys.argv[1] if len(sys.argv) > 1 else None)
