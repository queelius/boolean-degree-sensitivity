"""Typed frontier of the one-free residual-six case after attempt 016.

Types I and III are declared excluded by their written closures. Every Type
II departure shape class (type2_shapes.py) gets a status: excluded by the
private-vertex argument, by a rigid-shape argument, by the three-+1 star
argument, or OPEN. Each status names the note and review that carry it,
pinned by SHA-256. The independent check is one_free_frontier_reader.py.
"""
import argparse
import json
import sys
from hashlib import sha256
from pathlib import Path

import type2_shapes as t2

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def pin(name):
    path = (HERE / name).resolve()
    return dict(path=str(path), sha256=sha256(path.read_bytes()).hexdigest())


def deps(*items):
    return [(k, frozenset(s)) for k, s in items]


# TYPE-II-RIGID-SHAPES.md labels; shape 1 is the one left open.
RIGID = {
    1: deps(('-2', {0, 1}), ('-2', {2, 3}), ('Q2', {0, 1, 2, 3})),
    2: deps(('-2', {0, 1}), ('+1', {2, 3}), ('Q2', {0, 1, 2, 3})),
    3: deps(('+1', {0, 1}), ('+1', {2, 3}), ('Q2', {0, 1, 2, 3})),
    4: deps(('-2', {0, 1}), ('Q2', {0, 2, 3, 4}), ('Q2', {1, 2, 3, 4})),
    5: deps(('+1', {0, 1}), ('Q2', {0, 2, 3, 4}), ('Q2', {1, 2, 3, 4})),
    6: deps(('Q2', {0, 1, 2, 3}), ('Q2', {0, 1, 2, 4}), ('Q2', {0, 1, 3, 4})),
    7: deps(('Q2', {0, 1, 2, 3}), ('Q2', {0, 1, 4, 5}), ('Q2', {2, 3, 4, 5})),
}
STAR = deps(('+1', {0, 1}), ('+1', {0, 2}), ('+1', {0, 3}))


def classify(shape_list):
    rigid = {t2.canon(d): label for label, d in RIGID.items()}
    star = t2.canon(STAR)
    notes = dict(private=('TYPE-II-PRICING.md', 'REVIEW-star.md'),
                 rigid=('TYPE-II-RIGID-SHAPES.md', 'REVIEW-rigid.md'),
                 star=('TYPE-II-PLUS-STAR.md', 'REVIEW-star.md'))
    out = []
    for d in shape_list:
        key = t2.canon(d)
        row = dict(departures=[[k, sorted(s)] for k, s in d], rigid_label=rigid.get(key))
        if t2.private_quartic(d):
            row.update(status='EXCLUDED', reason='PRIVATE_VERTEX_DOUBLED_QUARTIC', basis='private')
        elif key in rigid and rigid[key] != 1:
            row.update(status='EXCLUDED', reason='RIGID_SHAPE_LOCAL_ARGUMENT', basis='rigid')
        elif key == star:
            row.update(status='EXCLUDED', reason='THREE_PLUS_ONE_STAR', basis='star')
        else:
            row.update(status='OPEN', reason='NEEDS_THREE_EXCEPTION_MODEL', basis=None)
        out.append(row)
    return out, {b: dict(note=pin(n), review=pin(r)) for b, (n, r) in notes.items()}


def frontier():
    rows, bases = classify(t2.shapes())
    types = [
        dict(type='III', constants=[0, 3], status='EXCLUDED', subcases=9,
             note=pin('TYPE-III-CLOSURE.md'), review=pin('REVIEW-closure.md'),
             extension=pin('EXTENSION-plus-plus-c3.md'), extension_review=pin('REVIEW-plus-plus-c3.md')),
        dict(type='I', constants=[1, 2], status='EXCLUDED',
             note=pin('TYPE-I-CLOSURE.md'), review=pin('REVIEW-typeI.md')),
        dict(type='II', constants=[1, 2], status='OPEN',
             shape_classes=len(rows), open_shape_classes=sum(r['status'] == 'OPEN' for r in rows)),
    ]
    return dict(
        status='ONE_FREE_RESIDUAL6_FRONTIER',
        scope='one-free residual Fourier defect <= 6 (1513/1523 trichotomy), selfdual existence representative',
        types=types, type_ii_bases=bases, type_ii_classes=rows,
        sources=[pin(n) for n in ('one_free_frontier.py', 'type2_shapes.py')],
        global_status='OPEN', whole_patterns_changed=0)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args(argv)
    doc = frontier()
    a.out.write_text(json.dumps(doc, indent=1) + '\n')
    print(json.dumps({t['type']: t['status'] for t in doc['types']} | {'open_type_ii': doc['types'][2]['open_shape_classes']}))
    return doc


if __name__ == '__main__':
    main()
