"""Small structural/identity controls; no native propagation or solver."""
import copy
import itertools
import unittest

import positive_tip_inventory_cycle1511 as subject


def mask(vertices):
    return sum(1 << v for v in vertices)


def fixture(stacked=True):
    faces = [mask(t) for t in itertools.product((1, 2), (3, 4), (5, 6))]
    if stacked:
        old = mask((1, 3, 5))
        faces.remove(old)
        faces.extend(mask((7,) + edge) for edge in itertools.combinations((1, 3, 5), 2))
    n = 9
    variables = [mask(t) for k in (2, 3, 4) for t in itertools.combinations(range(n), k)]
    vertices = sorted({v for f in faces for v in range(n) if f >> v & 1})
    degrees = {v: sum(bool(f >> v & 1) for f in faces) for v in vertices}
    context = dict(n=n, root=0, root_link=sorted(faces),
                   source_to_physical=vertices, row_count=7,
                   model_id=dict(constant=1, native_identity=dict(
                       catalog_sha256='a' * 64, order=len(vertices), original_index=0)),
                   special_edges=[dict(pair_mask=(1 | (1 << v)), valence=d,
                                       quadratic_numerator=4-d)
                                  for v, d in degrees.items() if d in (3, 6)])
    return context, variables


class InventoryTests(unittest.TestCase):
    def test_positive_stacked_octahedron(self):
        context, variables = fixture()
        result = subject.derive_context(context, variables)
        self.assertEqual(len(result['positive_tips']), 1)
        p = result['positive_tips'][0]
        self.assertEqual((p['tip'], p['positive_edge_mask'], p['opposite_triangle_mask']),
                         (7, 129, mask((1, 3, 5))))
        self.assertEqual(p['native_triangle_variable_index'], variables.index(mask((1, 3, 5))))
        self.assertEqual(result['added_rows'][0]['terms'], [[mask((1, 3, 5)), 1]])
        self.assertEqual(result['added_rows'][1]['lower'], 7)
        self.assertEqual(result['added_rows'][1]['upper'], 8)
        self.assertEqual(len(result['added_rows'][1]['terms']), 8)
        self.assertIn([129, 1], result['added_rows'][1]['terms'])

    def test_no_positive_tip_is_retained(self):
        context, variables = fixture(False)
        result = subject.derive_context(context, variables)
        self.assertEqual(result['positive_tips'], [])
        self.assertEqual(result['added_rows'], [])

    def test_noninvolutive_full_coordinate_relabeling(self):
        context, variables = fixture()
        permutation = [2, 0, 1, 4, 3, 6, 5, 8, 7]
        def move(m):
            return sum(1 << permutation[v] for v in range(9) if m >> v & 1)
        other = copy.deepcopy(context)
        other['root'] = permutation[context['root']]
        other['root_link'] = sorted(move(f) for f in context['root_link'])
        other['source_to_physical'] = [permutation[v] for v in context['source_to_physical']]
        other['special_edges'] = sorted([
            dict(e, pair_mask=move(e['pair_mask'])) for e in context['special_edges']
        ], key=lambda e: e['pair_mask'])
        first = subject.derive_context(context, variables)
        second = subject.derive_context(other, variables)
        self.assertEqual(second['positive_tips'][0]['opposite_triangle_mask'],
                         move(first['positive_tips'][0]['opposite_triangle_mask']))
        self.assertEqual(second['positive_tips'][0]['tip'], permutation[7])
        self.assertEqual(second['positive_tips'][0]['degree_edge_masks'],
                         sorted(move(m) for m in first['positive_tips'][0]['degree_edge_masks']))

    def test_wrong_special_sign_or_alias_rejected(self):
        context, variables = fixture()
        for changed in ('sign', 'bool_sign', 'alias', 'face', 'root', 'variables', 'embedding'):
            with self.subTest(changed=changed):
                c, v = copy.deepcopy(context), variables[:]
                if changed == 'sign': c['special_edges'][0]['quadratic_numerator'] = -2
                if changed == 'bool_sign': c['special_edges'][0]['quadratic_numerator'] = True
                if changed == 'alias': c['special_edges'].append(c['special_edges'][0])
                if changed == 'face': c['root_link'].append(c['root_link'][0])
                if changed == 'root': c['root'] = True
                if changed == 'variables': v[0] = v[1]
                if changed == 'embedding': c['source_to_physical'][0] = 0
                with self.assertRaises(ValueError): subject.derive_context(c, v)

    def test_incomplete_or_non_surface_link_rejected(self):
        context, variables = fixture()
        context['root_link'].pop()
        with self.assertRaises(ValueError): subject.derive_context(context, variables)

    def test_native_identity_is_typed(self):
        good = fixture()[0]['model_id']
        self.assertEqual(subject.identity(good), ('a' * 64, 7, 0, 1))
        for c in [True, 3]:
            bad = copy.deepcopy(good); bad['constant'] = c
            with self.assertRaises(ValueError): subject.identity(bad)

    def test_complete_join_preserves_raw_vs_genuine_scope(self):
        context, variables = fixture()
        second = copy.deepcopy(context); second['model_id']['constant'] = 2
        contexts = [context, second]
        ids = [c['model_id'] for c in contexts]
        common = dict(n=9, variables=variables, row_count=10)
        packet = dict(completed=2, pending=0, expected_model_ids=ids, contexts=contexts)
        gate = dict(models_compared=2, variable_count=len(variables),
                    contexts=[dict(model_id=c['model_id'], rows=7) for c in contexts])
        frontier = dict(entries=[dict(model_id=c['model_id'],
            genuine_context_status='EXCLUDED', raw_row_model_status=s,
            genuine_exclusion_authority=dict(path='/proof', sha256='b'*64))
            for c, s in zip(contexts, ('EXCLUDED', 'OPEN'))])
        result = subject.inventory(common, packet, gate, frontier)
        self.assertEqual(result['genuine_context_counts'], {'EXCLUDED': 2})
        self.assertEqual(result['raw_row_counts'], {'EXCLUDED': 1, 'OPEN': 1})
        self.assertTrue(all(c['skip_future_queries'] for c in result['contexts']))
        self.assertEqual(result['contexts'][1]['raw_row_model_status'], 'OPEN')
        self.assertEqual(result['contexts'][0]['added_row_native_ids'], [17, 18])
        for altered in ('missing', 'duplicate', 'wrong_gate', 'pending', 'missing_proof', 'unknown_status'):
            p, g, f = copy.deepcopy(packet), copy.deepcopy(gate), copy.deepcopy(frontier)
            if altered == 'missing': f['entries'].pop()
            if altered == 'duplicate': p['contexts'][1] = p['contexts'][0]
            if altered == 'wrong_gate': g['contexts'][1]['model_id']['constant'] = 1
            if altered == 'pending': p['pending'] = 1
            if altered == 'missing_proof': f['entries'][0]['genuine_exclusion_authority'] = None
            if altered == 'unknown_status': f['entries'][0]['genuine_context_status'] = 'SAT'
            with self.subTest(altered=altered), self.assertRaises(ValueError):
                subject.inventory(common, p, g, f)


if __name__ == '__main__':
    unittest.main()
