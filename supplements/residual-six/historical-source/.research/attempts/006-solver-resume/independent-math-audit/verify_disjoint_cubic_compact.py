"""Independent selected-row reconstruction of disjoint cubic contradictions.

Uses only frozen independent audit primitives, with no producer/model/search
imports.  The authoritative key is (root_index, second_pair, second_value),
never a discovery-order orbit label.  Exact interval proof steps are replayed;
the 28 mixed fixed points are deliberately left unresolved.
"""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import sys
import time

sys.dont_write_bytecode = True
from verify_two_adjacent_negative_cubic import (
    A, P, bound, check_bindings, digest, layer, mask, read, rejected, replay,
    row, subfaces, vertices)
from verify_two_mixed_cubic import mixed_model, cycle_join_control

KEY = ('root_index','second_pair','second_value')


def key(record):
    return tuple(record[k] for k in KEY)


def exception_sets(cover, second, value):
    first = cover['first_exception']
    assert value in (-2,1) and first & second == 0
    assert first.bit_count() == second.bit_count() == 2
    valences = {first:6, second:6 if value == -2 else 3}
    negative = {v for e, k in valences.items() if k == 6 for v in vertices(e)}
    positive = {v for e, k in valences.items() if k == 3 for v in vertices(e)}
    assert negative.isdisjoint(positive)
    return valences, negative, positive


def reconstructed_model(cover, second, value, constant):
    assert constant in (1,2) and second in cover['second_pairs']
    valences, negative, positive = exception_sets(cover,second,value)
    root_faces = [f << 1 for f in cover['link']['face_masks']]
    result = mixed_model(13,49+constant,root_faces,valences)
    edges, quads = layer(13,2), layer(13,4)
    for v in range(13):
        low, high = (9,11) if v in negative else ((7,10) if v in positive else (6,12))
        result.append(row({e:1 for e in edges if e >> v & 1},low,high,'vertex_link_order'))
    for v in sorted(negative):
        for q in quads:
            if q >> v & 1:
                result.append(row({**{q ^ (1 << w):1 for w in vertices(q) if w != v},q:-1},
                                  -1,2,'negative_endpoint_flag'))
    return result


def recognize(r, cover, second, value):
    """Re-derive a row from its literal support, separately from row ordering."""
    assert set(r) == {'terms','lower','upper','reason'}
    ts = r['terms']; d = dict(ts)
    assert ts == sorted(ts) and len(d) == len(ts)
    assert all(type(m) is type(c) is int and 0 <= m < 8192 and
               2 <= m.bit_count() <= 4 and c for m,c in ts)
    assert type(r['lower']) is type(r['upper']) is int
    valences, negative, positive = exception_sets(cover,second,value)
    reason = r['reason']
    if reason == 'downward':
        f, = [m for m,c in ts if c == 1]
        t, = [m for m,c in ts if c == -1]
        assert len(ts) == 2 and t & f == t and f.bit_count() == t.bit_count()+1
        expected = row({f:1,t:-1},-1,0,reason)
    elif reason == 'triangle_two_tetrahedra':
        t, = [m for m,c in ts if c < 0]
        assert t.bit_count() == 3
        expected = row({**{t | (1 << v):1 for v in range(13) if not t >> v & 1},t:-2},0,0,reason)
    elif reason == 'root_link':
        f, = d
        assert f & 1
        present = int((f ^ 1) in subfaces([q << 1 for q in cover['link']['face_masks']]))
        expected = row({f:1},present,present,reason)
    elif reason == 'induced_euler':
        support = 0
        for f in d:
            support |= f
        size = support.bit_count()
        assert size >= 3
        expected = row({mask(t):(-1)**(j+1) for j in (2,3,4)
                        for t in combinations(vertices(support),j)},-size,2-size,reason)
    elif reason == 'ordinary_edge_four_or_five':
        e, = [m for m,c in ts if c < 0]
        assert e.bit_count() == 2 and e not in valences
        expected = row({**{q:1 for q in layer(13,4) if q & e == e},e:-4},0,1,reason)
    elif reason == 'exceptional_edge_present':
        e, = d
        assert e in valences
        expected = row({e:1},1,1,reason)
    elif reason == 'exceptional_edge_valence':
        common = 8191
        for q in d:
            common &= q
        assert common in valences
        expected = row({q:1 for q in layer(13,4) if q & common == common},
                       valences[common],valences[common],reason)
    elif reason in ('ordinary_vertex_link_flag','negative_endpoint_flag'):
        q, = [m for m,c in ts if c < 0]
        triangles = [m for m,c in ts if c > 0]
        assert q.bit_count() == 4 and len(triangles) == 3
        common = triangles[0] & triangles[1] & triangles[2]
        v, = vertices(common)
        assert common & q == common
        if reason == 'ordinary_vertex_link_flag':
            assert v not in negative | positive
        else:
            assert v in negative  # includes the root; excludes both +1 endpoints
        expected = row({**{common | mask(t):1 for t in combinations(vertices(q ^ common),2)},q:-1},
                       -1,2,reason)
    elif reason == 'vertex_link_order':
        common = 8191
        for e in d:
            common &= e
        v, = vertices(common)
        low, high = (9,11) if v in negative else ((7,10) if v in positive else (6,12))
        expected = row({edge:1 for edge in layer(13,2) if edge & common},low,high,reason)
    else:
        raise AssertionError(('unsupported or constant-sensitive row',reason))
    assert r == expected, (reason,r,expected)


def coverage_check(compact, original, covers):
    expected = [(i,e,k) for i,c in enumerate(covers) for e in c['second_pairs'] for k in (-2,1)]
    assert len(expected) == 94
    assert [key(c) for c in original['cases']] == expected
    assert [c['case_index'] for c in original['cases']] == list(range(94))
    assert original['status'] == 'COMPLETE_INTERVAL_PROBES' and original['untested'] == 0
    assert all(c['constant'] == 1 for c in original['cases'])
    assert all(c['status'] in ('EXACT_INTERVAL_CONTRADICTION','INTERVAL_FIXED_POINT_INCONCLUSIVE')
               for c in original['cases'])
    certified = [key(c) for c in original['cases'] if c['status'] == 'EXACT_INTERVAL_CONTRADICTION']
    assert compact['authoritative_case_key'] == list(KEY)
    assert compact['status'] == 'COMPLETE_COMPACT_CONTRADICTIONS_AUDIT_PENDING'
    assert compact['unexported'] == 0
    assert [key(c) for c in compact['cases']] == certified
    assert len(certified) == len(set(certified)) == 66
    assert {k for k in certified if k[2] == -2} == {k for k in expected if k[2] == -2}
    assert sum(k[2] == -2 for k in certified) == 47
    assert sum(k[2] == 1 for k in certified) == 19
    for case in compact['cases']:
        i,second,value = key(case)
        cover = covers[i]
        assert second in cover['second_pairs']
        assert case['root_link'] == cover['link'] and case['first_exception'] == cover['first_exception']
        assert case['constants'] == [1,2] and not case['uses_global_face_count']
    return expected, certified


def check_case(case, original, cover, model):
    assert key(case) == key(original)
    assert case['root_link'] == cover['link'] and case['first_exception'] == cover['first_exception']
    assert case['constants'] == [1,2] and not case['uses_global_face_count']
    assert case['second_pair'] in cover['second_pairs']
    indices = case['original_row_indices']
    assert indices == sorted(set(indices)) and len(indices) == len(case['rows'])
    assert all(type(i) is int and 0 <= i < len(model) for i in indices)
    assert [model[i] for i in indices] == case['rows']
    assert original['rows'] == len(model)
    model_digest = sha256(json.dumps(model,sort_keys=True).encode()).hexdigest()
    assert original['row_digest'] == model_digest
    for r in case['rows']:
        recognize(r,cover,case['second_pair'],case['second_value'])
    cursor = iter(original['steps'])
    for step in case['steps']:
        original_step = dict(step,row=indices[step['row']])
        assert any(old == original_step for old in cursor)
    assert indices[case['contradiction_row']] == original['contradiction_row']
    proof = replay(case)
    # Independent c=2 reconstruction changes only the three global face sums.
    second = [dict(r,lower=r['lower']+{2:1,3:2,4:1}[r['terms'][0][0].bit_count()],
                   upper=r['upper']+{2:1,3:2,4:1}[r['terms'][0][0].bit_count()])
              if r['reason'] == 'face_count' else r for r in model]
    assert sum(a != b for a,b in zip(model,second)) == 3
    assert [second[i] for i in indices] == case['rows']
    return dict(full_rows=len(model),c1_full_row_sha256=model_digest,
                compact_rows=len(case['rows']),constants_verified=[1,2],**proof)


def main():
    started = time.monotonic()
    cover_report_path = A/'disjoint-cubic-root-link-cover-independent-verification.json'
    cover_report = read(cover_report_path)
    assert cover_report['status'] == 'VERIFIED_COMPLETE_DISJOINT_CUBIC_ORDINARY_ROOT_LINK_COVER'
    check_bindings(cover_report['dependencies'])
    compact_path = P/'disjoint-cubic-ordinary-compact-proofs.json'
    original_path = P/'disjoint-cubic-ordinary-full-interval-probe.json'
    cover_path = P/'disjoint-cubic-root-link-cover.json'
    compact, original, cover_data = map(read,(compact_path,original_path,cover_path))
    for data in (compact,original,cover_data):
        check_bindings(data['sources'])
    covers = cover_data['covers']
    expected, certified = coverage_check(compact,original,covers)
    originals = {key(c):c for c in original['cases']}
    cases = {key(c):c for c in compact['cases']}
    reports, reasons, first_model = [], Counter(), None
    # Audit the complete -- subclass before the partial mixed subclass.
    ordered = sorted(certified,key=lambda k:(k[2] != -2,k[0],k[1]))
    for position,k in enumerate(ordered):
        case = cases[k]
        cover = covers[k[0]]
        model = reconstructed_model(cover,k[1],k[2],1)
        result = check_case(case,originals[k],cover,model)
        reasons.update(r['reason'] for r in case['rows'])
        reports.append(dict(root_index=k[0],second_pair=k[1],second_value=k[2],**result))
        if first_model is None:
            first_model, first = model, case
        if (position+1) % 10 == 0 or position == 46:
            print(json.dumps(dict(replayed=position+1,of=len(ordered),last_key=k)),flush=True)
    assert sum(r['compact_rows'] for r in reports) == 4731
    assert sum(r['deductions'] for r in reports) == 4721
    assert 'face_count' not in reasons
    # The c=2 rule above agrees with an independently constructed full model.
    first_c2 = reconstructed_model(covers[first['root_index']],first['second_pair'],first['second_value'],2)
    assert [first_c2[i] for i in first['original_row_indices']] == first['rows']
    assert sum(a != b for a,b in zip(first_model,first_c2)) == 3

    def altered_case(c):
        return check_case(c,originals[key(first)],covers[first['root_index']],first_model)
    controls = {}
    bad = deepcopy(first); bad['second_pair'] = next(e for e in covers[0]['second_pairs'] if e != bad['second_pair'])
    controls['copied_proof_under_wrong_case_key'] = rejected(lambda:altered_case(bad))
    bad = deepcopy(first); bad['rows'][0]['terms'][0][1] += 1
    controls['altered_coefficient'] = rejected(lambda:altered_case(bad))
    bad = deepcopy(first); bad['original_row_indices'][0] += 1
    controls['wrong_original_row_index'] = rejected(lambda:altered_case(bad))
    bad = deepcopy(first); bad['constants'] = [1]
    controls['missing_c2_coverage'] = rejected(lambda:altered_case(bad))
    bad = deepcopy(first); bad['steps'][0]['value'] ^= 1
    controls['flipped_deduction'] = rejected(lambda:replay(bad))
    bad = deepcopy(compact); bad['cases'] = bad['cases'][1:]
    controls['missing_case'] = rejected(lambda:coverage_check(bad,original,covers))
    bad = deepcopy(compact); bad['cases'][1] = deepcopy(bad['cases'][0])
    controls['duplicate_case'] = rejected(lambda:coverage_check(bad,original,covers))
    mixed = next(c for c in compact['cases'] if c['second_value'] == 1)
    q = next(q for q in layer(13,4) if q & mixed['second_pair'] == mixed['second_pair'])
    v = vertices(mixed['second_pair'])[0]
    forged = row({**{q ^ (1 << w):1 for w in vertices(q) if w != v},q:-1},-1,2,'negative_endpoint_flag')
    controls['positive_endpoint_falsely_declared_flag'] = rejected(
        lambda:recognize(forged,covers[mixed['root_index']],mixed['second_pair'],1))
    positive_controls = [cycle_join_control(4,4),cycle_join_control(3,6)]
    unresolved = [list(k) for k in expected if k not in set(certified)]
    assert len(unresolved) == 28 and all(k[2] == 1 for k in unresolved)
    paths = [Path(__file__),A/'verify_two_adjacent_negative_cubic.py',A/'verify_two_mixed_cubic.py',
             cover_report_path,compact_path,original_path,cover_path,
             P/'disjoint-cubic-local-reduction.md',P/'disjoint_cubic_complex.py',P/'compact_disjoint_cubic.py']
    report = dict(status='VERIFIED_ALL_DISJOINT_MINUS_MINUS_ORDINARY_AND_19_MIXED_CONTRADICTIONS',
                  global_goal='OPEN',authoritative_case_key=list(KEY),
                  scope='Thirteen-coordinate ternary derivative with c1/2, unit values zero, binary quartics, all ordinary quadratics0/1, exactly two disjoint Fourier-pair exceptions -2/-2 or -2/+1.',
                  complete_minus_minus_cases=47,certified_mixed_cases=19,unresolved_mixed_cases=unresolved,
                  cases=reports,compact_rows=4731,exact_deductions=4721,
                  selected_reason_counts=dict(reasons),constants_verified=[1,2],
                  face_count_used=False,positive_endpoint_flag_assumed=False,
                  symmetry_of_original_function_assumed=False,controls=controls,
                  positive_and_range_negative_controls=positive_controls,
                  producer_imports=False,research_solver_used=False,
                  seconds=time.monotonic()-started,dependencies=[bound(p) for p in paths])
    path = A/'disjoint-cubic-ordinary-compact-independent-verification.json'
    assert not path.exists()
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],cases=len(reports),rows=4731,deductions=4721,
                         mixed_unresolved=28,path=str(path),sha256=digest(path))),flush=True)


if __name__ == '__main__':
    main()
