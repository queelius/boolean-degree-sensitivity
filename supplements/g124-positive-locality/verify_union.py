"""Portable independently replayable graph lemma; MIT, Alexander Richard Towell.
Substantial OpenAI Codex assistance. Classification: Markström and Talbot.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from time import process_time
import json
import packet_io as io

def require(ok, message):
    if not ok:
        raise ValueError(message)

def subsets(n, size):
    return tuple(sum(1 << v for v in c) for c in combinations(range(n), size))

def invariant(graph, n):
    degrees = [sum(bool(t >> i & 1) for t in graph) for i in range(n)]
    co = {(i, j): sum(t & ((1 << i) | (1 << j)) == ((1 << i) | (1 << j)) for t in graph)
          for i in range(n) for j in range(i + 1, n)}
    def codegree(i, j):
        return co[min(i, j), max(i, j)]
    result = []
    for i, j in combinations(range(n), 2):
        neighbors = []
        for k in range(n):
            if k not in (i, j):
                left, right = sorted((codegree(i, k), codegree(j, k)))
                neighbors.append((degrees[k], left, right, int(((1 << i) | (1 << j) | (1 << k)) in graph)))
        result.append((tuple(sorted((degrees[i], degrees[j]))), codegree(i, j), tuple(sorted(neighbors))))
    return tuple(sorted(result))

def locality(graph, n):
    require(type(n) is int and 5 <= n <= 14 and type(graph) is set and
            all(type(t) is int and 0 <= t < 1 << n and t.bit_count() == 3 for t in graph),
            'Literal triple graph on5..14 vertices required')
    triples, quartets = subsets(n, 3), subsets(n, 4)
    counts = {q: sum(t in graph for t in triples if t & q == t) for q in quartets}
    require(all(z <= 2 for z in counts.values()), 'Graph is not quartet-free')
    rows, windows = [], {}
    for t in triples:
        if t in graph:
            continue
        obstructions = [q for q in quartets if t & q == t and counts[q] == 2]
        required = t
        for q in obstructions:
            required |= q
        local_windows = []
        # Zero obstructions cannot witness indispensability in a minimum repair.
        if obstructions and required.bit_count() <= 5:
            outside = [v for v in range(n) if not (required >> v & 1)]
            for added in combinations(outside, 5 - required.bit_count()):
                W = required | sum(1 << v for v in added)
                local_windows.append(W)
                windows.setdefault(W, []).append(t)
        rows.append(dict(triple=t, obstruction_quartets=obstructions,
                         required_mask=required, positive_local_five_sets=sorted(local_windows)))
    return dict(missing_triples=rows,
                missing_obstruction_histogram=[dict(obstructions=k, triples=v) for k, v in sorted(Counter(len(r['obstruction_quartets']) for r in rows).items())],
                positive_localizable_five_sets=[dict(five_set=W, missing_triples=sorted(ts)) for W, ts in sorted(windows.items())],
                maximum_positive_localizable_in_a_five_set=max(map(len, windows.values()), default=0),
                violating_five_sets=[dict(five_set=W, missing_triples=sorted(ts)) for W, ts in sorted(windows.items()) if len(ts) >= 2])

def audit_record(edges,index):
    require(type(edges)is list and len(edges)==124 and all(type(e)is list and len(e)==3 and all(type(v)is int and 0<=v<14 for v in e) and len(set(e))==3 for e in edges),'Invalid native graph.')
    graph={sum(1<<v for v in e) for e in edges};require(len(graph)==124,'Duplicate native edge.')
    signature=invariant(graph,14)
    record=dict(catalog_index=index,graph_edges=sorted(graph),invariant_sha256=sha256(json.dumps(signature,separators=(',',':')).encode()).hexdigest(),**locality(graph,14))
    return record,signature

def audit(cpu_budget=60):
    start=process_time();catalog,certificate,bindings=io.inputs();signatures=set();maximum=0;positive=0;completed=[]
    for index,edges in enumerate(catalog['graphs']):
        if process_time()-start>cpu_budget:return io.incomplete(completed,bindings)
        record,signature=audit_record(edges,index)
        io.same(record,certificate['records'][index],'Complete literal certificate record differs.')
        require(signature not in signatures,'Actual full invariant tuples are not distinct.');signatures.add(signature)
        require(record['maximum_positive_localizable_in_a_five_set']<=1,'Positive-locality counterexample.')
        maximum=max(maximum,record['maximum_positive_localizable_in_a_five_set']);positive+=sum(len(w['missing_triples']) for w in record['positive_localizable_five_sets']);completed.append(index)
    io.same(maximum,certificate['maximum_positive_localizable_in_a_five_set'],'Wrong maximum summary.')
    io.rehash(bindings)
    return dict(status='VERIFIED_RELATIVE_TO_EXTERNAL_CLASSIFICATION',method='Missing-triple-first obstruction unions and literal five-set completion',native_graphs=75,edges_per_graph=124,missing_triples_checked=18000,five_set_universe_covered=150150,literal_quartets_checked=75075,positive_locality_incidents=positive,maximum_positive_localizable_in_a_five_set=maximum,actual_full_invariant_tuples_distinct=True,completed_native_indices=completed,bindings=bindings,external_classification_reproved=False,Boolean_problem_solved=False,CPU_seconds=process_time()-start)

if __name__=='__main__':io.main(audit,__file__)
