"""Small closed-surface triangulations: brute force and vertex splitting.

Two independent routes to the projective-plane triangulations used by the
vertex-type classification:

- `brute(n, chi)`: every connected closed combinatorial surface on n
  labelled vertices containing the face {0,1,2}, by a closing search that
  always completes the least half-open edge; classes are kept by a
  pynauty certificate of the vertex-face incidence graph, which is a
  complete invariant of a simplicial complex. Practical for n <= 8.
- `by_splits(seeds, nmax)`: closure under vertex splitting (015
  `spheres.splits`, which works at any vertex with a cycle link). For RP2
  it is complete when seeded with the classes at orders 6 and 7, by
  Barnette's theorem (the two irreducible triangulations of RP2 have 6 and
  7 vertices).

The two routes agree at orders 6 to 8 (tests), and the split route gives the
census counts 1, 3, 16, 134 at orders 6 to 9.
"""
import itertools
import sys
from pathlib import Path

import pynauty

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '015-sphere-catalog-audit'))
import spheres  # noqa: E402


class SurfaceError(Exception):
    pass


def require(cond, detail=None):
    if not cond:
        raise SurfaceError(detail)


def euler(faces):
    return len(spheres.vertices(faces)) - len(spheres.edges(faces)) + len(faces)


def is_closed_surface(faces):
    """Connected, every vertex link a single cycle (so every edge in two faces)."""
    vs = spheres.vertices(faces)
    try:
        for v in vs:
            spheres.link_cycle(faces, v)
    except ValueError:
        return False
    adj = {v: set() for v in vs}
    for a, b in spheres.edges(faces):
        adj[a].add(b)
        adj[b].add(a)
    seen, stack = {vs[0]}, [vs[0]]
    while stack:
        for w in adj[stack.pop()] - seen:
            seen.add(w)
            stack.append(w)
    return len(seen) == len(vs)


def certificate(faces):
    vs = spheres.vertices(faces)
    idx = {v: k for k, v in enumerate(vs)}
    fl = sorted(faces, key=sorted)
    n = len(vs)
    adj = {k: [] for k in range(n + len(fl))}
    for j, f in enumerate(fl):
        adj[n + j] = [idx[v] for v in f]
    g = pynauty.Graph(n + len(fl), adjacency_dict=adj,
                      vertex_coloring=[set(range(n)), set(range(n, n + len(fl)))])
    return n, pynauty.certificate(g)


def _ok_partial(faces, v):
    """Link of v so far is a disjoint union of paths, or one cycle using all its edges."""
    nbr = {}
    for f in faces:
        if v in f:
            a, b = sorted(f - {v})
            nbr.setdefault(a, set()).add(b)
            nbr.setdefault(b, set()).add(a)
    if any(len(x) > 2 for x in nbr.values()):
        return False
    seen = set()
    for s in nbr:
        if s in seen:
            continue
        comp, stack = {s}, [s]
        while stack:
            for w in nbr[stack.pop()] - comp:
                comp.add(w)
                stack.append(w)
        seen |= comp
        closed = all(len(nbr[w]) == 2 for w in comp)
        if closed and comp != set(nbr):
            return False
    return True


def brute(n, chi):
    """{certificate: faces} for connected closed surfaces on exactly n vertices with Euler char chi."""
    nfaces = 2 * (3 * n - 3 * chi) // 3
    require(3 * nfaces == 2 * (3 * n - 3 * chi), 'no closed surface with these numbers')
    out = {}

    def count(faces, e):
        return sum(1 for f in faces if e <= f)

    def rec(faces, used):
        if len(faces) > nfaces:
            return
        open_edges = sorted((tuple(sorted(e)) for e in spheres.edges(faces) if count(faces, e) == 1))
        if not open_edges:
            if len(faces) == nfaces and used == n and euler(faces) == chi and is_closed_surface(faces):
                out.setdefault(certificate(faces), faces)
            return
        a, b = open_edges[0]
        # the third vertex is an old vertex or the least unused one (labels are symmetric)
        for c in list(range(used)) + ([used] if used < n else []):
            f = frozenset((a, b, c))
            if c in (a, b) or f in faces:
                continue
            new = faces | {f}
            if any(count(new, frozenset(e)) > 2 for e in itertools.combinations(f, 2)):
                continue
            if all(_ok_partial(new, v) for v in f):
                rec(new, max(used, c + 1))

    rec(frozenset({frozenset((0, 1, 2))}), 3)
    return out


def by_splits(seeds, nmax, chi):
    """{n: {certificate: faces}}: seeds by order, closed under vertex splitting up to nmax."""
    lo = min(seeds)
    out = {lo: dict(seeds[lo])}
    for n in range(lo + 1, nmax + 1):
        layer = dict(seeds.get(n, {}))
        for faces in out[n - 1].values():
            for g in spheres.splits(faces):
                require(is_closed_surface(g) and euler(g) == chi and len(spheres.vertices(g)) == n)
                layer.setdefault(certificate(g), g)
        out[n] = layer
    return out


def rp2(nmax=9):
    """RP2 triangulations on 6..nmax vertices (seeds at 6 and 7 by brute force)."""
    return by_splits({6: brute(6, 1), 7: brute(7, 1)}, nmax, 1)
