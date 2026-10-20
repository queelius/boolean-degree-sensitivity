"""Resume a checked partial tree after appending necessary pointwise relations.

Old points and domain row indices must be unchanged. Checked closed subtrees
remain valid. The new relations are first applied at unresolved frontiers;
an immediate added-relation contradiction can also close an old open node.
"""
from finite_function_csp import FunctionCSP


class PriorityPointCSP(FunctionCSP):
    def __init__(self, tables, relations, point_order=None, *, priority_point):
        super().__init__(tables, relations, point_order)
        assert type(priority_point) is int and 0 <= priority_point < self.points
        self.priority_point = priority_point

    def split(self, domains):
        x = self.priority_point; options = []
        for j, d in enumerate(domains):
            possible = [(value, d & mask) for value, mask in self.parts[j][x].items() if d & mask]
            if len(possible) > 1: options.append((len(possible), d.bit_count(), j, possible))
        if not options: return super().split(domains)
        _, size, j, possible = min(options, key=lambda r: r[:3])
        value, left = max(possible, key=lambda r: min(r[1].bit_count(), size-r[1].bit_count()))
        return j, x, value, left


def node_count(tree):
    stack = [tree]; count = 0
    while stack:
        node = stack.pop()
        if node['kind'] != 'LIMIT': count += 1; stack.extend(node.get('children', []))
    return count


def resume_search(solver, previous_tree, *, max_new_nodes, added_point=None):
    assert previous_tree['kind'] in ('UNSAT', 'UNKNOWN', 'LIMIT')
    assert type(max_new_nodes) is int and max_new_nodes >= 0
    prior = node_count(previous_tree); new_nodes = 0; witness = None; reused = 0; shortened = 0
    def live_tuples(domains, x):
        choices = [tuple(v for v, mask in solver.parts[j][x].items() if mask & d) for j, d in enumerate(domains)]
        return [r for r in solver.relations[solver.relation_ids[x]] if all(v in c for v, c in zip(r, choices))]
    def apply_steps(domains, steps):
        for x in steps:
            live = live_tuples(domains, x); assert live
            updated = []
            for j, d in enumerate(domains):
                mask = 0
                for value in {r[j] for r in live}: mask |= solver.parts[j][x][value]
                updated.append(d & mask)
            assert all(updated) and tuple(updated) != domains
            domains = tuple(updated)
        return domains
    def combine(steps, split, children):
        statuses = [c['kind'] for c in children]
        status = 'SAT' if 'SAT' in statuses else ('UNSAT' if statuses == ['UNSAT', 'UNSAT'] else 'UNKNOWN')
        return dict(kind=status, propagation=steps, split=split, children=children)
    def new_visit(domains):
        nonlocal new_nodes, witness
        if new_nodes >= max_new_nodes: return dict(kind='LIMIT')
        new_nodes += 1; domains, steps, bad = solver.propagate(domains)
        if bad is not None: return dict(kind='UNSAT', propagation=steps, contradiction_point=bad)
        if all(d.bit_count() == 1 for d in domains):
            witness = [d.bit_length()-1 for d in domains]
            assert all(tuple(int(t[i, x]) for t, i in zip(solver.tables, witness)) in solver.relations[solver.relation_ids[x]] for x in range(solver.points))
            return dict(kind='SAT', propagation=steps, witness=witness)
        j, x, v, chosen = solver.split(domains); left = list(domains); right = list(domains)
        left[j] = chosen; right[j] ^= chosen
        a = new_visit(tuple(left)); c = new_visit(tuple(right)) if a['kind'] == 'UNSAT' else dict(kind='LIMIT')
        return combine(steps, dict(variable=j, point=x, value=v), [a, c])
    def revisit(node, domains):
        nonlocal reused, shortened
        if node['kind'] == 'UNSAT': reused += node_count(node); return node
        if node['kind'] == 'LIMIT': return new_visit(domains)
        assert node['kind'] == 'UNKNOWN'
        reduced = apply_steps(domains, node['propagation'])
        if added_point is not None and not live_tuples(reduced, added_point):
            shortened += 1
            return dict(kind='UNSAT', propagation=node['propagation'], contradiction_point=added_point)
        split = node['split']; j, x, v = split['variable'], split['point'], split['value']
        chosen = reduced[j] & solver.parts[j][x][v]; assert chosen and chosen != reduced[j]
        left = list(reduced); right = list(reduced); left[j] = chosen; right[j] ^= chosen
        a = revisit(node['children'][0], tuple(left))
        c = node['children'][1] if witness is not None else revisit(node['children'][1], tuple(right))
        return combine(node['propagation'], split, [a, c])
    tree = revisit(previous_tree, solver.initial); status = 'UNKNOWN' if tree['kind'] == 'LIMIT' else tree['kind']
    count = node_count(tree); assert count <= prior+new_nodes
    return dict(status=status, nodes=count, max_nodes=prior+max_new_nodes, witness=witness, tree=tree,
                new_nodes_explored=new_nodes, prior_certificate_nodes=prior,
                reused_closed_nodes=reused, added_relation_shortened_nodes=shortened,
                necessary_components_only=True)
