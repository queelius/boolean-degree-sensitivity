"""Independent graph-subset enumeration and exact cube/Walsh checks (MIT).

This module does not import the catalog producer or any research workspace.
The written a=2 exclusion is a separate mathematical proof in THEOREM.md.
"""
from argparse import ArgumentParser
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import comb, factorial
from pathlib import Path
from time import monotonic
import json

import numpy as np


class VerificationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def validate_row(row):
    require(isinstance(row, dict) and set(row) == {'exceptional_pair', 'cycle_edges'}, 'Invalid row fields.')
    pair, edges = row['exceptional_pair'], row['cycle_edges']
    require(type(pair) is int and 0 < pair < 1024 and pair.bit_count() == 2, 'Invalid exceptional pair.')
    require(isinstance(edges, list) and len(edges) == 5 and all(type(e) is int for e in edges) and
            len(set(edges)) == 5 and all(0 < e < 1024 and e.bit_count() == 2 and not e & pair for e in edges),
            'Cycle edges must be simple and avoid the exceptional pair.')
    degrees = Counter(v for e in edges for v in range(10) if e >> v & 1)
    require(len(degrees) == 5 and set(degrees.values()) == {2}, 'Edges do not form a simple five-cycle.')
    return pair, tuple(sorted(edges))


@lru_cache(maxsize=1)
def expected_keys():
    # Independent of rooted permutations: test every five-edge subset of K5.
    expected = set()
    for pair in combinations(range(10), 2):
        mask = sum(1 << v for v in pair)
        ordinary = set(range(10))-set(pair)
        for vertices in combinations(sorted(ordinary), 5):
            edges = [sum(1 << v for v in edge) for edge in combinations(vertices, 2)]
            for selected in combinations(edges, 5):
                if all(sum(bool(e & (1 << v)) for e in selected) == 2 for v in vertices):
                    expected.add((mask, tuple(sorted(selected))))
    return frozenset(expected)


def validate_catalog(payload):
    require(isinstance(payload, dict) and type(payload.get('schema_version')) is int and payload['schema_version'] == 1 and
            payload.get('kind') == 'DIVISIBLE_SINGLETON_BOUNDARY_CYCLE_CATALOG' and
            type(payload.get('outside_coordinates')) is int and payload['outside_coordinates'] == 10 and
            type(payload.get('constant_coefficient')) is int and payload['constant_coefficient'] == 1,
            'Wrong catalog claim or coefficient normalization.')
    require(payload.get('written_completeness_proof_required') is True and
            payload.get('actual_boolean_function') is False and payload.get('fourteen_variable_problem_solved') is False,
            'Finite catalog checking cannot promote mathematical scope.')
    count = comb(10, 2)*comb(8, 5)*factorial(4)//2
    rows = payload.get('forms')
    require(type(payload.get('expected_forms')) is int and payload['expected_forms'] == count and
            isinstance(rows, list) and len(rows) == count, 'Incomplete catalog size.')
    observed = [validate_row(row) for row in rows]
    require(len(set(observed)) == count, 'Repeated/aliased catalog row.')
    require(set(observed) == expected_keys(), 'Catalog differs from independent five-edge graph enumeration.')
    return observed


@lru_cache(maxsize=1024)
def character(mask):
    return np.array([1-2*((mask & x).bit_count() % 2) for x in range(1024)], dtype=np.int16)


def require_fourier_match(values, expected_coefficients):
    require(values.ndim == 2 and values.shape[1] == 1024 and expected_coefficients.shape == values.shape and
            np.issubdtype(values.dtype, np.integer) and np.issubdtype(expected_coefficients.dtype, np.integer),
            'Exact full cube arrays required.')
    transformed = values.astype(np.int32)
    for stride in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]:
        blocks = transformed.reshape((len(values), -1, 2*stride))
        left, right = blocks[:, :, :stride].copy(), blocks[:, :, stride:].copy()
        blocks[:, :, :stride], blocks[:, :, stride:] = left+right, left-right
    require(np.array_equal(transformed, expected_coefficients.astype(np.int32)*1024),
            'An exact Walsh coefficient, including a required zero, is incorrect.')


def check_batch(rows):
    values = np.empty((len(rows), 1024), dtype=np.int16)
    coefficients = np.zeros((len(rows), 1024), dtype=np.int32)
    for index, row in enumerate(rows):
        pair, edges = validate_row(row)
        edge_sum = sum((character(e) for e in edges), np.zeros(1024, dtype=np.int16))
        values[index] = (1-character(pair))*(1-edge_sum)
        coefficients[index, 0] = 1
        coefficients[index, pair] = -1
        for edge in edges:
            coefficients[index, edge] = -1
            coefficients[index, pair | edge] = 1
        require(int(values[index, 0]) == 0 and all(int(values[index, 1 << v]) ==
            (-8 if pair >> v & 1 else 0) for v in range(10)), 'Origin or singleton guard fails.')
    require(np.all(values % 8 == 0) and np.all(np.isin(values, [-8, 0, 8])), 'Cube divisibility/range fails.')
    require_fourier_match(values, coefficients)
    return values


def verify_catalog(payload, batch_size=256):
    require(type(batch_size) is int and 1 <= batch_size <= 4096, 'Positive bounded batch size required.')
    keys = validate_catalog(payload)
    histogram = Counter()
    rows = payload['forms']
    for start in range(0, len(rows), batch_size):
        values = check_batch(rows[start:start+batch_size])
        distinct, counts = np.unique(values, return_counts=True)
        histogram.update({str(int(v)): int(n) for v, n in zip(distinct, counts)})
    return dict(schema_version=1, status='EXACT_STANDALONE_CATALOG_CHECK_PASSED', forms_checked=len(keys),
        independent_expected_form_enumeration='ALL_FIVE_EDGE_SUBSETS_OF_EACH_ORDINARY_FIVE_SET',
        original_pair_choices=comb(10, 2), forms_per_pair=comb(8, 5)*12,
        cube_values_checked=len(rows)*1024, walsh_coefficients_checked=len(rows)*1024,
        value_histogram=dict(sorted(histogram.items())), constant_coefficient=1,
        negative_pair_coefficients_per_form=6, positive_quartic_coefficients_per_form=5,
        all_other_fourier_coefficients_zero=True,
        written_a2_completeness_proof_required=True, written_proof='THEOREM.md',
        finite_check_is_not_exhaustion_of_all_quartic_families=True,
        actual_boolean_function=False, fourteen_variable_problem_solved=False,
        formal_verification=False, human_review=False, novelty_established=False)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('catalog', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--batch-size', type=int, default=256)
    args = parser.parse_args()
    start = monotonic()
    raw = args.catalog.read_bytes()
    report = verify_catalog(json.loads(raw), args.batch_size)
    report.update(input_file=args.catalog.name, input_sha256=sha256(raw).hexdigest(), seconds=monotonic()-start)
    if args.output:
        with args.output.open('x') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
