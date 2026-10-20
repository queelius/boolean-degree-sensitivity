"""Finite function domains with exact pointwise relations and explicit search trees."""
import numpy as np


class FunctionCSP:
    def __init__(self, tables, relations, point_order=None):
        assert tables and all(t.ndim == 2 for t in tables)
        self.tables = tables; self.points = tables[0].shape[1]
        assert self.points > 0 and all(t.shape[1] == self.points and np.issubdtype(t.dtype, np.integer) for t in tables)
        assert len(relations) == self.points
        self.order = list(range(self.points)) if point_order is None else list(point_order)
        assert sorted(self.order) == list(range(self.points))
        self.initial = tuple((1 << len(t))-1 for t in tables)
        self.parts = []
        for table in tables:
            assert len({row.tobytes() for row in table}) == len(table)
            self.parts.append([{int(v): int.from_bytes(np.packbits(table[:, x] == v, bitorder='little').tobytes(), 'little')
                                for v in np.unique(table[:, x])} for x in range(self.points)])
        unique = {}; self.relation_ids = []; self.relations = []
        for relation in relations:
            key = tuple(sorted(set(tuple(map(int, r)) for r in relation)))
            assert all(len(r) == len(tables) for r in key)
            if key not in unique:
                unique[key] = len(self.relations); self.relations.append(key)
            self.relation_ids.append(unique[key])
        self.support_cache = {}; self.support_queries = 0; self.cache_hits = 0

    def propagate(self, domains):
        domains = list(domains); steps = []
        if any(not d for d in domains): return tuple(domains), steps, -1
        changed = True
        while changed:
            changed = False
            for x in self.order:
                available = tuple(tuple(v for v, mask in self.parts[j][x].items() if mask & d) for j, d in enumerate(domains))
                key = self.relation_ids[x], available; self.support_queries += 1
                if key in self.support_cache:
                    support = self.support_cache[key]; self.cache_hits += 1
                else:
                    live = [r for r in self.relations[key[0]] if all(v in options for v, options in zip(r, available))]
                    support = tuple(tuple(sorted({r[j] for r in live})) for j in range(len(domains))) if live else None
                    self.support_cache[key] = support
                if support is None: return tuple(domains), steps, x
                updated = []
                for j, (d, values) in enumerate(zip(domains, support)):
                    keep = 0
                    for v in values: keep |= self.parts[j][x][v]
                    updated.append(d & keep)
                assert all(updated)
                if updated != domains:
                    domains = updated; steps.append(x); changed = True
        return tuple(domains), steps, None

    def split(self, domains):
        variable = min((j for j, d in enumerate(domains) if d.bit_count() > 1), key=lambda j: domains[j].bit_count())
        size = domains[variable].bit_count(); best = None; score = -1
        for x in self.order:
            for value, mask in self.parts[variable][x].items():
                left = domains[variable] & mask; count = left.bit_count()
                balance = min(count, size-count)
                if balance > score and balance > 0:
                    score = balance; best = variable, x, value, left
            if score == size//2: break
        assert best is not None
        return best

    def search(self, max_nodes=1000):
        assert type(max_nodes) is int and max_nodes >= 0
        visited = 0; witness = None
        def visit(domains):
            nonlocal visited, witness
            if visited >= max_nodes: return dict(kind='LIMIT')
            visited += 1
            domains, steps, bad = self.propagate(domains)
            if bad is not None: return dict(kind='UNSAT', propagation=steps, contradiction_point=bad)
            if all(d.bit_count() == 1 for d in domains):
                witness = [d.bit_length()-1 for d in domains]
                assert all(tuple(int(t[i, x]) for t, i in zip(self.tables, witness)) in self.relations[self.relation_ids[x]] for x in range(self.points))
                return dict(kind='SAT', propagation=steps, witness=witness)
            j, x, value, left_mask = self.split(domains)
            left = list(domains); left[j] = left_mask
            right = list(domains); right[j] ^= left_mask
            a = visit(tuple(left))
            c = visit(tuple(right)) if a['kind'] == 'UNSAT' else dict(kind='LIMIT')
            status = 'SAT' if witness is not None else ('UNSAT' if a['kind'] == c['kind'] == 'UNSAT' else 'UNKNOWN')
            return dict(kind=status, propagation=steps, split=dict(variable=j, point=x, value=value), children=[a, c])
        tree = visit(self.initial)
        status = 'UNKNOWN' if tree['kind'] == 'LIMIT' else tree['kind']
        return dict(status=status, nodes=visited, max_nodes=max_nodes, witness=witness, tree=tree,
                    support_queries=self.support_queries, support_cache_hits=self.cache_hits,
                    necessary_components_only=True)
