"""Generate cycle forms by rooted permutations. Copyright2026 A.R.Towell, MIT."""
from argparse import ArgumentParser
from itertools import combinations, permutations
from math import comb, factorial
from pathlib import Path
import json

N = 10


def make_catalog():
    forms = []
    for pair in combinations(range(N), 2):
        exceptional = sum(1 << v for v in pair)
        ordinary = [v for v in range(N) if v not in pair]
        for vertices in combinations(ordinary, 5):
            # Fix the least vertex, then identify the two orientations.
            for tail in permutations(vertices[1:]):
                if tail[0] > tail[-1]:
                    continue
                cycle = (vertices[0],) + tail
                edges = sorted((1 << cycle[i]) | (1 << cycle[(i+1) % 5]) for i in range(5))
                forms.append(dict(exceptional_pair=exceptional, cycle_edges=edges))
    return dict(schema_version=1, kind='DIVISIBLE_SINGLETON_BOUNDARY_CYCLE_CATALOG',
        outside_coordinates=N, constant_coefficient=1,
        expected_forms=comb(N, 2)*comb(N-2, 5)*factorial(4)//2,
        written_completeness_proof_required=True, actual_boolean_function=False,
        fourteen_variable_problem_solved=False, forms=forms)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    payload = make_catalog()
    with args.output.open('x') as stream:
        json.dump(payload, stream, separators=(',', ':'))
        stream.write('\n')
    print(json.dumps(dict(forms=len(payload['forms']), output=args.output.name)))


if __name__ == '__main__':
    main()
