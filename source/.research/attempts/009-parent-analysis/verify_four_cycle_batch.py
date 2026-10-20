"""Independently finish every case in the accepted four-cycle second cover."""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_coupled_two_positive import literal_embedding
from verify_four_cube_pair_domains import LiteralCubeChecker
from verify_four_cycle_pilot import check_second

H=Path(__file__).resolve().parent


def validate_rows(expected,records):
    actual=[r['second_row'] for r in records]
    assert len(actual)==len(set(actual)) and actual==expected


def run(output):
    b=Bindings();path=H/'safe-four-cycle-second-batch-cycle105.json';source=b.read(path)
    assert source['status']=='PROPOSED_COMPLETE_SAFE_FOUR_CYCLE_SECOND_FRONTIER' and source['stop_reason'] is None
    authority=b.read(source['authority']['path'],source['authority']['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_SAFE_FOUR_CYCLE_FIRST_AND_SECOND_COVERS_WITH_SCOPED_PILOT'
    assert source['geometry']==authority['geometry'];g=source['geometry']
    assert [r['first_row'] for r in source['records']]==[r['first_row'] for r in authority['records']]
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];checker=LiteralCubeChecker(rows);results=[];done=0
    for record,case in zip(source['records'],authority['records']):
        assert all(record[k]==case[k] for k in ('first_row','parent','second_pair','cover'))
        parent=read_certificate(b,case['parent']);known=dict(parent['known']);cover=b.read(case['cover']['path'],case['cover']['sha256'])
        check_second(rows,g,known,parent['domains'],cover)
        validate_rows([r['row'] for r in cover['representatives']],record['records'])
        children=[];remaining=[];counts=Counter()
        for child in record['records']:
            more=literal_embedding(rows[child['second_row']],g,case['second_pair']);assert all(q not in known or known[q]==k for q,k in more.items())
            proof=read_certificate(b,child['proof']);checked=checker.replay(known|more,g,proof)
            assert proof['status']==child['status'];counts[child['status']]+=1
            if not checked['excluded']:remaining.append(child['second_row'])
            children.append({**child,'independently_excluded':checked['excluded']});done+=1
            if done%25==0:print(json.dumps(dict(checked=done)),flush=True)
        assert record['counts']==dict(counts) and record['remaining_rows']==remaining
        results.append(dict(first_row=case['first_row'],parent=case['parent'],second_pair=case['second_pair'],cover=case['cover'],
            records=children,remaining_rows=remaining,counts=dict(counts)))
        print(json.dumps(dict(first_row=case['first_row'],remaining=len(remaining),counts=dict(counts))),flush=True)
    for name in ('verify_four_cycle_batch.py','test_verify_four_cycle_batch.py','verify_four_cycle_pilot.py','verify_four_cube_pair_domains.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_COMPLETE_SAFE_FOUR_CYCLE_SECOND_FRONTIER',global_status='UNRESOLVED',
        whole_four_cycle_excluded=not any(r['remaining_rows'] for r in results),source=b.bind(path),cover_authority=source['authority'],geometry=g,
        records=results,complete_second_cases=done,remaining_second_cases=sum(len(r['remaining_rows']) for r in results),
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
