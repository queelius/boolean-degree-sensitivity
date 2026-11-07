"""Exhaustive checks of the small-sphere facts used in TYPE-II-RIGID-SHAPES.md,
over every 2-sphere on 4..12 vertices from the 015 vertex-split enumeration.

S4: a sphere whose vertex degrees are all in {3,4,5} with four degree-3
    vertices is the tetrahedron boundary.
S3: no sphere has degree-3 vertices exactly three and all others of degree 5
    (in particular no (3,3,3,5,5,5)), and no 5-vertex sphere has a degree-5
    vertex.
S6: a sphere with one degree-6 vertex, three pairwise non-adjacent degree-3
    vertices and all other degrees in {4,5} has exactly 7 vertices.
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '015-sphere-catalog-audit'))
import spheres  # noqa: E402
from spheres import require  # noqa: E402


def adjacency(faces):
    adj = {}
    for e in spheres.edges(faces):
        a, b = tuple(e)
        adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    return adj


def facts(cat):
    s4 = s3 = s6 = 0
    s6_orders = Counter()
    for n, classes in cat.items():
        for faces in classes.values():
            adj = adjacency(faces)
            deg = {v: len(a) for v, a in adj.items()}
            ds = Counter(deg.values())
            if set(ds) <= {3, 4, 5} and ds[3] == 4:
                require(n == 4, ('S4', n)); s4 += 1
            if set(ds) <= {3, 5} and ds[3] == 3:
                s3 += 1
            if n == 5:
                require(5 not in ds, 'S3 five-vertex')
            threes = [v for v in deg if deg[v] == 3]
            if (set(ds) <= {3, 4, 5, 6} and ds[6] == 1 and ds[3] == 3
                    and all(b not in adj[a] for a in threes for b in threes)):
                s6_orders[n] += 1
    require(s3 == 0, ('S3', s3))
    require(set(s6_orders) == {7}, ('S6', dict(s6_orders)))
    require(s4 == 1, ('S4 count', s4))
    return dict(status='RIGID_SHAPE_SPHERE_FACTS_VERIFIED', s4_tetrahedron_classes=s4,
                s3_three_threes_rest_five=s3, s6_orders=dict(s6_orders))


def main():
    out = facts(spheres.enumerate_spheres(12))
    print(json.dumps(out))
    return out


if __name__ == '__main__':
    main()
