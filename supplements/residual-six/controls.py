# Copyright (c) 2026 Alexander Richard Towell. MIT licensed.
# Adapted from independent cycle1386; see PROVENANCE.json for exact source pin.
# This file checks small combinatorial mechanisms, not old classification leaves.
"""Small independent controls for the written residual-six proof.

These controls do not decide a Boolean-function instance or re-prove the
inherited derivative obstructions. No producer or research solver is imported.
"""
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import cache
from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path
import sys
import time

@dataclass(frozen=True, order=True)
class ExceptionType:
    level: int
    value: int
    cost: int

def cost(level, value):
    if level == 1:
        return (value - 1) * (value - 2)
    if level == 3:
        return value * (value + 1)
    if level == 5:
        return value * (value - 1)
    raise ValueError('unsupported Fourier level')

@cache
def exception_types():
    return tuple((ExceptionType(level, value, cost(level, value)) for level in (1, 3, 5) for value in range(-8, 9) if (level != 5 or value >= 0) and 0 < cost(level, value) <= 6))

@cache
def allocations():
    types = exception_types()
    return tuple((a for size in range(4) for indices in combinations(range(len(types) + size - 1), size) for a in [tuple((types[x - j] for j, x in enumerate(indices)))] if sum((t.cost for t in a)) <= 6))

def validate_allocation_cover(rows):
    if len(rows) != len(set(rows)) or set(rows) != set(allocations()):
        raise ValueError('missing or aliased residual allocation')

def old_local_guard(constant, exceptions):
    if type(constant) is not int or any((t not in exception_types() or t.level == 1 or t.cost != 2 for t in exceptions)):
        raise ValueError('invalid old local coefficient context')
    if len(exceptions) == 0 and constant <= 3:
        return 'BASELINE'
    if len(exceptions) == 1:
        if exceptions[0].level == 5:
            return 'ONE_DOUBLE'
        if constant <= 3:
            return 'ONE_QUADRATIC'
    if len(exceptions) == 2 and constant in (1, 2):
        return 'TWO_WITH_DOUBLE' if any((t.level == 5 for t in exceptions)) else 'TWO_QUADRATICS'
    raise ValueError('old local theorem guard not established')

def _full_support_alias(types, masks):
    keys = [(t.level, m) for t, m in zip(types, masks) if m.bit_count() == t.level]
    return len(keys) != len(set(keys))

def route(types, masks):
    if len(types) != len(masks) or sum((t.cost for t in types)) > 6:
        raise ValueError('wrong allocation arity or budget')
    allowed = set(exception_types())
    if any((t not in allowed for t in types)):
        raise ValueError('invalid residual exception')
    if any((type(m) is not int or not 0 <= m < 16 or m.bit_count() > t.level for t, m in zip(types, masks))):
        raise ValueError('invalid incidence on four free coordinates')
    if _full_support_alias(types, masks):
        raise ValueError('two values or copies on the same complete support')
    if any((t.cost == 6 for t in types)):
        t, m = (types[0], masks[0])
        if m == 15:
            if t.level != 5 or t.value != 3:
                raise ValueError('uncovered cost-six type')
            return {'reason': 'TRIPLED_QUARTIC', 'free_coordinate': 0}
        v = next((v for v in range(4) if not m >> v & 1))
        return {'reason': 'OLD_LOCAL_BASELINE_CONSTANT', 'free_coordinate': v, 'guard': old_local_guard(1, ())}
    singleton_mask = 0
    for t, m in zip(types, masks):
        if t.level == 1:
            singleton_mask |= m
    for v in range(4):
        if singleton_mask >> v & 1:
            continue
        incident = tuple((t for t, m in zip(types, masks) if t.level != 1 and m >> v & 1))
        if len(incident) <= 2:
            guards = [old_local_guard(c, incident) for c in (1, 2)]
            if guards[0] != guards[1]:
                raise ValueError('constant-dependent missing old case')
            return {'reason': 'OLD_LOCAL_BASELINE_CONSTANT', 'free_coordinate': v, 'guard': guards[0]}
    if len(types) == 3 and all((t.level == 5 and t.value == 2 for t in types)) and (masks == (15, 15, 15)):
        return {'reason': 'THREE_DOUBLES_PRIVATE_TIP', 'free_coordinate': 0}
    raise ValueError('uncovered residual allocation/incidence')

def incidence_cover():
    counts, total, skipped, rows = (Counter(), 0, 0, [])
    for allocation in allocations():
        possibilities = [[m for m in range(16) if m.bit_count() <= t.level] for t in allocation]
        local = Counter()
        for masks in product(*possibilities):
            if _full_support_alias(allocation, masks):
                skipped += 1
                continue
            reason = route(allocation, masks)['reason']
            counts[reason] += 1
            local[reason] += 1
            total += 1
        rows.append({'types': [asdict(t) for t in allocation], 'incidence_cases': sum(local.values()), 'routes': dict(local)})
    return {'allocations': len(rows), 'incidence_cases': total, 'impossible_full_support_aliases_discarded': skipped, 'route_counts': dict(counts), 'allocation_rows': rows, 'three_double_common_four_cases': counts['THREE_DOUBLES_PRIVATE_TIP'], 'interpretation': 'Conservative incidence cover; no Boolean realizability claim.'}

def even_degrees(edges, weights, n):
    if len(edges) != len(weights) or len(edges) != len(set(edges)):
        raise ValueError('edge alias or weight arity')
    degrees = [0] * n
    for edge, weight in zip(edges, weights):
        if len(edge) != 2 or not 0 <= edge[0] < edge[1] < n or type(weight) is not int or (weight <= 0):
            raise ValueError('invalid weighted simple edge')
        for v in edge:
            degrees[v] += weight
    return all((x % 2 == 0 for x in degrees))

def baseline_link_sizes():
    return sorted({4 * m - a for m in (0, 1) for a in (-1, 0)})

def tripled_link_control():
    edges = list(combinations(range(6), 2))
    tested, valid = (0, 0)
    for heavy in edges:
        others = [e for e in edges if e != heavy]
        for length in range(3):
            for residual in combinations(others, length):
                tested += 1
                if 3 + length not in baseline_link_sizes():
                    continue
                if not even_degrees([heavy] + list(residual), [3] + [1] * length, 6):
                    continue
                valid += 1
                endpoint_sets = [set(e) for e in residual]
                shared = set.intersection(*endpoint_sets)
                if length != 2 or len(shared) != 1 or set.union(*endpoint_sets) - shared != set(heavy):
                    raise ValueError('even weighted link is not an endpoint path')
    return {'tested_links': tested, 'valid_links': valid, 'every_valid_residual_is_endpoint_path': True, 'scope': 'All heavy-edge plus at most two unit-edge configurations up to six vertices.'}

def triangle_completion_control():
    triangle = [(0, 1), (0, 2), (1, 2)]
    extra_edges = [e for e in combinations(range(7), 2) if e not in triangle]
    tested, even = (0, 0)
    for length in (1, 2):
        for extra in combinations(extra_edges, length):
            tested += 1
            even += even_degrees(triangle + list(extra), [1] * (3 + length), 7)
    return {'tested_completions': tested, 'even_completions': even, 'scope': 'All triangle plus one or two distinct unit edges up to seven vertices.'}

def quartic_forcing_control():
    cases = 0
    for d in combinations(range(7), 4):
        for z in set(range(7)) - set(d):
            for a, b, c, e in permutations(d):
                weights = {frozenset(d): 3}
                weights.update({frozenset(set(d) - {x} | {z}): 1 for x in d})
                for pair in combinations(d, 2):
                    if sum((w for s, w in weights.items() if set(pair) <= s)) != 5:
                        raise ValueError('wrong forced weighted inside-pair link')
                link = {tuple(sorted(s - {a, z})) for s, w in weights.items() if {a, z} <= s and w == 1}
                if link != set(combinations(sorted([b, c, e]), 2)):
                    raise ValueError('outside-pair link is not the forced triangle')
                cases += 1
    return {'labelled_cases': cases, 'outside_pair_link_size': 3}

def private_tip(doubles, exceptional_pairs, tip):
    if any((len(s) != 4 or tuple(sorted(set(s))) != s for s in doubles)) or len(doubles) != len(set(doubles)):
        raise ValueError('doubled support is invalid or aliased')
    if any((len(s) != 2 or tuple(sorted(set(s))) != s for s in exceptional_pairs)):
        raise ValueError('quadratic support is invalid')
    incident = [s for s in doubles if tip in s]
    if len(incident) != 1 or any((tip in s for s in exceptional_pairs)):
        raise ValueError('tip does not have the required incident-only domains')
    return incident[0]

def surface_summary(faces):
    if len(set(faces)) != len(faces) or any((len(t) != 3 or tuple(sorted(set(t))) != t for t in faces)):
        raise ValueError('triangles must be distinct literal triples')
    vertices = set().union(*(set(t) for t in faces))
    edges = set().union(*(set(combinations(t, 2)) for t in faces))
    degrees = Counter((sum((v in edge for edge in edges)) for v in vertices))
    return {'vertices': len(vertices), 'edges': len(edges), 'faces': len(faces), 'euler_characteristic': len(vertices) - len(edges) + len(faces), 'degree_counts': dict(sorted(degrees.items()))}

def closed_surface(faces):
    surface_summary(faces)
    if not faces:
        return False
    edge_uses = Counter((edge for face in faces for edge in combinations(face, 2)))
    if set(edge_uses.values()) != {2}:
        return False
    for v in set().union(*(set(t) for t in faces)):
        links = [set(t) - {v} for t in faces if v in t]
        vertices = set().union(*links)
        if any((sum((x in e for e in links)) != 2 for x in vertices)):
            return False
        reached = {min(vertices)}
        while True:
            new = reached | set().union(*(e for e in links if e & reached))
            if new == reached:
                break
            reached = new
        if reached != vertices:
            return False
    return True

def surface_control():
    chi_one = []
    for n3, n4, n5 in product(range(13), repeat=3):
        n = n3 + n4 + n5
        if 3 * n3 + 2 * n4 + n5 == 6 and n >= 6:
            chi_one.append([n3, n4, n5])
    sphere = [[a, b] for a in range(4) for b in range(4) if 9 + 2 * a + b == 12 and 3 + a + b <= 6]
    edges = list(combinations(range(6), 2))
    graph_count, face_count, surfaces = (0, 0, 0)
    for chosen in combinations(range(15), 12):
        graph = {edges[i] for i in chosen}
        if sorted((sum((v in e for e in graph)) for v in range(6))) != [3, 3, 3, 5, 5, 5]:
            continue
        graph_count += 1
        triangles = [t for t in combinations(range(6), 3) if set(combinations(t, 2)) <= graph]
        for faces in combinations(triangles, 8):
            face_count += 1
            surfaces += closed_surface(list(faces))
    return {'chi_one_curvature_options': chi_one, 'sphere_with_three_degree3_options': sphere, 'degree_sequence_graphs': graph_count, 'eight_face_candidates': face_count, 'closed_surfaces': surfaces, 'scope': 'Elementary small-surface arithmetic; no manifold/sphere catalog imports.'}

def normalization_control():
    derivative, ordinary, inversion = (0, 0, 0)
    for support in range(1, 32):
        if support.bit_count() % 2 != 1:
            continue
        for v in range(5):
            for x in range(32):
                x0, x1 = (x & ~(1 << v), x | 1 << v)
                chi0, chi1 = ((-1) ** (support & x0).bit_count(), (-1) ** (support & x1).bit_count())
                f0, f1 = (Fraction(1, 2) - Fraction(chi0, 32), Fraction(1, 2) - Fraction(chi1, 32))
                target = (-1) ** (support & ~(1 << v) & x).bit_count() if support >> v & 1 else 0
                if 16 * (f1 - f0) != target:
                    raise ValueError('derivative Fourier normalization')
                derivative += 1
    for pair in combinations(range(5), 2):
        for truth in (0, 1):
            p0, pi, pj, pij = (1, 0, 0, truth - 1)
            if pij - pi - pj + p0 != truth:
                raise ValueError('ordinary quadratic is not the original triple truth')
            ordinary += 1
    for size in (2, 4):
        for support in combinations(range(5), size):
            s = set(support)
            for order in (2, 3):
                for target in combinations(range(5), order):
                    actual = Fraction((-2) ** order, 16) if set(target) <= s else 0
                    expected = (Fraction(1, 4) if order == 2 else Fraction(-1, 2)) if set(target) <= s else 0
                    if actual != expected:
                        raise ValueError('quadratic/cubic Fourier inversion')
                inversion += 1
    return {'character_derivative_cases': derivative, 'ordinary_quadratic_cases': ordinary, 'quadratic_and_cubic_inversion_basis_cases': inversion}

def run_controls():
    start = time.process_time()
    allocation_rows = allocations()
    validate_allocation_cover(allocation_rows)
    result = {'schema_version': 1, 'status': 'INDEPENDENT_SMALL_CONTROLS_ONLY', 'normalization': normalization_control(), 'incidence': incidence_cover(), 'tripled_link': tripled_link_control(), 'triangle_completion': triangle_completion_control(), 'quartic_forcing': quartic_forcing_control(), 'surface': surface_control(), 'actual_boolean_function': False, 'whole_pattern_excluded': False, 'global_goal_complete': False, 'inherited_local_theorems_replayed': False}
    result['cpu_seconds'] = time.process_time() - start
    return result
