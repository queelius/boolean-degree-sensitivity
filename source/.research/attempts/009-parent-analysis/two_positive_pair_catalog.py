"""Complete proposed local catalog for an adjacent pair of positive doubles.

Scope: a negative-free pair contained in two positive double quintics whose
intersection is a quartet, baseline cubic numerators, empty-profile truths.
Completeness uses the surface lemma in the companion note and the accepted
complete sphere catalogs. These rows are necessary derivatives, not functions.
"""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

H = Path(__file__).resolve().parent
P = H.parent/'006-solver-resume'


def vertices(mask):
    return tuple(v for v in range(mask.bit_length()) if mask >> v & 1)


def eligible_pairs(negatives, positives):
    assert len(positives) == len(set(positives)) == 2
    common = positives[0] & positives[1]
    return [sum(1<<v for v in pair) for pair in combinations(vertices(common), 2)
            if not any(all(q>>v&1 for v in pair) for q in negatives)]


def validate_surface(order, faces):
    assert len(faces) == len(set(faces))
    assert all(type(f) is int and 0 < f < 1<<order and f.bit_count()==3 for f in faces)
    degree = Counter(v for f in faces for v in vertices(f))
    assert set(degree) == set(range(order))
    edge_counts = Counter(e for f in faces for e in combinations(vertices(f), 2))
    assert set(edge_counts.values()) == {2}
    assert order-len(edge_counts)+len(faces) == 2
    for v in range(order):
        edges = [vertices(f^(1<<v)) for f in faces if f>>v&1]
        adjacency = {}
        for a,b in edges:
            adjacency.setdefault(a,set()).add(b)
            adjacency.setdefault(b,set()).add(a)
        assert all(len(ns)==2 for ns in adjacency.values())
        todo, seen = [next(iter(adjacency))], set()
        while todo:
            u=todo.pop()
            if u not in seen:
                seen.add(u);todo.extend(adjacency[u]-seen)
        assert seen == set(adjacency)
    return degree


def signed_range(row):
    terms = {1<<v:k for v,k in enumerate(row['linear_numerators']) if k}
    terms.update(dict.fromkeys(row['unit_faces'],1))
    assert not set(row['double_faces']) & set(terms)
    terms.update(dict.fromkeys(row['double_faces'],2))
    hist = Counter()
    for x in range(1<<12):
        value = sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in terms.items())
        if value not in (-16,-8,0,8,16):
            return dict(status='EXACT_RANGE_CONTRADICTION',input=x,numerator=value)
        hist[value]+=1
    return dict(status='NECESSARY_RANGE_VALID',value_histogram=dict(sorted(hist.items())))


def make_row(order, faces):
    degree = validate_surface(order, faces)
    assert set(degree.values()) <= {3,4,5}
    special = [v for v in range(order) if degree[v]==3]
    assert len(special)==2 and order<=8
    shared = (1<<order)|(1<<(order+1))
    row = dict(surface_order=order, active_order=order+2, unit_faces=sorted(faces),
               double_faces=[shared|(1<<v) for v in special],
               linear_numerators=[-1 if degree[v] in (3,5) else 0 for v in range(12)])
    assert sum(row['linear_numerators'])+len(faces)+4 == 8
    row['range']=signed_range(row)
    return row


def pair_rows():
    rows=[]
    for n in range(5,9):
        source=json.loads((P/f'sphere-triangulations-{n:02d}.json').read_text())
        assert source['status']=='COMPLETE_INVERSE_CONTRACTION_COVER' and source['order']==n
        for entry in source['classes']:
            degree=Counter(v for f in entry['face_masks'] for v in vertices(f))
            if set(degree.values()) <= {3,4,5} and list(degree.values()).count(3)==2:
                rows.append(dict(index=len(rows), source_order=n, source_index=entry['index'],
                                 **make_row(n,entry['face_masks'])))
    return rows


def run():
    data=json.loads((P/'four-double-positive-cover.json').read_text())
    placements=[]
    for cl in data['classes']:
        for index,positives in enumerate(cl['cover']['two_positive_doubles']['placements']):
            pair_choices=eligible_pairs(cl['negative_supports'],positives)
            assert pair_choices and (positives[0]&positives[1]).bit_count()==4
            placements.append(dict(class_index=cl['class_index'],placement_index=index,
                                   negative_supports=cl['negative_supports'],positive_doubles=positives,
                                   eligible_pairs=pair_choices))
    rows=pair_rows()
    paths=[Path(__file__),H/'test_two_positive_pair_catalog.py',H/'two-positive-pair-surface-lemma.md',
           P/'four-double-positive-cover.json',P/'four-double-positive-cover-accepted-manifest.json',
           P/'independent-math-audit/d2-component-inventory-independent-manifest.json']
    paths += [P/f'sphere-triangulations-{n:02d}.json' for n in range(5,9)]
    return dict(status='PROPOSED_COMPLETE_ADJACENT_TWO_POSITIVE_PAIR_CATALOG',global_status='UNRESOLVED',
                independent_audit='PENDING',whole_support_exclusion=False,
                all_positive_pairs_adjacent=True,ambient_pair_variables=12,
                placements=placements,rows=rows,
                counts=dict(placements=len(placements),rows=len(rows),
                            selected_pairs=sum(len(p['eligible_pairs']) for p in placements)),
                sources=[dict(path=str(p.resolve()),sha256=sha256(p.read_bytes()).hexdigest()) for p in paths])


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    assert not args.output.exists()
    result=run()
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],counts=result['counts'])))
