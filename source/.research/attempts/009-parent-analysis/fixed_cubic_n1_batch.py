"""Complete literal one-negative placement screen for the first missing diagonal."""
from itertools import combinations
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from generic_parseval_envelope import permitted
from two_positive_four_cube_domains import CubeIndex
from fixed_cubic_box import build
from exact_box_row_lp import solve

H=Path(__file__).resolve().parent


def run():
    start=monotonic();b=Bindings();pilot_path=H/'fixed-cubic-box-pilot-cycle107.json';pilot=b.read(pilot_path)
    assert pilot['status']=='COMPLETE_SCOPED_FIXED_CUBIC_BOX_PLACEMENT_PILOT'
    authority=b.read(pilot['authority']['path'],pilot['authority']['sha256']);assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_SCOPED_FOUR_CYCLE_FIXED_FRONTIER'
    case=authority['records'][0];assert case['propagation']==pilot['parent'];parent=read_certificate(b,case['propagation']);g=authority['geometry'];mask=3
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];values=permitted(g,parent['domains'],CubeIndex.build(rows),[mask])[mask]
    negatives=[sum(1<<v for v in t) for t in combinations(range(10),3)];reused={tuple(r['negative']):r for r in pilot['records'] if r['core_mask']==mask}
    directory=H/'fixed-cubic-mask03-N1-batch-cycle107';directory.mkdir(exist_ok=True);output=H/(directory.name+'.json');assert not output.exists()
    report=dict(status='INCOMPLETE_FIXED_CUBIC_ONE_NEGATIVE_PLACEMENT_SCREEN',global_status='UNRESOLVED',independent_audit='PENDING',authority=pilot['authority'],
        geometry=g,parent=case['propagation'],third_row=case['third_row'],fourth_row=case['fourth_row'],core_mask=mask,negative_count=1,
        parameters=dict(seconds_per_lp=3,total_seconds=120),pilot=b.bind(pilot_path),records=[],stop_reason=None)
    def save():
        tmp=output.with_suffix('.partial.json');tmp.write_text(json.dumps(report,indent=2)+'\n');tmp.replace(output)
    save()
    for negative in negatives:
        if monotonic()-start>120:report['stop_reason']='BATCH_TIME_LIMIT';save();return
        if (negative,) in reused:record={**reused[negative,],'reused':True}
        else:
            variables,inequalities=build(10,[negative],values);result=solve(inequalities,len(variables),seconds=3)
            if 'fractional_variables' in result:result['fractional_variables']=int(result['fractional_variables'])
            detail=dict(parent=case['propagation'],core_mask=mask,negative=[negative],variables=variables,result=result)
            path=directory/f'negative{negative:04d}.json.gz';write_certificate(path,detail)
            record=dict(core_mask=mask,negative=[negative],status=result['status'],elapsed_seconds=result['elapsed_seconds'],proof=b.bind(path),reused=False)
        report['records'].append(record);save()
        if len(report['records'])%20==0:print(json.dumps(dict(done=len(report['records']),exact=sum(r['status']=='EXACT_BOX_ROW_LP_CONTRADICTION' for r in report['records']),seconds=monotonic()-start)),flush=True)
    for name in ('fixed_cubic_n1_batch.py','fixed_cubic_box.py','test_fixed_cubic_box.py'):b.bind(H/name)
    report.update(status='COMPLETE_FIXED_CUBIC_ONE_NEGATIVE_PLACEMENT_SCREEN',elapsed_seconds=monotonic()-start,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]);save()


if __name__=='__main__':run()
