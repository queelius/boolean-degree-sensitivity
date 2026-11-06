import copy
import itertools
import unittest

import link_profile_reader_cycle1517 as reader
import verify_link_profiles_cycle1517 as wrapper


def mask(t):
    return sum(1 << v for v in t)


def octahedron():
    return [mask(t) for t in itertools.product((0, 1), (2, 3), (4, 5))]


class LiteralProfileTests(unittest.TestCase):
    def test_octahedron_and_stacked_positive(self):
        faces = octahedron()
        self.assertEqual(reader.analyze(6, faces), ([4]*6, 'ordinary'))
        faces.remove(mask((0, 2, 4)))
        faces += [mask((6,)+e) for e in itertools.combinations((0, 2, 4), 2)]
        degrees, kind = reader.analyze(7, faces)
        self.assertEqual(kind, 'positive_tip')
        self.assertEqual(degrees, [5, 4, 5, 4, 5, 4, 3])

    def test_literal_negative_and_two_exception_rejection(self):
        faces = [19,44,81,104,112,146,164,176,259,268,321,328,386,388]
        degrees, kind = reader.analyze(9, faces)
        self.assertEqual(kind, 'negative_tip')
        self.assertEqual(degrees.count(6), 1)
        # Hexagonal bipyramid: two degree6 vertices, not one negative tip.
        doubled = [mask((tip, i, (i+1)%6)) for tip in (6, 7) for i in range(6)]
        self.assertEqual(reader.analyze(8, doubled)[1], None)

    def test_noninvolutive_relabeling(self):
        faces = [19,44,81,104,112,146,164,176,259,268,321,328,386,388]
        p = [1,2,0,4,3,5,6,8,7]
        moved = [sum(1 << p[i] for i in range(9) if f >> i & 1) for f in faces]
        degrees, kind = reader.analyze(9, faces)
        other, other_kind = reader.analyze(9, moved)
        self.assertEqual(other_kind, kind)
        self.assertEqual([other[p[i]] for i in range(9)], degrees)

    def test_missing_duplicate_nonface_and_boolean_alias(self):
        faces = octahedron()
        for n, changed in [(6,faces[:-1]),(6,faces+[faces[0]]),(6,[True]+faces[1:]),
                           (6,[3]+faces[1:]),(7,faces),(True,faces)]:
            with self.subTest(n=n, changed=changed), self.assertRaises(ValueError):
                reader.analyze(n,changed)

    def test_profile_guard_table(self):
        self.assertEqual(reader.classify([3,4,4,4,5,5,5]), 'positive_tip')
        self.assertEqual(reader.classify([4,4,4,4,5,5,5,5,6]), 'negative_tip')
        self.assertEqual(reader.classify([4,5]*4), 'ordinary')
        for degrees in ([3,3,4,4,5,5], [3,4,4,5,6], [4,4,5,6,6], [4,5,7]):
            self.assertIsNone(reader.classify(degrees))

    def test_strict_output_comparison(self):
        wanted = dict(index=0, degrees=[4,5], kind='ordinary')
        self.assertTrue(reader.exact(wanted, copy.deepcopy(wanted)))
        self.assertFalse(reader.exact(wanted, dict(wanted,index=False)))
        self.assertFalse(reader.exact(wanted, dict(wanted,degrees=[4])))

    def test_native_index_and_selected_coverage(self):
        catalog=dict(status='COMPLETE_INVERSE_CONTRACTION_COVER',order=6,
                     classes=[dict(index=0,face_masks=octahedron())])
        records,total=wrapper.catalog_records(catalog)
        self.assertEqual((len(records),total),(1,1))
        for badindex in (1,False):
            bad=copy.deepcopy(catalog);bad['classes'][0]['index']=badindex
            with self.assertRaises(ValueError):wrapper.catalog_records(bad)
        proposal=dict(native_records_checked=1,catalogs_checked=[6],selected=records,
                      summary=dict(ordinary={'6':1},positive_tip={},negative_tip={}))
        self.assertEqual(wrapper.compare_proposal(proposal,records,1,[6]),proposal['summary'])
        for field,value in [('selected',[]),('native_records_checked',True),
                            ('summary',dict(ordinary={},positive_tip={},negative_tip={}))]:
            bad=dict(proposal);bad[field]=value
            with self.assertRaises(ValueError):wrapper.compare_proposal(bad,records,1,[6])


if __name__ == '__main__':
    unittest.main()
