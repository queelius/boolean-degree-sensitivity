"""Accept independently checked sparse transfers and retain exact surviving counts."""
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings

H=Path(__file__).resolve().parent;b=Bindings()
previous_path=H/'parent00-coupled-projection-frontier-cycle114.json';previous=b.read(previous_path)
path=H/'parent00-coefficient-transfers-independent-manifest-cycle115.json';authority=b.read(path)
assert authority['status']=='INDEPENDENTLY_VERIFIED_PARENT00_VARIABLE_CUBIC_CERTIFICATE_TRANSFERS' and authority['frontier']==b.bind(previous_path)
orbits=b.read(previous['orbit_cover']['path'],previous['orbit_cover']['sha256']);records=[]
for old in previous['records']:
    updates=[r for r in authority['records'] if r['index']==old['index']];assert {r['projection_index'] for r in updates}==set(old['remaining_representatives'])
    closed={r['projection_index'] for r in updates if r['projection_excluded']};orbit=next(r for r in orbits['records'] if r['index']==old['index'])
    excluded=set(old['excluded_projection_indices'])|{m['projection_index'] for m in orbit['maps'] if m['representative'] in closed}
    record=dict(index=old['index'],catalog_size=old['catalog_size'],excluded_projection_indices=sorted(excluded),
        remaining_projection_indices=sorted(set(range(old['catalog_size']))-excluded),remaining_representatives=[r['projection_index'] for r in updates if not r['projection_excluded']],
        remaining_row_pairs=sum(r['remaining_pairs'] for r in updates),remaining_count_cases=sum(r['remaining_count_cases'] for r in updates),negative_position_excluded=not any(not r['projection_excluded'] for r in updates))
    records.append(record)
assert sum(len(r['remaining_projection_indices']) for r in records)==172 and sum(r['remaining_row_pairs'] for r in records)==3974 and sum(r['remaining_count_cases'] for r in records)==6376
b.bind(H/'compose_projection_frontier_cycle115.py');output=H/'parent00-coupled-projection-frontier-cycle115.json';assert not output.exists()
result={k:previous[k] for k in ('geometry','parent','negative_position_frontier','joint_authority','orbit_cover')}
result.update(status='ACCEPTED_PARENT00_COUPLED_PROJECTION_FRONTIER',global_status='UNRESOLVED',previous=b.bind(previous_path),pair_authority=b.bind(path),records=records,whole_parent_excluded=False,
    files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(remaining_projections=sum(len(r['remaining_projection_indices']) for r in records),remaining_orbits=sum(len(r['remaining_representatives']) for r in records),remaining_pairs=3974,remaining_count_cases=6376)))
