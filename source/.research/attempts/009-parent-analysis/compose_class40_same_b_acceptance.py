"""Compose complete independent same-B exclusions into the accepted frontier.

This checks coverage and source integrity, not the mathematical replay itself.
The independent row checkers and the accepted interface remain dependencies.
"""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json


def unique(values):
    assert len(values) == len(set(values))
    return set(values)


def combine_frontiers(accepted, remaining, added, universe):
    old, left, new = map(unique, (accepted, remaining, added))
    assert not old & left and old | left == set(universe)
    assert new <= left
    return sorted(old | new), sorted(left - new)


def validate_pair(first, second):
    assert first['status'] == 'INDEPENDENT_UNIVERSAL_FIRST_ROW_CACHED_REPLAYS_PASS'
    assert second['status'] == 'INDEPENDENT_COMPLETE_UNIVERSAL_SAME_B_REPLAYS_PASS'
    assert first['producer_imports'] is second['producer_imports'] is False
    left = {r['index']: r for r in first['reports']}
    right = {r['index']: r for r in second['reports']}
    assert len(left) == len(first['reports']) and len(right) == len(second['reports'])
    assert left.keys() == right.keys() and left
    total = Counter()
    exact = {'EXACT_PROJECTED_FOUR_CUBE_CONTRADICTION', 'TAIL_FREE_CLOSURE_CONTRADICTION'}
    for index, report in right.items():
        parent = left[index]
        assert parent['complete_representative_screen'] is True
        frontier = parent['residual_representatives']
        unique(frontier)
        assert report['complete_first_frontier'] is report['whole_local_placement_excluded'] is True
        assert report['residual_first_rows'] == []
        assert [r['first_row_id'] for r in report['records']] == frontier
        total['first_fixed_points'] += len(frontier)
        for entry in report['records']:
            assert entry['first_row_excluded'] is True and entry['remaining_second_rows'] == []
            unique([r['row_id'] for r in entry['records']])
            counts = Counter(r['status'] for r in entry['records'])
            assert set(counts) <= exact and dict(counts) == entry['counts']
            assert all(r['excluded'] is True for r in entry['records'])
            assert len(entry['records']) == entry['three_cube_survivors']
            assert 0 <= entry['three_cube_survivors'] <= entry['complete_conditional_rows']
            total['conditional_rows'] += entry['complete_conditional_rows']
            total['three_cube_survivors'] += entry['three_cube_survivors']
            total.update(counts)
    return sorted(right), total


class Bindings:
    def __init__(self):
        self.files = {}
        self.checks = 0

    def bind(self, path, expected=None):
        path = Path(path).resolve()
        if str(path) not in self.files:
            self.files[str(path)] = sha256(path.read_bytes()).hexdigest()
        digest = self.files[str(path)]
        assert expected is None or digest == expected, str(path)
        self.checks += expected is not None
        return dict(path=str(path), sha256=digest)

    def walk(self, value):
        if isinstance(value, dict):
            if 'path' in value and 'sha256' in value:
                self.bind(value['path'], value['sha256'])
            for item in value.values():
                self.walk(item)
        elif isinstance(value, list):
            for item in value:
                self.walk(item)

    def read(self, path, expected=None):
        binding = self.bind(path, expected)
        data = json.loads(Path(binding['path']).read_text())
        self.walk(data)
        return data


def compose(previous, audits):
    here = Path(__file__).resolve().parent
    bindings = Bindings()
    old = bindings.read(previous)
    assert old['global_status'] == 'UNRESOLVED' and old['whole_class40_excluded'] is False
    quotient = bindings.read(here / 'class40-local-five-pair-placement-quotient.json')
    universe = [r['index'] for r in quotient['classes']]
    assert len(unique(universe)) == quotient['class_count']
    interface = here.parent / '006-solver-resume/independent-math-audit/class40-same-b-interface-independent-manifest.json'
    bindings.read(interface)
    added, total = [], Counter()
    for audit in audits:
        second = bindings.read(audit)
        source = second['first_row_audit']
        first = bindings.read(source['path'], source['sha256'])
        indices, counts = validate_pair(first, second)
        added.extend(indices)
        total.update(counts)
    accepted, remaining = combine_frontiers(old['accepted_local_classes'], old['remaining_local_classes'], added, universe)
    for path in (Path(__file__), here / 'test_compose_class40_same_b_acceptance.py'):
        bindings.bind(path)
    metrics = {key: total.pop(key) for key in ('first_fixed_points', 'conditional_rows', 'three_cube_survivors')}
    return dict(status='PARENT_ACCEPTED_COMPLETE_UNIVERSAL_SAME_B_LOCAL_EXCLUSIONS',
                global_status='UNRESOLVED', whole_class40_excluded=not remaining,
                new_excluded_local_classes=sorted(added), accepted_local_classes=accepted,
                remaining_local_classes=remaining, all_CD_assignments=old['all_CD_assignments'],
                **metrics, counts=dict(total), source_binding_checks=bindings.checks,
                files=[dict(path=p, sha256=d) for p, d in sorted(bindings.files.items())])


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--previous', type=Path, required=True)
    parser.add_argument('--audits', type=Path, nargs='+', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists()
    result = compose(args.previous, args.audits)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('files', 'accepted_local_classes', 'remaining_local_classes')}
                     | dict(accepted=len(result['accepted_local_classes']), remaining=len(result['remaining_local_classes']))))
