"""Count/Parseval broadening pilot on the three56/56 survivors and two0/0 controls."""
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from generic_parseval_envelope import permitted
from two_positive_four_cube_domains import CubeIndex
from fixed_cubic_energy import build
from exact_box_row_lp import solve

H=Path(__file__).resolve().parent


def run():
    start=monotonic();b=Bindings();source_path=H/'cubic-parent-pattern-pilot-independent-manifest-cycle110.json';source=b.read(source_path)
    assert source['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_TWO_FIXED_ROW_CUBIC_INTERVAL_COVERS'
    g=source['geometry'];data=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b');cubes=CubeIndex.build(data['domain']['rows'])
    directory=H/'cubic-parent-energy-pilot-cycle110';output=directory.with_suffix('.json');assert not output.exists() and not directory.exists();directory.mkdir()
    report=dict(status='INCOMPLETE_TWO_FIXED_ROW_CUBIC_ENERGY_PILOT',global_status='UNRESOLVED',independent_audit='PENDING',
        authority=b.bind(source_path),geometry=g,core_mask=3,parameters=dict(seconds_per_lp=5,total_seconds=180),cases=[],stop_reason=None)
    def save():
        tmp=output.with_suffix('.partial.json');tmp.write_text(json.dumps(report,indent=2)+'\n');tmp.replace(output)
    save()
    for case in source['records']:
        selected=[r for r in case['remaining'] if case['first_row']==56 or r['negative'] in ([7],[13,50])]
        parent=read_certificate(b,case['parent']);values=permitted(g,parent['domains'],cubes,[3])[3]
        current=dict(first_row=case['first_row'],second_row=case['second_row'],parent=case['parent'],selected=selected,records=[],complete=False);report['cases'].append(current)
        for pattern in selected:
            for count in range(0,11,2):
                if monotonic()-start>180:report['stop_reason']='BATCH_TIME_LIMIT';save();return
                negative=pattern['negative'];variables,rows=build(negative,values,count);solved=solve(rows,len(variables),seconds=5)
                if 'fractional_variables' in solved:solved['fractional_variables']=int(solved['fractional_variables'])
                path=directory/f'a{case["first_row"]:04d}-b{case["second_row"]:04d}-r{pattern["index"]:04d}-Q{count:02d}.json.gz'
                write_certificate(path,dict(parent=case['parent'],core_mask=3,negative=negative,linear_count=count,variables=[v.metadata() for v in variables],result=solved))
                record=dict(index=pattern['index'],negative=negative,linear_count=count,status=solved['status'],proof=b.bind(path));current['records'].append(record);save()
            print(json.dumps(dict(first=case['first_row'],second=case['second_row'],negative=negative,exact=sum(r['status']=='EXACT_BOX_ROW_LP_CONTRADICTION' for r in current['records'] if r['index']==pattern['index']),seconds=monotonic()-start)),flush=True)
        current['complete']=True;save()
    for name in ('probe_cubic_parent_energy.py','fixed_cubic_energy.py','test_fixed_cubic_two_negative_models.py','signed-divisibility-criterion-cycle107.md'):b.bind(H/name)
    report.update(status='COMPLETE_TWO_FIXED_ROW_CUBIC_ENERGY_PILOT',elapsed_seconds=monotonic()-start,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]);save()


if __name__=='__main__':run()
