"""Literal graph/marking/subspace certificate replay; standard library, MIT.
Adapted from the separately reviewed cycle1220 reader; no canonicalizer.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations

def require(condition, message):
    if not condition:
        raise ValueError(message)

def integer(value, low, high):
    return type(value) is int and low <= value <= high

def graph_edges(edges, n):
    require(integer(n, 1, 10), 'Invalid vertex count.')
    require(isinstance(edges, (list, tuple)) and all((integer(e, 1, (1 << n) - 1) and e.bit_count() == 2 for e in edges)) and (len(set(edges)) == len(edges)), 'Expected distinct literal pair masks.')
    return tuple(sorted(edges))

def image_mask(mask, permutation):
    return sum((1 << permutation[i] for i in range(len(permutation)) if mask >> i & 1))

def check_transport(source, source_color, target, target_color, permutation, n):
    source = graph_edges(source, n)
    target = graph_edges(target, n)
    require(integer(source_color, 0, (1 << n) - 1) and integer(target_color, 0, (1 << n) - 1), 'Invalid literal color mask.')
    require(isinstance(permutation, (list, tuple)) and len(permutation) == n and all((integer(i, 0, n - 1) for i in permutation)) and (len(set(permutation)) == n), 'Expected a literal vertex permutation.')
    require(tuple(sorted((image_mask(edge, permutation) for edge in source))) == target, 'Wrong literal edge transport.')
    require(image_mask(source_color, permutation) == target_color, 'Wrong literal color transport.')

def verify_augmentation(grades, n, max_edges):
    require(type(grades) is list and len(grades) == max_edges + 1, 'Missing augmentation grades.')
    require(grades[0] == {'representatives': [[]], 'extensions': []}, 'Missing empty-graph base.')
    all_edges = {1 << u | 1 << v for (u, v) in combinations(range(n), 2)}
    checked = 0
    for (degree, grade) in enumerate(grades):
        require(set(grade) == {'representatives', 'extensions'}, 'Wrong grade schema.')
        representatives = grade['representatives']
        require(type(representatives) is list and representatives, 'Empty graph grade.')
        keys = [graph_edges(graph, n) for graph in representatives]
        require(all((len(graph) == degree for graph in keys)) and len(set(keys)) == len(keys), 'Wrong or repeated graph representative.')
        if degree == 0:
            continue
        parents = grades[degree - 1]['representatives']
        expected = {(i, edge) for (i, graph) in enumerate(parents) for edge in all_edges - set(graph)}
        (seen, reached) = (set(), set())
        require(type(grade['extensions']) is list, 'Missing extension list.')
        for extension in grade['extensions']:
            require(set(extension) == {'parent_index', 'added_edge', 'target_index', 'old_to_target'}, 'Wrong extension schema.')
            (p, edge, target) = (extension[k] for k in ('parent_index', 'added_edge', 'target_index'))
            require(integer(p, 0, len(parents) - 1) and integer(target, 0, len(keys) - 1) and (type(edge) is int) and ((p, edge) in expected) and ((p, edge) not in seen), 'Missing, duplicate, or aliased extension identity.')
            check_transport(parents[p] + [edge], 0, representatives[target], 0, extension['old_to_target'], n)
            seen.add((p, edge))
            reached.add(target)
            checked += 1
        require(seen == expected and reached == set(range(len(keys))), 'The grade is not closed under every missing-edge extension.')
    return dict(representatives_by_grade=[len(g['representatives']) for g in grades], missing_edge_extensions=checked)

def connected_components(edges, n=10):
    adjacency = [set() for _ in range(n)]
    for edge in graph_edges(edges, n):
        (u, v) = [i for i in range(n) if edge >> i & 1]
        adjacency[u].add(v)
        adjacency[v].add(u)
    (unseen, masks) = (set(range(n)), [])
    while unseen:
        (pending, found) = ([min(unseen)], set())
        while pending:
            u = pending.pop()
            if u not in found:
                found.add(u)
                pending.extend(adjacency[u] - found)
        unseen -= found
        masks.append(sum((1 << i for i in found)))
    return sorted(masks)

def linear_span(basis):
    result = {0}
    for row in basis:
        result = result | {v ^ row for v in result}
    return frozenset(result)

@lru_cache(maxsize=None)
def even_subspaces(c, dimension):
    """Enumerate spaces as sets by span extension, not RREF bases."""
    require(integer(c, 1, 6) and integer(dimension, 0, c - 1), 'Invalid even-space dimensions.')
    ambient = tuple((v for v in range(1 << c) if v.bit_count() % 2 == 0))
    spaces = {frozenset((0,))}
    for _ in range(dimension):
        spaces = {space | frozenset((v ^ w for w in space)) for space in spaces for v in ambient if v not in space}
    return tuple(sorted(spaces, key=lambda s: tuple(sorted(s))))

def exact_integer_list(actual, expected, message):
    require(type(actual) is list and len(actual) == len(expected) and all((type(a) is int and a == e for (a, e) in zip(actual, expected))), message)

def check_profile(case):
    edges = graph_edges(case['negative_pairs'], 10)
    require(len(edges) == 8 and type(case['exceptional_mask']) is int and (case['exceptional_mask'] == 7), 'Wrong constant-one, three-exceptional graph slice.')
    groups = connected_components(edges)
    c = len(groups)
    require(3 <= c <= 6, 'Graph rank violates the signed-code necessary bound.')
    degrees = [sum((1 for edge in edges if edge >> j & 1)) for j in range(10)]
    targets = [degrees[j] + (4 if j < 3 else 0) for j in range(10)]
    reasons = []
    if max(targets) > 7:
        reasons.append('POSITIVE_INCIDENCE_EXCEEDS_SEVEN')
    if c == 3:
        if any((group.bit_count() == 1 and group & 7 for group in groups)):
            reasons.append('TIGHT_EXCEPTIONAL_ISOLATE')
        if any((group.bit_count() == 2 and group & 7 != group for group in groups)):
            reasons.append('TIGHT_ORDINARY_ISOLATED_EDGE')
    profile = case['profile']
    require(set(profile) == {'components', 'component_masks', 'negative_degrees', 'positive_incidence_targets', 'rejection_reasons', 'covers'}, 'Wrong profile schema.')
    require(type(profile['components']) is int and profile['components'] == c, 'Wrong component count.')
    exact_integer_list(profile['component_masks'], groups, 'Wrong component masks.')
    exact_integer_list(profile['negative_degrees'], degrees, 'Wrong negative degrees.')
    exact_integer_list(profile['positive_incidence_targets'], targets, 'Wrong positive incidence targets.')
    require(profile['rejection_reasons'] == reasons, 'Graph guards do not match their literal premises.')
    covers = profile['covers']
    require(type(covers) is list, 'Missing subspace cover list.')
    if reasons:
        require(covers == [], 'Rejected graph has unexpected cover records.')
        return dict(guards_pass=False, components=c, reasons=reasons, subspace_covers=0, capacity_passing_covers=0, universe_sizes=[], passing_sizes=[])
    (expected_spaces, seen) = (set(even_subspaces(c, c - 3)), set())
    quartets = [(sum((1 << j for j in vertices)), vertices) for vertices in combinations(range(10), 4)]
    (sizes, passing) = ([], [])
    for cover in covers:
        require(set(cover) == {'component_parity_basis', 'candidate_quartics', 'candidate_incidences', 'incidence_capacity_pass', 'quartic_masks'}, 'Wrong subspace cover schema.')
        basis = cover['component_parity_basis']
        require(type(basis) is list and len(basis) == c - 3 and all((integer(v, 1, (1 << c) - 1) and v.bit_count() % 2 == 0 for v in basis)), 'The purported basis is not in the correct even parity space.')
        space = linear_span(basis)
        require(len(space) == 1 << c - 3 and space in expected_spaces and (space not in seen), 'Dependent, aliased, or wrong-dimensional subspace.')
        seen.add(space)
        candidates = []
        for (mask, vertices) in quartets:
            if any((targets[j] == 0 and j in vertices or (targets[j] == 7 and j not in vertices) for j in range(10))):
                continue
            signature = sum((1 << k for (k, group) in enumerate(groups) if (group & mask).bit_count() % 2))
            if signature in space:
                candidates.append(mask)
        exact_integer_list(cover['quartic_masks'], candidates, 'Incomplete or aliased candidate quartet universe.')
        incidences = [sum((1 for mask in candidates if mask >> j & 1)) for j in range(10)]
        exact_integer_list(cover['candidate_incidences'], incidences, 'Wrong candidate incidence capacities.')
        require(type(cover['candidate_quartics']) is int and cover['candidate_quartics'] == len(candidates), 'Wrong candidate quartet count.')
        capacity = len(candidates) >= 7 and all((incidences[j] >= targets[j] and len(candidates) - incidences[j] >= 7 - targets[j] for j in range(10)))
        require(type(cover['incidence_capacity_pass']) is bool and cover['incidence_capacity_pass'] == capacity, 'Wrong necessary capacity result.')
        sizes.append(len(candidates))
        if capacity:
            passing.append(len(candidates))
    require(seen == expected_spaces, 'Missing maximal parity subspace: the necessary cover is incomplete.')
    return dict(guards_pass=True, components=c, reasons=[], subspace_covers=len(sizes), capacity_passing_covers=len(passing), universe_sizes=sizes, passing_sizes=passing)

def check_header(source):
    require(type(source.get('schema_version')) is int and source['schema_version'] == 1 and (source.get('status') == 'PROPOSED_COMPLETE_CANONICAL_GRAPH_AND_SUBSPACE_FEASIBILITY_CATALOG'), 'Wrong graph-cover source status.')
    require(source.get('independent_review') == 'PENDING' and all((source.get(key) is False for key in ('quartic_selection_search_performed', 'actual_boolean_function', 'whole_geometry_excluded', 'global_goal_complete'))), 'The graph-cover proposal overstates its scope.')
    expected = dict(vertices=10, negative_edges=8, exceptional_vertices=3, minimum_components=3, constant_coefficient=1, simple_positive_quartics_to_select=7)
    parameters = source.get('parameters')
    require(type(parameters) is dict and set(parameters) == set(expected) | {'cpu_budget_seconds'} and all((type(parameters.get(k)) is int and parameters[k] == v for (k, v) in expected.items())), 'Wrong graph-cover mathematical parameters.')

def check_marked_cover(raw, cases, eligible):
    require(type(raw) is list and len(raw) == len(eligible) and (type(cases) is list) and cases, 'Incomplete uncolored graph or colored case inventory.')
    all_markings = {sum((1 << j for j in group)) for group in combinations(range(10), 3)}
    (multiplicities, marked) = (Counter(), 0)
    for (actual, (index, graph)) in zip(raw, eligible):
        require(type(actual['source_grade_index']) is int and actual['source_grade_index'] == index and (actual['negative_pairs'] == list(graph)), 'Missing or aliased uncolored source graph.')
        transports = actual['exceptional_transports']
        require(type(transports) is list and len(transports) == len(all_markings), 'Missing exceptional markings.')
        seen = set()
        for transport in transports:
            (exception, case_id) = (transport['exceptional_mask'], transport['case_id'])
            require(type(exception) is int and exception in all_markings and (exception not in seen) and integer(case_id, 0, len(cases) - 1), 'Aliased exceptional marking or colored case.')
            check_transport(graph, exception, cases[case_id]['negative_pairs'], 7, transport['old_to_canonical'], 10)
            seen.add(exception)
            multiplicities[case_id] += 1
            marked += 1
        require(seen == all_markings, 'Incomplete exceptional coloring cover.')
    require(set(multiplicities) == set(range(len(cases))), 'Unreachable colored catalog case.')
    for (i, case) in enumerate(cases):
        require(type(case['raw_marked_set_multiplicity']) is int and case['raw_marked_set_multiplicity'] == multiplicities[i], 'Wrong marked-set multiplicity.')
    return marked
