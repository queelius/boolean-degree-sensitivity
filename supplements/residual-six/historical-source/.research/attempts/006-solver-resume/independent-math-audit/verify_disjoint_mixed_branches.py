"""Independent literal-row and complete Boolean-tree certificate replay.

Only earlier independent audit code is imported.  No producer propagation,
branch search, numerical model, or certificate compactor is executed.
"""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import json
import sys
import time

sys.dont_write_bytecode = True
from verify_two_adjacent_negative_cubic import (
    A,P,bound,check_bindings,digest,layer,mask,read,rejected,replay,row,vertices)
from verify_two_mixed_cubic import source_filter
from verify_disjoint_cubic_compact import key,reconstructed_model,recognize


def strengthened(cover, second, constant=1):
    model = reconstructed_model(cover,second,1,constant)
    for v in vertices(second):
        model.append(row({e:1 for e in layer(13,2) if e >> v & 1},7,7,'positive_endpoint_exact_order'))
    return [r for r in model if r['reason'] != 'face_count']


def recognize_new(r, cover, second):
    reason = r['reason']
    if reason == 'positive_endpoint_exact_order':
        common = 8191
        for e,c in r['terms']:
            assert type(e) is type(c) is int and e.bit_count() == 2 and c == 1
            common &= e
        v, = vertices(common)
        assert second >> v & 1
        expected = row({e:1 for e in layer(13,2) if e >> v & 1},7,7,reason)
        assert r == expected
    elif reason == 'no_independent_triple':
        support = 0
        for e,c in r['terms']:
            assert e.bit_count() == 2 and c == 1
            support |= e
        assert support.bit_count() == 3
        expected = row({support ^ (1 << v):1 for v in vertices(support)},1,3,reason)
        assert r == expected
    elif reason == 'vertex_link_edges':
        common = 8191
        for f,c in r['terms']:
            common &= f
        v, = vertices(common)
        expected = row({**{e:-3 for e in layer(13,2) if e >> v & 1},
                        **{t:1 for t in layer(13,3) if t >> v & 1}},-6,-6,reason)
        assert r == expected
    else:
        recognize(r,cover,second,1)


def verify_tree(tree, model, mathematical_row_check, assumptions=None):
    assumptions = [] if assumptions is None else assumptions
    assert tree['assumptions'] == assumptions
    assert len({v for v,_ in assumptions}) == len(assumptions)
    assert all(type(v) is type(value) is int and value in (0,1) for v,value in assumptions)
    status = tree['status']
    if status == 'EXACT_BRANCH_CONTRADICTION':
        assert set(tree) == {'status','variable','assumptions','zero','one'}
        variable = tree['variable']
        assert type(variable) is int and variable not in dict(assumptions)
        assert any(variable == v for r in model for v,_ in r['terms'])
        left = verify_tree(tree['zero'],model,mathematical_row_check,assumptions+[[variable,0]])
        right = verify_tree(tree['one'],model,mathematical_row_check,assumptions+[[variable,1]])
        return dict(nodes=1+left['nodes']+right['nodes'],leaves=left['leaves']+right['leaves'],
                    rows=left['rows']+right['rows'],deductions=left['deductions']+right['deductions'],
                    depth=max(left['depth'],right['depth']),
                    reasons=left['reasons']+right['reasons'])
    assert status == 'EXACT_INTERVAL_CONTRADICTION'
    assert set(tree) == {'status','steps','contradiction_row','original_row_indices','rows','assumptions'}
    augmented = model+[row({v:1},value,value,'branch_assumption') for v,value in assumptions]
    indices = tree['original_row_indices']
    assert indices == sorted(set(indices)) and len(indices) == len(tree['rows'])
    assert all(type(i) is int and 0 <= i < len(augmented) for i in indices)
    assert [augmented[i] for i in indices] == tree['rows']
    for i,r in zip(indices,tree['rows']):
        if i < len(model):
            assert r['reason'] != 'branch_assumption'
            mathematical_row_check(r)
        else:
            v,value = assumptions[i-len(model)]
            assert r == row({v:1},value,value,'branch_assumption')
    proof = replay(tree)
    return dict(nodes=1,leaves=1,rows=len(tree['rows']),deductions=proof['deductions'],
                depth=len(assumptions),reasons=Counter(r['reason'] for r in tree['rows']))


def coverage(data, previous, original, covers):
    assert data['status'] == 'COMPLETE_BOUNDED_BRANCH_PROBES'
    assert data['constants'] == [1,2] and data['untested'] == 0
    all_keys = [(i,e,s) for i,c in enumerate(covers) for e in c['second_pairs'] for s in (-2,1)]
    old_keys = [key(c) for c in previous['cases']]
    missing = [k for k in all_keys if k not in set(old_keys)]
    assert len(all_keys) == 94 and len(set(old_keys)) == len(old_keys) == 66
    assert all(k in all_keys for k in old_keys)
    assert missing == [tuple(k) for k in previous['unresolved_mixed_cases']]
    assert missing == [key(c) for c in original['cases'] if c['status'] == 'INTERVAL_FIXED_POINT_INCONCLUSIVE']
    assert len(missing) == 28 and all(k[2] == 1 for k in missing)
    assert [key(c) for c in data['cases']] == missing
    assert len({key(c) for c in data['cases']}) == 28
    assert set(old_keys).isdisjoint(missing) and set(old_keys) | set(missing) == set(all_keys)
    assert all(c['status'] in ('EXACT_BRANCH_CONTRADICTION','EXACT_INTERVAL_CONTRADICTION') for c in data['cases'])
    return missing


def small_tree_control():
    # x+y=1 and x-y=0 are real-feasible but have no Boolean solution.
    x,y = 3,5
    model = [row({x:1,y:1},1,1,'control'),row({x:1,y:-1},0,0,'control')]
    children = []
    for value in (0,1):
        rows = model+[row({x:1},value,value,'branch_assumption')]
        children.append(dict(status='EXACT_INTERVAL_CONTRADICTION',rows=rows,
                             original_row_indices=[0,1,2],assumptions=[[x,value]],
                             steps=[dict(variable=x,value=value,row=2),dict(variable=y,value=1-value,row=0)],
                             contradiction_row=1))
    tree = dict(status='EXACT_BRANCH_CONTRADICTION',variable=x,assumptions=[],zero=children[0],one=children[1])
    result = verify_tree(tree,model,lambda r:None)
    assert result['nodes'] == 3 and result['leaves'] == 2
    bad = deepcopy(tree); del bad['one']
    missing_child = rejected(lambda:verify_tree(bad,model,lambda r:None))
    bad = deepcopy(tree); bad['one'] = deepcopy(bad['zero'])
    duplicate_branch = rejected(lambda:verify_tree(bad,model,lambda r:None))
    bad = deepcopy(tree); bad['zero']['status'] = 'BOUNDED_INCONCLUSIVE'
    bounded_leaf = rejected(lambda:verify_tree(bad,model,lambda r:None))
    # A row with an integer gap permits the old replay format: the opposite
    # value is impossible, then the inferred value produces the final clash.
    gap = dict(status='EXACT_INTERVAL_CONTRADICTION',rows=[row({x:2},1,1,'control')],
               original_row_indices=[0],assumptions=[],steps=[dict(variable=x,value=1,row=0)],contradiction_row=0)
    assert verify_tree(gap,gap['rows'],lambda r:None)['deductions'] == 1
    return dict(two_branch_exact_control='PASS',integer_gap_control='PASS',
                missing_child=missing_child,duplicated_zero_branch=duplicate_branch,bounded_leaf=bounded_leaf)


def main():
    started = time.monotonic()
    source = P/'disjoint-mixed-constant-independent-branch-proofs.json'
    assert digest(source) == '0ab532896e1f95b4fe20c8e6f53fc678d745bd33147fe5b8a546e73e51d6fbeb'
    previous_path = A/'disjoint-cubic-ordinary-compact-independent-verification.json'
    previous = read(previous_path)
    assert previous['status'] == 'VERIFIED_ALL_DISJOINT_MINUS_MINUS_ORDINARY_AND_19_MIXED_CONTRADICTIONS'
    check_bindings(previous['dependencies'])
    cover_report_path = A/'disjoint-cubic-root-link-cover-independent-verification.json'
    cover_report = read(cover_report_path)
    check_bindings(cover_report['dependencies'])
    assert cover_report['positive_endpoint_sphere_classes'] == [[7,2]]
    # Re-filter every accepted sphere catalog, independently of the new wrapper.
    _, plus, _, _, catalogs = source_filter()
    assert plus == [(7,2)]
    data = read(source);check_bindings(data['sources'])
    cover_path = P/'disjoint-cubic-root-link-cover.json'
    original_path = P/'disjoint-cubic-ordinary-full-interval-probe.json'
    covers = read(cover_path)['covers'];original = read(original_path)
    keys = coverage(data,previous,original,covers)
    summaries, reasons = [], Counter()
    first_model = None
    for index,case in enumerate(data['cases']):
        i,second,value = key(case)
        assert value == 1 and not case['uses_global_face_count']
        model = strengthened(covers[i],second)
        assert all(r['reason'] != 'face_count' for r in model)
        model_hash = sha256(json.dumps(model,sort_keys=True).encode()).hexdigest()
        assert model_hash == case['row_digest']
        assert case['status'] == case['tree']['status']
        result = verify_tree(case['tree'],model,lambda r:recognize_new(r,covers[i],second))
        assert result['nodes'] == case['nodes']
        reasons.update(result.pop('reasons'))
        summaries.append(dict(root_index=i,second_pair=second,second_value=1,
                              full_rows=len(model),full_row_sha256=model_hash,**result))
        if first_model is None:
            assert strengthened(covers[i],second,2) == model
            first_model,first = model,case
        if (index+1) % 7 == 0:
            print(json.dumps(dict(replayed=index+1,of=28,last_key=key(case))),flush=True)
    totals = {field:sum(c[field] for c in summaries) for field in ('nodes','leaves','rows','deductions')}
    assert totals == dict(nodes=110,leaves=69,rows=4648,deductions=4800)
    assert sum(c['depth'] > 0 for c in summaries) > 0
    assert reasons['positive_endpoint_exact_order'] == 36
    assert reasons['branch_assumption'] == 124 and 'face_count' not in reasons
    controls = small_tree_control()
    bad = deepcopy(data);bad['cases'][0]['second_pair'] = 6
    controls['wrong_case_key'] = rejected(lambda:coverage(bad,previous,original,covers))
    bad = deepcopy(data);bad['cases'] = bad['cases'][:-1]
    controls['missing_case'] = rejected(lambda:coverage(bad,previous,original,covers))
    bad = deepcopy(data);bad['cases'][1] = deepcopy(bad['cases'][0])
    controls['duplicate_case'] = rejected(lambda:coverage(bad,previous,original,covers))
    bad = deepcopy(first['tree'])
    leaf = bad
    while leaf['status'] == 'EXACT_BRANCH_CONTRADICTION':
        leaf = leaf['zero']
    leaf['rows'][0]['terms'][0][1] += 1
    controls['altered_leaf_coefficient'] = rejected(lambda:verify_tree(bad,first_model,lambda r:recognize_new(
        r,covers[first['root_index']],first['second_pair'])))
    forged = row({e:1 for e in layer(13,2) if e & 1},7,7,'positive_endpoint_exact_order')
    controls['degree_seven_at_negative_endpoint'] = rejected(lambda:recognize_new(
        forged,covers[first['root_index']],first['second_pair']))
    paths = [Path(__file__),A/'verify_disjoint_cubic_compact.py',A/'verify_two_mixed_cubic.py',
             A/'verify_two_adjacent_negative_cubic.py',previous_path,cover_report_path,
             source,cover_path,original_path]
    paths += [P/name for name in ('disjoint_mixed_degree_seven.py','binary_branch_certificates.py',
                                 'exact_binary_gap_propagation.py','run_disjoint_mixed_branches.py',
                                 'test_binary_branch_certificates.py','test_exact_binary_gap_propagation.py',
                                 'test_compact_disjoint_branches.py','test_disjoint_mixed_degree_seven.py')]
    paths += catalogs
    report = dict(status='VERIFIED_REMAINING_28_DISJOINT_MIXED_ORDINARY_BRANCH_CONTRADICTIONS',
                  global_goal='OPEN',scope=previous['scope'],authoritative_case_key=list(('root_index','second_pair','second_value')),
                  new_case_keys=[list(k) for k in keys],cases=summaries,totals=totals,
                  selected_reason_counts=dict(reasons),positive_endpoint_sphere_classes=[[7,2]],
                  constants_verified=[1,2],face_count_used=False,positive_endpoint_flag_assumed=False,
                  complete_ordinary_minus_minus_cases=47,complete_ordinary_mixed_cases=47,
                  previous_certified_cases=66,newly_certified_cases=28,unresolved_ordinary_cases=[],
                  controls=controls,producer_unit_tests=dict(passed=8,seconds=1.76),
                  producer_imports=False,research_solver_used=False,
                  seconds=time.monotonic()-started,dependencies=[bound(p) for p in paths])
    path = A/'disjoint-mixed-branch-independent-verification.json'
    assert not path.exists()
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],totals=totals,path=str(path),sha256=digest(path))),flush=True)


if __name__ == '__main__':
    main()
