"""Independent finite ingredients for the two-positive-pair derivative proof."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

from negative_free_endpoint_strips import strip_roots, vertices

HERE = Path(__file__).resolve().parent
SIX = HERE.parent / '006-solver-resume'


def pentagon_disks():
    boundary = {frozenset((v, (v+1) % 5)) for v in range(5)}
    triangulations = []
    for faces in combinations(combinations(range(5), 3), 3):
        counts = Counter(frozenset(e) for face in faces for e in combinations(face, 2))
        if {e for e, value in counts.items() if value == 1} != boundary:
            continue
        if len(counts) != 7 or any(value not in (1, 2) for value in counts.values()):
            continue
        diagonals = [e for e in counts if e not in boundary]
        assert len(diagonals) == 2 and diagonals[0] & diagonals[1]
        triangulations.append([list(face) for face in faces])
    assert len(triangulations) == 5
    return triangulations


def evaluate():
    controls = []
    for n in (7, 8, 9):
        boundary = {(1 << v) | (1 << ((v+2) % n)) for v in range(n)}
        roots = strip_roots(boundary)
        histogram = Counter()
        for left in roots:
            le = {sum(1 << v for v in e) for face in left['faces']
                  for e in combinations(vertices(face), 2)} - boundary
            for right in roots:
                re = {sum(1 << v for v in e) for face in right['faces']
                      for e in combinations(vertices(face), 2)} - boundary
                common = set(left['faces']) & set(right['faces'])
                labels = [{e for e in boundary if e & face == e} for face in common]
                assert all(len(label) == 1 for label in labels)
                assert len(set().union(*labels)) == len(common) if labels else not common
                histogram[len(common), len(le & re)] += 1
                if len(common) <= 2:
                    assert n == 8 and len(le & re) <= 4
        controls.append(dict(vertices=n, roots=len(roots), histogram=[
            dict(faces=k[0], edges=k[1], count=value) for k, value in sorted(histogram.items())]))
    expected = json.loads((SIX / 'two-positive-cubic-controls.json').read_text())
    for actual, saved in zip(controls, expected['cycle_roots']):
        assert actual['vertices'] == saved['vertices'] and actual['roots'] == saved['roots']
        assert actual['histogram'] == saved['common_face_edge_histogram']
    return dict(status='INDEPENDENT_FINITE_CONTROLS_PASS', global_status='UNRESOLVED',
                cycle_roots=controls, pentagon_disk_positive_controls=pentagon_disks(),
                sources=[dict(path=str(p), sha256=sha256(p.read_bytes()).hexdigest()) for p in
                         [Path(__file__), HERE / 'negative_free_endpoint_strips.py',
                          SIX / 'two-positive-cubic-free-derivative.md',
                          SIX / 'two-positive-cubic-controls.json']])


if __name__ == '__main__':
    target = HERE / 'two-positive-cubic-independent-controls.json'
    assert not target.exists()
    result = evaluate()
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'cycle_roots')}))
