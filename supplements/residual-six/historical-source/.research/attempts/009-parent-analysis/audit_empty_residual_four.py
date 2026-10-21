"""Independent finite scope accounting for the residual-four theorem transfer."""
from collections import Counter
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SIX = HERE.parent/'006-solver-resume'


def key(row):
    return json.dumps(row, sort_keys=True, separators=(',', ':'))


def expected_cases():
    # Solving the three integer quadratic inequalities for defect <=4
    # gives these five cost-two departures; the next cost is six.
    types = ((1, 0), (1, 3), (3, -2), (3, 1), (5, 2))
    rows, allocations = [], 0
    for count in range(3):
        for allocation in combinations_with_replacement(types, count):
            allocations += 1
            nonsingletons = tuple(t for t in allocation if t[0] != 1)
            constants = {1, 2} | {v for degree, v in allocation if degree == 1}
            for bits in product((False, True), repeat=len(nonsingletons)):
                incident = tuple(t for t, chosen in zip(nonsingletons, bits) if chosen)
                intersections = (0, 1) if len(incident) == 2 and all(d == 3 for d, v in incident) else (None,)
                for constant, intersection in product(constants, intersections):
                    if len(incident) <= 1:
                        theorem = 'at_most_one_incident_exception_constant_at_most_three'
                    elif any(d == 5 for d, v in incident):
                        theorem = 'two_exceptions_including_doubled_positive_quartic'
                    elif all(v == 1 for d, v in incident):
                        theorem = 'two_positive_quadratics'
                    elif intersection == 0:
                        theorem = 'two_disjoint_quadratics_with_a_negative'
                    elif all(v == -2 for d, v in incident):
                        theorem = 'two_adjacent_negative_quadratics'
                    else:
                        theorem = 'two_adjacent_mixed_quadratics'
                    assert constant <= 3 and (len(incident) < 2 or constant in (1, 2))
                    rows.append(dict(global_exceptions=[dict(degree=d, value=v) for d, v in allocation],
                                     global_cost=2*count,
                                     incident_nonsingleton_exceptions=[dict(degree=d, value=v) for d, v in incident],
                                     constant=constant, pair_intersection=intersection, theorem=theorem))
    return allocations, Counter(map(key, rows))


def check_report(report, ledger):
    assert report['status'] == 'PROPOSED_TRANSFER_OF_ACCEPTED_LOCAL_THEOREMS'
    assert report['global_status'] == 'OPEN' and report['whole_patterns_excluded'] == 0
    allocations, rows = expected_cases()
    assert report['global_allocation_count'] == allocations
    assert report['local_case_count'] == sum(rows.values())
    assert Counter(map(key, report['local_cases'])) == rows
    expected = []
    for row in ledger['empty_pair']['patterns']:
        if row['status'] == 'excluded':
            continue
        magnitudes = row['negative_magnitudes']
        cost = sum(k*(k+1) for k in magnitudes)
        residual = ledger['empty_pair']['defect_budget']-cost
        assert cost == row['negative_defect'] and residual == row['remaining_defect']
        if residual > 4:
            continue
        components = next(c for c in range(1, len(magnitudes)+1) if len(magnitudes)+3*c+1 >= 14)
        expected.append(dict(negative_magnitudes=magnitudes, remaining_defect=residual,
                             necessary_negative_union_size=14, necessary_johnson_components=components,
                             new_relative_to_residual_two_theorem=residual > 2))
    assert report['covered_open_patterns'] == expected
    assert report['new_residual_four_open_patterns'] == [r for r in expected if r['remaining_defect'] > 2]
    return dict(global_allocations=allocations, local_cases=sum(rows.values()),
                covered_open_patterns=len(expected), new_patterns=sum(r['remaining_defect'] > 2 for r in expected))


def audit():
    report_path, ledger_path = SIX/'empty-residual-four-cover.json', SIX/'empty-residual-four-ledger-input.json'
    report, ledger = (json.loads(p.read_text()) for p in (report_path, ledger_path))
    counts = check_report(report, ledger)
    assert sha256(ledger_path.read_bytes()).hexdigest() == report['ledger_snapshot']['sha256']
    direct, authorities = 0, []
    for source in report['authorities']:
        path = ROOT/source['path']
        assert sha256(path.read_bytes()).hexdigest() == source['sha256']
        manifest = json.loads(path.read_text())
        assert manifest['status'] == source['accepted_status']
        entries = manifest.get('files', manifest.get('artifacts'))
        if isinstance(entries, dict):
            entries = [dict(path=p, sha256=d) for p, d in entries.items()]
        assert entries
        for entry in entries:
            assert sha256((ROOT/entry['path']).read_bytes()).hexdigest() == entry['sha256']
            direct += 1
        authorities.append(path)
    assert direct == report['source_hash_checks']
    paths = [Path(__file__), report_path, ledger_path, *authorities]
    return dict(status='INDEPENDENT_RESIDUAL_FOUR_SCOPE_ACCOUNTING_PASS', global_status='UNRESOLVED',
                counts=counts, immediate_source_hashes_checked=direct,
                limitation='Mathematical transfer relies on the explicitly accepted local derivative theorems; no historical census regenerated.',
                sources=[dict(path=str(p), sha256=sha256(p.read_bytes()).hexdigest()) for p in paths])


if __name__ == '__main__':
    target = HERE/'empty-residual-four-independent-audit.json'
    assert not target.exists()
    report = audit()
    target.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('status', 'counts', 'immediate_source_hashes_checked')}))
