"""Near-flag check of every possible vertex link (NEAR-FLAG.md).

A sphere is near-flag if every 3-cycle of its graph that is not a face is the
neighbourhood of a degree-3 vertex. For each vertex type (n(-2), n(+1)) with
no split partner, take every sphere on at most 12 vertices (015 enumeration)
with exactly that many degree-6 and degree-3 vertices and all others of
degree 4 or 5; type (0,0) is an ordinary vertex. Report which types have
only near-flag (and only flag) links.
"""
import itertools
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '015-sphere-catalog-audit'))
import spheres  # noqa: E402

TYPES = [(c6, p) for c6 in range(4) for p in range(4) if c6 + p <= 3]


def classify(faces):
    F = {frozenset(f) for f in faces}
    E = spheres.edges(faces)
    vs = spheres.vertices(faces)
    nb = {x: {y for e in E if x in e for y in e if y != x} for x in vs}
    deg3 = [x for x in vs if len(nb[x]) == 3]
    empty = [t for t in itertools.combinations(vs, 3)
             if all(frozenset(p) in E for p in itertools.combinations(t, 2)) and frozenset(t) not in F]
    near = all(any(set(t) == nb[y] for y in deg3) for t in empty)
    return dict(flag=not empty, near_flag=near, degrees={len(n) for n in nb.values()},
                n6=sum(len(n) == 6 for n in nb.values()), n3=len(deg3))


def main():
    cat = spheres.enumerate_spheres(12)
    rows = {t: dict(spheres=0, flag=0, near_flag=0, orders=set()) for t in TYPES}
    for n, classes in cat.items():
        for faces in classes.values():
            r = classify(faces)
            if not r['degrees'] <= {3, 4, 5, 6}:
                continue
            t = (r['n6'], r['n3'])
            if t in rows:
                rows[t]['spheres'] += 1
                rows[t]['flag'] += r['flag']
                rows[t]['near_flag'] += r['near_flag']
                rows[t]['orders'].add(n)
    out = [dict(minus2=t[0], plus1=t[1], spheres=v['spheres'], flag=v['flag'], near_flag=v['near_flag'],
                orders=sorted(v['orders']), all_near_flag=v['spheres'] == v['near_flag'])
           for t, v in sorted(rows.items())]
    doc = dict(status='NEAR_FLAG_CHECK', rows=out,
               near_flag_types=[[r['minus2'], r['plus1']] for r in out if r['all_near_flag'] and r['spheres']])
    print(json.dumps(doc, indent=1))
    return doc


if __name__ == '__main__':
    main()
