"""Explicit coordinate-map covers under the full conditional spectrum stabilizer.

Automorphisms identify branch assignments, never assert invariance of f.
Every known coefficient, including zero, and each ordered marked pair is
preserved. Completeness depends on explicit maps for all input rows, not on
whether the canonicalizer found the entire automorphism group.
"""
from argparse import ArgumentParser
from collections import defaultdict,deque
from pathlib import Path
from time import monotonic
import json
import pynauty
from compose_class40_same_b_acceptance import Bindings
from verify_coupled_two_positive import PairChecker,literal_embedding

H=Path(__file__).resolve().parent


def move(q,p):return sum(1<<p[v] for v in range(len(p)) if q>>v&1)


def coordinate_generators(known,marks,*,n=14):
    ordered=sorted(known.items());colors=defaultdict(set);adjacency={v:[] for v in range(n+len(ordered))}
    for v in range(n):colors[('coordinate',tuple((m>>v)&1 for m in marks))].add(v)
    for i,(q,k) in enumerate(ordered):
        assert 0<q<1<<n and type(k) is int
        colors[('coefficient',k)].add(n+i)
        for v in range(n):
            if q>>v&1:adjacency[v].append(n+i);adjacency[n+i].append(v)
    graph=pynauty.Graph(n+len(ordered),adjacency_dict=adjacency,vertex_coloring=list(colors.values()))
    raw,_,_,_,_=pynauty.autgrp(graph);result=[]
    for generator in raw:
        p=list(generator[:n]);assert sorted(p)==list(range(n))
        assert {move(q,p):k for q,k in known.items()}==known
        assert tuple(move(m,p) for m in marks)==tuple(marks)
        result.append(p)
    return result


def cover(geometry,rows,known,pair,candidates):
    assert candidates==sorted(set(candidates)) and pair in geometry['eligible_pairs']
    generators=coordinate_generators(known,(geometry['selected_pair'],pair))
    spectra={r:literal_embedding(rows[r],geometry,pair) for r in candidates}
    def key(spectrum):return tuple(sorted((q,k) for q,k in spectrum.items() if k))
    lookup={key(s):r for r,s in spectra.items()};assert len(lookup)==len(candidates)
    reached={};representatives=[]
    for first in candidates:
        if first in reached:continue
        ordinal=len(representatives);representatives.append(dict(index=ordinal,row=first))
        reached[first]=(ordinal,list(range(14)));queue=deque([first])
        while queue:
            source=queue.popleft();_,image=reached[source]
            for generator in generators:
                mapped={move(q,generator):k for q,k in spectra[source].items()}
                target=lookup.get(key(mapped))
                # A partial diagnostic input set need not be group-invariant.
                if target is None:continue
                assert mapped==spectra[target]
                if target not in reached:
                    reached[target]=(ordinal,[generator[v] for v in image]);queue.append(target)
    maps=[]
    for row_id in candidates:
        target,image=reached[row_id];inverse=[None]*14
        for old,new in enumerate(image):inverse[new]=old
        assert {move(q,inverse):k for q,k in spectra[row_id].items()}==spectra[representatives[target]['row']]
        maps.append(dict(source_row=row_id,representative=target,map=inverse))
    return dict(representatives=representatives,maps=maps,generators=generators,
                raw_rows=len(candidates),representative_count=len(representatives))


def run(first_row,output):
    start=monotonic();b=Bindings();data=b.read(H/'two-positive-pair-embeddings.json')
    authority=b.read(H/'two-positive-marked-screens-independent-manifest.json',
                     '87b7221f29281233e1bbfd5c290a44ada628bfbee6b11b498b97b6bf58d295aa')
    accepted=next(r for r in authority['records'] if r['geometry']==18)
    assert first_row in accepted['remaining_rows']
    parents=b.read(accepted['source']['path'],accepted['source']['sha256'])
    meta=next(r for r in parents['records'] if r['row']==first_row);parent=b.read(meta['proof']['path'],meta['proof']['sha256'])
    known=dict(parent['closure']['known']);geometry=data['representatives'][18];rows=data['domain']['rows'];checker=PairChecker(rows)
    options=[(len(checker.live(geometry,p,known)),p,checker.live(geometry,p,known)) for p in geometry['eligible_pairs'] if p!=geometry['selected_pair']]
    _,pair,candidates=min(options)
    result=cover(geometry,rows,known,pair,candidates)
    for name in ('two_positive_conditional_orbits.py','test_two_positive_conditional_orbits.py','verify_coupled_two_positive.py'):b.bind(H/name)
    result.update(status='PROPOSED_COMPLETE_CONDITIONAL_TWO_POSITIVE_ROW_ORBIT_COVER',global_status='UNRESOLVED',
                  independent_audit='PENDING',geometry=18,first_row=first_row,second_pair=pair,
                  initial_known=sorted(known.items()),parent=meta['proof'],parent_authority=b.bind(H/'two-positive-marked-screens-independent-manifest.json'),
                  input_rows=candidates,canonicalizer_trusted_for_completeness=False,elapsed_seconds=monotonic()-start,
                  sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('geometry','first_row','second_pair','raw_rows','representative_count','elapsed_seconds')}))


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--first-row',type=int,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.first_row,a.output)
