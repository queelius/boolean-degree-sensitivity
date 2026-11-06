"""Independent reader for the one-free residual-six frontier.

Shares no code with type2_shapes.py or one_free_frontier.py and does not use
pynauty. Three labelled sets are determined up to relabelling of the ground
set by their seven Venn-region sizes, so a Type II shape class is a kinds
triple with region sizes, up to permutations of equal-kind departures. The
reader enumerates these classes directly, applies its own status rules, and
checks the frontier row by row: a bijection of classes, the same statuses,
and every pinned file's hash. It checks bookkeeping and shape completeness,
not the written arguments behind the statuses.
"""
import argparse
import itertools
import json
import sys
from hashlib import sha256
from pathlib import Path

sys.dont_write_bytecode = True
SIZE = {'-2': 2, '+1': 2, 'Q2': 4}
REGIONS = [r for n in (1, 2, 3) for r in itertools.combinations(range(3), n)]


class ReaderError(Exception):
    pass


def require(cond, detail):
    if not cond:
        raise ReaderError(detail)


def sizes_ok(kinds, venn):
    return all(sum(venn[r] for r in REGIONS if i in r) == SIZE[kinds[i]] for i in range(3))


def same_set(venn, i, j):
    return all(venn[r] == 0 for r in REGIONS if (i in r) != (j in r))


def distinct(kinds, venn):
    for i, j in itertools.combinations(range(3), 2):
        clash = kinds[i] == kinds[j] or (kinds[i] != 'Q2' and kinds[j] != 'Q2')
        if clash and same_set(venn, i, j):
            return False
    return True


def key(kinds, venn):
    best = None
    for perm in itertools.permutations(range(3)):
        k = tuple(kinds[perm[i]] for i in range(3))
        moved = {tuple(sorted(perm.index(x) for x in r)): venn[r] for r in REGIONS}
        cand = (k, tuple(moved[r] for r in REGIONS))
        best = cand if best is None or cand < best else best
    return best


def classes():
    out = set()
    for kinds in itertools.combinations_with_replacement(('+1', '-2', 'Q2'), 3):
        for counts in itertools.product(range(5), repeat=len(REGIONS)):
            venn = dict(zip(REGIONS, counts))
            if sizes_ok(kinds, venn) and distinct(kinds, venn):
                out.add(key(kinds, venn))
    return out


def venn_of(departures):
    sets = [set(s) for _, s in departures]
    venn = {r: 0 for r in REGIONS}
    for v in set().union(*sets):
        venn[tuple(i for i in range(3) if v in sets[i])] += 1
    return tuple(k for k, _ in departures), venn


def expected_status(kinds, venn, rigid_open, rigid_closed, star):
    k = key(kinds, venn)
    if any(kinds[i] == 'Q2' and venn[(i,)] > 0 for i in range(3)):
        return 'EXCLUDED', 'PRIVATE_VERTEX_DOUBLED_QUARTIC'
    if k in rigid_closed:
        return 'EXCLUDED', 'RIGID_SHAPE_LOCAL_ARGUMENT'
    if k == star:
        return 'EXCLUDED', 'THREE_PLUS_ONE_STAR'
    require(k == rigid_open or 'Q2' not in kinds, 'unlisted covered doubled-quartic shape')
    return 'OPEN', 'NEEDS_THREE_EXCEPTION_MODEL'


def check_pins(value, seen):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            got = sha256(Path(value['path']).read_bytes()).hexdigest()
            require(got == value['sha256'], 'pin mismatch: ' + value['path'])
            seen.add(value['path'])
        for item in value.values():
            check_pins(item, seen)
    elif isinstance(value, list):
        for item in value:
            check_pins(item, seen)


# Written definitions, re-entered from TYPE-II-RIGID-SHAPES.md and TYPE-II-PLUS-STAR.md.
RIGID_OPEN = [('-2', {0, 1}), ('-2', {2, 3}), ('Q2', {0, 1, 2, 3})]
RIGID_CLOSED = [
    [('-2', {0, 1}), ('+1', {2, 3}), ('Q2', {0, 1, 2, 3})],
    [('+1', {0, 1}), ('+1', {2, 3}), ('Q2', {0, 1, 2, 3})],
    [('-2', {0, 1}), ('Q2', {0, 2, 3, 4}), ('Q2', {1, 2, 3, 4})],
    [('+1', {0, 1}), ('Q2', {0, 2, 3, 4}), ('Q2', {1, 2, 3, 4})],
    [('Q2', {0, 1, 2, 3}), ('Q2', {0, 1, 2, 4}), ('Q2', {0, 1, 3, 4})],
    [('Q2', {0, 1, 2, 3}), ('Q2', {0, 1, 4, 5}), ('Q2', {2, 3, 4, 5})],
]
STAR = [('+1', {9, 1}), ('+1', {9, 2}), ('+1', {9, 3})]


def read(doc):
    require(doc['status'] == 'ONE_FREE_RESIDUAL6_FRONTIER' and doc['global_status'] == 'OPEN', 'bad header')
    require(doc['whole_patterns_changed'] == 0, 'frontier claims a whole pattern')
    pinned = set()
    check_pins(doc, pinned)
    types = {t['type']: t for t in doc['types']}
    require(sorted(types) == ['I', 'II', 'III'], 'types must be exactly I, II, III')
    require(types['I']['status'] == types['III']['status'] == 'EXCLUDED', 'types I and III not excluded')
    require(types['II']['status'] == 'OPEN', 'type II must stay open while classes are open')

    rigid_open = key(*venn_of(RIGID_OPEN))
    rigid_closed = {key(*venn_of(d)) for d in RIGID_CLOSED}
    star = key(*venn_of(STAR))
    universe = classes()
    got = {}
    for row in doc['type_ii_classes']:
        kinds, venn = venn_of(row['departures'])
        require(sizes_ok(kinds, venn) and distinct(kinds, venn), 'invalid shape in frontier')
        k = key(kinds, venn)
        require(k not in got, 'duplicate class in frontier')
        got[k] = row
        require((row['status'], row['reason']) == expected_status(kinds, venn, rigid_open, rigid_closed, star),
                'status disagrees for ' + json.dumps(row['departures']))
        basis = row['basis']
        require((basis is None) == (row['status'] == 'OPEN') and (basis is None or basis in doc['type_ii_bases']),
                'excluded class without a pinned basis')
    require(set(got) == universe, f'class sets differ: frontier {len(got)}, reader {len(universe)}')
    n_open = sum(r['status'] == 'OPEN' for r in got.values())
    require(types['II']['shape_classes'] == len(universe) and types['II']['open_shape_classes'] == n_open,
            'type II counts disagree')
    by_reason = {}
    for r in got.values():
        by_reason[r['reason']] = by_reason.get(r['reason'], 0) + 1
    return dict(status='ONE_FREE_FRONTIER_READER_PASS', classes=len(universe), open=n_open,
                by_reason=dict(sorted(by_reason.items())), pinned_files_checked=len(pinned),
                checks='class bijection by Venn signature, status rules, counts, pins; not the written arguments')


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('frontier', type=Path)
    p.add_argument('--out', type=Path)
    a = p.parse_args(argv)
    result = read(json.loads(a.frontier.read_text()))
    result['frontier'] = dict(path=str(a.frontier.resolve()), sha256=sha256(a.frontier.read_bytes()).hexdigest())
    result['reader'] = dict(path=str(Path(__file__).resolve()), sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    if a.out:
        a.out.write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps(result))
    return result


if __name__ == '__main__':
    main()
