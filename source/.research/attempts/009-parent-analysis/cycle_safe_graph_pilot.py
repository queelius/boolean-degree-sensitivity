"""Read the residual safe graphs and probe an abstract four-cycle first cover."""
from collections import Counter,defaultdict
from itertools import permutations
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import write_certificate
from abstract_safe_star_pilot import first_map
from verify_coupled_two_positive import literal_embedding,PairChecker
from two_positive_pair_domains import index_rows
from two_positive_four_cube_domains import CubeIndex,propagate,setup
from core_fourier_envelope import core_words

H=Path(__file__).resolve().parent


def run():
    b=Bindings();ledger_path=H/'two-positive-signed-geometry-frontier-cycle103.json';ledger=b.read(ledger_path)
    data=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')
    groups=defaultdict(list)
    for index in ledger['remaining_geometries']:
        actual=data['representatives'][index];core=actual['positive_doubles'][0]&actual['positive_doubles'][1]
        vertices=[v for v in range(14) if core>>v&1]
        edges=[tuple(i for i,v in enumerate(vertices) if q>>v&1) for q in actual['eligible_pairs']]
        key=min(tuple(sorted(tuple(sorted(p[v] for v in edge)) for edge in edges)) for p in permutations(range(4)))
        groups[key].append(index)
    inventory=[dict(canonical_edges=k,geometries=v,degrees=sorted(sum(x in e for e in k) for x in range(4))) for k,v in sorted(groups.items())]
    cyclic=[r for r in inventory if r['degrees']==[2,2,2,2]];assert len(cyclic)==1
    original=data['representatives'][cyclic[0]['geometries'][0]]
    g={k:original[k] for k in ('positive_doubles','eligible_pairs','selected_pair')};g['negative_supports']=[]
    rows=data['domain']['rows'];canonical={}
    for row in rows:canonical.setdefault(row['template'],row['index'])
    maps=[dict(source_row=r['index'],target_row=canonical[r['template']],map=first_map(r,rows[canonical[r['template']]],g)) for r in rows]
    first_path=H/'abstract-safe-four-cycle-first-cover-cycle104.json';assert not first_path.exists()
    first_path.write_text(json.dumps(dict(geometry=g,representative_rows=sorted(canonical.values()),maps=maps),indent=2)+'\n')
    index=index_rows(rows);cubes=CubeIndex.build(rows);pairs,_=setup(g);words,_,delta,_,_=core_words(pairs);records=[]
    for first in sorted(canonical.values()):
        initial=literal_embedding(rows[first],g,g['selected_pair']);proof=propagate(initial,g,index,cubes)
        path=H/f'abstract-safe-four-cycle-first{first:04d}-cycle104.json.gz';write_certificate(path,proof)
        record=dict(first_row=first,status=proof['status'],proof=b.bind(path),domain_sizes=[dict(pair=d['pair'],rows=len(d['rows'])) for d in proof.get('domains',[])])
        records.append(record);print(json.dumps(record),flush=True)
    for name in ('cycle_safe_graph_pilot.py','abstract_safe_star_pilot.py','test_abstract_safe_star_pilot.py','two_positive_four_cube_domains.py','core_fourier_envelope.py'):b.bind(H/name)
    output=H/'abstract-safe-four-cycle-first-pilot-cycle104.json';assert not output.exists()
    output.write_text(json.dumps(dict(status='PROPOSED_ABSTRACT_SAFE_FOUR_CYCLE_FIRST_SCREEN',global_status='UNRESOLVED',independent_audit='PENDING',
        ledger=b.bind(ledger_path),inventory=inventory,geometry=g,first_cover=b.bind(first_path),core_words=len(words),
        words_by_delta=dict(Counter(map(int,delta))),records=records,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]),indent=2)+'\n')
    print(json.dumps(dict(graph_inventory=[dict(degrees=r['degrees'],count=len(r['geometries'])) for r in inventory],core_words=len(words))),flush=True)


if __name__=='__main__':run()
