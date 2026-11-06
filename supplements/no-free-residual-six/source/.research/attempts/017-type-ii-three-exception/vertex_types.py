"""Possible unit links at a vertex meeting pair exceptions (PLAN.md step 3).

Setting (pair-only Type II shapes, no bowtie): at a vertex x, every partner r
with m_xr = 1 has as link of xr a single cycle, except a -2 partner whose link
may be two disjoint triangles (split). After splitting each such partner into
two copies, the unit link U_x is a disjoint union of closed surfaces with

    chi(U_x) = 2 + s,    vertices(U_x) = d + s,    d <= 12,

where s is the number of split partners and d the number of partners. Degrees
in U_x: 6 at a -2 partner with a C6 link, 3 at a +1 partner, 3 at each split
copy, 4 or 5 elsewhere. The two copies of one partner are non-adjacent with
disjoint neighbourhoods (their links are the two disjoint triangles). Every
component has a vertex of degree at most 5 (at most three degree-6 vertices,
and a surface has at least four vertices), so chi >= 1: spheres and
projective planes only.

A vertex type is (c6, s, p): numbers of C6, split and +1 partners. For each
type this module lists every multiset of components (from complete catalogs)
with a consistent assignment of the special vertices. Sphere components have
at most 12 vertices (curvature: n = 12 - 2 n3 - n4 + n6 and at most n3 / 2
copy pairs merge, against n6 <= 3), projective planes at most 6 + n6 <= 9.
Catalogs: spheres from the 015 vertex-split enumeration, projective planes
from `surfaces.brute` (no classification theorem used).
"""
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '015-sphere-catalog-audit'))
import spheres  # noqa: E402
import surfaces  # noqa: E402

BUDGET = 12
TYPES = [(c6, s, p) for c6 in range(4) for s in range(4) for p in range(4) if 1 <= c6 + s + p <= 3]


def adjacency(faces):
    adj = {}
    for a, b in spheres.edges(faces):
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj


def max_internal_pairs(adj, d3):
    """Largest number of disjoint copy-compatible pairs among the degree-3 vertices."""
    ok = [(a, b) for a, b in itertools.combinations(sorted(d3), 2)
          if b not in adj[a] and not (adj[a] & adj[b])]
    best = 0
    for k in range(1, len(d3) // 2 + 1):
        if any(len(set().union(*[set(e) for e in m])) == 2 * k for m in itertools.combinations(ok, k)):
            best = k
    return best


def component_types(sphere_cat, rp2_cat):
    """Distinct (chi, n, n6, n3, max internal pairs) over allowed components, with a witness count."""
    out = Counter()
    for chi, cat in ((2, sphere_cat), (1, rp2_cat)):
        for n, classes in cat.items():
            for faces in classes.values():
                adj = adjacency(faces)
                deg = {v: len(a) for v, a in adj.items()}
                if not set(deg.values()) <= {3, 4, 5, 6}:
                    continue
                d6 = [v for v, k in deg.items() if k == 6]
                d3 = [v for v, k in deg.items() if k == 3]
                if len(d6) > 3 or len(d3) > 6:
                    continue
                out[(chi, n, len(d6), len(d3), max_internal_pairs(adj, d3))] += 1
    return out


def realizable(comps, c6, s, p):
    """Can the special vertices of these components be assigned to the type?"""
    if sum(x[2] for x in comps) != c6 or sum(x[3] for x in comps) != p + 2 * s:
        return False
    # choose internal pairs per component; remaining copies pair across distinct components
    for internal in itertools.product(*[range(min(x[4], s) + 1) for x in comps]):
        k = sum(internal)
        if k > s:
            continue
        ext_needed = 2 * (s - k)
        # free degree-3 vertices per component after internal pairs
        free = [x[3] - 2 * i for x, i in zip(comps, internal)]
        # pick e_j external copies from component j, sum = ext_needed, pairable across components
        for ext in itertools.product(*[range(f + 1) for f in free]):
            if sum(ext) != ext_needed or (ext and max(ext) > ext_needed - max(ext)):
                continue
            if sum(f - e for f, e in zip(free, ext)) == p:
                return True
    return False


def classify(ctypes):
    kinds = sorted(ctypes)
    out = {}
    for c6, s, p in TYPES:
        found = []
        for ncomp in range(1, 2 + s + 1):
            for comps in itertools.combinations_with_replacement(kinds, ncomp):
                if sum(x[0] for x in comps) != 2 + s or sum(x[1] for x in comps) - s > BUDGET:
                    continue
                if realizable(comps, c6, s, p):
                    found.append(comps)
        out[(c6, s, p)] = found
    return out


def summary(result, ctypes):
    rows = []
    for (c6, s, p), found in sorted(result.items()):
        shapes = sorted({tuple(('S2' if x[0] == 2 else 'RP2', x[1]) for x in comps) for comps in found})
        rows.append(dict(c6=c6, split=s, plus1=p, configurations=len(found),
                         only_single_sphere=all(len(cf) == 1 and cf[0][0] == 'S2' for cf in shapes),
                         component_patterns=[list(map(list, cf)) for cf in shapes]))
    return rows


def main(nsphere=12, nrp2=9):
    sph = spheres.enumerate_spheres(nsphere)
    rp = {n: surfaces.brute(n, 1) for n in range(6, nrp2 + 1)}
    ctypes = component_types(sph, rp)
    rows = summary(classify(ctypes), ctypes)
    doc = dict(status='VERTEX_TYPE_CLASSIFICATION', budget=BUDGET, sphere_max=nsphere, rp2_max=nrp2,
               component_types=len(ctypes), rows=rows)
    print(json.dumps(doc, indent=1))
    return doc


if __name__ == '__main__':
    main()
