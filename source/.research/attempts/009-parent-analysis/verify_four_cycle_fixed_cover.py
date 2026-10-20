"""Literal independent audit of a complete third/fourth conditional cover."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_coupled_two_positive import literal_embedding
from verify_four_cube_pair_domains import LiteralCubeChecker
from verify_four_cycle_pilot import check_second
from verify_two_positive_conditional_orbits import relabel

H=Path(__file__).resolve().parent


def check_marked_cover(rows,g,known,domains,cover):
    assert cover['coordinate_marks']==g['eligible_pairs']
    count=check_second(rows,g,known,domains,{**cover,'second_pair':cover['requested_pair']})
    for image in {tuple(w['map']) for w in cover['maps']}:
        assert all(relabel(q,image)==q for q in cover['coordinate_marks'])
    return count


def check_record_cover(cover,records):
    assert [r['third_row'] for r in records]==[r['row'] for r in cover['representatives']]


def run(source_path,output):
    b=Bindings();source=b.read(source_path)
    assert source['status']=='PROPOSED_COMPLETE_SAFE_FOUR_CYCLE_THIRD_FOURTH_COVER' and source['stop_reason'] is None
    authority=b.read(source['authority']['path'],source['authority']['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_SAFE_FOUR_CYCLE_SECOND_FRONTIER'
    g=source['geometry'];assert g==authority['geometry']
    first=next(r for r in authority['records'] if r['first_row']==source['first_row'])
    assert source['second_pair']==first['second_pair'] and source['second_row'] in first['remaining_rows']
    second=next(r for r in first['records'] if r['second_row']==source['second_row'])
    assert second['proof']==source['parent'] and not second['independently_excluded']
    parent=read_certificate(b,source['parent']);known=dict(parent['known'])
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows']
    cover=b.read(source['third_cover']['path'],source['third_cover']['sha256'])
    assert cover['requested_pair']==source['third_pair']
    assert set((g['selected_pair'],source['second_pair'],source['third_pair'],source['fourth_pair']))==set(g['eligible_pairs'])
    count=check_marked_cover(rows,g,known,parent['domains'],cover);check_record_cover(cover,source['records'])
    checker=LiteralCubeChecker(rows);results=[];fixed=[]
    for child in source['records']:
        more=literal_embedding(rows[child['third_row']],g,source['third_pair'])
        assert all(q not in known or known[q]==k for q,k in more.items())
        proof=read_certificate(b,child['proof']);answer=checker.replay(known|more,g,proof)
        assert proof['status']==child['status']
        if answer['excluded']:
            assert 'fourth_cover' not in child
        else:
            chosen={g['selected_pair']:source['first_row'],source['second_pair']:source['second_row'],source['third_pair']:child['third_row']}
            assert all(d['rows']==[chosen[d['pair']]] for d in answer['domains'] if d['pair'] in chosen)
            fourth=b.read(child['fourth_cover']['path'],child['fourth_cover']['sha256'])
            assert fourth['requested_pair']==source['fourth_pair']
            check_marked_cover(rows,g,answer['known'],answer['domains'],fourth)
            assert child['literal_fourth_rows']==fourth['raw_rows']
            assert child['fourth_representatives']==[r['row'] for r in fourth['representatives']]
            fixed.extend(dict(third_row=child['third_row'],fourth_row=r) for r in child['fourth_representatives'])
        results.append({**child,'independently_excluded':answer['excluded']})
        print(json.dumps(dict(third_row=child['third_row'],excluded=answer['excluded'],fixed_choices=len(fixed))),flush=True)
    for name in ('verify_four_cycle_fixed_cover.py','test_verify_four_cycle_fixed_cover.py','verify_four_cycle_pilot.py','verify_four_cube_pair_domains.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_COMPLETE_SCOPED_FOUR_CYCLE_FIXED_COVER',global_status='UNRESOLVED',
        source=b.bind(source_path),authority=source['authority'],geometry=g,first_row=source['first_row'],second_row=source['second_row'],
        second_pair=source['second_pair'],third_pair=source['third_pair'],fourth_pair=source['fourth_pair'],parent=source['parent'],
        third_cover=source['third_cover'],third_representatives=count,records=results,fixed_choices=fixed,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.source,a.output)
