"""Root-link catalogs by vertex type (PLAN.md step 5).

For a type (c6, p) with no split partner, every sphere on at most 12 vertices
(015 enumeration) with exactly c6 vertices of degree 6, p of degree 3 and all
others of degree 4 or 5. VERTEX-TYPES.md shows these are all the possible
links of such a vertex. Faces are relabelled 1..order; the root is 0.
"""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '015-sphere-catalog-audit'))
import spheres  # noqa: E402

TYPES = [(c6, p) for c6 in range(4) for p in range(4) if 1 <= c6 + p <= 3]


def catalog(cat):
    out = {f'{c6},{p}': [] for c6, p in TYPES}
    for n, classes in sorted(cat.items()):
        for faces in classes.values():
            deg = {}
            for e in spheres.edges(faces):
                for v in e:
                    deg[v] = deg.get(v, 0) + 1
            if not set(deg.values()) <= {3, 4, 5, 6}:
                continue
            key = f'{list(deg.values()).count(6)},{list(deg.values()).count(3)}'
            if key in out:
                lab = {v: i + 1 for i, v in enumerate(sorted(deg))}
                out[key].append(dict(order=n, faces=sorted(sorted(lab[v] for v in f) for f in faces)))
    return out


def main(path):
    doc = dict(status='ROOT_LINK_CATALOG', source='015 spheres.enumerate_spheres(12)',
               catalog=catalog(spheres.enumerate_spheres(12)))
    Path(path).write_text(json.dumps(doc) + '\n')
    print(json.dumps({k: [r['order'] for r in v] for k, v in doc['catalog'].items()}))


if __name__ == '__main__':
    main(sys.argv[1])
