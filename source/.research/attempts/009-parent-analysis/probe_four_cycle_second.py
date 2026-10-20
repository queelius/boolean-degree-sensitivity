"""Complete second covers and a bounded structural pilot with all four domains."""
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from verify_coupled_two_positive import literal_embedding,PairChecker
from two_positive_conditional_orbits import cover,move
from two_positive_pair_domains import index_rows
from two_positive_four_cube_domains import CubeIndex,propagate

H=Path(__file__).resolve().parent


def run():
    start=monotonic();b=Bindings();source_path=H/'abstract-safe-four-cycle-first-pilot-cycle104.json';source=b.read(source_path)
    assert source['status']=='PROPOSED_ABSTRACT_SAFE_FOUR_CYCLE_FIRST_SCREEN'
    data=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b');rows=data['domain']['rows'];g=source['geometry']
    index=index_rows(rows);cubes=CubeIndex.build(rows);checker=PairChecker(rows);records=[]
    pair=next(p for p in g['eligible_pairs'] if p!=g['selected_pair'] and p&g['selected_pair'])
    for first in source['records']:
        parent=read_certificate(b,first['proof']);assert parent['status']=='NECESSARY_FOUR_CUBE_PAIR_DOMAIN_FIXED_POINT'
        known=dict(parent['known']);candidates=checker.live(g,pair,known)
        domain=next(d['rows'] for d in parent['domains'] if d['pair']==pair)
        candidates=sorted(set(candidates)&set(domain));c=cover(g,rows,known,pair,candidates)
        assert all({move(q,m) for q in g['eligible_pairs']}==set(g['eligible_pairs']) for m in c['generators'])
        c.update(geometry=0,first_row=first['first_row'],second_pair=pair,input_rows=candidates,initial_known=sorted(known.items()),parent=first['proof'])
        cover_path=H/f"abstract-safe-four-cycle-first{first['first_row']:04d}-second-cover-cycle105.json";assert not cover_path.exists()
        cover_path.write_text(json.dumps(c,indent=2)+'\n')
        selected={}
        for representative in c['representatives']:
            row_id=representative['row'];selected.setdefault(rows[row_id]['template'],row_id)
        record=dict(first_row=first['first_row'],parent=first['proof'],second_pair=pair,cover=b.bind(cover_path),literal_second_rows=len(candidates),
                    second_representatives=len(c['representatives']),records=[])
        for second in selected.values():
            more=literal_embedding(rows[second],g,pair);assert all(q not in known or known[q]==k for q,k in more.items())
            proof=propagate(known|more,g,index,cubes)
            path=H/f"abstract-safe-four-cycle-a{first['first_row']:04d}-b{second:04d}-cycle105.json.gz";write_certificate(path,proof)
            entry=dict(second_row=second,template=rows[second]['template'],status=proof['status'],proof=b.bind(path),
                       domain_sizes=[dict(pair=d['pair'],rows=len(d['rows'])) for d in proof.get('domains',[])])
            record['records'].append(entry)
            print(json.dumps(dict(first_row=first['first_row'],second_row=second,status=entry['status'],domain_sizes=entry['domain_sizes'],seconds=monotonic()-start)),flush=True)
        records.append(record)
    for name in ('probe_four_cycle_second.py','two_positive_conditional_orbits.py','test_two_positive_conditional_orbits.py','two_positive_four_cube_domains.py'):b.bind(H/name)
    output=H/'abstract-safe-four-cycle-second-pilot-cycle105.json';assert not output.exists()
    output.write_text(json.dumps(dict(status='COMPLETE_SCOPED_SAFE_FOUR_CYCLE_SECOND_PILOT',global_status='UNRESOLVED',independent_audit='PENDING',
        first_source=b.bind(source_path),geometry=g,records=records,elapsed_seconds=monotonic()-start,
        sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]),indent=2)+'\n')


if __name__=='__main__':run()
