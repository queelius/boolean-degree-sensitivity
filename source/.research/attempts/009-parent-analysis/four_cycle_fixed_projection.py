"""Bounded fixed-four-derivative pilot with exact interval LP certificates."""
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from verify_coupled_two_positive import literal_embedding
from two_positive_pair_domains import index_rows
from two_positive_four_cube_domains import CubeIndex,propagate
from core_fourier_envelope import envelopes
from unspecified_negative_envelope import build_projection
from exact_box_row_lp import solve

H=Path(__file__).resolve().parent


def run():
    start=monotonic();b=Bindings();authority_path=H/'four-cycle-a0056-b0056-fixed-cover-independent-manifest.json';authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_SCOPED_FOUR_CYCLE_FIXED_COVER'
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows']
    g=authority['geometry'];index=index_rows(rows);cubes=CubeIndex.build(rows)
    directory=H/'four-cycle-a0056-b0056-fixed-projections-cycle106';directory.mkdir(exist_ok=True)
    output=H/(directory.name+'.json');assert not output.exists()
    report=dict(status='INCOMPLETE_SCOPED_FOUR_CYCLE_FIXED_PROJECTIONS',global_status='UNRESOLVED',independent_audit='PENDING',
        authority=b.bind(authority_path),geometry=g,parameters=dict(seconds_per_lp=3,total_seconds=180,masks=[3,12,1,2,4,8]),records=[],stop_reason=None)
    def save():
        tmp=output.with_suffix('.partial.json');tmp.write_text(json.dumps(report,indent=2)+'\n');tmp.replace(output)
    save()
    for choice in authority['fixed_choices']:
        if monotonic()-start>180:report['stop_reason']='PILOT_TIME_LIMIT';save();return
        third,fourth=choice['third_row'],choice['fourth_row']
        parent_ref=next(r['proof'] for r in authority['records'] if r['third_row']==third);parent=read_certificate(b,parent_ref)
        known=dict(parent['known']);more=literal_embedding(rows[fourth],g,authority['fourth_pair']);assert all(q not in known or known[q]==k for q,k in more.items())
        proof=propagate(known|more,g,index,cubes);path=directory/f't{third:04d}-u{fourth:04d}-propagation.json.gz';write_certificate(path,proof)
        record={**choice,'parent':parent_ref,'propagation':b.bind(path),'status':proof['status'],'projections':[]}
        if proof['status']=='NECESSARY_FOUR_CUBE_PAIR_DOMAIN_FIXED_POINT':
            assert all(len(d['rows'])==1 for d in proof['domains']);known=dict(proof['known']);env=envelopes(g,proof['domains'],cubes)
            record['retained_cube_maximum']=max(env['retained_cubes'])
            for mask in report['parameters']['masks']:
                variables,inequalities=build_projection(g,known,env,mask);result=solve(inequalities,len(variables),seconds=3)
                if 'fractional_variables' in result:result['fractional_variables']=int(result['fractional_variables'])
                detail=dict(core_mask=mask,variables=[dict(support=v.support,role=v.role.value) for v in variables],result=result)
                lp_path=directory/f't{third:04d}-u{fourth:04d}-mask{mask:02d}.json.gz';write_certificate(lp_path,detail)
                record['projections'].append(dict(core_mask=mask,status=result['status'],proof=b.bind(lp_path),elapsed_seconds=result['elapsed_seconds']))
                if result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION':break
        report['records'].append(record);save()
        print(json.dumps(dict(third=third,fourth=fourth,status=record['status'],projections=[r['status'] for r in record['projections']],seconds=monotonic()-start)),flush=True)
    for name in ('four_cycle_fixed_projection.py','unspecified_negative_envelope.py','test_unspecified_negative_envelope.py','core_fourier_envelope.py','exact_box_row_lp.py'):b.bind(H/name)
    report.update(status='COMPLETE_SCOPED_FOUR_CYCLE_FIXED_PROJECTIONS',elapsed_seconds=monotonic()-start,
        sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]);save()


if __name__=='__main__':run()
