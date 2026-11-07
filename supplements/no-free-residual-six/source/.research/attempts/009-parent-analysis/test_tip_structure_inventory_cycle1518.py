import copy
import itertools
import unittest

from positive_tip_inventory_cycle1511 import derive_context
import tip_structure_inventory_cycle1518 as subject


def variables():
    return [sum(1<<v for v in c) for k in (2,3,4) for c in itertools.combinations(range(13),k)]


def fixture():
    # Accepted root7 literal link; a small labeled structural fixture only.
    faces=[50,76,104,112,140,146,162,168,196,208]
    c=dict(n=13,root=0,root_link=faces,source_to_physical=list(range(1,8)),
           special_edges=[dict(pair_mask=3,valence=3,quadratic_numerator=1),
                          dict(pair_mask=5,valence=3,quadratic_numerator=1),
                          dict(pair_mask=129,valence=6,quadratic_numerator=-2)])
    return derive_context(c,variables())


def value(row,assignment):
    return sum(a*assignment.get(m,0) for m,a in row['terms'])


class TipStructureTests(unittest.TestCase):
    def test_complete_rows_and_shared_pair_dedup(self):
        r=subject.rows_for_context(fixture(),variables())
        self.assertEqual(r['row_occurrences_before_deduplication'],135)
        self.assertEqual(len(r['added_rows']),134)
        self.assertEqual(r['ordinary_vertices'],[3,4,5,6,8,9,10,11,12])
        shared=[(row,p) for row,p in zip(r['added_rows'],r['row_provenance']) if row['key']['subject']==6]
        self.assertEqual(len(shared),1)
        self.assertEqual(shared[0][0]['key']['family'],'POSITIVE_TIP_OTHER_EDGE_VALENCE')
        self.assertEqual({p['vertex'] for p in shared[0][1]},{1,2})
        neg=next(row for row in r['added_rows'] if row['key']['family']=='NEGATIVE_TIP_DEGREE_INTERVAL')
        self.assertEqual(neg['key']['subject'],128)
        for row in r['added_rows']:
            self.assertEqual(row['terms'],sorted(row['terms']))
            self.assertEqual(len(row['terms']),len({m for m,a in row['terms']}))

    def test_exact_degree_and_absence_controls(self):
        rows=subject.rows_for_context(fixture(),variables())['added_rows']
        unit=rows[0];degree=rows[1]
        negative=next(row for row in rows if row['key']['family']=='NEGATIVE_TIP_DEGREE_INTERVAL')
        self.assertEqual((unit['lower'],unit['upper']),(0,0))
        self.assertEqual(value(unit,{}),0)
        self.assertEqual(value(unit,{unit['terms'][0][0]:1}),1)
        for selected,expected in [(6,False),(7,True),(8,False)]:
            assignment={m:1 for m,a in degree['terms'][:selected]}
            self.assertEqual(degree['lower']<=value(degree,assignment)<=degree['upper'],expected)
        for selected,expected in [(8,False),(9,True),(10,True),(11,True),(12,False)]:
            assignment={m:1 for m,a in negative['terms'][:selected]}
            self.assertEqual(negative['lower']<=value(negative,assignment)<=negative['upper'],expected)

    def test_conditional_valence_is_not_unconditional_presence(self):
        rows=subject.rows_for_context(fixture(),variables())['added_rows']
        ordinary=next(r for r in rows if r['key']['family']=='POSITIVE_TIP_OTHER_EDGE_VALENCE')
        pair=ordinary['key']['subject']; tetra=[m for m,a in ordinary['terms'] if m.bit_count()==4]
        self.assertEqual(len(tetra),55)
        self.assertIn([pair,-4],ordinary['terms'])
        for edge,count,expected in [(0,0,True),(0,1,False),(1,3,False),(1,4,True),(1,5,False)]:
            assignment={m:1 for m in tetra[:count]};assignment[pair]=edge
            self.assertEqual(value(ordinary,assignment)==0,expected)
        fixed=next(r for r in rows if r['key']['family']=='POSITIVE_TIP_A_EDGE_VALENCE')
        self.assertEqual(len(fixed['terms']),55)
        self.assertEqual((fixed['lower'],fixed['upper']),(5,5))
        self.assertEqual(value(fixed,{m:1 for m,a in fixed['terms'][:5]}),5)

    def test_noninvolutive_physical_relabeling(self):
        context=fixture(); p=[2,0,1,3,4,5,6,7,8,9,10,11,12]
        def move(m):return sum(1<<p[v] for v in range(13) if m>>v&1)
        c=dict(n=13,root=p[0],root_link=sorted(move(f) for f in context['root_link']),
               source_to_physical=[p[v] for v in context['source_to_physical']],
               special_edges=sorted([dict(e,pair_mask=move(e['pair_mask']))
                                     for e in context['special_edges']],key=lambda e:e['pair_mask']))
        moved=derive_context(c,variables())
        left=subject.rows_for_context(context,variables())['added_rows']
        right=subject.rows_for_context(moved,variables())['added_rows']
        signatures=lambda rows:{(tuple(map(tuple,r['terms'])),r['lower'],r['upper']) for r in rows}
        mapped=[dict(r,terms=sorted([[move(m),a] for m,a in r['terms']])) for r in left]
        self.assertEqual(signatures(mapped),signatures(right))

    def test_negative_only_context_kept(self):
        faces=[14,49,74,97,134,145,193,194,268,304,328,352,388,400]
        c=derive_context(dict(n=13,root=0,root_link=[f<<1 for f in faces],
            source_to_physical=list(range(1,10)),special_edges=[
                dict(pair_mask=1|(1<<v),valence=6,quadratic_numerator=-2)
                for v in (7,8,9)]),variables())
        r=subject.rows_for_context(c,variables())
        self.assertEqual(len(r['added_rows']),111)
        self.assertEqual(r['added_rows'][0]['lower'],9)

    def test_all4096_ordinary_degree_vectors(self):
        result=subject.rows_for_context(fixture(),variables())
        vertex=result['ordinary_vertices'][0]; vmask=1<<vertex
        rows=[row for row in result['added_rows']
              if row['key']['family']=='ORDINARY_VERTEX_NO_DEGREE11' and row['key']['subject']==vmask]
        self.assertEqual(len(rows),12)
        edges=sorted(m for m in variables() if m.bit_count()==2 and m&vmask)
        for vector in range(1<<12):
            assignment={m:(vector>>i)&1 for i,m in enumerate(edges)}
            passes=all(row['lower']<=value(row,assignment)<=row['upper'] for row in rows)
            self.assertEqual(passes,vector.bit_count()!=11)

    def test_missing_native_slot_corrupt_A_and_boolean_alias(self):
        for change in ('variables','opposite','tip','negative_sign','duplicate_tip'):
            c=fixture();v=variables()
            if change=='variables':v.pop()
            if change=='opposite':c['positive_tips'][0]['opposite_triangle_mask']^=8
            if change=='tip':c['positive_tips'][0]['tip']=True
            if change=='negative_sign':c['special_edges'][-1]['quadratic_numerator']=1
            if change=='duplicate_tip':c['positive_tips'].append(c['positive_tips'][0])
            with self.subTest(change=change),self.assertRaises(ValueError):subject.rows_for_context(c,v)


if __name__=='__main__':unittest.main()
