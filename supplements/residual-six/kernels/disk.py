# Original code copyright(c)2026 Alexander Richard Towell; MIT.
"""Pure mathematical functions adapted from heptagon_disk_controls_cycle1399.py; original source and AST equality are bundled."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import comb

def need(ok, message):
    if not ok:
        raise ValueError(message)

def inverse(p):
    need(type(p) is list and all((type(x) is int for x in p)) and (sorted(p) == list(range(len(p)))), 'Exact coordinate bijection required.')
    q = [0] * len(p)
    for old, new in enumerate(p):
        q[new] = old
    return q

def transport(F, p):
    inverse(p)
    n = len(p)
    need(type(F) is list and all((type(f) is int and 0 < f < 1 << n for f in F)) and (len(F) == len(set(F))), 'Distinct native faces required.')
    return sorted((sum((1 << p[v] for v in range(n) if f >> v & 1)) for f in F))

def mask(vertices):
    return sum((1 << v for v in vertices))

def fan(boundary, center):
    return sorted((mask((center, boundary[i], boundary[(i + 1) % len(boundary)])) for i in range(len(boundary))))

def connected(adjacency):
    seen = set()
    pending = [next(iter(adjacency))]
    while pending:
        x = pending.pop()
        if x not in seen:
            seen.add(x)
            pending.extend(adjacency[x] - seen)
    return seen == set(adjacency)

def profile(boundary, interior, faces):
    need(type(boundary) is list and type(interior) is list and (len(boundary) >= 3) and all((type(v) is int for v in boundary + interior)), 'Typed coordinate partition required.')
    n = len(boundary) + len(interior)
    need(sorted(boundary + interior) == list(range(n)), 'Coordinates must be distinct and complete.')
    need(type(faces) is list and all((type(f) is int and 0 < f < 1 << n and (f.bit_count() == 3) for f in faces)) and (len(faces) == len(set(faces))), 'Literal distinct triangular faces required.')
    triples = [tuple((v for v in range(n) if f >> v & 1)) for f in faces]
    edges = Counter((tuple(e) for t in triples for e in combinations(t, 2)))
    B = {tuple(sorted((boundary[i], boundary[(i + 1) % len(boundary)]))) for i in range(len(boundary))}
    need(set(edges.values()) <= {1, 2} and {e for e, k in edges.items() if k == 1} == B, 'Boundary or edge incidence mismatch.')
    adjacency = {v: set() for v in range(n)}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    need(connected(adjacency), 'Disconnected whole surface.')
    degrees = [sum((v in e for e in edges)) for v in range(n)]
    for v in range(n):
        link = [tuple((w for w in t if w != v)) for t in triples if v in t]
        adj = {w: set() for e in link for w in e}
        need(bool(adj), 'Inactive coordinate.')
        for a, b in link:
            adj[a].add(b)
            adj[b].add(a)
        ds = Counter(map(len, adj.values()))
        need(connected(adj), 'Disconnected vertex link.')
        need(ds == Counter({2: len(adj)}) if v in interior else ds[1] == 2 and ds[1] + ds[2] == len(adj), 'Wrong cycle/path vertex link.')
    need(n - len(edges) + len(faces) == 1, 'Wrong disk Euler characteristic.')
    bd = [degrees[v] for v in boundary]
    idg = [degrees[v] for v in interior]
    return {'boundary': boundary, 'interior': interior, 'faces': sorted(faces), 'vertices': n, 'edges': len(edges), 'triangles': len(faces), 'Euler': 1, 'boundary_degrees': bd, 'interior_degrees': idg, 'all_target_guards': len(boundary) == 7 and all((x in (3, 4) for x in bd)) and all((x in (4, 5) for x in idg)), 'disk_validity_scope': 'Connected compact triangular surface with one boundary cycle and chi1; hence a disk.'}

def require_target_guards(r):
    need(r['all_target_guards'] is True, 'Valid disk does not satisfy the stated degree hypotheses.')

@lru_cache(None)
def triangulations(poly):
    if len(poly) < 3:
        return ((),)
    out = []
    for k in range(1, len(poly) - 1):
        t = mask((poly[0], poly[k], poly[-1]))
        for left in triangulations(poly[:k + 1]):
            for right in triangulations(poly[k:]):
                out.append(tuple(sorted((t,) + left + right)))
    need(len(out) == len(set(out)), 'Repeated rooted polygon triangulation.')
    return tuple(out)

def ear_controls():
    counts = {}
    checks = 0
    for n in range(3, 8):
        T = triangulations(tuple(range(n)))
        need(len(T) == comb(2 * (n - 2), n - 2) // (n - 1), 'Polygon Catalan count mismatch.')
        counts[str(n)] = len(T)
        for F in T:
            p = profile(list(range(n)), [], list(F))
            ears = {i for i, d in enumerate(p['boundary_degrees']) if d == 2}
            need(len(ears) >= 2, 'Polygon lacks two ears.')
            for i in range(n):
                need(bool(ears - {i, (i + 1) % n}), 'No ear away from the distinguished base edge.')
                checks += 1
    return {'orders_checked': list(range(3, 8)), 'counts': counts, 'rooted_base_checks': checks, 'scope': 'Tiny controls of the general rooted-dual-tree ear lemma, not a complete target disk search.'}

def control_disks():
    disks = {}
    disks['cone_I1'] = profile(list(range(7)), [7], fan(list(range(7)), 7))
    disks['one_chord_two_fans_I2'] = profile(list(range(7)), [7, 8], fan([0, 1, 2, 3], 7) + fan([0, 3, 4, 5, 6], 8))
    disks['two_chords_empty_middle_I2'] = profile(list(range(7)), [7, 8], fan([0, 1, 2, 3], 7) + [mask((0, 3, 4))] + fan([0, 4, 5, 6], 8))
    adjacent = [(7, 0, 1), (7, 1, 2), (7, 2, 3), (8, 3, 4), (8, 4, 5), (8, 5, 6), (8, 6, 0), (7, 8, 0), (7, 8, 3)]
    disks['adjacent_centers_I2'] = profile(list(range(7)), [7, 8], [mask(t) for t in adjacent])
    need(all((not r['all_target_guards'] for r in disks.values())), 'A countercontrol was mislabeled as satisfying all target guards.')
    return disks

def allocation_controls():
    nonboundary = 3 * 2 + 7 - 3
    r = nonboundary - 1
    need(nonboundary == 10 and r + 2 == 11 > 10, 'Adjacent-center exact degree count changed.')
    cases = [{'chords': d, 'cross_edges': nonboundary - d} for d in range(nonboundary + 1) if 8 <= nonboundary - d <= 10]
    return {'I2_nonboundary_edges': nonboundary, 'adjacent_no_chord_interior_degree_sum': r + 2, 'nonadjacent_cases': cases, 'case_rejections_require_written_planar_disk_proof': True}
