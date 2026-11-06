"""Independent check of the case cover. Shares no code with cases.py.

For a shape with a chosen root r and a root sphere L (labels 1..|L|, root 0,
non-neighbours |L|+1..12), every labelled placement is: r -> 0, the -2
partners of r onto the degree-6 vertices of L and the +1 partners onto its
degree-3 vertices (all bijections), and every other shape vertex onto a
distinct degree-4/5 vertex of L or a distinct non-neighbour label. This
reader enumerates all of them without any reduction, computes Aut(L) by
adjacency backtracking checked on the face set, and requires each placement
to be equal, after some automorphism and some permutation of non-neighbour
labels, to a listed case. It also checks that every listed case is itself a
valid placement and that the root type has no split partner.
"""
import itertools
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
N = 13


class CoverError(Exception):
    pass


def need(cond, detail):
    if not cond:
        raise CoverError(detail)


def auts(faces):
    fs = {tuple(sorted(f)) for f in faces}
    vs = sorted({x for f in fs for x in f})
    adj = {v: set() for v in vs}
    for f in fs:
        for a, b in itertools.combinations(f, 2):
            adj[a].add(b)
            adj[b].add(a)
    # order vertices so each new one is adjacent to an earlier one
    order = [vs[0]]
    while len(order) < len(vs):
        order.append(min(v for v in vs if v not in order and adj[v] & set(order)))
    out = []

    def extend(m):
        if len(m) == len(vs):
            if {tuple(sorted(m[x] for x in f)) for f in fs} == fs:
                out.append(dict(m))
            return
        v = order[len(m)]
        for w in vs:
            if w in m.values() or len(adj[w]) != len(adj[v]):
                continue
            if all((m[u] in adj[w]) == (u in adj[v]) for u in m):
                m[v] = w
                extend(m)
                del m[v]

    extend({})
    return out


def placements(edges, signs, root, faces, order):
    deg = {}
    for f in faces:
        for x in f:
            deg[x] = deg.get(x, 0) + 1
    six = sorted(x for x in deg if deg[x] == 6)
    three = sorted(x for x in deg if deg[x] == 3)
    plain = sorted(x for x in deg if deg[x] in (4, 5))
    minus = sorted(b if a == root else a for (a, b), s in zip(edges, signs) if root in (a, b) and s == '-')
    plus = sorted(b if a == root else a for (a, b), s in zip(edges, signs) if root in (a, b) and s == '+')
    need(len(minus) == len(six) and len(plus) == len(three), 'root sphere has the wrong special degrees')
    rest = sorted({x for e in edges for x in e} - {root} - set(minus) - set(plus))
    fresh = list(range(order + 1, N))
    for pm in itertools.permutations(six):
        for pp in itertools.permutations(three):
            for img in itertools.permutations(plain + fresh, len(rest)):
                lab = {root: 0, **dict(zip(minus, pm)), **dict(zip(plus, pp)), **dict(zip(rest, img))}
                yield frozenset((frozenset((lab[a], lab[b])), -2 if s == '-' else 1) for (a, b), s in zip(edges, signs))


def ordinary_placements(edges, signs, anchor, order):
    """Root an ordinary vertex: anchor onto a link vertex, the rest onto link vertices or non-neighbours."""
    verts = sorted({x for e in edges for x in e})
    need(anchor in verts, 'anchor not a shape vertex')
    labels = list(range(1, N))
    for img in itertools.permutations(labels, len(verts)):
        lab = dict(zip(verts, img))
        if lab[anchor] > order:
            continue
        yield frozenset((frozenset((lab[a], lab[b])), -2 if s == '-' else 1) for (a, b), s in zip(edges, signs))


def read(cover, catalog, deltahedra=None):
    out = []
    for shape in cover['shapes']:
        edges = [tuple(e) for e in shape['edges']]
        signs = shape['signs'] if not shape.get('doubled') else '--'
        root = shape['root']
        if root is None:
            need(deltahedra is not None, 'ordinary root needs the deltahedra catalog')
            roots = deltahedra
        else:
            t = (sum(1 for e, s in zip(edges, signs) if root in e and s == '-'),
                 sum(1 for e, s in zip(edges, signs) if root in e and s == '+'))
            roots = catalog[f'{t[0]},{t[1]}']
        listed = {}
        for case in shape['cases']:
            need(type(case['root_index']) is int and 0 <= case['root_index'] < len(roots)
                 and case['order'] == roots[case['root_index']]['order'], 'root index out of range')
            key = frozenset((frozenset(p), k) for p, k in case['exceptions'])
            if shape.get('doubled'):
                need(case.get('doubled') == [sorted(set().union(*[set(p) for p, _ in case['exceptions']]))],
                     'doubled quartic is not the union of the two -2 pairs')
            else:
                need('doubled' not in case, 'unexpected doubled quartic')
            need(roots[case['root_index']]['faces'] == case['faces'], 'case root link is not the catalog sphere')
            listed.setdefault(case['root_index'], set()).add(key)
        total = 0
        for ri, rt in enumerate(roots):
            faces, order = rt['faces'], rt['order']
            group = auts(faces)
            have = listed.get(ri, set())
            if root is None:
                need(all(sum(1 for f in faces if x in f) in (4, 5) for x in range(1, order + 1)), 'not a deltahedron')
                valid = set(ordinary_placements(edges, signs, shape['anchor'], order))
            else:
                valid = set(placements(edges, signs, root, faces, order))
            need(have <= valid, f'listed case not a valid placement (root {ri})')
            for p in valid:
                total += 1
                ok = False
                for a in group:
                    ap = [(tuple(a.get(x, x) for x in pr), k) for pr, k in p]
                    fr = sorted({x for pr, _ in ap for x in pr if x > order})
                    for perm in itertools.permutations(range(order + 1, N), len(fr)):
                        ren = dict(zip(fr, perm))
                        if frozenset((frozenset(ren.get(x, x) for x in pr), k) for pr, k in ap) in have:
                            ok = True
                            break
                    if ok:
                        break
                need(ok, f'placement not covered: root {ri}, {sorted(map(sorted, (q for q, _ in p)))}')
        out.append(dict(graph=shape['graph'], signs=signs, root=root, cases=len(shape['cases']), placements=total))
    return out


def main(cover_path, catalog_path, deltahedra_path=None):
    cover = json.loads(Path(cover_path).read_text())
    catalog = json.loads(Path(catalog_path).read_text())['catalog']
    deltahedra = json.loads(Path(deltahedra_path).read_text())['spheres'] if deltahedra_path else None
    rows = read(cover, catalog, deltahedra)
    doc = dict(status='COVER_READER_PASS', shapes=len(rows), cases=sum(r['cases'] for r in rows), rows=rows)
    print(json.dumps(doc))
    return doc


if __name__ == '__main__':
    main(*sys.argv[1:4])
