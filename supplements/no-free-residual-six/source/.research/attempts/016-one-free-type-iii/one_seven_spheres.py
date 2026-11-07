"""No 2-sphere on at most 12 vertices has exactly one vertex of degree 7 and
every other vertex of degree 4 or 5.

Checked twice, from independent sources: the vertex-split enumeration of
015-sphere-catalog-audit (n = 4..12, counts equal OEIS A000109), and the 006
sphere catalogs (n = 5..12), whose SHA-256s are pinned by the 015 audit and
re-checked here. A relaxed control (degree 3 also allowed) must find spheres,
so the filter is not vacuous.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent / '015-sphere-catalog-audit'
sys.path.insert(0, str(AUDIT))
import spheres  # noqa: E402
from spheres import require  # noqa: E402

OEIS = {4: 1, 5: 1, 6: 2, 7: 5, 8: 14, 9: 50, 10: 233, 11: 1249, 12: 7595}


def degrees(faces):
    return Counter(v for e in spheres.edges(faces) for v in e)


def has_pattern(faces, allowed=(4, 5)):
    """Exactly one degree-7 vertex; every other degree in `allowed`."""
    ds = list(degrees(faces).values())
    return ds.count(7) == 1 and all(d == 7 or d in allowed for d in ds)


def count(classes, allowed=(4, 5)):
    return sum(has_pattern(f, allowed) for f in classes)


def catalog_006():
    """{n: [faces]} from the 006 catalogs, hash-checked against the 015 audit."""
    audit = json.loads((AUDIT / 'audit-result.json').read_text())
    pins = {c['order']: c for c in audit['catalogs']}
    out = {}
    for n in range(5, 13):
        path = (AUDIT / f'../006-solver-resume/sphere-triangulations-{n:02d}.json').resolve()
        if n in pins:
            require(hashlib.sha256(path.read_bytes()).hexdigest() == pins[n]['sha256'], ('catalog changed', n))
        out[n] = [spheres.from_masks(c['face_masks']) for c in json.loads(path.read_text())['classes']]
    return out


def main():
    enum = spheres.enumerate_spheres(12)
    require({n: len(enum[n]) for n in enum} == OEIS, 'enumeration counts')
    cat = catalog_006()
    require(all(len(cat[n]) == OEIS[n] for n in cat), '006 catalog counts')
    target = {n: count(enum[n].values()) for n in enum}
    target_006 = {n: count(cat[n]) for n in cat}
    control = {n: count(enum[n].values(), allowed=(3, 4, 5)) for n in enum}
    require(not any(target.values()) and not any(target_006.values()), ('pattern found', target, target_006))
    require(any(control.values()), 'relaxed control found nothing')
    out = dict(status='NO_ONE_SEVEN_FOUR_FIVE_SPHERE_UP_TO_12', enumerated=target, catalog_006=target_006,
               relaxed_control_with_degree_3=control)
    print(json.dumps(out))
    return out


if __name__ == '__main__':
    main()
