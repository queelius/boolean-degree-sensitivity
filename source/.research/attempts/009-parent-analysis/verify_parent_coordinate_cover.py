"""Literal verification of parent maps and transfers of previously complete exclusions."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate


def check_map(image,known,target,geometry,n=14):
    assert all(type(v) is int for v in image) and sorted(image)==list(range(n))
    def transport(q):return sum(1<<image[v] for v in range(n) if q&(1<<v))
    assert {transport(q):k for q,k in known.items()}==target
    assert {transport(q) for q in geometry['positive_doubles']}==set(geometry['positive_doubles'])
    assert {transport(q) for q in geometry['eligible_pairs']}==set(geometry['eligible_pairs'])


def run(source_path,output,frontier_output):
    b=Bindings();source=b.read(source_path);assert source['status']=='PROPOSED_COMPLETE_PARENT_COORDINATE_COVER'
    previous=b.read(source['previous']['path'],source['previous']['sha256'])
    assert previous['status']=='ACCEPTED_ACTUAL_FOUR_CYCLE_SECOND_FRONTIER' and previous['geometry']==source['geometry']
    assert source['authority']==previous['source']
    authority=b.read(source['authority']['path'],source['authority']['sha256'])
    assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_SAFE_FOUR_CYCLE_SECOND_FRONTIER' and authority['geometry']==source['geometry']
    excluded={(r['first_row'],r['second_row']) for r in previous['excluded']}
    remaining={(r['first_row'],s) for r in previous['records'] for s in r['remaining_rows']}
    inputs={(p['first_row'],r['second_row']):r['proof'] for p in authority['records'] for r in p['records']}
    assert len(inputs)==sum(len(p['records']) for p in authority['records']) and set(inputs)==excluded|remaining
    assert not excluded&remaining and len(remaining)==previous['remaining_second_cases']
    records={(r['first_row'],r['second_row']):r for r in source['records']}
    assert len(records)==len(source['records']) and set(records)==set(inputs)
    representatives={(r['first_row'],r['second_row']):r for r in source['representatives']}
    assert len(representatives)==len(source['representatives']) and set(representatives)=={tuple(r['representative']) for r in records.values()}
    known={k:dict(read_certificate(b,ref)['known']) for k,ref in inputs.items()};new=[]
    for key,record in records.items():
        target=tuple(record['representative']);assert target in inputs and record['parent']==inputs[key]
        assert tuple(records[target]['representative'])==target
        assert record['prior_excluded']==(key in excluded) and record['representative_prior_excluded']==(target in excluded)
        check_map(record['map'],known[key],known[target],source['geometry'])
        if key in remaining and target in excluded:new.append(dict(first_row=key[0],second_row=key[1],representative=list(target),map=record['map'],parent=record['parent']))
    for key,r in representatives.items():
        assert r['prior_excluded']==(key in excluded) and r['cases']==sum(tuple(q['representative'])==key for q in records.values())
    for name in ('verify_parent_coordinate_cover.py','test_verify_parent_coordinate_cover.py','parent_coordinate_transfer_soundness_cycle151.md'):b.bind(Path(name))
    result=dict(status='INDEPENDENTLY_VERIFIED_PARENT_COORDINATE_COVER',global_status='UNRESOLVED',
        source=b.bind(source_path),previous=source['previous'],geometry=source['geometry'],actual_scope_geometries=previous['actual_scope_geometries'],
        records=source['records'],representatives=source['representatives'],newly_excluded=new,canonicalizer_imported=False,
        open_representatives=sum(not r['prior_excluded'] for r in representatives.values()),
        global_goal_complete=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists() and not frontier_output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    newly={(r['first_row'],r['second_row']) for r in new}
    records=[{**r,'remaining_rows':[s for s in r['remaining_rows'] if (r['first_row'],s) not in newly]} for r in previous['records']]
    total=sum(len(r['remaining_rows']) for r in records);assert total==previous['remaining_second_cases']-len(newly)
    updated={k:previous[k] for k in ('status','global_status','geometry','actual_scope_geometries','source','original_second_cases')}
    updated.update(previous=b.bind(Path(source['previous']['path'])),excluded=previous['excluded']+[dict(first_row=r['first_row'],second_row=r['second_row'],proof=b.bind(output)) for r in new],
        records=records,remaining_second_cases=total,whole_four_cycle_excluded=total==0,coordinate_cover=b.bind(output),files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    frontier_output.write_text(json.dumps(updated,indent=2)+'\n')
    print(json.dumps(dict(maps_checked=len(inputs),newly_excluded=len(newly),remaining_second_cases=total,open_representatives=result['open_representatives'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--frontier-output',type=Path,required=True)
    a=p.parse_args();run(a.source,a.output,a.frontier_output)
