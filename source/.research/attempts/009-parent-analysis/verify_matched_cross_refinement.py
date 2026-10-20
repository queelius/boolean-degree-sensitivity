"""Independent literal character sums and cross-intersection column checks."""
from argparse import ArgumentParser
from itertools import combinations
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate

H = Path(__file__).resolve().parent


def run(source_path, output):
    assert not output.exists(); start = monotonic(); b = Bindings(); source = b.read(source_path)
    assert source['status'] == 'PROPOSED_MATCHED_ORDINARY_CROSS_REFINEMENT'
    base = b.read(source['base_refinement']['path'], source['base_refinement']['sha256'])
    assert base['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_SAFE_COUNT_REFINEMENT' and base['complete_actual_cover'] is True
    original = b.read(base['base_refinement']['path'], base['base_refinement']['sha256'])
    assert original['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT' and original['complete_actual_cover'] is True
    quota = b.read(original['base_authority']['path'], original['base_authority']['sha256'])
    assert quota['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    instance = read_certificate(b, quota['instance']); proof = read_certificate(b, source['proof'])
    assert proof['base_refinement'] == source['base_refinement'] and proof['quotient_authority'] == original['base_authority']
    assert source['geometry_index'] == proof['geometry_index'] == base['geometry_index'] == quota['geometry_index']
    positives = quota['geometry']['positive_doubles']; apex = positives[0] ^ positives[1]
    assert apex.bit_count() == 2 and {v for v in range(14) if apex >> v & 1} == set(instance['outside'][:2])
    assert all(n & 3 for c in instance['components'] for n in c.get('negative', []))
    pairs = instance['core_pair_order']; assert proof['core_pair_order'] == pairs
    core = set(range(4)); pair_sets = [{i for i in core if p >> i & 1} for p in pairs]
    partners = [(j,k) for j in range(len(pairs)) for k in range(j+1,len(pairs)) if pair_sets[j].isdisjoint(pair_sets[k]) and pair_sets[j] | pair_sets[k] == core]
    assert len(partners) == 3
    checked_relations = 0
    for relation in instance['relation_types']:
        if relation['delta'] != 0: continue
        for row in relation['tuples']:
            assert sum(row[j]*row[k] for j,k in partners) == 0
            checked_relations += 1
    assert checked_relations
    triples = [sum(1 << i for i in c) for c in combinations(range(2,10),3)]
    assert proof['ordinary_triples'] == triples and proof['old_point_count'] == 1026
    characters = np.array([[1-2*((x & (t >> 2)).bit_count() % 2) for t in triples] for x in range(256)], dtype=np.int32)
    features = []; columns = []; checked_candidates = 0
    assert len(proof['components']) == len(pairs)
    for j, (component, record) in enumerate(zip(instance['components'], proof['components'])):
        assert record['component_index'] == j
        values = np.load(component['values']['path'], allow_pickle=False)
        if j == quota['component_index']: values = np.stack([values[i] for i in quota['selected_row_indices']])
        expected = np.empty((len(values), len(triples)), dtype=np.int8)
        for lo in range(0,len(values),512):
            chunk = values[lo:lo+512].astype(np.int32)
            summed = sum(chunk[:,r::4] for r in range(4))
            coefficients = summed @ characters
            assert np.all((coefficients == 0) | (coefficients == 1024))
            expected[lo:lo+len(chunk)] = coefficients // 1024
        stored = np.load(record['features']['path'], allow_pickle=False)
        assert record['rows'] == len(values) and stored.dtype == np.int8 and np.array_equal(stored,expected)
        features.append(expected); columns.append(np.load(record['columns']['path'], allow_pickle=False)); checked_candidates += len(values)
    expected_descriptions = [dict(left=j,right=k,triple=t) for j,k in partners for t in triples]
    assert proof['descriptions'] == expected_descriptions and source['added_points'] == len(expected_descriptions)
    assert all(col.dtype == np.int8 and col.shape == (len(f),len(expected_descriptions)) for col,f in zip(columns,features))
    assert len(proof['relations']) == len(expected_descriptions)
    triple_sets = [{i for i in range(10) if t >> i & 1} for t in triples]
    for x, record in enumerate(expected_descriptions):
        j,k = record['left'],record['right']; index = triples.index(record['triple'])
        disjoint = np.array([int(triple_sets[index].isdisjoint(s)) for s in triple_sets], dtype=np.int32)
        incompatible = (features[k].astype(np.int32) @ disjoint > 0).astype(np.int8)
        for v,col in enumerate(columns):
            want = features[j][:,index] if v == j else incompatible if v == k else np.zeros(len(col),dtype=np.int8)
            assert np.array_equal(col[:,x],want)
        actual = set(map(tuple,proof['relations'][x])); expected = set()
        for left,right in ((0,0),(0,1),(1,0)):
            row = [0]*len(pairs); row[j]=left; row[k]=right; expected.add(tuple(row))
        assert actual == expected and len(proof['relations'][x]) == len(expected)
    for name in ('verify_matched_cross_refinement.py','matched_ordinary_cross_intersection_cycle331.md'): b.bind(H/name)
    result = dict(status='INDEPENDENTLY_VERIFIED_MATCHED_ORDINARY_CROSS_REFINEMENT',global_status='UNRESOLVED',
                  source=b.bind(source_path),base_refinement=source['base_refinement'],refinement=source['proof'],
                  geometry_index=source['geometry_index'],complete_actual_cover=True,old_point_count=1026,
                  added_points=len(expected_descriptions),candidates_checked=checked_candidates,
                  delta_zero_relation_tuples_checked=checked_relations,old_point_semantics_unchanged=True,
                  producer_imported=False,fast_walsh_transform_used=False,global_goal_complete=False,
                  seconds=monotonic()-start,files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ('geometry_index','added_points','candidates_checked','delta_zero_relation_tuples_checked','seconds')}),flush=True)


if __name__ == '__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output)
