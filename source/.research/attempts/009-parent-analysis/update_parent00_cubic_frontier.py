"""Apply the complete cycle exclusion to the previously audited parent cover."""
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate

H=Path(__file__).resolve().parent;b=Bindings()
authority_path=H/'cubic-parent-energy-pilot-independent-manifest-cycle110.json';authority=b.read(authority_path,'58224360b6ec45139c34cff4fafc463fa9511ac98d0dcb4ebea06d0a274dd956')
case=next(r for r in authority['records'] if (r['first_row'],r['second_row'])==(0,0));assert len(case['remaining'])==10
proof_path=H/'parent00-negative7-cycle-independent-manifest-cycle111.json';proof=b.read(proof_path)
assert proof['status']=='INDEPENDENTLY_VERIFIED_PARENT00_NEGATIVE7_CYCLE_ENUMERATION' and proof['negative_position_excluded'] and not proof['survivors']
assert proof['parent']==case['parent'] and proof['geometry']==authority['geometry'] and proof['negative']==[7]
interval=b.read(authority['interval_authority']['path'],authority['interval_authority']['sha256']);parent_case=next(r for r in interval['records'] if r['parent']==case['parent']);cover=read_certificate(b,parent_case['cover'])
matches=[r for r in case['remaining'] if r['negative']==[7]];assert len(matches)==1;index=matches[0]['index'];assert cover['representatives'][index]['pattern']==[7]
excluded_literals=[r['pattern'] for r in cover['maps'] if r['representative']==index];assert excluded_literals==[[7],[11],[19]]
for name in ('update_parent00_cubic_frontier.py','parent00-negative7-cycle-exclusion-proof-cycle111.md'):b.bind(H/name)
result=dict(status='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER',global_status='UNRESOLVED',authority=b.bind(authority_path),geometry=authority['geometry'],
    first_row=0,second_row=0,parent=case['parent'],core_mask=3,cover=parent_case['cover'],
    excluded=[dict(index=index,negative=[7],literal_positions=excluded_literals,proof=b.bind(proof_path))],
    remaining=[r for r in case['remaining'] if r['index']!=index],whole_parent_excluded=False,
    files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
output=H/'parent00-cubic-position-frontier-cycle111.json';assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(excluded_literals=excluded_literals,remaining_representatives=len(result['remaining']))),flush=True)
