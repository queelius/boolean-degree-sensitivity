"""Necessary positive-double support cover from a local ordinary-pair obstruction.

The cover enumerates supports, not symmetric Boolean functions. The four fixed
negative quintics have numerator -2. Defect four permits two cost-two exceptions;
accepted common-vertex zeros are charged before enumerating positive doubles.
"""
from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def subset_masks(n: int, size: int) -> tuple[int, ...]:
    return tuple(sorted(sum(1 << v for v in group)
                        for group in combinations(range(n), size)))


def pair_shadow(supports: tuple[int, ...]) -> frozenset[int]:
    return frozenset((1 << a) | (1 << b) for q in supports
                     for a, b in combinations((v for v in range(q.bit_length())
                                                if q >> v & 1), 2))


def uncovered_pairs(positive: int, negatives: tuple[int, ...]) -> tuple[int, ...]:
    covered = pair_shadow(negatives)
    return tuple(sorted(pair for pair in pair_shadow((positive,)) if pair not in covered))


def candidate_cover(negatives: tuple[int, ...], *, n: int,
                    common_zero_count: int) -> dict:
    if len(negatives) != 4 or len(set(negatives)) != 4 \
            or any(type(q) is not int or q.bit_count() != 5 or not 0 <= q < 1 << n
                   for q in negatives):
        raise ValueError('Expected four distinct five-subsets of the coordinate set.')
    if type(common_zero_count) is not int or not 0 <= common_zero_count <= 2:
        raise ValueError('At most two accepted common zero singletons fit defect four.')
    positives = tuple(q for q in subset_masks(n, 5) if q not in negatives)
    shadow = pair_shadow(negatives)
    uncovered = {}
    for q in positives:
        vertex_union = 0
        for pair in pair_shadow((q,)) - shadow:
            vertex_union |= pair
        uncovered[q] = vertex_union
    available_slots = 2 - common_zero_count
    single = [q for q in positives if uncovered[q] == 0] if available_slots >= 1 else []
    mixed = []
    double = []
    if available_slots >= 2:
        triples = subset_masks(n, 3)
        mixed = [dict(positive_quintic=q, cubic_support=j, cubic_values=[-2, 1])
                 for q in positives if uncovered[q].bit_count() <= 3
                 for j in triples if uncovered[q] & j == uncovered[q]]
        # If all five vertices occur in uncovered pairs, a distinct second
        # quintic cannot cover them. This removes no possible distinct pair.
        candidates = [q for q in positives if uncovered[q].bit_count() <= 4]
        double = [[q, r] for q, r in combinations(candidates, 2)
                  if uncovered[q] & r == uncovered[q]
                  and uncovered[r] & q == uncovered[r]]
    return {
        'single_double_with_singleton_defect': {
            'positive_quintics': single,
            'additional_singleton_defects': 1 - common_zero_count if single else None,
        },
        'single_double_with_cubic_defect': {'placements': mixed},
        'two_positive_doubles': {'placements': double},
    }


@lru_cache(maxsize=1)
def build_report() -> dict:
    geometry_path = HERE / 'empty-four-double-geometry.json'
    geometry = json.loads(geometry_path.read_text())
    selected = [row for row in geometry['classes']
                if row['top_screen']['status'] == 'pairwise_intersecting_open']
    records = []
    for row in selected:
        common_count = row['common_intersection'].bit_count()
        cover = candidate_cover(tuple(row['negative_supports']), n=14,
                                common_zero_count=common_count)
        counts = {
            'single_with_singleton': len(cover['single_double_with_singleton_defect']['positive_quintics']),
            'mixed_support_pairs': len(cover['single_double_with_cubic_defect']['placements']),
            'two_double_pairs': len(cover['two_positive_doubles']['placements']),
        }
        counts['all_positive_double_placements'] = sum(counts.values())
        records.append({
            'class_index': row['class_index'],
            'negative_supports': row['negative_supports'],
            'common_zero_singletons': [v for v in range(14) if row['common_intersection'] >> v & 1],
            'common_zero_count': common_count,
            'nonnegative_top_without_doubles_remains_open': True,
            'counts': counts, 'cover': cover,
        })
    paths = [Path(__file__), geometry_path,
             HERE.parent / '009-parent-analysis' / 'empty-four-double-geometry-accepted-manifest.json',
             HERE.parent / '009-parent-analysis' / 'empty-pair-single-positive-double-link.md',
             HERE / 'empty-pair-positive-double-independent-math-audit.json']
    return {
        'status': 'NECESSARY_POSITIVE_DOUBLE_COVER_PENDING_INDEPENDENT_BINDING',
        'global_status': 'OPEN', 'whole_support_classes_excluded': 0,
        'scope': 'Sixteen pairwise-intersecting empty-profile four-negative-double geometries.',
        'coverage': 'Every positive doubled quintic must have each pair covered by a negative quintic, the sole other double, or the sole exceptional cubic.',
        'classes': records,
        'counts': {
            'classes': len(records),
            'common_vertex_classes_without_any_positive_double': sum(
                r['common_zero_count'] > 0 and r['counts']['all_positive_double_placements'] == 0
                for r in records),
            **{key: sum(r['counts'][key] for r in records)
               for key in ('single_with_singleton', 'mixed_support_pairs', 'two_double_pairs')},
        },
        'sources': [{'path': str(path), 'sha256': sha256(path.read_bytes()).hexdigest()}
                    for path in paths],
    }


if __name__ == '__main__':
    output = HERE / 'four-double-positive-cover.json'
    if output.exists():
        raise SystemExit('Refusing to overwrite the saved support cover.')
    report = build_report()
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['counts'], sort_keys=True))
