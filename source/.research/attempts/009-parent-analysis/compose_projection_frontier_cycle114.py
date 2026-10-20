"""Compose complete-pair coefficient exclusions with the verified projection orbits."""
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings

H=Path(__file__).resolve().parent;b=Bindings()
joint_path=H/'parent00-joint-pairs-independent-manifest-cycle113.json';joint=b.read(joint_path,'6224a59051dcf5c2b41af5ab1fd97e23348c126a9e819f59927002f312966824')
new_path=H/'parent00-second-coefficient-independent-manifest-cycle114.json';new=b.read(new_path,'e4d3625ca7655925f5b6dbdd0703141a20526daaf974c12a683bf94a4e82b643')
assert new['status']=='INDEPENDENTLY_VERIFIED_CONDITIONAL_SECOND_CUBIC_COEFFICIENT_EXCLUSIONS' and new['authority']==b.bind(joint_path)
orbits=b.read(joint['orbit_cover']['path'],joint['orbit_cover']['sha256']);closed={tuple(k) for k in new['closed_projection_representatives']};records=[]
for orbit in orbits['records']:
    previous=next(s for s in joint['summaries'] if s['index']==orbit['index']);new_reps={j for i,j in closed if i==orbit['index']}
    for j in new_reps:
        old=next(r for r in joint['records'] if (r['index'],r['projection_index'])==(orbit['index'],j))
        accepted=[r for r in new['records'] if (r['index'],r['projection_index'])==(orbit['index'],j)]
        assert len(accepted)==old['surviving_pairs'] and {r['pair_index'] for r in accepted}==set(range(old['surviving_pairs']))
    all_reps=set(previous['excluded_representatives'])|new_reps
    excluded=sorted(m['projection_index'] for m in orbit['maps'] if m['representative'] in all_reps)
    remaining=[r for r in joint['records'] if r['index']==orbit['index'] and r['projection_index'] not in all_reps]
    records.append(dict(index=orbit['index'],catalog_size=orbit['projection_count'],excluded_projection_indices=excluded,
        remaining_projection_indices=sorted(set(range(orbit['projection_count']))-set(excluded)),remaining_representatives=[r['projection_index'] for r in remaining],
        remaining_row_pairs=sum(r['surviving_pairs'] for r in remaining),negative_position_excluded=not remaining))
assert sum(len(r['remaining_projection_indices']) for r in records)==270 and sum(r['remaining_row_pairs'] for r in records)==7404
b.bind(H/'compose_projection_frontier_cycle114.py');output=H/'parent00-coupled-projection-frontier-cycle114.json';assert not output.exists()
result=dict(status='ACCEPTED_PARENT00_COUPLED_PROJECTION_FRONTIER',global_status='UNRESOLVED',geometry=joint['geometry'],parent=joint['parent'],negative_position_frontier=joint['frontier'],
    joint_authority=b.bind(joint_path),coefficient_authority=b.bind(new_path),orbit_cover=joint['orbit_cover'],records=records,whole_parent_excluded=False,
    files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(remaining_projections=270,remaining_row_pairs=7404,remaining_orbits=sum(len(r['remaining_representatives']) for r in records))))
