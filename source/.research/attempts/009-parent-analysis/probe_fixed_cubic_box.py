"""Bounded fixed-negative cubic LP placement pilot below one fixed C4 quartet."""
from itertools import combinations
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from generic_parseval_envelope import permitted
from two_positive_four_cube_domains import CubeIndex
from fixed_cubic_box import build
from exact_box_row_lp import solve

H=Path(__file__).resolve().parent


def run():
    b=Bindings();authority_path=H/'four-cycle-a0056-b0056-fixed-frontier-independent-manifest.json';authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_SCOPED_FOUR_CYCLE_FIXED_FRONTIER'
    case=authority['records'][0];parent=read_certificate(b,case['propagation']);g=authority['geometry']
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];values=permitted(g,parent['domains'],CubeIndex.build(rows),[3,12])
    triples=[sum(1<<v for v in t) for t in combinations(range(10),3)];chosen=[triples[i] for i in sorted({0,len(triples)//2,len(triples)-1})];records=[]
    for mask in (3,12):
        for negative in chosen:
            variables,inequalities=build(10,[negative],values[mask]);result=solve(inequalities,len(variables),seconds=3)
            if 'fractional_variables' in result:result['fractional_variables']=int(result['fractional_variables'])
            detail=dict(parent=case['propagation'],core_mask=mask,negative=[negative],variables=variables,result=result)
            path=H/f'fixed-cubic-box-mask{mask:02d}-negative{negative:04d}-cycle107.json.gz';write_certificate(path,detail)
            record=dict(core_mask=mask,negative=[negative],status=result['status'],elapsed_seconds=result['elapsed_seconds'],proof=b.bind(path));records.append(record)
            print(json.dumps({k:v for k,v in record.items() if k!='proof'}),flush=True)
    for name in ('fixed_cubic_box.py','test_fixed_cubic_box.py','probe_fixed_cubic_box.py'):b.bind(H/name)
    output=H/'fixed-cubic-box-pilot-cycle107.json';assert not output.exists()
    output.write_text(json.dumps(dict(status='COMPLETE_SCOPED_FIXED_CUBIC_BOX_PLACEMENT_PILOT',global_status='UNRESOLVED',independent_audit='PENDING',
        authority=b.bind(authority_path),geometry=g,third_row=case['third_row'],fourth_row=case['fourth_row'],parent=case['propagation'],
        chosen_negative_supports=chosen,records=records,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]),indent=2)+'\n')


if __name__=='__main__':run()
