"""Audit the 006 sphere catalogs (orders 7..12) and the 1424 root domain.

1. Enumerate all sphere triangulations by vertex splitting (spheres.py).
2. For each pinned 006 catalog: hash check, literal sphere check, and an
   exact bijection between catalog records and enumerated isomorphism classes.
3. Re-apply the 1413 necessary guards to every enumerated class and compare
   the survivors, as isomorphism classes, with the 13 accepted native roots.
"""
import hashlib
import itertools
import json
import os
import sys
import time

sys.dont_write_bytecode = True
import spheres
from spheres import require

HERE = os.path.dirname(os.path.abspath(__file__))
H = os.path.join(HERE, '..', '009-parent-analysis')
GEOMETRY = os.path.join(H, 'signed-star-full-geometry-result-cycle1422.json')
GEOMETRY_SHA = 'c863c922418d037e0192a4ce6b87f5b1b6bde58a748236439f0e577b3eacfd74'
OEIS_A000109 = {4: 1, 5: 1, 6: 2, 7: 5, 8: 14, 9: 50, 10: 233, 11: 1249, 12: 7595}


def sha256(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def degrees(faces):
    deg = {}
    for a, b in spheres.edges(faces):
        deg[a] = deg.get(a, 0) + 1
        deg[b] = deg.get(b, 0) + 1
    return deg


def induced_euler_range(faces):
    """Min and max of V-E+F over every vertex subset, by direct counting."""
    vs = spheres.vertices(faces)
    bit = {v: 1 << k for k, v in enumerate(vs)}
    em = [sum(bit[x] for x in e) for e in spheres.edges(faces)]
    fm = [sum(bit[x] for x in f) for f in faces]
    lo, hi = None, None
    for s in range(1 << len(vs)):
        chi = bin(s).count('1') - sum((m & s) == m for m in em) + sum((m & s) == m for m in fm)
        lo = chi if lo is None else min(lo, chi)
        hi = chi if hi is None else max(hi, chi)
    return lo, hi


def first_failed_guard(faces):
    """The 1413 necessary guards, in the 1414 order; None means survival."""
    deg = degrees(faces)
    if any(d not in (3, 4, 5, 6) for d in deg.values()):
        return 'degree_support', None
    n3 = sum(d == 3 for d in deg.values())
    n6 = sum(d == 6 for d in deg.values())
    if n3 + n6 != 3 or not 1 <= n6 <= 3:
        return 'special_vertex_count', None
    lo, hi = induced_euler_range(faces)
    if lo < -1 or hi > 3:
        return 'induced_euler_interval', (lo, hi)
    return None, (lo, hi)


def check_catalog(n, classes, layer):
    """{certificate: index}; raises unless records are spheres in bijection with layer."""
    require([c['index'] for c in classes] == list(range(len(classes))))
    certs = {}
    for c in classes:
        faces = spheres.from_masks(c['face_masks'])
        require(len(faces) == len(c['face_masks']) == 2 * n - 4, ('face count', n, c['index']))
        require(spheres.vertices(faces) == list(range(n)) and spheres.is_sphere(faces), ('not a sphere', n, c['index']))
        cert = spheres.certificate(faces)
        require(cert not in certs, ('duplicate class', n, c['index'], certs.get(cert)))
        certs[cert] = c['index']
    missing, extra = set(layer) - set(certs), set(certs) - set(layer)
    require(not missing and not extra, ('missing/extra classes', n, len(missing), len(extra)))
    return certs


def main():
    t0 = time.time()
    if sha256(GEOMETRY) != GEOMETRY_SHA:
        raise SystemExit('1422 geometry result hash mismatch')
    geo = json.load(open(GEOMETRY))
    accepted = {(r['native_identity']['order'], r['native_identity']['original_index'])
                for r in geo['results'] if r['status'] == 'SURVIVES_NECESSARY_GUARDS'}
    require(len(accepted) == 13)

    enum = spheres.enumerate_spheres(12)
    counts = {n: len(v) for n, v in enum.items()}
    require(counts == OEIS_A000109, counts)

    report = dict(status=None, enumeration_counts=counts, catalogs=[], guard_counts={},
                  survivors=[], accepted_native_roots=sorted(accepted))
    native_of = {}
    for stage in geo['input_catalog_stages']:
        n, cat = stage['order'], stage['catalog']
        path = os.path.join(HERE, '..', '006-solver-resume', os.path.basename(cat['path']))
        got = sha256(path)
        require(got == cat['sha256'], (n, got))
        data = json.load(open(path))
        require(data['order'] == n)
        certs = check_catalog(n, data['classes'], enum[n])
        native_of.update({cert: (n, idx) for cert, idx in certs.items()})
        report['catalogs'].append(dict(order=n, path=os.path.relpath(path, HERE), sha256=got,
                                       records=len(certs), bijective_with_enumeration=True))

    for n in range(7, 13):
        for cert, faces in enum[n].items():
            guard, rng = first_failed_guard(faces)
            report['guard_counts'][str(guard)] = report['guard_counts'].get(str(guard), 0) + 1
            if guard is None:
                deg = degrees(faces)
                report['survivors'].append(dict(
                    order=n, native_original_index=native_of[cert][1],
                    q=sum(d == 6 for d in deg.values()),
                    degree_counts={str(d): sum(x == d for x in deg.values()) for d in (3, 4, 5, 6)},
                    induced_euler_range=list(rng)))
    found = {(s['order'], s['native_original_index']) for s in report['survivors']}
    require(found == accepted, (sorted(found ^ accepted)))
    report['survivors_equal_accepted_roots'] = True
    report['status'] = 'CATALOG_COMPLETENESS_AND_ROOT_DOMAIN_REPRODUCED'
    report['wall_seconds'] = round(time.time() - t0, 1)
    report['sources'] = {f: sha256(os.path.join(HERE, f)) for f in ('spheres.py', 'audit.py')}
    report['premises'] = ['Steinitz-Rademacher contractible-edge lemma (classical)',
                          'Whitney uniqueness of 3-connected planar embeddings (classical)',
                          'pynauty certificate correctness',
                          'the 1413 guards themselves (degree support, special count, induced Euler [-1,3]) are taken as stated, not re-derived here']
    json.dump(report, open(os.path.join(HERE, 'audit-result.json'), 'w'), indent=1)
    print(json.dumps({k: report[k] for k in ('status', 'enumeration_counts', 'guard_counts', 'wall_seconds')}))


if __name__ == '__main__':
    main()
