"""Screen of one-vertex link types for pair-only Type II departures.

At a vertex x meeting 1..3 pair exceptions, with every -2 partner's pair link
a C6 (degree 6 in the unit link) and every +1 partner's a C3 (degree 3), ask
whether some 2-sphere on at most 12 vertices has exactly those numbers of
degree-6 and degree-3 vertices and all other degrees 4 or 5. This is a screen,
not an exclusion: it ignores split (two-triangle or bowtie) -2 links and
non-sphere unit links, so an empty row needs its own argument
(TYPE-II-PLUS-STAR.md) and a nonempty row only shows that one-vertex counting
does not decide the case.
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '015-sphere-catalog-audit'))
import spheres  # noqa: E402

TYPES = [(m, q) for m in range(4) for q in range(4) if 1 <= m + q <= 3]


def screen(cat):
    hits = {t: Counter() for t in TYPES}
    for n, classes in cat.items():
        for faces in classes.values():
            ds = Counter(Counter(v for e in spheres.edges(faces) for v in e).values())
            key = (ds[6], ds[3])
            if set(ds) <= {3, 4, 5, 6} and key in hits:
                hits[key][n] += 1
    return {f'minus2={m},plus1={q}': dict(sorted(hits[(m, q)].items())) for m, q in TYPES}


def main():
    out = screen(spheres.enumerate_spheres(12))
    print(json.dumps(out))
    return out


if __name__ == '__main__':
    main()
