"""Complete marked rs+B placement cover with explicit coordinate maps.

The signed spectrum and the distinguished two-set B are preserved. The
other six coordinates are unmarked: this is a quotient only for the stated
local five-pair necessary model, not for full global negative geometries.
"""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

import pynauty

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent/'006-solver-resume/independent-math-audit'


def vertices(mask):
    return tuple(v for v in range(mask.bit_length()) if mask >> v & 1)


def relabel(mask, image):
    return sum(1 << image[v] for v in vertices(mask))


def canonical(terms, n, marked):
    terms = {s: k for s, k in terms.items() if k}
    assert 0 <= marked < 1 << n and all(0 < s < 1 << n for s in terms)
    ordered = sorted(terms.items())
    adjacency = {v: [] for v in range(n+len(ordered))}
    colors = [set(vertices(marked)), set(range(n))-set(vertices(marked))]
    for value in sorted(set(terms.values())):
        colors.append({n+i for i, (_, k) in enumerate(ordered) if k == value})
    colors = [group for group in colors if group]
    for i, (support, _) in enumerate(ordered):
        for v in vertices(support):
            adjacency[v].append(n+i)
            adjacency[n+i].append(v)
    graph = pynauty.Graph(n+len(ordered), adjacency_dict=adjacency, vertex_coloring=colors)
    order = [v for v in pynauty.canon_label(graph) if v < n]
    assert sorted(order) == list(range(n))
    image = [None]*n
    for new, old in enumerate(order):
        image[old] = new
    key = (relabel(marked, image), tuple(sorted((relabel(s, image), k) for s, k in terms.items())))
    return key, image


def spectrum(row):
    terms = {1 << v: k for v, k in enumerate(row['linear_numerators']) if k}
    terms.update(dict.fromkeys(row['unit_faces'], 1))
    assert row['negative_face'] not in terms and row['positive_face'] not in terms
    terms[row['negative_face']] = -2
    terms[row['positive_face']] = 2
    return terms


def run():
    source = AUDIT/'class40-adjacent-double-pair-complete-cover.json'
    cover = json.loads(source.read_text())
    classes, ids, maps = [], {}, []
    for row_id in cover['class40_zero_coface_retained_row_ids']:
        row = cover['marked_rows'][row_id]
        terms = spectrum(row)
        available = [v for v in range(12) if v not in (row['a'], row['p'], row['q'], row['t'])]
        assert len(available) == 8
        for pair in combinations(available, 2):
            marked = sum(1 << v for v in pair)
            key, image = canonical(terms, 12, marked)
            if key not in ids:
                ids[key] = len(classes)
                degrees = [sum(f >> v & 1 for f in row['unit_faces']) for v in pair]
                edge_faces = sum(f & marked == marked for f in row['unit_faces'])
                classes.append(dict(index=len(classes), marked_B=key[0], spectrum=list(key[1]),
                                    source_row=row_id, source_B=list(pair),
                                    source_to_representative=image,
                                    B_unit_link_sizes=sorted(degrees), B_pair_face_degree=edge_faces))
            maps.append(dict(source_row=row_id, source_B=list(pair), target_class=ids[key],
                             source_to_representative=image))
    assert len(maps) == len(cover['class40_zero_coface_retained_row_ids'])*28 == 4508
    # Literal coordinate-map validation is the completeness certificate.
    for record in maps:
        row = cover['marked_rows'][record['source_row']]
        terms = spectrum(row)
        marked = sum(1 << v for v in record['source_B'])
        image = record['source_to_representative']
        target = classes[record['target_class']]
        assert sorted(image) == list(range(12))
        assert relabel(marked, image) == target['marked_B']
        assert sorted((relabel(s, image), k) for s, k in terms.items()) == [tuple(x) for x in target['spectrum']]
    counts = Counter(tuple(c['B_unit_link_sizes']) for c in classes)
    row2 = next(r['target_class'] for r in maps if r['source_row'] == 2 and r['source_B'] == [2, 3])
    return dict(status='COMPLETE_LOCAL_FIVE_PAIR_MARKED_PLACEMENT_QUOTIENT',
                independent_audit='PENDING', global_status='UNRESOLVED',
                scope='Signed rs spectrum plus unordered B; C/D placements are unmarked and omitted only for this local necessary model.',
                source_rows=161, raw_B_placements=4508, class_count=len(classes),
                unit_link_size_counts=[dict(sizes=k, count=v) for k, v in sorted(counts.items())],
                explicit_row2_B23_target_class=row2, classes=classes, coverage_maps=maps,
                sources=[dict(path=str(p), sha256=sha256(p.read_bytes()).hexdigest()) for p in (Path(__file__), source)],
                canonicalizer=dict(name='pynauty', version=pynauty.__version__, trusted_for_completeness=False))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = run()
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('raw_B_placements', 'class_count', 'unit_link_size_counts', 'explicit_row2_B23_target_class')}))
