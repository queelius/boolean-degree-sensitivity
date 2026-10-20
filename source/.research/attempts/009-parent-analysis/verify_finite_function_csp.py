"""Independent set-domain replay of a finite function constraint search tree."""
import numpy as np


def verify_tree(tables, relations, tree):
    assert tables and len(relations) == tables[0].shape[1]
    relations = [set(map(tuple, r)) for r in relations]
    n = len(tables); points = len(relations)
    def compatible(domains, x):
        assert type(x) is int and 0 <= x < points
        choices = [set(map(int, table[domain, x])) for table, domain in zip(tables, domains)]
        return [r for r in relations[x] if all(v in c for v, c in zip(r, choices))]
    def replay(node, domains):
        if node['kind'] == 'LIMIT':
            assert set(node) == {'kind'}
            return 'UNKNOWN'
        for x in node['propagation']:
            live = compatible(domains, x); assert live
            reduced = [domain[np.isin(table[domain, x], sorted({r[j] for r in live}))]
                       for j, (table, domain) in enumerate(zip(tables, domains))]
            assert all(len(d) for d in reduced) and any(len(a) < len(c) for a, c in zip(reduced, domains))
            domains = reduced
        if 'split' in node:
            split = node['split']; j, x, value = split['variable'], split['point'], split['value']
            assert type(j) is int and 0 <= j < n and type(x) is int and 0 <= x < points and type(value) is int
            select = tables[j][domains[j], x] == value
            assert np.any(select) and not np.all(select) and len(node['children']) == 2
            left = list(domains); right = list(domains)
            left[j] = domains[j][select]; right[j] = domains[j][~select]
            answers = [replay(node['children'][0], left), replay(node['children'][1], right)]
            expected = 'SAT' if 'SAT' in answers else ('UNSAT' if answers == ['UNSAT', 'UNSAT'] else 'UNKNOWN')
            assert node['kind'] == expected
            return expected
        if node['kind'] == 'UNSAT':
            point = node['contradiction_point']
            if point == -1: assert any(not len(d) for d in domains)
            else: assert not compatible(domains, point)
            return 'UNSAT'
        assert node['kind'] == 'SAT' and all(len(d) == 1 for d in domains)
        witness = [int(d[0]) for d in domains]; assert node['witness'] == witness
        assert all(tuple(int(t[i, x]) for t, i in zip(tables, witness)) in relations[x] for x in range(points))
        return 'SAT'
    return replay(tree, [np.arange(len(t), dtype=np.int64) for t in tables])
