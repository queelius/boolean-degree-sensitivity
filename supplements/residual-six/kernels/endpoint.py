# Original code copyright(c)2026 Alexander Richard Towell; MIT.
"""Pure mathematical functions adapted from minus_three_links_independent_cycle1395.py; original source and AST equality are bundled."""
from collections import Counter, defaultdict
import itertools

def supports(rows, size):
    result = tuple((tuple(row) for row in rows))
    for row in result:
        if len(row) != size or any((type(v) is not int or v < 0 for v in row)) or tuple(sorted(set(row))) != row:
            raise ValueError('supports must have distinct sorted nonnegative integer labels')
    if len(set(result)) != len(result):
        raise ValueError('duplicate support')
    return tuple(sorted(result))

def graph_components(edges):
    edges = supports(edges, 2)
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    todo = set(adj)
    components = []
    while todo:
        stack = [min(todo)]
        reached = set(stack)
        while stack:
            for other in adj[stack.pop()] - reached:
                reached.add(other)
                stack.append(other)
        todo.difference_update(reached)
        components.append(tuple(sorted(reached)))
    return (tuple(components), dict(adj))

def cycle_components(edges):
    components, adj = graph_components(edges)
    if any((len(neighbors) != 2 for neighbors in adj.values())):
        raise ValueError('link is not 2-regular')
    return components

def vertex_link(facets, vertex):
    return tuple(sorted((tuple((v for v in f if v != vertex)) for f in facets if vertex in f)))

def triangle_summary(facets):
    facets = supports(facets, 3)
    edge_counts = Counter((e for f in facets for e in itertools.combinations(f, 2)))
    components, adj = graph_components(edge_counts)
    links = {v: vertex_link(facets, v) for v in adj}
    regular_links = []
    for v, link in links.items():
        try:
            valid = len(cycle_components(link)) == 1
        except ValueError:
            valid = False
        regular_links.append(valid)
    return {'V': len(adj), 'E': len(edge_counts), 'F': len(facets), 'chi': len(adj) - len(edge_counts) + len(facets), 'degrees': [len(adj[v]) for v in sorted(adj)], 'components': [list(c) for c in components], 'every_edge_twice': bool(facets) and all((n == 2 for n in edge_counts.values())), 'surface': bool(facets) and all((n == 2 for n in edge_counts.values())) and all(regular_links)}

def split_vertex(facets, vertex):
    facets = supports(facets, 3)
    vertices = {v for f in facets for v in f}
    if type(vertex) is not int or vertex not in vertices:
        raise ValueError('pivot must be an existing native vertex')
    before = triangle_summary(facets)
    if not before['every_edge_twice']:
        raise ValueError('all edges must have two faces before splitting')
    parts = cycle_components(vertex_link(facets, vertex))
    if len(parts) < 2:
        raise ValueError('pivot link must have multiple cycle components')
    if any((len(cycle_components(vertex_link(facets, v))) != 1 for v in vertices - {vertex})):
        raise ValueError('every other vertex link must be a circle')
    copies = tuple((max(vertices) + 1 + j for j in range(len(parts))))
    owner = {v: copy for part, copy in zip(parts, copies) for v in part}
    result = []
    for f in facets:
        if vertex not in f:
            result.append(f)
            continue
        others = tuple((v for v in f if v != vertex))
        if owner[others[0]] != owner[others[1]]:
            raise ValueError('a face crosses link components')
        result.append(tuple(sorted(others + (owner[others[0]],))))
    result = supports(result, 3)
    after = triangle_summary(result)
    if not after['surface'] or after['E'] != before['E'] or after['F'] != before['F'] or (after['V'] != before['V'] + len(parts) - 1):
        raise ValueError('split failed its literal incidence checks')
    return (result, copies)

def pair_link_controls():
    edges = tuple(itertools.combinations(range(6), 2))
    by_edges = Counter()
    tested = 0
    for size in (0, 1, 4, 5):
        for choice in itertools.combinations(edges, size):
            tested += 1
            _, adj = graph_components(choice)
            if any((len(neighbors) % 2 for neighbors in adj.values())):
                continue
            cycles = cycle_components(choice)
            if choice and (len(cycles) != 1 or len(cycles[0]) != size):
                raise ValueError('unexpected even baseline link')
            by_edges[str(size)] += 1
    return {'six_vertex_graphs_tested': tested, 'accepted_by_edges': dict(sorted(by_edges.items()))}

def pentagon_controls():
    rings = [(0,) + tail for tail in itertools.permutations(range(1, 5)) if tail[0] < tail[-1]]
    triples = tuple(itertools.combinations(range(5), 3))
    accepted = Counter()
    trials = 0
    for ring in rings:
        star = tuple((tuple(sorted((5, ring[i], ring[(i + 1) % 5]))) for i in range(5)))
        for complement in itertools.combinations(triples, 3):
            trials += 1
            summary = triangle_summary(star + complement)
            if summary['surface']:
                accepted[tuple(sorted(summary['degrees']))] += 1
    return {'labeled_universal_vertex_links': len(rings), 'trials': trials, 'surface_completions': sum(accepted.values()), 'degree_sequences': [{'degrees': list(k), 'count': v} for k, v in sorted(accepted.items())], 'target_degree_sequence_count': accepted[3, 4, 4, 4, 4, 5]}

def heptagon_controls():
    n = 7
    sides = {tuple(sorted((i, (i + 1) % n))) for i in range(n)}
    diagonals = tuple((e for e in itertools.combinations(range(n), 2) if e not in sides))
    tested = 0
    ears = Counter()
    for choice in itertools.combinations(diagonals, n - 3):
        tested += 1
        crossing = False
        for (a, b), (c, d) in itertools.combinations(choice, 2):
            if len({a, b, c, d}) == 4 and (a < c < b) != (a < d < b):
                crossing = True
                break
        if crossing:
            continue
        edges = sides | set(choice)
        inside = tuple((f for f in itertools.combinations(range(n), 3) if all((e in edges for e in itertools.combinations(f, 2)))))
        star = tuple((tuple(sorted((n,) + side)) for side in sorted(sides)))
        summary = triangle_summary(inside + star)
        if len(inside) != n - 2 or not summary['surface'] or summary['chi'] != 2:
            raise ValueError('noncrossing diagonals failed literal triangulation checks')
        ordinary = summary['degrees'][:n]
        ears[ordinary.count(3)] += 1
    return {'diagonal_sets_tested': tested, 'triangulations': sum(ears.values()), 'minimum_ears': min(ears), 'ear_histogram': dict(sorted(ears.items()))}

def run_controls():
    chi1 = []
    m0_sphere = []
    for n3, n4, n5 in itertools.product(range(14), repeat=3):
        n = n3 + n4 + n5
        if n < 4:
            continue
        curvature = 3 * n3 + 2 * n4 + n5
        if curvature == 6 and 3 * (n - 1) <= n * (n - 1) // 2:
            chi1.append([n3, n4, n5])
        if n3 == 1 and n <= 6 and (curvature == 12) and all((count == 0 or degree < n for degree, count in ((3, n3), (4, n4), (5, n5)))):
            m0_sphere.append([n3, n4, n5])
    return {'status': 'INDEPENDENT_ENDPOINT_LINK_SMALL_CONTROLS_PASS', 'baseline_pair_links': pair_link_controls(), 'chi1_degree345': chi1, 'm0_sphere_candidate_degree_counts': m0_sphere, 'pentagon': pentagon_controls(), 'heptagon': heptagon_controls(), 'global_goal_complete': False, 'target_derivative_search_performed': False, 'global_manifold_classification_performed': False}
