"""Compose a verified incremental transfer cover and its explicit projection orbits."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate

H=Path(__file__).resolve().parent


def run(authority_path,output,positions_output):
    b=Bindings();authority=b.read(authority_path);assert authority['status']=='INDEPENDENTLY_VERIFIED_INCREMENTAL_CUBIC_COEFFICIENT_TRANSFERS'
    previous=b.read(authority['frontier']['path'],authority['frontier']['sha256']);assert previous['status']=='ACCEPTED_PARENT00_COUPLED_PROJECTION_FRONTIER'
    assert authority['geometry']==previous['geometry'] and authority['parent']==previous['parent'];orbits=b.read(previous['orbit_cover']['path'],previous['orbit_cover']['sha256']);records=[];new_closed=[]
    for old in previous['records']:
        updates=[r for r in authority['records'] if r['index']==old['index']]
        assert {r['projection_index'] for r in updates}==set(old['remaining_representatives'])
        closed={r['projection_index'] for r in updates if r['projection_excluded']};orbit=next(r for r in orbits['records'] if r['index']==old['index'])
        excluded=set(old['excluded_projection_indices'])|{m['projection_index'] for m in orbit['maps'] if m['representative'] in closed}
        record=dict(index=old['index'],catalog_size=old['catalog_size'],excluded_projection_indices=sorted(excluded),
            remaining_projection_indices=sorted(set(range(old['catalog_size']))-excluded),remaining_representatives=[r['projection_index'] for r in updates if not r['projection_excluded']],
            remaining_row_pairs=sum(r['remaining_pairs'] for r in updates),remaining_count_cases=sum(r['remaining_count_cases'] for r in updates),negative_position_excluded=not any(not r['projection_excluded'] for r in updates))
        assert bool(record['remaining_projection_indices'])==bool(record['remaining_representatives'])
        if record['negative_position_excluded'] and not old['negative_position_excluded']:new_closed.append(old['index'])
        records.append(record)
    b.bind(H/'compose_coupled_projection_frontier.py');position_ref=previous['negative_position_frontier']
    if new_closed:
        assert positions_output is not None and not positions_output.exists();positions=b.read(position_ref['path'],position_ref['sha256']);cover=read_certificate(b,positions['cover'])
        assert positions['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER';remaining={r['index']:r for r in positions['remaining']};excluded=list(positions['excluded'])
        for i in new_closed:
            case=remaining.pop(i);assert cover['representatives'][i]['pattern']==case['negative']
            excluded.append(dict(index=i,negative=case['negative'],literal_positions=sorted(m['pattern'] for m in cover['maps'] if m['representative']==i),
                proof=b.bind(authority_path),previous_projection_frontier=authority['frontier']))
        new={k:positions[k] for k in ('geometry','first_row','second_row','parent','core_mask','cover')}
        new.update(status='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER',global_status='UNRESOLVED',previous=position_ref,excluded=sorted(excluded,key=lambda r:r['index']),remaining=[remaining[i] for i in sorted(remaining)],
            whole_parent_excluded=not remaining,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
        positions_output.write_text(json.dumps(new,indent=2)+'\n');position_ref=b.bind(positions_output)
    result={k:previous[k] for k in ('geometry','parent','joint_authority','orbit_cover')}
    result.update(status='ACCEPTED_PARENT00_COUPLED_PROJECTION_FRONTIER',global_status='UNRESOLVED',previous=authority['frontier'],pair_authority=b.bind(authority_path),negative_position_frontier=position_ref,
        records=records,newly_closed_negative_positions=new_closed,whole_parent_excluded=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(remaining_projections=sum(len(r['remaining_projection_indices']) for r in records),remaining_orbits=sum(len(r['remaining_representatives']) for r in records),remaining_pairs=sum(r['remaining_row_pairs'] for r in records),remaining_count_cases=sum(r['remaining_count_cases'] for r in records),newly_closed_positions=new_closed)))


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--authority',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--positions-output',type=Path);a=p.parse_args();run(a.authority,a.output,a.positions_output)
