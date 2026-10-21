"""Portable exact positive, negative, completeness and tamper controls; MIT."""
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import importlib
import importlib.util
from itertools import combinations
import gzip
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT=Path(__file__).resolve().parent


@lru_cache(maxsize=1)
def catalog():
    return json.loads(gzip.decompress((ROOT/'data/graph-catalog.json.gz').read_bytes()))


class Controls(unittest.TestCase):
    def module(self,name):
        self.assertIsNotNone(importlib.util.find_spec(name),'Missing portable '+name+' implementation.')
        return importlib.import_module(name)

    def triangle_cover(self):
        return [dict(representatives=[[]],extensions=[]),
          dict(representatives=[[3]],extensions=[
            dict(parent_index=0,added_edge=3,target_index=0,old_to_target=[0,1,2]),
            dict(parent_index=0,added_edge=5,target_index=0,old_to_target=[0,2,1]),
            dict(parent_index=0,added_edge=6,target_index=0,old_to_target=[2,0,1])]),
          dict(representatives=[[3,5]],extensions=[
            dict(parent_index=0,added_edge=5,target_index=0,old_to_target=[0,1,2]),
            dict(parent_index=0,added_edge=6,target_index=0,old_to_target=[1,0,2])]),
          dict(representatives=[[3,5,6]],extensions=[
            dict(parent_index=0,added_edge=6,target_index=0,old_to_target=[0,1,2])])]

    def test_complete_triangle_augmentation_and_omission_map_tampering(self):
        m=self.module('graph_cover');grades=self.triangle_cover()
        result=m.verify_augmentation(grades,3,3)
        self.assertEqual(result,dict(representatives_by_grade=[1,1,1,1],missing_edge_extensions=6))
        bad=deepcopy(grades);bad[1]['extensions'].pop()
        with self.assertRaises(ValueError):m.verify_augmentation(bad,3,3)
        bad=deepcopy(grades);bad[2]['extensions'][1]['old_to_target']=[0,1,2]
        with self.assertRaises(ValueError):m.verify_augmentation(bad,3,3)

    def test_literal_coordinate_transport_checks_color_and_nonpermutation(self):
        m=self.module('graph_cover')
        m.check_transport([3,6],1,[3,5],2,[1,0,2],3)
        with self.assertRaises(ValueError):m.check_transport([3,6],1,[3,5],1,[1,0,2],3)
        with self.assertRaises(ValueError):m.check_transport([3,6],1,[3,5],2,[0,0,2],3)

    def test_known_profile_and_candidate_omission_are_checked(self):
        m=self.module('graph_cover');case=deepcopy(catalog()['canonical_cases'][7045])
        result=m.check_profile(case)
        self.assertEqual(result['capacity_passing_covers'],1)
        self.assertEqual(case['profile']['covers'][0]['candidate_quartics'],70)
        case['profile']['covers'][0]['quartic_masks'].pop()
        with self.assertRaises(ValueError):m.check_profile(case)

    def test_all_lower_parity_spaces_are_covered(self):
        m=self.module('graph_cover')
        for c in range(3,7):
            covers=m.even_subspaces(c,c-3)
            for k in range(c-2):
                for space in m.even_subspaces(c,k):
                    self.assertTrue(any(space<=cover for cover in covers))

    def test_quota_search_matches_naive_tiny_enumerator_and_negative(self):
        m=self.module('quota_search');n=6
        candidates=[sum(1<<v for v in vertices) for vertices in combinations(range(n),4)]
        seed=candidates[:3];targets=[sum((q>>j)&1 for q in seed) for j in range(n)]
        def boundary(family):
            value=0
            for q in family:value^=m.clique_boundary(q,n)
            return value
        target=boundary(seed)
        expected=sorted(sorted(f) for f in combinations(candidates,3) if
                        [sum((q>>j)&1 for q in f) for j in range(n)]==targets and boundary(f)==target)
        result=m.enumerate_families(candidates,targets,target,n,3,cpu_limit=5)
        self.assertEqual((result['status'],result['families']),('EXHAUSTED',expected))
        self.assertTrue(expected)
        result=m.enumerate_families(candidates,targets,target^1,n,3,cpu_limit=5)
        self.assertEqual((result['status'],result['families']),('EXHAUSTED',[]))
        result=m.enumerate_families(candidates,targets,target,n,3,cpu_limit=0)
        self.assertEqual(result['status'],'OPEN_CPU_LIMIT');self.assertTrue(result['frontier'])

    def test_exact_component_converse_and_changed_support(self):
        m=self.module('verify_packet');data=json.loads((ROOT/'data/components.json').read_text())
        result=m.verify_components(data)
        self.assertEqual(len(result),17)
        self.assertTrue(all(row['histogram']=={'-8':64,'0':768,'8':192} for row in result))
        self.assertTrue(all(row['real_degree']==4 and row['active_coordinates']<=9 for row in result))
        bad=deepcopy(data);bad['components'][0]['positive_quartics'][0]=15
        with self.assertRaises(ValueError):m.verify_components(bad)

    def test_component_scope_rejects_boolean_integer_alias(self):
        m=self.module('verify_packet');data=json.loads((ROOT/'data/components.json').read_text())
        data['parameters']['constant_coefficient']=True
        with self.assertRaises(ValueError):m.verify_components(data)

    def test_real_uncolored_bridge_and_omitted_link(self):
        m=self.module('verify_packet')
        augmentation=json.loads(gzip.decompress((ROOT/'data/augmentation.json.gz').read_bytes()))
        bridge=json.loads((ROOT/'data/frame-links.json').read_text())
        self.assertEqual(len(m.check_bridge(augmentation,catalog(),bridge)),329)
        bridge['links'].pop()
        with self.assertRaises(ValueError):m.check_bridge(augmentation,catalog(),bridge)

    def test_site_disabled_replay_entrypoint_from_unrelated_directory(self):
        with TemporaryDirectory() as directory:
            d=Path(directory);copy=d/'packet'
            shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('__pycache__','.coverage*'))
            result=subprocess.run([sys.executable,'-S',str(copy/'verify_packet.py'),'--check-files-only',
                                   '--output',str(d/'receipt.json')],cwd=d,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertFalse(json.loads((d/'receipt.json').read_text())['complete_proof_replay'])

    def test_family_set_comparison_catches_omission_and_duplicate(self):
        m=self.module('verify_packet')
        self.assertTrue(m.compare_family_sets([[15]],[[15]]))
        for changed in [[],[[23]],[[15],[15]]]:
            with self.assertRaises(ValueError):m.compare_family_sets(changed,[[15]])

    def test_file_pins_and_path_escape_are_rejected(self):
        m=self.module('verify_packet')
        with TemporaryDirectory() as directory:
            d=Path(directory);(d/'x').write_bytes(b'control')
            manifest=dict(files=[dict(path='x',sha256=sha256(b'control').hexdigest(),bytes=7)])
            m.check_files(d,manifest)
            (d/'x').write_bytes(b'tamper')
            with self.assertRaises(ValueError):m.check_files(d,manifest)
            manifest['files'][0]['path']='../x'
            with self.assertRaises(ValueError):m.check_files(d,manifest)


if __name__=='__main__':unittest.main()
