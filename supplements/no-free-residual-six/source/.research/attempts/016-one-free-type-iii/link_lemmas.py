"""Exhaustive check of the two link lemmas used in EXTENSION-plus-plus-c3.md.

Lemma 7: in every 7-vertex 2-sphere whose vertex degrees all lie in {4,5},
each degree-5 vertex w has exactly one non-neighbour, and it is adjacent to
every neighbour of w.

Lemma 8: in every 8-vertex 2-sphere whose vertex degrees all lie in {4,5},
each degree-5 vertex w has exactly two non-neighbours, and at least 7 edges
join them to the neighbours of w (the bound the argument uses; it is tight).

Spheres come from the independent vertex-split enumeration of
015-sphere-catalog-audit (counts checked there against OEIS A000109).
"""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '015-sphere-catalog-audit'))
import spheres  # noqa: E402
from spheres import require  # noqa: E402


def adjacency(faces):
    adj = {v: set() for v in spheres.vertices(faces)}
    for e in spheres.edges(faces):
        a, b = tuple(e)
        adj[a].add(b); adj[b].add(a)
    return adj


def degree_45(adj):
    return all(len(n) in (4, 5) for n in adj.values())


def outside(adj, w):
    """(neighbours of w, non-neighbours other than w, edges between them)."""
    nbr = adj[w]
    rest = set(adj) - nbr - {w}
    return nbr, rest, sum(len(adj[b] & nbr) for b in rest)


def lemma7(classes):
    cases = 0
    for faces in classes:
        adj = adjacency(faces)
        if not degree_45(adj):
            continue
        for w in adj:
            if len(adj[w]) == 5:
                nbr, rest, _ = outside(adj, w)
                require(len(rest) == 1, ('lemma 7 non-neighbours', sorted(rest)))
                (b,) = rest
                require(adj[b] >= nbr, ('lemma 7 fails', sorted(faces)))
                cases += 1
    return cases


def lemma8(classes, need=7):
    cases, least = 0, None
    for faces in classes:
        adj = adjacency(faces)
        if not degree_45(adj):
            continue
        for w in adj:
            if len(adj[w]) == 5:
                _, rest, m = outside(adj, w)
                require(len(rest) == 2, ('lemma 8 non-neighbours', sorted(rest)))
                require(m >= need, ('lemma 8 fails', m, sorted(faces)))
                cases, least = cases + 1, m if least is None else min(least, m)
    return cases, least


def main():
    cat = spheres.enumerate_spheres(8)
    require(len(cat[7]) == 5 and len(cat[8]) == 14, 'A000109 counts at n = 7, 8')
    c7 = lemma7(cat[7].values())
    c8, least = lemma8(cat[8].values())
    require(c7 > 0 and c8 > 0, 'lemmas must not hold vacuously')
    deg45 = {n: sum(degree_45(adjacency(f)) for f in cat[n].values()) for n in (7, 8)}
    out = dict(status='LINK_LEMMAS_VERIFIED', sphere_classes={7: len(cat[7]), 8: len(cat[8])},
               classes_with_degrees_4_5=deg45, lemma7_rooted_cases=c7, lemma8_rooted_cases=c8,
               lemma8_min_edges_to_link_of_w=least)
    print(json.dumps(out))
    return out


if __name__ == '__main__':
    main()
