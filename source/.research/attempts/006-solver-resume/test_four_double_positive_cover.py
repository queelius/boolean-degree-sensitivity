from itertools import combinations
import json
from pathlib import Path

import pytest

from four_double_positive_cover import build_report, candidate_cover, uncovered_pairs


def masks(n, k):
    return sorted(sum(1 << v for v in vertices) for vertices in combinations(range(n), k))


def directly_covered(positive, negatives, other_double=None, cubic=None):
    vertices = [v for v in range(positive.bit_length()) if positive >> v & 1]
    for a, b in combinations(vertices, 2):
        pair = (1 << a) | (1 << b)
        if not any(pair & q == pair for q in negatives) \
                and (other_double is None or pair & other_double != pair) \
                and (cubic is None or pair & cubic != pair):
            return False
    return True


def test_candidate_coverage_matches_literal_pair_quantifiers():
    negatives = (31, 227, 348, 440)
    report = candidate_cover(negatives, n=9, common_zero_count=0)
    positives = [p for p in masks(9, 5) if p not in negatives]
    expected_single = [p for p in positives if directly_covered(p, negatives)]
    expected_mixed = [(p, j) for p in positives for j in masks(9, 3)
                      if directly_covered(p, negatives, cubic=j)]
    expected_double = [(p, r) for p, r in combinations(positives, 2)
                       if directly_covered(p, negatives, other_double=r)
                       and directly_covered(r, negatives, other_double=p)]
    assert report['single_double_with_singleton_defect']['positive_quintics'] == expected_single
    assert [(row['positive_quintic'], row['cubic_support']) for row in
            report['single_double_with_cubic_defect']['placements']] == expected_mixed
    assert report['two_positive_doubles']['placements'] == [list(x) for x in expected_double]


def test_common_zero_singletons_spend_the_available_defect():
    negatives = (31, 227, 348, 440)
    one = candidate_cover(negatives, n=9, common_zero_count=1)
    two = candidate_cover(negatives, n=9, common_zero_count=2)
    assert one['single_double_with_singleton_defect']['additional_singleton_defects'] == 0
    assert one['single_double_with_cubic_defect']['placements'] == []
    assert one['two_positive_doubles']['placements'] == []
    assert all(not branch.get('placements', branch.get('positive_quintics', []))
               for branch in (two['single_double_with_singleton_defect'],
                              two['single_double_with_cubic_defect'],
                              two['two_positive_doubles']))


def test_uncovered_pair_is_not_covered_by_one_shared_vertex():
    positive = 31
    negatives = (47, 79, 143, 263)
    missing = uncovered_pairs(positive, negatives)
    assert missing
    pair = missing[0]
    one_vertex = pair & -pair
    assert not directly_covered(positive, negatives, other_double=one_vertex)


def test_guarded_domains_reject_bad_inputs():
    with pytest.raises(ValueError):
        candidate_cover((31, 31, 227, 348), n=9, common_zero_count=0)
    with pytest.raises(ValueError):
        candidate_cover((31, 227, 348, 440), n=9, common_zero_count=3)
    with pytest.raises(ValueError):
        candidate_cover((31, 227, 348, 440), n=8, common_zero_count=0)


def test_complete_source_has_no_positive_double_in_common_vertex_classes():
    report = build_report()
    common = [row for row in report['classes'] if row['common_zero_count']]
    assert len(common) == 9
    assert all(row['counts']['all_positive_double_placements'] == 0 for row in common)
    assert len(report['classes']) == 16
    assert report['whole_support_classes_excluded'] == 0


def test_report_binds_the_exact_sources():
    from hashlib import sha256
    report = build_report()
    assert report['status'] == 'NECESSARY_POSITIVE_DOUBLE_COVER_PENDING_INDEPENDENT_BINDING'
    for source in report['sources']:
        assert sha256(Path(source['path']).read_bytes()).hexdigest() == source['sha256']
