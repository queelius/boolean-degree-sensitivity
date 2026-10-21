"""Exact tiny common-core controls conditional on C7; no producer imports."""
from collections import Counter
from itertools import combinations, permutations, product
from math import comb
import argparse
import json
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def character(mask, point):
    return -1 if (mask & point).bit_count() % 2 else 1


def coefficients(word):
    require(len(word) == 8 and all(type(t) is int and t in (0, 1) for t in word),
            'core word must have eight literal Boolean integers')
    return [2 * sum(character(u, x) * (1 - 2 * word[x]) for x in range(8))
            for u in range(8)]


def all_word_basis_control():
    checked = 0
    for word in product((0, 1), repeat=8):
        values = coefficients(word)
        for x in range(8):
            require(sum(values[u] * character(u, x) for u in range(8))
                    == 16 * (1 - 2 * word[x]), 'core Fourier reconstruction scale/sign')
            checked += 1
        require(values[7] == -4 * sum(character(7, x) * word[x] for x in range(8)),
                'highest core coefficient sign')
    return {'Boolean_core_words': 256, 'exact_reconstruction_inputs': checked}


def low_layer_words():
    return [list(word) for word in product((0, 1), repeat=8)
            if all(word[x] == 1 for x in (0, 1, 2, 4))]


def block_control():
    scalar_zero = [w for w in low_layer_words() if coefficients(w)[7] == 0]
    cycle = [w for w in scalar_zero if all(w[x] == 1 for x in (3, 5, 6))]
    off = [w for w in low_layer_words() if coefficients(w)[7] == 4]
    for word in off:
        active = sum(word[x] for x in (3, 5, 6))
        require(active - word[7] == 1 and active in (1, 2), 'offcycle truth constraint')
        top = word[7]
        expected = [-4 - 8 * top] + [None] * 7
        for i in (1, 2, 4):
            expected[i] = -4 + 8 * top - 8 * word[7 ^ i]
        for pair in (3, 5, 6):
            expected[pair] = 4 - 8 * word[pair]
        expected[7] = 4
        require(coefficients(word) == expected, 'offcycle full eight-sector formula')
    return {'cycle_words_with_pair_truths_one': cycle,
            'scalar_zero_alone_word_count': len(scalar_zero),
            'offcycle_words': off,
            'offcycle_pair_truth_counts': sorted(sum(w[x] for x in (3, 5, 6)) for w in off),
            'offcycle_full_sector_records': [{'word': w, 'B_sectors': coefficients(w)} for w in off]}


def scalar_control():
    edges = [(1 << i) | (1 << ((i + 1) % 7)) for i in range(7)]
    def value(y):
        return -3 + sum(character(e, y) for e in edges)
    return {'origin': value(0), 'cycle_units': [value(1 << i) for i in range(7)],
            'offcycle_units': [value(1 << i) for i in range(7, 11)],
            'full_scalar_histogram': dict(sorted(Counter(value(y) for y in range(2048)).items()))}


def forced_cycle_pair_truths():
    return [{'a': a, 'truth': t, 'other_positive_cofaces': r}
            for a, t, r in product((-1, 0), (0, 1), range(6)) if 4 * t == a + 2 + r]


def offcycle_link_control():
    edges = list(combinations(range(6), 2)); checked = inactive = four = five = 0
    for size in (0, 1, 4, 5):
        for chosen in combinations(edges, size):
            checked += 1
            degrees = [sum(v in e for e in chosen) for v in range(6)]
            if any(d % 2 for d in degrees):
                continue
            for a, truth in product((-1, 0), (0, 1)):
                if 4 * truth != a + size:
                    continue
                if not truth:
                    require(size == 0 and a == 0, 'inactive offcycle row must be empty')
                    inactive += 1
                else:
                    require(size in (4, 5) and all(d in (0, 2) for d in degrees),
                            'active offcycle link is not an ordinary cycle')
                    if size == 4:
                        four += 1
                    else:
                        five += 1
    return {'checked_graphs': checked, 'inactive_link_cases': inactive,
            'active_four_cycles': four, 'active_five_cycles': five}


def path_control():
    checked = 0
    for z in range(7):
        left, right = (z - 1) % 7, (z + 1) % 7
        choices = set(range(11)) - {z, left, right}
        # 11 is the third core vertex, not an outside coordinate.
        for count in (1, 2):
            for middle in permutations(sorted(choices), count):
                path = (left,) + middle + (right,)
                graph = {tuple(sorted((a, b))) for a, b in zip(path, path[1:])}
                graph |= {tuple(sorted((left, 11))), tuple(sorted((11, right)))}
                degrees = Counter(v for edge in graph for v in edge)
                require(len(graph) == count + 3 and set(degrees.values()) == {2},
                        'path plus known core segment is not a simple four/five cycle')
                checked += 1
    return {'cycle_vertices': 7, 'short_paths_per_vertex': 8,
            'long_paths_per_vertex': 56, 'literal_simple_cycle_checks': checked,
            'scope': 'Local path mechanism only; no compatible global triangle families enumerated.'}


def count_control():
    result = []
    for M in range(5):
        rows = [(q, P) for q in range(12) for P in range(comb(11, 3) + 1)
                if P - q == 4 and 3 * P - q == 14 + 4 * M]
        require(len(rows) == 1, 'count equations lack a unique necessary integer solution')
        q, P = rows[0]
        result.append({'M': M, 'q': q, 'P': P})
    return result


def offcycle_combination_control():
    blocks = block_control()['offcycle_words']; histogram = Counter(); all_large = 0
    for words in product(blocks, repeat=4):
        sizes = [sum(word[pair] for word in words) for pair in (3, 5, 6)]
        total = sum(sizes)
        require(4 <= total <= 8, 'four offcycle words give impossible total activity')
        histogram[total] += 1
        all_large += all(size >= 3 for size in sizes)
    return {'four_offcycle_combinations': sum(histogram.values()),
            'total_disk_interior_incidence_histogram': dict(sorted(histogram.items())),
            'all_three_row_interior_counts_at_least_three': all_large,
            'last_count_is_conditional_on_separate_disk_lower_bound': True}


def run():
    start = time.process_time()
    result = {'schema_version': 1, 'status': 'INDEPENDENT_CONDITIONAL_COMMON_CORE_NECESSARY_CONTROLS_PASS',
              'normalization': all_word_basis_control(), 'blocks': block_control(),
              'scalar': scalar_control(), 'cycle_pair_truth': forced_cycle_pair_truths(),
              'offcycle_link': offcycle_link_control(), 'cycle_paths': path_control(),
              'necessary_counts': count_control(), 'offcycle_combinations': offcycle_combination_control(),
              'C7_topology_assumed_not_proved': True, 'global_triangle_family_enumeration': False,
              'actual_Boolean_function_constructed': False, 'new_geometric_exclusion_accepted_here': False,
              'global_goal_complete': False, 'solver_runs': 0, 'ledger_changes': False}
    result['cpu_seconds'] = time.process_time() - start
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    result = run()
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'cpu_seconds': result['cpu_seconds'], 'status': result['status']}))


if __name__ == '__main__':
    main()
