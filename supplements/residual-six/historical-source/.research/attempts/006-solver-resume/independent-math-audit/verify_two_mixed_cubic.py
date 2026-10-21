"""Independent mixed-sign derivative cover and exact compact-row replay.

Imports only the previous independent audit's standard-library primitives.
No producer, numerical model, propagation search, or solver imports.
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
    A, P, R, S, bound, check_bindings, digest, layer, mask, ordered_model,
    read, recognize_necessary_row, rejected, replay, row, sphere_check,
    subfaces, vertices, flag_check)


def source_filter():
    audit = read(A/'d10-normalization-spheres-independent-verification.json')
    assert audit['status'] == 'VERIFIED_D10_NORMALIZATION_ARITHMETIC_AND_SPHERE_COVER'
    stages = {r['order']:r for r in audit['sphere_stages']}
    mixed, plus, private, ordinary, paths = [], [], [], [], []
    for n in range(5,13):
        path = P/f'sphere-triangulations-{n:02d}.json'
        assert digest(path) == stages[n]['source_sha256']
        data = read(path)
        assert data['status'] == 'COMPLETE_INVERSE_CONTRACTION_COVER' and data['order'] == n
        assert len(data['classes']) == stages[n]['representatives']
        assert [r['index'] for r in data['classes']] == list(range(len(data['classes'])))
        for record in data['classes']:
            faces = record['face_masks']
            edges = {mask(t) for f in faces for t in combinations(vertices(f),2)}
            degrees = [sum(bool(e & (1 << v)) for e in edges) for v in range(n)]
            if degrees.count(3) == degrees.count(6) == 1 and set(degrees) <= {3,4,5,6}:
                assert sphere_check(faces,n)[1] == degrees
                mixed.append(dict(order=n,index=record['index'],face_masks=faces,
                                  degree_vector=degrees,positive_vertex=degrees.index(3),
                                  negative_vertex=degrees.index(6)))
            if degrees.count(3) == 1 and set(degrees) <= {3,4,5}:
                sphere_check(faces,n)
                plus.append((n,record['index']))
            if degrees.count(6) == 1 and set(degrees) <= {4,5,6}:
                sphere_check(faces,n); flag_check(faces,edges,n)
                private.append((n,record['index']))
            if set(degrees) <= {4,5}:
                sphere_check(faces,n); flag_check(faces,edges,n)
                ordinary.append((n,record['index']))
        paths.append(path)
    assert [(r['order'],r['index']) for r in mixed] == [(8,6),(9,10)]
    assert plus == [(7,2)]  # Only the weaker bounds 7..10 occur in producer rows.
    assert private == [(9,22),(10,185),(11,762)]
    # Order four consists of the tetrahedron boundary, with four degree-threes;
    # it has none of the one-degree-three profiles under discussion.
    tetra_boundary = [7,11,13,14]
    assert sphere_check(tetra_boundary,4)[1] == [3]*4
    return mixed,plus,private,ordinary,paths


def mixed_model(n, edge_count, root_faces, valences, instance_vertices=None, all_euler=True):
    # Reuse the frozen independent implementation only for the unchanged
    # downward/incidence/vertex/root/Euler prefix, not producer constructors.
    keep = {'downward','triangle_two_tetrahedra','minimum_degree',
            'vertex_link_faces','vertex_link_edges','face_count','root_link'}
    if all_euler:
        keep.add('induced_euler')
    rows = [r for r in ordered_model(n,edge_count,root_faces,set()) if r['reason'] in keep]
    edges,quads = layer(n,2),layer(n,4)
    bad = {v for e in valences for v in vertices(e)}
    for e in edges:
        inc = {q:1 for q in quads if q & e == e}
        if e in valences:
            rows.append(row({e:1},1,1,'exceptional_edge_present'))
            rows.append(row(inc,valences[e],valences[e],'exceptional_edge_valence'))
        else:
            rows.append(row({**inc,e:-4},0,1,'ordinary_edge_four_or_five'))
    for q in quads:
        for v in vertices(q):
            if v not in bad:
                rows.append(row({**{q ^ (1 << w):1 for w in vertices(q) if w != v},q:-1},
                                -1,2,'ordinary_vertex_link_flag'))
    if all_euler:
        for t in combinations(range(n),3):
            rows.append(row({mask(e):1 for e in combinations(t,2)},1,3,'no_independent_triple'))
    if instance_vertices is not None:
        positive,negative = instance_vertices
        for v in range(n):
            lo,hi = (9,11) if v == negative else ((7,10) if v == positive else (6,12))
            rows.append(row({e:1 for e in edges if e >> v & 1},lo,hi,'vertex_link_order'))
        for q in quads:
            if q >> negative & 1:
                rows.append(row({**{q ^ (1 << v):1 for v in vertices(q) if v != negative},q:-1},
                                -1,2,'negative_private_endpoint_flag'))
    return rows


def row_check(r, link):
    translated = dict(link,exceptional_vertices=[link['positive_vertex'],link['negative_vertex']])
    if r['reason'] == 'negative_private_endpoint_flag':
        positive_terms = [m for m,c in r['terms'] if c > 0]
        assert len(positive_terms) == 3
        center = positive_terms[0] & positive_terms[1] & positive_terms[2]
        assert center == 1 << (link['negative_vertex']+1)
        recognized = dict(r,reason='private_endpoint_one_six_link_flag')
        recognize_necessary_row(recognized,translated)
    else:
        assert r['reason'] in {'root_link','ordinary_edge_four_or_five',
                               'ordinary_vertex_link_flag','induced_euler','downward'}
        # The previous independent parser prohibits both exceptional private
        # endpoints and the root as ordinary-flag centers.
        recognize_necessary_row(r,translated)


def case_check(case, link, full, model):
    assert case['link'] == link and case['constant'] == 1
    assert not case['uses_global_face_count']
    indexes = case['original_row_indices']
    assert indexes == sorted(set(indexes)) and len(indexes) == len(case['rows'])
    assert [model[i] for i in indexes] == case['rows']
    assert len(model) == full['row_count']
    assert sha256(json.dumps(model,sort_keys=True).encode()).hexdigest() == full['row_digest']
    for r in case['rows']:
        row_check(r,link)
    source_steps = iter(full['steps'])
    for s in case['steps']:
        original_step = dict(s,row=indexes[s['row']])
        assert any(old == original_step for old in source_steps)
    assert indexes[case['contradiction_row']] == full['contradiction_row']
    return replay(case)


def cycle_join_control(a,b):
    n = a+b
    quads = {mask((i,(i+1)%a,a+j,a+(j+1)%b)) for i in range(a) for j in range(b)}
    faces = subfaces(quads)
    edges = {e for e in faces if e.bit_count() == 2}
    valences = {e:sum(q & e == e for q in quads) for e in edges}
    exceptional = {e:v for e,v in valences.items() if v not in (4,5)}
    assert all(v in (3,6) for v in exceptional.values())
    root = {q ^ 1 for q in quads if q & 1}
    geometric = mixed_model(n,len(edges),root,exceptional,all_euler=False)
    evaluate = lambda r:sum(c for f,c in r['terms'] if f in faces)
    assert all(r['lower'] <= evaluate(r) <= r['upper'] for r in geometric)
    ranged = mixed_model(n,len(edges),root,exceptional)
    failures = Counter(r['reason'] for r in ranged if not r['lower'] <= evaluate(r) <= r['upper'])
    if (a,b) == (4,4):
        assert not failures
    else:
        assert failures and set(failures) <= {'induced_euler','no_independent_triple'}
    return dict(vertices=n,edges=len(edges),tetrahedra=len(quads),
                geometric_rows=len(geometric),ranged_rows=len(ranged),range_failures=dict(failures))


def curvature_control():
    checked = 0
    survivors = {1:[],2:[]}
    # n counts all link vertices other than the high-degree vertex b; one of
    # those n vertices has degree three. No topology or sphere assumption.
    for s in (8,9):
        for n in range(1,12):
            for n4 in range(n):
                checked += 1
                direct_degree_sum = s + 3 + 4*n4 + 5*(n-1-n4)
                assert direct_degree_sum == s+5*n-2-n4
                for chi in (1,2):
                    euler_sum = 6*(n+1-chi)
                    assert (direct_degree_sum == euler_sum) == (n+n4 == s-8+6*chi)
                    if direct_degree_sum == euler_sum and n >= s:
                        survivors[chi].append([s,n,n4])
    assert not survivors[1] and survivors[2]
    # In the ordinary case link(a)'s one degree-three vertex and no six gives
    # N+N4=4 (projective plane) or10 (sphere). At x the possible six changes
    # these totals to5 or11. A projective plane needs at least six vertices.
    assert max(4,5) < 6
    return dict(integer_profiles_checked=checked,special_chi_one_survivors=0,
                relaxed_chi_two_profiles=survivors[2],
                ordinary_projective_bounds=[4,5],projective_minimum_vertices=6)


def check_coverage(cases,links):
    assert [c['link'] for c in cases] == links


def main():
    start = time.monotonic()
    old_helper = A/'verify_two_adjacent_negative_cubic.py'
    old_report = read(A/'two-adjacent-negative-cubic-independent-verification.json')
    assert old_report['status'] == 'VERIFIED_TWO_ADJACENT_NEGATIVE_CUBIC_ORDINARY_DERIVATIVE_EXCLUSION'
    assert next(r['sha256'] for r in old_report['dependencies'] if r['path'] == str(old_helper)) == digest(old_helper)
    links,plus,private,ordinary,catalogs = source_filter()
    cp = P/'two-mixed-cubic-ordinary-compact-proofs.json'
    fp = P/'two-mixed-cubic-ordinary-interval-probe.json'
    compact,full = read(cp),read(fp)
    check_bindings(compact['sources']);check_bindings(full['sources'])
    assert full['link_types'] == links
    check_coverage(compact['cases'],links)
    originals = {(r['link_order'],r['link_index'],r['constant']):r for r in full['cases']}
    assert len(originals) == len(full['cases']) == 4
    results,reasons,stored = [],Counter(),[]
    for case,link in zip(compact['cases'],links):
        a,b = link['positive_vertex']+1,link['negative_vertex']+1
        roots = [f << 1 for f in link['face_masks']]
        model = mixed_model(13,50,roots,{1 | (1 << a):3,1 | (1 << b):6},(a,b))
        key = (link['order'],link['index'])
        old = originals[key+(1,)]
        proof = case_check(case,link,old,model)
        second = [dict(r,lower=r['lower']+{2:1,3:2,4:1}[r['terms'][0][0].bit_count()],
                       upper=r['upper']+{2:1,3:2,4:1}[r['terms'][0][0].bit_count()])
                  if r['reason'] == 'face_count' else r for r in model]
        assert [second[i] for i in case['original_row_indices']] == case['rows']
        assert len(second) == originals[key+(2,)]['row_count']
        assert sha256(json.dumps(second,sort_keys=True).encode()).hexdigest() == originals[key+(2,)]['row_digest']
        reasons.update(r['reason'] for r in case['rows'])
        results.append(dict(order=key[0],index=key[1],full_rows=len(model),compact_rows=len(case['rows']),**proof))
        stored.append((model,old))
    assert sum(r['compact_rows'] for r in results) == 132
    assert sum(r['deductions'] for r in results) == 131
    assert 'face_count' not in reasons

    first = compact['cases'][0]
    verify = lambda c:case_check(c,links[0],stored[0][1],stored[0][0])
    controls = {}
    corrupt = deepcopy(first); corrupt['link']['positive_vertex'] = corrupt['link']['negative_vertex']
    controls['wrong_sign_marking'] = rejected(lambda:verify(corrupt))
    corrupt = deepcopy(first); corrupt['rows'][0]['terms'][0][1] += 1
    controls['wrong_row_coefficient'] = rejected(lambda:verify(corrupt))
    corrupt = deepcopy(first); corrupt['original_row_indices'][0] += 1
    controls['wrong_original_row_index'] = rejected(lambda:verify(corrupt))
    corrupt = deepcopy(first); corrupt['steps'][0]['value'] ^= 1
    controls['wrong_forced_assignment'] = rejected(lambda:replay(corrupt))
    corrupt = deepcopy(first); corrupt['contradiction_row'] = first['steps'][0]['row']
    controls['noncontradictory_terminal_row'] = rejected(lambda:replay(corrupt))
    controls['omitted_link_case'] = rejected(lambda:check_coverage(compact['cases'][:-1],links))
    controls['duplicated_link_case'] = rejected(lambda:check_coverage(compact['cases']+[first],links))
    # A plus endpoint is not allowed to borrow the private-minus flag theorem.
    a = links[0]['positive_vertex']+1
    q = mask((a,2,3,4))
    bad_flag = row({**{q ^ (1 << v):1 for v in vertices(q) if v != a},q:-1},
                   -1,2,'negative_private_endpoint_flag')
    controls['flag_at_positive_endpoint'] = rejected(lambda:row_check(bad_flag,links[0]))

    dependencies = {Path(r['path']) for r in compact['sources']+full['sources']}
    dependencies.update(catalogs+[Path(__file__),old_helper,cp,fp,
        A/'two-adjacent-negative-cubic-independent-verification.json',
        A/'two-adjacent-negative-cubic-audit.md',
        A/'d10-normalization-spheres-independent-verification.json',
        A/'generic-d10-normalization-audit.md',
        R/'one-negative-quadratic-derivative.md',
        S/'one-negative-quadratic-derivative-independent-audit.md'])
    result = dict(status='VERIFIED_ADJACENT_MIXED_CUBIC_ORDINARY_AND_SPECIAL_EDGE_OBSTRUCTIONS',
                  global_function_status='UNRESOLVED',
                  ordinary_scope='n13; c in {1,2}; p(0)=1 and units0; pair numerators +1 at ax and -2 at bx, all others -1/0; binary quartic numerators; all ordinary quadratic coefficients0/1.',
                  special_scope='Same exception placement, with only ordinary coefficient ab=2; independent curvature contradiction, no finite extension model.',
                  root_links=links,ordinary_flag_link_classes=ordinary,
                  negative_private_flag_link_classes=private,positive_private_link_classes=plus,
                  positive_and_root_flag_rows_used=0,cases=results,
                  compact_rows=132,exact_integer_deductions=131,
                  selected_row_reasons=dict(reasons),original_model_digests_bound=4,
                  global_face_count_rows_used=0,constant_independent_selected_rows=True,
                  controls=dict(curvature=curvature_control(),cycle4_join_cycle4=cycle_join_control(4,4),
                                cycle3_join_cycle6=cycle_join_control(3,6),corruption_checks=controls),
                  producer_imports=False,research_solver_used=False,
                  sphere_completeness='Previously independently verified inverse-contraction coverage through order12, hashes and literal filters checked again.',
                  seconds=time.monotonic()-start,
                  dependencies=[bound(p) for p in sorted(dependencies)])
    (A/'two-mixed-cubic-independent-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
