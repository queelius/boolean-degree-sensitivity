"""Independent literal sphere filter and compact integer-row proof audit.

Standard library only. No producer, model, propagation, or solver imports.
Rows are first recognized from their mathematical form, then bound to an
independently assembled ordered model and its saved digest. Only the nine
compact traces are replayed; no contradiction search is performed.
"""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import sys
import time

sys.dont_write_bytecode = True
A = Path(__file__).resolve().parent
P = A.parent
R = P.parent / '009-parent-analysis'
S = P.parent / '008-sparse-spectrum-proof'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def bound(path):
    return dict(path=str(path), sha256=digest(path))


def check_bindings(rows):
    assert len({r['path'] for r in rows}) == len(rows)
    for row in rows:
        assert digest(Path(row['path'])) == row['sha256'], row['path']


def mask(items):
    return sum(1 << v for v in items)


def vertices(value):
    return tuple(v for v in range(value.bit_length()) if value >> v & 1)


@lru_cache(None)
def layer(n, size):
    return tuple(mask(t) for t in combinations(range(n), size))


def subfaces(facets):
    return {mask(t) for f in facets for size in range(1, f.bit_count() + 1)
            for t in combinations(vertices(f), size)}


def sphere_check(faces, n):
    assert len(faces) == len(set(faces)) == 2*n-4
    assert all(f.bit_count() == 3 and 0 <= f < 1 << n for f in faces)
    ec = Counter(mask(t) for f in faces for t in combinations(vertices(f), 2))
    assert len(ec) == 3*n-6 and set(ec.values()) == {2}
    adjacency = {v: set() for v in range(n)}
    for e in ec:
        u, v = vertices(e)
        adjacency[u].add(v)
        adjacency[v].add(u)
    for v in range(n):
        le = [f ^ (1 << v) for f in faces if f >> v & 1]
        la = {u: set() for u in adjacency[v]}
        for e in le:
            u, w = vertices(e)
            la[u].add(w)
            la[w].add(u)
        assert all(len(z) == 2 for z in la.values())
        reached, stack = set(), [next(iter(la))]
        while stack:
            x = stack.pop()
            if x not in reached:
                reached.add(x)
                stack.extend(la[x] - reached)
        assert reached == set(la)
    reached, stack = set(), [0]
    while stack:
        x = stack.pop()
        if x not in reached:
            reached.add(x)
            stack.extend(adjacency[x] - reached)
    assert len(reached) == n
    return set(ec), [len(adjacency[v]) for v in range(n)]


def flag_check(faces, edges, n):
    fs = set(faces)
    for size in (3, 4):
        for t in combinations(range(n), size):
            if all(mask(e) in edges for e in combinations(t, 2)):
                assert size == 3 and mask(t) in fs


def filter_catalogs():
    audit = read(A / 'd10-normalization-spheres-independent-verification.json')
    assert audit['status'] == 'VERIFIED_D10_NORMALIZATION_ARITHMETIC_AND_SPHERE_COVER'
    stages = {r['order']: r for r in audit['sphere_stages']}
    groups = {0: [], 1: [], 2: []}
    sources = []
    for n in range(5, 13):
        path = P / f'sphere-triangulations-{n:02d}.json'
        assert digest(path) == stages[n]['source_sha256']
        data = read(path)
        assert data['order'] == n and data['status'] == 'COMPLETE_INVERSE_CONTRACTION_COVER'
        assert len(data['classes']) == stages[n]['representatives']
        assert [r['index'] for r in data['classes']] == list(range(len(data['classes'])))
        for row in data['classes']:
            # Reconstruct adjacency without using stored degree statistics.
            faces = row['face_masks']
            neighbors = [set() for _ in range(n)]
            for face in faces:
                vs = vertices(face)
                for v in vs:
                    neighbors[v].update(w for w in vs if w != v)
            deg = [len(z) for z in neighbors]
            if set(deg) <= {4, 5, 6} and deg.count(6) <= 2:
                edges, checked = sphere_check(faces, n)
                assert checked == deg
                record = dict(order=n, index=row['index'], face_masks=faces,
                              degree_vector=deg,
                              exceptional_vertices=[v for v, d in enumerate(deg) if d == 6])
                groups[deg.count(6)].append(record)
                # Needed only for ordinary and private vertex links.
                if deg.count(6) <= 1:
                    flag_check(faces, edges, n)
        sources.append(path)
    assert [(r['order'], r['index']) for r in groups[1]] == [(9,22), (10,185), (11,762)]
    assert [(r['order'], r['index']) for r in groups[2]] == [
        (8,12), (9,32), (10,74), (10,75), (10,168),
        (11,499), (11,764), (12,2537), (12,5741)]
    root = read(R / 'two-adjacent-negative-cubic-link-filter-independent.json')
    check_bindings(root['sources'])
    assert root['status'] == 'INDEPENDENT_SPHERE_FILTER_AND_STRUCTURAL_AUDIT_PASS'
    assert root['link_types'] == groups[2]
    return groups, sources


def row(terms, low, high, reason):
    return dict(terms=[[m, c] for m, c in sorted(terms.items()) if c],
                lower=low, upper=high, reason=reason)


@lru_cache(None)
def euler_rows(n):
    variables = layer(n, 2) + layer(n, 3) + layer(n, 4)
    return tuple(row({f: (-1)**(f.bit_count()+1) for f in variables if f & x == f},
                     -x.bit_count(), 2-x.bit_count(), 'induced_euler')
                 for x in range(1 << n) if x.bit_count() >= 3)


def ordered_model(n, edges_total, root_faces, exceptions, private=()):
    """Declarative order reproduces saved indices; formulas have separate check."""
    edges, triangles, tets = (layer(n, size) for size in (2, 3, 4))
    variables = edges + triangles + tets
    result = []
    for f in triangles + tets:
        for v in vertices(f):
            result.append(row({f:1, f ^ (1 << v):-1}, -1, 0, 'downward'))
    for t in triangles:
        result.append(row({**{q:1 for q in tets if q & t == t}, t:-2},
                          0, 0, 'triangle_two_tetrahedra'))
    # The producer removes its original edge-valence block before extension.
    for v in range(n):
        incident = {e:-2 for e in edges if e >> v & 1}
        result.append(row({e:1 for e in incident}, 0, n-1, 'minimum_degree'))
        result.append(row({**incident, **{q:1 for q in tets if q >> v & 1}},
                          -4, -4, 'vertex_link_faces'))
        result.append(row({**{e:-3 for e in incident},
                           **{t:1 for t in triangles if t >> v & 1}},
                          -6, -6, 'vertex_link_edges'))
    for size, count in ((2, edges_total), (3, 2*(edges_total-n)), (4, edges_total-n)):
        result.append(row({f:1 for f in layer(n, size)}, count, count, 'face_count'))
    root_closure = subfaces(root_faces)
    for f in variables:
        if f & 1:
            value = int((f ^ 1) in root_closure)
            result.append(row({f:1}, value, value, 'root_link'))
    result.extend(euler_rows(n))
    exceptional_vertices = set(v for e in exceptions for v in vertices(e))
    for e in edges:
        inc = {q:1 for q in tets if q & e == e}
        if e in exceptions:
            result.append(row({e:1}, 1, 1, 'exceptional_edge_present'))
            result.append(row(inc, 6, 6, 'exceptional_edge_valence_six'))
        else:
            result.append(row({**inc, e:-4}, 0, 1, 'ordinary_edge_four_or_five'))
    for v in range(n):
        result.append(row({e:1 for e in edges if e >> v & 1}, 6, n-1, 'degree_at_least_six'))
    for q in tets:
        for v in vertices(q):
            if v not in exceptional_vertices:
                result.append(row({**{q ^ (1 << w):1 for w in vertices(q) if w != v}, q:-1},
                                  -1, 2, 'ordinary_vertex_link_flag'))
    for vs in combinations(range(n), 3):
        result.append(row({mask(e):1 for e in combinations(vs, 2)}, 1, 3, 'no_independent_triple'))
    all_root = set(v for f in root_faces for v in vertices(f))
    for vs in combinations(sorted(set(range(1, n))-all_root), 2):
        result.append(row({mask(vs):1}, 1, 1, 'root_nonneighbors_clique'))
    for v in private:
        result.append(row({e:1 for e in edges if e >> v & 1},
                          9, 11, 'private_endpoint_one_six_link_order'))
        for q in tets:
            if q >> v & 1:
                result.append(row({**{q ^ (1 << w):1 for w in vertices(q) if w != v}, q:-1},
                                  -1, 2, 'private_endpoint_one_six_link_flag'))
    return result


def recognize_necessary_row(r, link, n=13):
    """Derive a selected row from its literal mathematical support."""
    assert set(r) == {'terms', 'lower', 'upper', 'reason'}
    terms = r['terms']
    assert terms == sorted(terms) and len({m for m,c in terms}) == len(terms)
    assert all(type(m) is type(c) is int and 0 <= m < 1 << n and
               2 <= m.bit_count() <= 4 and c != 0 for m,c in terms)
    assert type(r['lower']) is type(r['upper']) is int
    d = dict(terms)
    reason = r['reason']
    private = {v+1 for v in link['exceptional_vertices']}
    exceptional = {1 | (1 << v) for v in private}
    if reason == 'downward':
        assert len(d) == 2 and sorted(d.values()) == [-1,1]
        f, = [m for m,c in terms if c == 1]
        t, = [m for m,c in terms if c == -1]
        assert t & f == t and f.bit_count() == t.bit_count()+1
        expect = row({f:1,t:-1}, -1, 0, reason)
    elif reason == 'triangle_two_tetrahedra':
        t, = [m for m,c in terms if c < 0]
        assert t.bit_count() == 3
        expect = row({**{t | (1 << v):1 for v in range(n) if not t >> v & 1}, t:-2},0,0,reason)
    elif reason == 'root_link':
        assert len(d) == 1
        f, = d
        assert f & 1
        value = int((f ^ 1) in subfaces([t << 1 for t in link['face_masks']]))
        expect = row({f:1}, value, value, reason)
    elif reason == 'induced_euler':
        x = 0
        for f in d:
            x |= f
        assert x.bit_count() >= 3
        expect = row({mask(t):(-1)**(size+1) for size in (2,3,4)
                      for t in combinations(vertices(x), size)},
                     -x.bit_count(), 2-x.bit_count(), reason)
    elif reason == 'ordinary_edge_four_or_five':
        e, = [m for m,c in terms if c < 0]
        assert e.bit_count() == 2 and e not in exceptional
        expect = row({**{e | mask(t):1 for t in combinations(
                         [v for v in range(n) if not e >> v & 1], 2)}, e:-4},0,1,reason)
    elif reason in {'ordinary_vertex_link_flag','private_endpoint_one_six_link_flag'}:
        q, = [m for m,c in terms if c < 0]
        assert q.bit_count() == 4
        positives = [m for m,c in terms if c > 0]
        assert len(positives) == 3
        common = positives[0] & positives[1] & positives[2]
        assert common.bit_count() == 1
        v, = vertices(common)
        if reason == 'ordinary_vertex_link_flag':
            assert v not in private | {0}
        else:
            assert v in private
        expect = row({**{common | mask(t):1 for t in combinations(vertices(q ^ common), 2)},
                      q:-1},-1,2,reason)
    elif reason == 'private_endpoint_one_six_link_order':
        common = (1 << n)-1
        for e in d:
            common &= e
        assert common.bit_count() == 1
        v, = vertices(common)
        assert v in private
        expect = row({common | (1 << w):1 for w in range(n) if w != v},9,11,reason)
    elif reason == 'no_independent_triple':
        x = 0
        for e in d:
            x |= e
        assert x.bit_count() == 3
        expect = row({mask(t):1 for t in combinations(vertices(x),2)},1,3,reason)
    else:
        raise AssertionError(('unsupported selected reason', reason))
    assert r == expect, (reason, r, expect)


def limits(r, fixed, hypothetical=None):
    """Exact extremal interval over the remaining Boolean variables."""
    lo = hi = 0
    for variable, coefficient in r['terms']:
        values = (hypothetical[1],) if hypothetical is not None and variable == hypothetical[0] else (
            (fixed[variable],) if variable in fixed else (0,1))
        products = [coefficient*v for v in values]
        lo += min(products)
        hi += max(products)
    return lo, hi


def outside(r, interval):
    return interval[1] < r['lower'] or interval[0] > r['upper']


def replay(case):
    assert case['status'] == 'EXACT_INTERVAL_CONTRADICTION'
    fixed = {}
    for step in case['steps']:
        assert set(step) == {'variable','value','row'}
        v, value, i = step['variable'], step['value'], step['row']
        assert type(v) is type(value) is type(i) is int
        assert v not in fixed and value in (0,1) and 0 <= i < len(case['rows'])
        r = case['rows'][i]
        assert v in dict(r['terms'])
        assert outside(r, limits(r, fixed, (v,1-value))), step
        fixed[v] = value
    r = case['rows'][case['contradiction_row']]
    interval = limits(r, fixed)
    assert outside(r, interval)
    return dict(deductions=len(fixed), contradiction_interval=interval,
                allowed_interval=[r['lower'],r['upper']])


def verify_case(case, expected_link, original_case, model):
    assert case['link'] == expected_link and case['constant'] == 1
    assert not case['uses_global_face_count']
    originals = case['original_row_indices']
    assert originals == sorted(set(originals)) and len(originals) == len(case['rows'])
    assert [model[i] for i in originals] == case['rows']
    assert original_case['row_count'] == len(model)
    assert original_case['row_digest'] == sha256(json.dumps(model,sort_keys=True).encode()).hexdigest()
    for r in case['rows']:
        recognize_necessary_row(r, expected_link)
    # The compact deductions are a subsequence of the saved larger trace.
    remapped = [dict(s, row=originals[s['row']]) for s in case['steps']]
    cursor = iter(original_case['steps'])
    for target in remapped:
        assert any(old == target for old in cursor)
    assert originals[case['contradiction_row']] == original_case['contradiction_row']
    return replay(case)


def rejected(fn):
    try:
        fn()
    except (AssertionError, KeyError, IndexError, StopIteration, ValueError):
        return 'REJECTED'
    raise AssertionError('corrupted artifact was accepted')


def join_control(a, b):
    n = a+b
    facets = {mask((i,(i+1)%a,a+j,a+(j+1)%b)) for i in range(a) for j in range(b)}
    closure = subfaces(facets)
    edges = {f for f in closure if f.bit_count() == 2}
    tets = {f for f in closure if f.bit_count() == 4}
    exceptional = {e for e in edges if sum(q & e == e for q in tets) == 6}
    roots = {q ^ 1 for q in facets if q & 1}
    rows = ordered_model(n,len(edges),roots,exceptional)
    failed = Counter(r['reason'] for r in rows if not r['lower'] <=
                     sum(c for f,c in r['terms'] if f in closure) <= r['upper'])
    chi = []
    for x in range(1 << n):
        chi.append(sum((-1)**(f.bit_count()+1) for f in closure if f & x == f))
    if (a,b) == (4,4):
        assert not failed and min(chi) == 0 and max(chi) == 2
    else:
        assert set(failed) <= {'induced_euler','no_independent_triple'} and failed
        assert max(chi) > 2
    return dict(vertices=n, facets=len(facets), edges=len(edges), rows=len(rows),
                failing_reasons=dict(failed), induced_euler_range=[min(chi),max(chi)])


def main():
    started = time.monotonic()
    groups, catalogs = filter_catalogs()
    compact_path = P / 'two-negative-cubic-ordinary-compact-proofs.json'
    full_path = P / 'two-negative-cubic-ordinary-interval-probe.json'
    compact, full = read(compact_path), read(full_path)
    check_bindings(compact['sources'])
    check_bindings(full['sources'])
    revision = full['proof_note_revision_after_run']
    assert digest(Path(revision['path'])) == revision['sha256']
    assert full['link_types'] == groups[2]
    assert [c['link'] for c in compact['cases']] == groups[2]
    assert len(full['cases']) == 18
    full_cases = {(c['link_order'],c['link_index'],c['constant']):c for c in full['cases']}
    assert len(full_cases) == 18
    reports, all_reasons, models = [], Counter(), {}
    for case in compact['cases']:
        link = case['link']
        private = [v+1 for v in link['exceptional_vertices']]
        exceptions = {1 | (1 << v) for v in private}
        root_faces = [f << 1 for f in link['face_masks']]
        model = ordered_model(13,50,root_faces,exceptions,private)
        key = (link['order'],link['index'])
        old = full_cases[key+(1,)]
        proof = verify_case(case,link,old,model)
        # c=2 changes only global counts, which these compact proofs do not use.
        second = [dict(r,lower=r['lower']+({2:1,3:2,4:1}[r['terms'][0][0].bit_count()]),
                       upper=r['upper']+({2:1,3:2,4:1}[r['terms'][0][0].bit_count()]))
                  if r['reason']=='face_count' else r for r in model]
        assert [second[i] for i in case['original_row_indices']] == case['rows']
        assert sha256(json.dumps(second,sort_keys=True).encode()).hexdigest() == full_cases[key+(2,)]['row_digest']
        assert len(second) == full_cases[key+(2,)]['row_count']
        all_reasons.update(r['reason'] for r in case['rows'])
        reports.append(dict(order=key[0],index=key[1],full_rows=len(model),
                            compact_rows=len(case['rows']),**proof))
        if not models:
            models[key] = model
    assert sum(r['compact_rows'] for r in reports) == 945
    assert sum(r['deductions'] for r in reports) == 1111
    assert 'face_count' not in all_reasons

    first = compact['cases'][0]
    model = next(iter(models.values()))
    original = full_cases[(first['link']['order'],first['link']['index'],1)]
    def verify_mutant(mutant):
        return verify_case(mutant,groups[2][0],original,model)
    controls = {}
    mutant = deepcopy(first); mutant['link']['index'] += 1
    controls['wrong_link_id'] = rejected(lambda:verify_mutant(mutant))
    mutant = deepcopy(first); mutant['rows'][0]['terms'][0][1] += 1
    controls['altered_coefficient'] = rejected(lambda:verify_mutant(mutant))
    mutant = deepcopy(first); mutant['original_row_indices'][0] += 1
    controls['wrong_original_row_index'] = rejected(lambda:verify_mutant(mutant))
    mutant = deepcopy(first); mutant['steps'][0]['value'] ^= 1
    controls['wrong_forced_value'] = rejected(lambda:replay(mutant))
    mutant = deepcopy(first); mutant['contradiction_row'] = first['steps'][0]['row']
    controls['noncontradictory_terminal_row'] = rejected(lambda:replay(mutant))
    controls['omitted_case'] = rejected(lambda:assert_same_links(compact['cases'][:-1],groups[2]))
    controls['duplicated_case'] = rejected(lambda:assert_same_links(compact['cases']+[first],groups[2]))

    scope_dependencies = [R/'two-adjacent-negative-cubic-structural-audit.md',
                          R/'two-adjacent-negative-cubic-link-filter-independent.json',
                          R/'one-negative-quadratic-derivative.md',
                          R/'low-residual-derivative-complete-manifest.json',
                          A/'d10-normalization-spheres-independent-verification.json',
                          A/'generic-d10-normalization-audit.md',
                          S/'one-negative-quadratic-derivative-independent-audit.md',
                          S/'one-six-edge-vertex-links-independent-verification.json']
    low_manifest = read(R/'low-residual-derivative-complete-manifest.json')
    # Its artifact list is a frozen, already accepted theorem dependency.
    manifest_bindings = next(v for k,v in low_manifest.items() if isinstance(v,list) and v and
                             isinstance(v[0],dict) and set(v[0]) >= {'path','sha256'})
    check_bindings(manifest_bindings)
    dependencies = {Path(r['path']) for r in compact['sources']+full['sources']+manifest_bindings}
    dependencies.update(catalogs+scope_dependencies+[compact_path,full_path,Path(__file__)])
    result = dict(status='VERIFIED_TWO_ADJACENT_NEGATIVE_CUBIC_ORDINARY_DERIVATIVE_EXCLUSION',
                  global_function_status='UNRESOLVED',
                  scope='Thirteen active variables; c in {1,2}; all ordinary quadratic coefficients 0/1; exactly two adjacent Fourier pair numerators -2, others -1/0; all quartic numerators 0/1.',
                  structural_reduction='Independently reviewed and bound; no special ordinary coefficient2 or nonadjacent exception claim.',
                  sphere_catalog_coverage='Previously independently verified inverse-contraction cover through order12; filtered afresh here.',
                  ordinary_flag_link_classes=[(r['order'],r['index']) for r in groups[0]],
                  private_flag_link_classes=[(r['order'],r['index']) for r in groups[1]],
                  root_link_types=groups[2], cases=reports,
                  compact_rows=sum(r['compact_rows'] for r in reports),
                  exact_integer_deductions=sum(r['deductions'] for r in reports),
                  selected_row_reasons=dict(all_reasons),
                  original_models_bound=18, full_trace_search_or_replay=False,
                  global_face_count_rows_used=0,
                  common_endpoint_flag_rows_used=0,
                  constant_independent_selected_rows=True,
                  controls=dict(cycle4_join_cycle4=join_control(4,4),
                                cycle4_join_cycle6=join_control(4,6),
                                corruption_checks=controls),
                  producer_imports=False, research_solver_used=False,
                  seconds=time.monotonic()-started,
                  dependencies=[bound(p) for p in sorted(dependencies)])
    target = A/'two-adjacent-negative-cubic-independent-verification.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


def assert_same_links(cases, expected):
    assert [c['link'] for c in cases] == expected


if __name__ == '__main__':
    main()
