"""Finish the complete258-case second frontier using the accepted four-cycle covers."""
from collections import Counter
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from verify_coupled_two_positive import literal_embedding
from two_positive_pair_domains import index_rows
from two_positive_four_cube_domains import CubeIndex,propagate

H=Path(__file__).resolve().parent


def run():
    start=monotonic();b=Bindings();authority_path=H/'safe-four-cycle-first-second-covers-independent-manifest.json';authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_SAFE_FOUR_CYCLE_FIRST_AND_SECOND_COVERS_WITH_SCOPED_PILOT'
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];g=authority['geometry'];index=index_rows(rows);cubes=CubeIndex.build(rows)
    directory=H/'safe-four-cycle-second-batch-cycle105';directory.mkdir(exist_ok=True)
    output=H/'safe-four-cycle-second-batch-cycle105.json';assert not output.exists()
    report=dict(status='INCOMPLETE_SAFE_FOUR_CYCLE_SECOND_FRONTIER',global_status='UNRESOLVED',independent_audit='PENDING',
        authority=b.bind(authority_path),geometry=g,seconds_limit=180,records=[],stop_reason=None)
    def save():
        temp=output.with_suffix('.partial.json');temp.write_text(json.dumps(report,indent=2)+'\n');temp.replace(output)
    save();done=0
    for first in authority['records']:
        parent=read_certificate(b,first['parent']);known=dict(parent['known']);cover=b.read(first['cover']['path'],first['cover']['sha256'])
        reuse={r['second_row']:r for r in first['pilot_records']};record=dict(first_row=first['first_row'],parent=first['parent'],second_pair=first['second_pair'],cover=first['cover'],records=[])
        report['records'].append(record)
        for representative in cover['representatives']:
            if monotonic()-start>180:report['stop_reason']='BATCH_TIME_LIMIT';save();return
            second=representative['row']
            if second in reuse:proof=read_certificate(b,reuse[second]['proof']);binding=reuse[second]['proof']
            else:
                more=literal_embedding(rows[second],g,first['second_pair']);assert all(q not in known or known[q]==k for q,k in more.items())
                proof=propagate(known|more,g,index,cubes)
                path=directory/f"a{first['first_row']:04d}-b{second:04d}.json.gz";write_certificate(path,proof);binding=b.bind(path)
            record['records'].append(dict(second_row=second,status=proof['status'],proof=binding,reused_pilot=second in reuse));done+=1
            if done%25==0:save();print(json.dumps(dict(done=done,seconds=monotonic()-start)),flush=True)
        record['remaining_rows']=[r['second_row'] for r in record['records'] if r['status']!='EXACT_FOUR_CUBE_PAIR_DOMAIN_CONTRADICTION']
        record['counts']=dict(Counter(r['status'] for r in record['records']));save()
        print(json.dumps(dict(first_row=first['first_row'],cases=len(record['records']),counts=record['counts'])),flush=True)
    for name in ('four_cycle_second_batch.py','two_positive_four_cube_domains.py','test_two_positive_four_cube_domains.py'):b.bind(H/name)
    report.update(status='PROPOSED_COMPLETE_SAFE_FOUR_CYCLE_SECOND_FRONTIER',elapsed_seconds=monotonic()-start,
                  sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]);save()


if __name__=='__main__':run()
