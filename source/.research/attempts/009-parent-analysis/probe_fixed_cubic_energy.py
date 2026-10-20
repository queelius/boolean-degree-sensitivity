"""Complete even-count Parseval pilot on both surviving N=1 cubic positions."""
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from generic_parseval_envelope import permitted
from two_positive_four_cube_domains import CubeIndex
from fixed_cubic_energy import build
from exact_box_row_lp import solve

H=Path(__file__).resolve().parent


def run():
    b=Bindings();authority_path=H/'fixed-cubic-mask03-N1-independent-manifest.json';authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_FIXED_CUBIC_ONE_NEGATIVE_PLACEMENT_SCREEN'
    parent=read_certificate(b,authority['parent']);g=authority['geometry'];mask=authority['core_mask']
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];values=permitted(g,parent['domains'],CubeIndex.build(rows),[mask])[mask];records=[]
    for negative in authority['remaining_negative_supports']:
        for linear_count in range(0,11,2):
            variables,inequalities=build([negative],values,linear_count);result=solve(inequalities,len(variables),seconds=5)
            if 'fractional_variables' in result:result['fractional_variables']=int(result['fractional_variables'])
            detail=dict(parent=authority['parent'],core_mask=mask,negative=[negative],linear_count=linear_count,variables=[v.metadata() for v in variables],result=result)
            path=H/f'fixed-cubic-energy-negative{negative:04d}-Q{linear_count:02d}-cycle107.json.gz';write_certificate(path,detail)
            record=dict(negative=[negative],linear_count=linear_count,status=result['status'],proof=b.bind(path),elapsed_seconds=result['elapsed_seconds']);records.append(record)
            print(json.dumps({k:v for k,v in record.items() if k!='proof'}),flush=True)
    for name in ('fixed_cubic_energy.py','test_fixed_cubic_energy.py','probe_fixed_cubic_energy.py','generic_parseval_envelope.py','signed-divisibility-criterion-cycle107.md','test_signed_divisibility_criterion.py'):b.bind(H/name)
    output=H/'fixed-cubic-energy-pilot-cycle107.json';assert not output.exists()
    output.write_text(json.dumps(dict(status='COMPLETE_SCOPED_FIXED_CUBIC_ENERGY_COUNT_PILOT',global_status='UNRESOLVED',independent_audit='PENDING',
        authority=b.bind(authority_path),geometry=g,parent=authority['parent'],core_mask=mask,records=records,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]),indent=2)+'\n')


if __name__=='__main__':run()
