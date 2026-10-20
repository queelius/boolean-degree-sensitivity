"""Replay open spines and project six pair domains onto remaining components.

Closed subtrees must already have an independent acceptance authority.
This helper does not verify those subtrees or certify global completeness.
"""
from functools import lru_cache
import numpy as np
from verify_core_fourier_envelope_certificate import literal_words


def open_frontier(solver, tree):
    result = []
    def visit(node, domains, path):
        if node['kind'] == 'UNSAT': return
        if node['kind'] == 'LIMIT': result.append((path, domains)); return
        assert node['kind'] == 'UNKNOWN'
        for x in node['propagation']:
            possible = [tuple(v for v, m in solver.parts[j][x].items() if m & d) for j, d in enumerate(domains)]
            live = [r for r in solver.relations[solver.relation_ids[x]] if all(v in p for v, p in zip(r, possible))]
            assert live
            updated = []
            for j, d in enumerate(domains):
                mask = 0
                for value in {r[j] for r in live}: mask |= solver.parts[j][x][value]
                updated.append(d & mask)
            assert all(updated) and tuple(updated) != domains
            domains = tuple(updated)
        split = node['split']; j, x, v = split['variable'], split['point'], split['value']
        chosen = domains[j] & solver.parts[j][x][v]
        assert chosen and chosen != domains[j]
        left = list(domains); right = list(domains); left[j] = chosen; right[j] ^= chosen
        visit(node['children'][0], tuple(left), path+(0,))
        visit(node['children'][1], tuple(right), path+(1,))
    visit(tree, solver.initial, ())
    return result


@lru_cache(None)
def guarded_words(weight, delta):
    rows = []
    for word, d, _, _ in literal_words((3, 12), 0):
        if d != delta: continue
        if any((weight+x.bit_count() in (0, 12, 13) and word >> x & 1) or
               (weight+x.bit_count() in (1, 2, 14) and not (word >> x & 1)) for x in range(16)):
            continue
        rows.append([sum((1-2*(word >> x & 1))*(-1 if (x & q).bit_count() % 2 else 1)
                         for x in range(16)) for q in range(16)])
    return np.asarray(rows, dtype=np.int16).reshape(-1, 16)


def pair_envelope(tables, domains, *, points=range(1024)):
    assert len(tables) == len(domains) == 6 and all(domains)
    indices = [[i for i in range(len(t)) if d >> i & 1] for t, d in zip(tables, domains)]
    assert all(indices)
    lower = []; upper = []; retained = []
    for x in points:
        rows = guarded_words(x.bit_count(), 1-(x & 1)-((x >> 1) & 1))
        valid = np.ones(len(rows), dtype=bool)
        for pair, table, selected in zip((3, 5, 6, 9, 10, 12), tables, indices):
            valid &= np.isin(rows[:, pair], np.unique(table[selected, x]))
        if not np.any(valid): raise ValueError(f'No core truth word at outside point {x}')
        lower.append(rows[valid].min(axis=0).astype(int).tolist())
        upper.append(rows[valid].max(axis=0).astype(int).tolist())
        retained.append(int(valid.sum()))
    return lower, upper, retained
