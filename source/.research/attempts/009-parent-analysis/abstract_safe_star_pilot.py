"""Relax a safe star by leaving negative quintic supports unspecified.

Only the accepted pair catalog and Boolean four-cube consistency are used.
The full hybrid coefficient model would impose invalid extra domains here.
This file proposes explicit covers and proof records, pending independent audit.
"""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import write_certificate
from verify_coupled_two_positive import literal_embedding,PairChecker
from two_positive_conditional_orbits import cover,move
from two_positive_pair_domains import index_rows,vertices
from two_positive_four_cube_domains import CubeIndex,propagate

H=Path(__file__).resolve().parent


def first_map(source,target,g):
    assert source['template']==target['template']
    before,after=source['source_to_row'],target['source_to_row']
    assert sorted(before)==sorted(after)==list(range(12))
    local=[None]*12
    for original,physical in enumerate(before):local[physical]=after[original]
    p,r=g['positive_doubles'];common=p&r;pair=g['selected_pair']
    image=vertices(p^common)+vertices(r^common)+vertices(common^pair)
    image+=sorted(set(range(14))-set(vertices(pair))-set(image))
    mapping=list(range(14))
    for old,new in enumerate(local):mapping[image[old]]=image[new]
    assert all(move(q,mapping)==q for q in g['eligible_pairs']+g['positive_doubles'])
    assert {move(q,mapping):k for q,k in literal_embedding(source,g,pair).items()}==literal_embedding(target,g,pair)
    return mapping


def run(output):
    start=monotonic();b=Bindings();data=b.read(H/'two-positive-pair-embeddings.json',
                                            '0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')
    original=data['representatives'][18]
    g={k:original[k] for k in ('positive_doubles','eligible_pairs','selected_pair')};g['negative_supports']=[]
    rows=data['domain']['rows'];canonical={}
    for row in rows:canonical.setdefault(row['template'],row['index'])
    first_maps=[dict(source_row=r['index'],target_row=canonical[r['template']],map=first_map(r,rows[canonical[r['template']]],g)) for r in rows]
    first_cover=dict(geometry=g,representative_rows=sorted(canonical.values()),maps=first_maps)
    first_path=output.with_name(output.stem+'-first-cover.json');assert not first_path.exists()
    first_path.write_text(json.dumps(first_cover,indent=2)+'\n')
    result=dict(status='INCOMPLETE_ABSTRACT_SAFE_STAR_SECOND_SCREEN',global_status='UNRESOLVED',independent_audit='PENDING',
                negative_supports_fixed=False,full_hybrid_used=False,geometry=g,first_cover=b.bind(first_path),records=[])
    assert not output.exists()
    def save():
        temp=output.with_suffix('.partial.json');temp.write_text(json.dumps(result,indent=2)+'\n');temp.replace(output)
    save();index=index_rows(rows);cubes=CubeIndex.build(rows);pair=next(p for p in g['eligible_pairs'] if p!=g['selected_pair'])
    for first in sorted(canonical.values()):
        initial=literal_embedding(rows[first],g,g['selected_pair']);proof=propagate(initial,g,index,cubes)
        assert proof['status']=='NECESSARY_FOUR_CUBE_PAIR_DOMAIN_FIXED_POINT'
        path=output.with_name(output.stem+f'-a{first:04d}-first.json.gz');write_certificate(path,proof)
        known=dict(proof['known']);candidates=PairChecker(rows).live(g,pair,known);c=cover(g,rows,known,pair,candidates)
        assert all({move(q,m) for q in g['eligible_pairs']}==set(g['eligible_pairs']) for m in c['generators'])
        c.update(geometry=0,first_row=first,second_pair=pair,input_rows=candidates,initial_known=sorted(known.items()))
        cover_path=output.with_name(output.stem+f'-a{first:04d}-second-cover.json');assert not cover_path.exists()
        cover_path.write_text(json.dumps(c,indent=2)+'\n')
        record=dict(first_row=first,first_proof=b.bind(path),second_pair=pair,cover=b.bind(cover_path),records=[])
        result['records'].append(record);save()
        for request in c['representatives']:
            second=request['row'];more=literal_embedding(rows[second],g,pair)
            assert all(q not in known or known[q]==k for q,k in more.items())
            p=propagate(known|more,g,index,cubes)
            path=output.with_name(output.stem+f'-a{first:04d}-b{second:04d}.json.gz');write_certificate(path,p)
            record['records'].append(dict(second_row=second,status=p['status'],proof=b.bind(path)))
        record['counts']=dict(Counter(r['status'] for r in record['records']))
        record['remaining_rows']=[r['second_row'] for r in record['records'] if r['status']!='EXACT_FOUR_CUBE_PAIR_DOMAIN_CONTRADICTION']
        save();print(json.dumps(dict(first_row=first,representatives=len(c['representatives']),counts=record['counts'],remaining=record['remaining_rows'],elapsed_seconds=monotonic()-start)),flush=True)
    result['status']='PROPOSED_COMPLETE_ABSTRACT_SAFE_STAR_SECOND_SCREEN';result['elapsed_seconds']=monotonic()-start
    for name in ('abstract_safe_star_pilot.py','test_abstract_safe_star_pilot.py','two_positive_conditional_orbits.py','two_positive_four_cube_domains.py','two_positive_pair_domains.py','gzip_certificate_io.py'):b.bind(H/name)
    result['sources']=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())];save()


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();run(args.output)
