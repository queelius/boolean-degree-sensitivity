"""Bounded complete third/fourth row covers with every cycle edge marked."""
from argparse import ArgumentParser
from collections import deque
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from verify_coupled_two_positive import literal_embedding,PairChecker
from two_positive_conditional_orbits import coordinate_generators,move
from two_positive_pair_domains import index_rows
from two_positive_four_cube_domains import CubeIndex,propagate

H=Path(__file__).resolve().parent


def marked_cover(g,rows,known,pair,candidates):
    assert candidates==sorted(set(candidates)) and pair in g['eligible_pairs']
    marks=tuple(g['eligible_pairs']);generators=coordinate_generators(known,marks)
    spectra={r:literal_embedding(rows[r],g,pair) for r in candidates}
    def key(s):return tuple(sorted(s.items()))
    lookup={key(s):r for r,s in spectra.items()};assert len(lookup)==len(candidates)
    reached={};representatives=[]
    for first in candidates:
        if first in reached:continue
        index=len(representatives);representatives.append(dict(index=index,row=first));reached[first]=(index,list(range(14)));queue=deque([first])
        while queue:
            current=queue.popleft();_,image=reached[current]
            for generator in generators:
                target=lookup.get(key({move(q,generator):k for q,k in spectra[current].items()}))
                if target is None:continue
                if target not in reached:reached[target]=(index,[generator[v] for v in image]);queue.append(target)
    maps=[]
    for row in candidates:
        target,image=reached[row];inverse=[None]*14
        for old,new in enumerate(image):inverse[new]=old
        assert {move(q,inverse):k for q,k in spectra[row].items()}==spectra[representatives[target]['row']]
        maps.append(dict(source_row=row,representative=target,map=inverse))
    return dict(requested_pair=pair,coordinate_marks=list(marks),initial_known=sorted(known.items()),input_rows=candidates,
                raw_rows=len(candidates),representative_count=len(representatives),representatives=representatives,maps=maps,generators=generators)


def run(first_id,second_id):
    start=monotonic();b=Bindings();authority_path=H/'safe-four-cycle-second-frontier-independent-manifest.json';authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_SAFE_FOUR_CYCLE_SECOND_FRONTIER'
    first=next(r for r in authority['records'] if r['first_row']==first_id);assert second_id in first['remaining_rows']
    child=next(r for r in first['records'] if r['second_row']==second_id);parent=read_certificate(b,child['proof']);assert parent['status']=='NECESSARY_FOUR_CUBE_PAIR_DOMAIN_FIXED_POINT'
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];g=authority['geometry'];known=dict(parent['known'])
    choices=[(len(d['rows']),d['pair']) for d in parent['domains'] if d['pair'] not in (g['selected_pair'],first['second_pair'])]
    _,third_pair=min(choices);fourth_pair=next(p for p in g['eligible_pairs'] if p not in (g['selected_pair'],first['second_pair'],third_pair))
    checker=PairChecker(rows);index=index_rows(rows);cubes=CubeIndex.build(rows)
    candidates=sorted(set(checker.live(g,third_pair,known))&set(next(d['rows'] for d in parent['domains'] if d['pair']==third_pair)))
    cover=marked_cover(g,rows,known,third_pair,candidates)
    prefix=f'four-cycle-a{first_id:04d}-b{second_id:04d}-fixed-cover-cycle106'
    directory=H/prefix;directory.mkdir(exist_ok=True);cover_path=directory/'third-cover.json';assert not cover_path.exists();cover_path.write_text(json.dumps(cover,indent=2)+'\n')
    output=H/(prefix+'.json');assert not output.exists()
    report=dict(status='INCOMPLETE_SAFE_FOUR_CYCLE_THIRD_FOURTH_COVER',global_status='UNRESOLVED',independent_audit='PENDING',
        authority=b.bind(authority_path),geometry=g,first_row=first_id,second_row=second_id,second_pair=first['second_pair'],parent=child['proof'],
        third_pair=third_pair,fourth_pair=fourth_pair,third_cover=b.bind(cover_path),seconds_limit=180,records=[],stop_reason=None)
    def save():
        temp=output.with_suffix('.partial.json');temp.write_text(json.dumps(report,indent=2)+'\n');temp.replace(output)
    save()
    for representative in cover['representatives']:
        if monotonic()-start>180:report['stop_reason']='COVER_TIME_LIMIT';save();return
        third=representative['row'];more=literal_embedding(rows[third],g,third_pair);assert all(q not in known or known[q]==k for q,k in more.items())
        proof=propagate(known|more,g,index,cubes);path=directory/f'third{third:04d}.json.gz';write_certificate(path,proof)
        record=dict(third_row=third,status=proof['status'],proof=b.bind(path))
        if proof['status']=='NECESSARY_FOUR_CUBE_PAIR_DOMAIN_FIXED_POINT':
            fixed={g['selected_pair']:first_id,first['second_pair']:second_id,third_pair:third}
            assert all(d['rows']==[fixed[d['pair']]] for d in proof['domains'] if d['pair'] in fixed)
            new_known=dict(proof['known']);last=sorted(set(checker.live(g,fourth_pair,new_known))&set(next(d['rows'] for d in proof['domains'] if d['pair']==fourth_pair)))
            fourth=marked_cover(g,rows,new_known,fourth_pair,last);last_path=directory/f'third{third:04d}-fourth-cover.json';assert not last_path.exists();last_path.write_text(json.dumps(fourth,indent=2)+'\n')
            record.update(fourth_cover=b.bind(last_path),literal_fourth_rows=len(last),fourth_representatives=[r['row'] for r in fourth['representatives']])
        report['records'].append(record);save()
        print(json.dumps(dict(third=third,status=record['status'],literal_fourth_rows=record.get('literal_fourth_rows',0),fourth_representatives=len(record.get('fourth_representatives',[])),seconds=monotonic()-start)),flush=True)
    for name in ('four_cycle_fixed_cover.py','test_four_cycle_fixed_cover.py','two_positive_conditional_orbits.py','two_positive_four_cube_domains.py'):b.bind(H/name)
    report.update(status='PROPOSED_COMPLETE_SAFE_FOUR_CYCLE_THIRD_FOURTH_COVER',elapsed_seconds=monotonic()-start,
                  sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]);save()


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--first',type=int,required=True);p.add_argument('--second',type=int,required=True);a=p.parse_args();run(a.first,a.second)
