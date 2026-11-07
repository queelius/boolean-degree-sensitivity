"""Independent enumeration of triangulated 2-spheres by vertex splitting.

Shares no code with 006 (inverse-contraction cover), 1414 (filter) or 1424
(reader). Completeness rests on Steinitz-Rademacher: every triangulated
2-sphere with more than four vertices has a contractible edge, so every class
on n vertices is a vertex split of a class on n-1 vertices. Isomorphism is
decided by a pynauty certificate of the 1-skeleton, a complete invariant for
sphere triangulations (Whitney: 3-connected planar graphs embed uniquely).
"""
import itertools
import sys

sys.dont_write_bytecode = True
import pynauty

class AuditError(Exception):
    pass


def require(cond, detail=None):
    """Survives python -O, unlike assert."""
    if not cond:
        raise AuditError(detail)


K4 = frozenset(frozenset(t) for t in itertools.combinations(range(4), 3))


def vertices(faces):
    return sorted(set().union(*faces))


def edges(faces):
    return {frozenset(e) for f in faces for e in itertools.combinations(sorted(f), 2)}


def link_cycle(faces, v):
    """Neighbours of v in cyclic order; raises unless the link is one cycle."""
    nbr = {}
    for f in faces:
        if v in f:
            a, b = sorted(f - {v})
            nbr.setdefault(a, []).append(b)
            nbr.setdefault(b, []).append(a)
    if not nbr or any(len(x) != 2 for x in nbr.values()):
        raise ValueError(f'link of {v} is not a cycle')
    start = min(nbr)
    cyc, prev, cur = [start], None, start
    while True:
        a, b = nbr[cur]
        nxt = a if a != prev else b
        if nxt == start:
            break
        cyc.append(nxt)
        prev, cur = cur, nxt
    if len(cyc) != len(nbr):
        raise ValueError(f'link of {v} is disconnected')
    return cyc


def is_sphere(faces):
    """Closed connected combinatorial surface with Euler characteristic 2."""
    if any(len(f) != 3 for f in faces):
        return False
    vs = vertices(faces)
    try:
        for v in vs:
            link_cycle(faces, v)
    except ValueError:
        return False
    adj = {v: set() for v in vs}
    for e in edges(faces):
        a, b = e
        adj[a].add(b)
        adj[b].add(a)
    seen, stack = {vs[0]}, [vs[0]]
    while stack:
        for w in adj[stack.pop()] - seen:
            seen.add(w)
            stack.append(w)
    return len(seen) == len(vs) and len(vs) - len(edges(faces)) + len(faces) == 2


def splits(faces):
    """Every vertex split: v -> v, w along the link positions i < j."""
    w = max(vertices(faces)) + 1
    for v in vertices(faces):
        cyc = link_cycle(faces, v)
        k = len(cyc)
        star = [frozenset({v, cyc[t], cyc[(t + 1) % k]}) for t in range(k)]
        rest = faces - set(star)
        for i, j in itertools.combinations(range(k), 2):
            # v keeps link faces t = i..j-1, w takes t = j..i-1 (cyclically)
            new = set(rest)
            for t in range(k):
                f = star[t]
                new.add(f if i <= t < j else (f - {v}) | {w})
            new.add(frozenset({v, w, cyc[i]}))
            new.add(frozenset({v, w, cyc[j]}))
            yield frozenset(new)


def certificate(faces):
    vs = vertices(faces)
    idx = {v: k for k, v in enumerate(vs)}
    adj = {k: [] for k in range(len(vs))}
    for a, b in edges(faces):
        adj[idx[a]].append(idx[b])
    return len(vs), pynauty.certificate(pynauty.Graph(len(vs), adjacency_dict=adj))


def enumerate_spheres(nmax):
    """{n: {certificate: faces}} for n = 4..nmax."""
    out = {4: {certificate(K4): K4}}
    for n in range(5, nmax + 1):
        layer = {}
        for faces in out[n - 1].values():
            for g in splits(faces):
                require(is_sphere(g) and len(vertices(g)) == n)
                layer.setdefault(certificate(g), g)
        out[n] = layer
    return out


def from_masks(masks):
    return frozenset(frozenset(i for i in range(m.bit_length()) if m >> i & 1) for m in masks)
