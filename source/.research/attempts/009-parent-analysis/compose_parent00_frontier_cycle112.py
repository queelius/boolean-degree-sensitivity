"""Compose the two new exclusions and retain complete surviving projection catalogs."""
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate

H=Path(__file__).resolve().parent
b=Bindings();previous_path=H/'parent00-cubic-position-frontier-cycle111.json'
previous=b.read(previous_path,'def75edd753c090f628bf4df76009c16864d87020657e1fe013d8207ced65f2d')
assert previous['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER'
cover=read_certificate(b,previous['cover']);excluded=list(previous['excluded']);catalogs=[];remaining={r['index']:r for r in previous['remaining']}
paths=[H/'parent00-negative13-euler-independent-manifest-cycle112.json',H/'parent00-direct-cycle-catalogs-independent-manifest-cycle112.json',H/'parent00-link-cycle-catalogs-independent-manifest-cycle112.json']
statuses=['INDEPENDENTLY_VERIFIED_PARENT00_NEGATIVE13_EULER_EXCLUSION','INDEPENDENTLY_VERIFIED_COMPLETE_PARENT00_DIRECT_CUBIC_CATALOGS','INDEPENDENTLY_VERIFIED_COMPLETE_PARENT00_ONE_LINK_CUBIC_CATALOGS']
for path,status in zip(paths,statuses):
    proof=b.read(path);assert proof['status']==status and proof['frontier']==b.bind(previous_path)
    assert proof['geometry']==previous['geometry'] and proof['parent']==previous['parent'] and proof['core_mask']==3 and not proof['whole_parent_excluded']
    for r in proof.get('records',[proof]):
        representative=cover['representatives'][r['index']]
        assert representative['index']==r['index'] and r['negative']==remaining[r['index']]['negative']==representative['pattern']
        if r['negative_position_excluded']:
            assert not r.get('survivors',[])
            positions=sorted(m['pattern'] for m in cover['maps'] if m['representative']==r['index'])
            if 'excluded_literal_positions' in r:assert positions==r['excluded_literal_positions']
            excluded.append(dict(index=r['index'],negative=r['negative'],literal_positions=positions,proof=b.bind(path)));del remaining[r['index']]
        else:
            assert r['survivors'] and all(s['negative']==r['negative'] and s['inputs_checked']==1024 for s in r['survivors'])
            catalogs.append(dict(index=r['index'],negative=r['negative'],survivors=len(r['survivors']),authority=b.bind(path)))
assert sorted(r['index'] for r in excluded)==[0,1,9] and sorted(remaining)==[2,3,4,5,6,7,8]
assert sum(c['survivors'] for c in catalogs)==322
b.bind(H/'compose_parent00_frontier_cycle112.py')
result={k:previous[k] for k in ('geometry','first_row','second_row','parent','core_mask','cover')}
result.update(status='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER',global_status='UNRESOLVED',previous=b.bind(previous_path),
    excluded=sorted(excluded,key=lambda r:r['index']),remaining=[remaining[i] for i in sorted(remaining)],complete_projection_catalogs=sorted(catalogs,key=lambda r:r['index']),
    whole_parent_excluded=False,boolean_function_on14_constructed=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
output=H/'parent00-cubic-position-frontier-cycle112.json';assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(excluded=len(excluded),literal_positions=sum(len(r['literal_positions']) for r in excluded),remaining=len(remaining),catalog_survivors=322)))
