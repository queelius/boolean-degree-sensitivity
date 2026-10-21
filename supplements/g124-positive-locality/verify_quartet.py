"""Portable independently replayable graph lemma; MIT, Alexander Richard Towell.
Substantial OpenAI Codex assistance. Classification: Markström and Talbot.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from time import process_time
import json
import packet_io as io

def require(condition,message):
    if not condition:raise ValueError(message)

def same(actual,expected,message):
    require(json.dumps(actual,sort_keys=True,allow_nan=False)==json.dumps(expected,sort_keys=True,allow_nan=False),message)

def mask(vertices):return sum(1<<v for v in vertices)

def literal_graph(edges,n,expected):
    require(type(n) is int and 5<=n<=14 and isinstance(edges,list) and len(edges)==expected and
        all(isinstance(e,(list,tuple)) and len(e)==3 and all(type(v) is int and 0<=v<n for v in e) and
            len(set(e))==3 for e in edges),'Invalid literal native graph schema.')
    graph={tuple(sorted(e)) for e in edges}
    require(len(graph)==expected,'Aliased native graph edges.')
    return graph

def quartet_first_locality(graph,n):
    require(type(graph) is set,'A literal set of edges is required.')
    graph=literal_graph(list(graph),n,len(graph))
    triples=list(combinations(range(n),3));quartets=list(combinations(range(n),4))
    obstructions={t:[] for t in triples if t not in graph}
    # Distribute each saturated quartet to its missing faces, rather than
    # searching all quartets separately from each missing triple.
    for quartet in quartets:
        faces=list(combinations(quartet,3));present=[t for t in faces if t in graph]
        require(len(present)<=2,'Literal graph is not free: a quartet has at least three edges.')
        if len(present)==2:
            for face in faces:
                if face not in graph:obstructions[face].append(quartet)
    qsets={q:frozenset(q) for q in quartets}
    windows={};local={t:[] for t in obstructions}
    # Enumerate every five-set directly. Zero-obstruction triples are excluded
    # explicitly; no required-union completion algorithm is reused.
    for window in combinations(range(n),5):
        ws=frozenset(window);active=[]
        for face in combinations(window,3):
            obs=obstructions.get(face)
            if obs and all(qsets[q]<=ws for q in obs):active.append(mask(face));local[face].append(mask(window))
        if active:windows[mask(window)]=sorted(active)
    rows=[]
    for triple,obs in obstructions.items():
        required=set(triple)
        for q in obs:required.update(q)
        rows.append(dict(triple=mask(triple),obstruction_quartets=[mask(q) for q in obs],required_mask=mask(required),
            positive_local_five_sets=sorted(local[triple])))
    return dict(missing_triples=rows,missing_obstruction_histogram=[dict(obstructions=k,triples=v) for k,v in
        sorted(Counter(len(obs) for obs in obstructions.values()).items())],
        positive_localizable_five_sets=[dict(five_set=q,missing_triples=v) for q,v in sorted(windows.items())],
        maximum_positive_localizable_in_a_five_set=max(map(len,windows.values()),default=0),
        violating_five_sets=[dict(five_set=q,missing_triples=v) for q,v in sorted(windows.items()) if len(v)>=2])

def incidence_invariant(graph,n):
    # Accumulate incidences edge-by-edge; the producer instead scans all edges
    # separately for each vertex/pair. Actual invariant tuples, not hashes,
    # establish distinction between all native rows.
    degrees=[0]*n;co=[[0]*n for _ in range(n)]
    for triple in graph:
        for v in triple:degrees[v]+=1
        for i,j in combinations(triple,2):co[i][j]+=1;co[j][i]+=1
    rows=[]
    for i,j in combinations(range(n),2):
        neighbors=[]
        for k in range(n):
            if k not in (i,j):neighbors.append((degrees[k],min(co[i][k],co[j][k]),max(co[i][k],co[j][k]),int(tuple(sorted((i,j,k))) in graph)))
        rows.append((tuple(sorted((degrees[i],degrees[j]))),co[i][j],tuple(sorted(neighbors))))
    return tuple(sorted(rows))

def require_distinct(signatures):
    require(len(set(signatures))==len(signatures),'Actual full graph incidence invariant tuples are not distinct.')

def check_graph(graph,index):
    locality=quartet_first_locality(graph,14);signature=incidence_invariant(graph,14)
    record=dict(catalog_index=index,graph_edges=sorted(map(mask,graph)),
        invariant_sha256=sha256(json.dumps(signature,separators=(',',':')).encode()).hexdigest(),**locality)
    return record,signature

def compare_record(source,computed):
    same(source,computed,'Literal native graph, obstruction, invariant or complete five-window record differs.')

def audit_record(edges,index):return check_graph(literal_graph(edges,14,124),index)

def audit(cpu_budget=60):
    start=process_time();catalog,certificate,bindings=io.inputs();signatures=[];maximum=0;positive=0;completed=[]
    for index,edges in enumerate(catalog['graphs']):
        if process_time()-start>cpu_budget:return io.incomplete(completed,bindings)
        record,signature=audit_record(edges,index);compare_record(certificate['records'][index],record)
        require(record['maximum_positive_localizable_in_a_five_set']<=1 and not record['violating_five_sets'],'Positive-locality counterexample.')
        signatures.append(signature);maximum=max(maximum,record['maximum_positive_localizable_in_a_five_set']);positive+=sum(len(w['missing_triples']) for w in record['positive_localizable_five_sets']);completed.append(index)
    require_distinct(signatures);same(maximum,certificate['maximum_positive_localizable_in_a_five_set'],'Wrong maximum summary.');io.rehash(bindings)
    return dict(status='VERIFIED_RELATIVE_TO_EXTERNAL_CLASSIFICATION',method='Saturated-quartet-first face distribution and direct every-five-set scan',native_graphs=75,edges_per_graph=124,missing_triples_checked=18000,five_sets_checked=150150,literal_quartets_checked=75075,positive_locality_incidents=positive,maximum_positive_localizable_in_a_five_set=maximum,actual_full_invariant_tuples_distinct=True,completed_native_indices=completed,bindings=bindings,external_classification_reproved=False,Boolean_problem_solved=False,CPU_seconds=process_time()-start)

if __name__=='__main__':io.main(audit,__file__)
