"""Exact quota-vertex enumeration; standard library, MIT.
Adapted from independent cycle1226; explicit checks also run under -O.
Only the historical __debug__ restriction is removed.
"""
from collections import Counter
from itertools import combinations
from math import comb
from time import process_time

def require(ok, message):
    if not ok:
        raise ValueError(message)

def clique_boundary(mask, n):
    return sum((1 << i for (i, (u, v)) in enumerate(combinations(range(n), 2)) if mask >> u & 1 and mask >> v & 1))

def in_span(vectors, target):
    pivots = {}
    for value in vectors:
        while value:
            p = value.bit_length() - 1
            if p in pivots:
                value ^= pivots[p]
            else:
                pivots[p] = value
                break
    while target:
        p = target.bit_length() - 1
        if p not in pivots:
            return False
        target ^= pivots[p]
    return True

def build_problem(case, cover_index):
    require(isinstance(case, dict) and type(case.get('case_id')) is int and (type(cover_index) is int) and (0 <= cover_index < len(case['profile']['covers'])), 'Native graph case and cover identities required.')
    edges = case['negative_pairs']
    exception = case['exceptional_mask']
    profile = case['profile']
    require(len(edges) == len(set(edges)) == 8 and all((type(e) is int and 0 < e < 1024 and (e.bit_count() == 2) for e in edges)) and (type(exception) is int) and (0 <= exception < 1024) and (exception.bit_count() == 3), 'Simple a1 ell3 colored negative graph required.')
    adjacency = [set() for _ in range(10)]
    for edge in edges:
        (u, v) = [j for j in range(10) if edge >> j & 1]
        adjacency[u].add(v)
        adjacency[v].add(u)
    remaining = set(range(10))
    groups = []
    while remaining:
        stack = [min(remaining)]
        seen = set()
        while stack:
            v = stack.pop()
            if v not in seen:
                seen.add(v)
                stack.extend(adjacency[v] - seen)
        remaining -= seen
        groups.append(sum((1 << v for v in seen)))
    groups.sort()
    degrees = list(map(len, adjacency))
    targets = [degrees[j] + 4 * (exception >> j & 1) for j in range(10)]
    c = len(groups)
    cover = profile['covers'][cover_index]
    basis = cover['component_parity_basis']
    require(3 <= c <= 6 and groups == profile['component_masks'] and (c == profile['components']) and (degrees == profile['negative_degrees']) and (targets == profile['positive_incidence_targets']) and (not profile['rejection_reasons']), 'Original graph profile differs from literal reconstruction.')
    span = {0}
    require(isinstance(basis, list) and len(basis) == c - 3, 'Wrong parity-subspace dimension.')
    for row in basis:
        require(type(row) is int and 0 < row < 1 << c and (row.bit_count() % 2 == 0) and (row not in span), 'Invalid or dependent even component-parity basis.')
        span |= {s ^ row for s in tuple(span)}
    candidates = []
    for vertices in combinations(range(10), 4):
        mask = sum((1 << v for v in vertices))
        if any((targets[v] == 0 and mask >> v & 1 or (targets[v] == 7 and (not mask >> v & 1)) for v in range(10))):
            continue
        parity = sum((1 << j for (j, group) in enumerate(groups) if (mask & group).bit_count() % 2))
        if parity in span:
            candidates.append(mask)
    incidence = [sum((mask >> v & 1 for mask in candidates)) for v in range(10)]
    capacity = len(candidates) >= 7 and all((incidence[v] >= targets[v] and len(candidates) - incidence[v] >= 7 - targets[v] for v in range(10)))
    require(candidates == cover['quartic_masks'] and len(candidates) == cover['candidate_quartics'] and (incidence == cover['candidate_incidences']) and (type(cover['incidence_capacity_pass']) is bool) and (capacity == cover['incidence_capacity_pass']), 'Exact candidate universe or capacity metadata differs.')
    boundary = 0
    for edge in edges:
        boundary ^= clique_boundary(edge, 10)
    return dict(n=10, choose=7, quartics=candidates, targets=targets, boundary=boundary, negative_pairs=edges, exceptional_mask=exception, case_id=case['case_id'], cover_index=cover_index)

def enumerate_families(candidates, targets, boundary, n, choose, cpu_limit=10, node_limit=1000000, branch_limit=10000):
    require(True and type(n) is int and (4 <= n <= 10) and (type(choose) is int) and (choose >= 0) and isinstance(candidates, list) and (len(candidates) == len(set(candidates))) and all((type(m) is int and 0 < m < 1 << n and (m.bit_count() == 4) for m in candidates)) and isinstance(targets, list) and (len(targets) == n) and all((type(q) is int and q >= 0 for q in targets)) and (type(boundary) is int) and (0 <= boundary < 1 << n * (n - 1) // 2) and (type(node_limit) is int) and (node_limit >= 0) and (type(branch_limit) is int) and (branch_limit >= 0) and (cpu_limit >= 0), 'Exact valid finite selection problem required.')
    start = process_time()
    stack = [dict(available_mask=(1 << len(candidates)) - 1, selected_ids=[])]
    families = []
    nodes = 0
    prunes = Counter()
    bits = [clique_boundary(m, n) for m in candidates]
    width = n * (n - 1) // 2
    vertex_masks = [sum((1 << i for (i, m) in enumerate(candidates) if m >> v & 1)) for v in range(n)]
    status = 'EXHAUSTED'
    while stack:
        if process_time() - start >= cpu_limit:
            status = 'OPEN_CPU_LIMIT'
            break
        if nodes >= node_limit:
            status = 'OPEN_NODE_LIMIT'
            break
        state = stack.pop()
        nodes += 1
        available = state['available_mask']
        selected = state['selected_ids']
        slots = choose - len(selected)
        quotas = [q - sum((candidates[i] >> v & 1 for i in selected)) for (v, q) in enumerate(targets)]
        residual = boundary
        for i in selected:
            residual ^= bits[i]
        if slots < 0 or sum(quotas) != 4 * slots or any((q < 0 or q > slots for q in quotas)):
            prunes['QUOTAS'] += 1
            continue
        if not slots:
            if not any(quotas) and residual == 0:
                families.append(sorted((candidates[i] for i in selected)))
            else:
                prunes['LEAF_BOUNDARY'] += 1
            continue
        for (v, q) in enumerate(quotas):
            if q == 0:
                available &= ~vertex_masks[v]
            elif q == slots:
                available &= vertex_masks[v]
        size = available.bit_count()
        if size < slots or any(((available & vertex_masks[v]).bit_count() < q or (available & ~vertex_masks[v]).bit_count() < slots - q for (v, q) in enumerate(quotas))):
            prunes['CAPACITY'] += 1
            continue
        ids = [i for i in range(len(candidates)) if available >> i & 1]
        if not in_span([bits[i] | 1 << width for i in ids], residual | slots % 2 << width):
            prunes['BINARY_SPAN'] += 1
            continue
        choices = [(comb((available & vertex_masks[v]).bit_count(), q), v) for (v, q) in enumerate(quotas) if q]
        (count, vertex) = min(choices)
        if count > branch_limit:
            stack.append(state)
            status = 'OPEN_BRANCH_LIMIT'
            break
        incident = [i for i in ids if candidates[i] >> vertex & 1]
        remainder = available & ~vertex_masks[vertex]
        for bundle in reversed(list(combinations(incident, quotas[vertex]))):
            stack.append(dict(available_mask=remainder, selected_ids=selected + list(bundle)))
    require(len(families) == len({tuple(f) for f in families}), 'Quota branching duplicated a family.')
    return dict(status=status, frontier=stack, nodes=nodes, prunes=dict(prunes), families=sorted(families), cpu_seconds=process_time() - start, exhausted=status == 'EXHAUSTED')
