"""Independent replay of every fourth-row trace below the accepted fixed cover."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_coupled_two_positive import literal_embedding
from verify_four_cube_pair_domains import LiteralCubeChecker

H=Path(__file__).resolve().parent


def check_choices(choices,records):
    expected=[(r['third_row'],r['fourth_row']) for r in choices]
    actual=[(r['third_row'],r['fourth_row']) for r in records]
    assert actual==expected and len(set(actual))==len(actual)


def run(output):
    b=Bindings();path=H/'four-cycle-a0056-b0056-fixed-projections-cycle106.json';source=b.read(path)
    assert source['status']=='COMPLETE_SCOPED_FOUR_CYCLE_FIXED_PROJECTIONS' and source['stop_reason'] is None
    authority=b.read(source['authority']['path'],source['authority']['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_SCOPED_FOUR_CYCLE_FIXED_COVER'
    assert source['geometry']==authority['geometry'];g=source['geometry'];check_choices(authority['fixed_choices'],source['records'])
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];checker=LiteralCubeChecker(rows);results=[]
    for child in source['records']:
        accepted=next(r for r in authority['records'] if r['third_row']==child['third_row'])
        assert not accepted['independently_excluded'] and accepted['proof']==child['parent']
        parent=read_certificate(b,child['parent']);known=dict(parent['known']);more=literal_embedding(rows[child['fourth_row']],g,authority['fourth_pair'])
        assert all(q not in known or known[q]==k for q,k in more.items())
        proof=read_certificate(b,child['propagation']);answer=checker.replay(known|more,g,proof)
        assert not answer['excluded'] and proof['status']==child['status']=='NECESSARY_FOUR_CUBE_PAIR_DOMAIN_FIXED_POINT'
        fixed={g['selected_pair']:authority['first_row'],authority['second_pair']:authority['second_row'],authority['third_pair']:child['third_row'],authority['fourth_pair']:child['fourth_row']}
        assert answer['domains']==[dict(pair=p,rows=[fixed[p]]) for p in g['eligible_pairs']]
        assert [r['core_mask'] for r in child['projections']]==source['parameters']['masks']
        for projection in child['projections']:
            detail=read_certificate(b,projection['proof']);assert detail['core_mask']==projection['core_mask']
            assert detail['result']['status']==projection['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'
        results.append({**child,'independently_excluded':False})
    for name in ('verify_four_cycle_fixed_frontier.py','test_verify_four_cycle_fixed_frontier.py','verify_four_cube_pair_domains.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_COMPLETE_SCOPED_FOUR_CYCLE_FIXED_FRONTIER',global_status='UNRESOLVED',
        source=b.bind(path),authority=source['authority'],geometry=g,first_row=authority['first_row'],second_row=authority['second_row'],
        second_pair=authority['second_pair'],third_pair=authority['third_pair'],fourth_pair=authority['fourth_pair'],
        records=results,remaining_fixed_choices=len(results),numerically_feasible_projections=sum(len(r['projections']) for r in results),
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(remaining=len(results),status=result['status'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
