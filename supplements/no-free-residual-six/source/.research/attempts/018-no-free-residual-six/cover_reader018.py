"""Independent check of l1-cover.json. Shares no code with cases018.py.

For each part and departure type the lemma needs (B-ord: none, c0, c3 and a
pair inside Q; B-exc: a pair meeting Q in 0 or 1 vertex, rooted at its
endpoint outside Q; A: every type), and each root link of that part, it
enumerates every labelled placement of Q (4 labels in 1..12) and the
departure pair, computes the root link's automorphisms by backtracking on
the face set (components handled separately), and requires each placement to
equal a listed case after some automorphism and some permutation of the
non-neighbour labels. It also checks every listed case is a valid placement
of its part and type, and that the root links are the catalog spheres.
"""
import itertools
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C017 = HERE.parent / '017-type-ii-three-exception'
N = 13
LAB = list(range(1, N))


class CoverError(Exception):
    pass


def need(cond, detail):
    if not cond:
        raise CoverError(detail)


def auts(faces, fixed=()):
    """All permutations of the link vertices preserving the face set (and fixing `fixed`)."""
    fs = {tuple(sorted(f)) for f in faces}
    vs = sorted({x for f in fs for x in f})
    adj = {v: set() for v in vs}
    for f in fs:
        for a, b in itertools.combinations(f, 2):
            adj[a].add(b)
            adj[b].add(a)
    order, left = [], set(vs)
    while left:                                   # BFS order per component
        s = min(left)
        comp, frontier = [s], [s]
        left.discard(s)
        while frontier:
            nxt = sorted(w for v in frontier for w in adj[v] if w in left)
            for w in nxt:
                if w in left:
                    left.discard(w)
                    comp.append(w)
            frontier = nxt
        order += comp
    out = []

    def ext(mp):
        if len(mp) == len(vs):
            if {tuple(sorted(mp[x] for x in f)) for f in fs} == fs:
                out.append(dict(mp))
            return
        v = order[len(mp)]
        for w in vs:
            if w in mp.values() or len(adj[w]) != len(adj[v]) or (v in fixed and w != v):
                continue
            if all((mp[u] in adj[w]) == (u in adj[v]) for u in mp):
                mp[v] = w
                ext(mp)
                del mp[v]

    ext({})
    return out


def placements(part, typ, order, y=None):
    pairs = typ in ('pm', 'pp')
    for Q in itertools.combinations(LAB, 4):
        if part == 'B-exc':
            if (y in Q) == (typ_meet(typ) == 1):
                yield frozenset(Q), frozenset((0, y))
            continue
        if not pairs:
            yield frozenset(Q), frozenset()
            continue
        for P in itertools.combinations(LAB, 2):
            if part == 'B-ord' and not set(P) <= set(Q):
                continue
            yield frozenset(Q), frozenset(P)


def typ_meet(typ):
    return CURRENT_MEET[0]


CURRENT_MEET = [None]


def match(p, have, group, order):
    Q, P = p
    for a in group:
        aQ = [a.get(x, x) for x in Q]
        aP = [a.get(x, x) for x in P]
        fr = sorted({x for x in aQ + aP if x > order})
        for perm in itertools.permutations(range(order + 1, N), len(fr)):
            ren = dict(zip(fr, perm))
            if (frozenset(ren.get(x, x) for x in aQ), frozenset(ren.get(x, x) for x in aP)) in have:
                return True
    return False


def read(cover):
    deltas = json.loads((C017 / 'deltahedra.json').read_text())['spheres']
    cat = json.loads((C017 / 'roots-catalog.json').read_text())['catalog']
    rows = cover['rows']
    listed = {}
    for r in rows:
        need(r['part'] in ('A', 'B-ord', 'B-exc') and r['type'] in ('none', 'c0', 'c3', 'pm', 'pp'), 'part/type')
        Q, P = frozenset(r['Q']), frozenset(r['pair'])
        need(len(Q) == 4 and 0 not in Q and all(1 <= x <= 12 for x in Q), 'Q labels')
        need((len(P) == 2) == (r['type'] in ('pm', 'pp')) and (not P or len(P) == 2), 'pair')
        if r['part'] == 'B-ord':
            need(r['root']['kind'] == 'deltahedron' and deltas[r['root']['index']]['faces'] == r['faces'], 'root')
            need(P <= Q, 'B-ord pair inside Q')
        elif r['part'] == 'B-exc':
            key = '1,0' if r['type'] == 'pm' else '0,1'
            need(r['root']['kind'] == 'catalog-' + key and cat[key][r['root']['index']]['faces'] == r['faces'], 'root')
            need(0 in P and len(P & Q) <= 1, 'B-exc pair')
        else:
            need(r['root']['kind'] == 'rp2-pair' and r['order'] == 12, 'root')
        meet = len(P & Q) if P else None
        listed.setdefault((r['part'], r['type'], r['root']['index'], meet), set()).add((Q, P))
    report = []
    # B-ord
    for i, d in enumerate(deltas):
        need(all(sum(1 for f in d['faces'] if x in f) in (4, 5) for x in range(1, d['order'] + 1)), 'not a deltahedron')
        g = auts(d['faces'])
        for typ in ('none', 'c0', 'c3', 'pm', 'pp'):
            meet = 2 if typ in ('pm', 'pp') else None
            have = listed.get(('B-ord', typ, i, meet), set())
            cnt = 0
            for p in placements('B-ord', typ, d['order']):
                cnt += 1
                need(match(p, have, g, d['order']), f'B-ord {typ} root {i} uncovered')
            report.append(('B-ord', typ, i, cnt, len(have)))
    # B-exc
    for typ, key, deg in (('pm', '1,0', 6), ('pp', '0,1', 3)):
        for i, r in enumerate(cat[key]):
            dg = {x: sum(1 for f in r['faces'] if x in f) for x in range(1, r['order'] + 1)}
            ys = [x for x in dg if dg[x] == deg]
            need(len(ys) == 1 and all(dg[x] in (4, 5) for x in dg if x not in ys), 'catalog sphere degrees')
            y = ys[0]
            g = auts(r['faces'], fixed=(y,))
            for meet in (0, 1):
                CURRENT_MEET[0] = meet
                have = listed.get(('B-exc', typ, i, meet), set())
                cnt = 0
                for p in placements('B-exc', typ, r['order'], y):
                    cnt += 1
                    need(match(p, have, g, r['order']), f'B-exc {typ} root {i} meet {meet} uncovered')
                report.append(('B-exc', typ, i, meet, cnt, len(have)))
    # A
    a_rows = [r for r in rows if r['part'] == 'A']
    need(a_rows, 'no part A cases')
    faces = a_rows[0]['faces']
    need(all(r['faces'] == faces for r in a_rows), 'part A root links differ')
    comps = [sorted({x for f in faces for x in f if x <= 6}), sorted({x for f in faces for x in f if x > 6})]
    need(comps == [list(range(1, 7)), list(range(7, 13))] and len(faces) == 20, 'part A root shape')
    import surfaces  # 017 brute-force closed surfaces: each component must be the six-vertex RP2
    sys.path.insert(0, str(C017))
    for comp in comps:
        sub = [f for f in faces if set(f) <= set(comp)]
        lab = {x: i for i, x in enumerate(comp)}
        need(surfaces.is_closed_surface(frozenset(frozenset(lab[x] for x in f) for f in sub))
             and surfaces.euler(frozenset(frozenset(lab[x] for x in f) for f in sub)) == 1, 'part A component')
    g = auts(faces)
    for typ in ('none', 'c0', 'c3', 'pm', 'pp'):
        for meet in ((None,) if typ in ('none', 'c0', 'c3') else (0, 1, 2)):
            have = listed.get(('A', typ, 0, meet), set())
            cnt = 0
            for Q in itertools.combinations(LAB, 4):
                Ps = [()] if meet is None else [P for P in itertools.combinations(LAB, 2) if len(set(P) & set(Q)) == meet]
                for P in Ps:
                    cnt += 1
                    need(match((frozenset(Q), frozenset(P)), have, g, 12), f'A {typ} meet {meet} uncovered')
            report.append(('A', typ, meet, cnt, len(have)))
    return dict(status='L1_COVER_READER_PASS', cases=len(rows), checks=report)


if __name__ == '__main__':
    sys.path.insert(0, str(C017))
    r = read(json.loads(Path(sys.argv[1]).read_text()))
    print(json.dumps(dict(status=r['status'], cases=r['cases'], groups=len(r['checks']))))
