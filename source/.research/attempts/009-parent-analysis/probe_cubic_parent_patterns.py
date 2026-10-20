"""Controlled broadening to two fixed catalog rows, with explicit position maps."""
from pathlib import Path
from itertools import combinations
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from two_positive_conditional_orbits import coordinate_generators
from center_negative_placement_cover import orbit_cover
from verify_four_cube_pair_domains import LiteralCubeChecker
from verify_cubic_negative_pair_cover import signature
from generic_parseval_envelope import permitted
from two_positive_four_cube_domains import CubeIndex
from fixed_cubic_box import build
from exact_box_row_lp import solve

H=Path(__file__).resolve().parent


def run():
    start=monotonic();b=Bindings();authority_path=H/'safe-four-cycle-second-frontier-independent-manifest.json';authority=b.read(authority_path,'593b03a76bd9c215afeb0ccbbf3bef3c8e8c1746759069685dde56a76b71b83c')
    g=authority['geometry'];_,outside=LiteralCubeChecker.coordinates(g)
    singleton=b.read(H/'cubic-N1-interval-transfers-independent-manifest-cycle109.json');pair=b.read(H/'cubic-two-negative-position-cover-independent-manifest.json')
    assert singleton['frames_authority']==pair['frames_authority'] and singleton['geometry']==pair['geometry']==g
    triples=[q for q in range(1024) if q.bit_count()==3]
    patterns=[(q,) for q in triples if (q&3).bit_count() in singleton['allowed_apex_counts']]
    patterns+=[p for p in combinations(triples,2) if list(signature(p,[0,1])) in pair['allowed_signatures']];assert len(patterns)==484
    data=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b');cubes=CubeIndex.build(data['domain']['rows'])
    directory=H/'cubic-parent-pattern-pilot-cycle110';output=directory.with_suffix('.json');assert not output.exists() and not directory.exists();directory.mkdir()
    report=dict(status='INCOMPLETE_TWO_FIXED_ROW_CUBIC_PATTERN_PILOT',global_status='UNRESOLVED',independent_audit='PENDING',accepted_exclusion=False,
        authority=b.bind(authority_path),actual_singleton_authority=b.bind(H/'cubic-N1-interval-transfers-independent-manifest-cycle109.json'),actual_pair_authority=b.bind(H/'cubic-two-negative-position-cover-independent-manifest.json'),
        geometry=g,core_mask=3,parameters=dict(seconds_per_lp=3,total_seconds=180),cases=[],stop_reason=None)
    def save():
        tmp=output.with_suffix('.partial.json');tmp.write_text(json.dumps(report,indent=2)+'\n');tmp.replace(output)
    save()
    for a,c in ((56,56),(0,0)):
        first=next(r for r in authority['records'] if r['first_row']==a);child=next(r for r in first['records'] if r['second_row']==c);parent=read_certificate(b,child['proof']);known=dict(parent['known'])
        full=coordinate_generators(known,tuple(g['eligible_pairs']));generators=[[outside.index(image[v]) for v in outside] for image in full]
        representatives,maps=orbit_cover(patterns,generators,10)
        cover=dict(geometry=g,parent=child['proof'],outside=outside,core_mask=3,initial_known=parent['known'],full_generators=full,generators=generators,
            representatives=[dict(index=i,pattern=list(p)) for i,p in enumerate(representatives)],maps=maps)
        path=directory/f'a{a:04d}-b{c:04d}-cover.json.gz';write_certificate(path,cover)
        current=dict(first_row=a,second_row=c,parent=child['proof'],cover=b.bind(path),representatives=len(representatives),records=[],complete=False);report['cases'].append(current);save()
        print(json.dumps(dict(first=a,second=c,representatives=len(representatives))),flush=True)
        values=permitted(g,parent['domains'],cubes,[3])[3]
        for i,negative in enumerate(representatives):
            if monotonic()-start>180:report['stop_reason']='BATCH_TIME_LIMIT';save();return
            negative=list(negative);variables,rows=build(10,negative,values);solved=solve(rows,len(variables),seconds=3)
            if 'fractional_variables' in solved:solved['fractional_variables']=int(solved['fractional_variables'])
            path=directory/f'a{a:04d}-b{c:04d}-r{i:04d}.json.gz';write_certificate(path,dict(parent=child['proof'],core_mask=3,negative=negative,variables=variables,result=solved))
            current['records'].append(dict(index=i,negative=negative,status=solved['status'],proof=b.bind(path)));save()
        current['complete']=True;save();print(json.dumps(dict(first=a,second=c,count=len(current['records']),exact=sum(r['status']=='EXACT_BOX_ROW_LP_CONTRADICTION' for r in current['records']),seconds=monotonic()-start)),flush=True)
    for name in ('probe_cubic_parent_patterns.py','center_negative_placement_cover.py','test_cubic_target_covers.py','fixed_cubic_box.py','test_fixed_cubic_two_negative_models.py'):b.bind(H/name)
    report.update(status='COMPLETE_TWO_FIXED_ROW_CUBIC_PATTERN_PILOT',elapsed_seconds=monotonic()-start,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]);save()


if __name__=='__main__':run()
