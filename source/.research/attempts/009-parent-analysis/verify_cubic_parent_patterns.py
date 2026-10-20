"""Independent complete position-cover and scalar interval audit at parent level."""
from argparse import ArgumentParser
from itertools import combinations
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_cubic_target_covers import verify_maps,move
from verify_cubic_negative_pair_cover import signature
from verify_four_cube_pair_domains import LiteralCubeChecker
from verify_cubic_n2_batch import read_basis
from cubic_partial_scalar import PartialScalarValues

H=Path(__file__).resolve().parent


def run(output):
    b=Bindings();source_path=H/'cubic-parent-pattern-pilot-cycle110.json';source=b.read(source_path)
    assert source['status']=='COMPLETE_TWO_FIXED_ROW_CUBIC_PATTERN_PILOT' and source['stop_reason'] is None
    authority=b.read(source['authority']['path'],source['authority']['sha256']);assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_SAFE_FOUR_CYCLE_SECOND_FRONTIER'
    single=b.read(source['actual_singleton_authority']['path'],source['actual_singleton_authority']['sha256']);pair=b.read(source['actual_pair_authority']['path'],source['actual_pair_authority']['sha256'])
    assert single['status']=='INDEPENDENTLY_VERIFIED_ACTUAL_CUBIC_SINGLETON_INTERVAL_TRANSFERS' and pair['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_CUBIC_TWO_NEGATIVE_COVER_WITH_ACTUAL_FILTER'
    assert single['frames_authority']==pair['frames_authority'] and single['geometry']==pair['geometry']==source['geometry']==authority['geometry']
    assert single['allowed_apex_counts']==[1,2] and pair['allowed_signatures']==[[1,2,0]]
    triples=[q for q in range(1024) if q.bit_count()==3];patterns={(q,) for q in triples if q&3}|{p for p in combinations(triples,2) if signature(p,[0,1])==(1,2,0)};assert len(patterns)==484
    g=source['geometry'];_,outside=LiteralCubeChecker.coordinates(g);rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];scalar=PartialScalarValues(rows,g);results=[]
    assert [(c['first_row'],c['second_row']) for c in source['cases']]==[(56,56),(0,0)]
    for case in source['cases']:
        assert case['complete'];first=next(r for r in authority['records'] if r['first_row']==case['first_row']);accepted=next(r for r in first['records'] if r['second_row']==case['second_row'])
        assert case['parent']==accepted['proof'];parent=read_certificate(b,case['parent']);known=dict(parent['known']);cover=read_certificate(b,case['cover'])
        assert cover['parent']==case['parent'] and cover['geometry']==g and cover['outside']==outside and cover['core_mask']==3 and cover['initial_known']==parent['known']
        verify_maps(10,patterns,cover['representatives'],cover['maps']);checked=set()
        for m in cover['maps']:
            image=tuple(m['map'])
            if image in checked:continue
            full=list(range(14))
            for i,v in enumerate(outside):full[v]=outside[image[i]]
            assert sorted(full)==list(range(14)) and {move(q,full):k for q,k in known.items()}==known
            assert all(move(q,full)==q for q in g['eligible_pairs']) and {move(q,full) for q in g['positive_doubles']}==set(g['positive_doubles']);checked.add(image)
        assert [(r['index'],r['negative']) for r in case['records']]==[(r['index'],r['pattern']) for r in cover['representatives']]
        values=scalar.allowed(parent['domains'],3);records=[]
        for record in case['records']:
            detail=read_certificate(b,record['proof']);assert detail['parent']==case['parent'] and detail['core_mask']==3 and detail['negative']==record['negative'] and detail['result']['status']==record['status']
            if record['status']=='EXACT_BOX_ROW_LP_CONTRADICTION':
                basis=read_basis(detail,len(record['negative']));rhs=basis.evaluate(values);assert rhs<0 and rhs==detail['result']['certificate']['integer_rhs']
                records.append({**record,'excluded':True,'integer_rhs':rhs})
            else:
                assert record['status'] in ('NUMERICALLY_FEASIBLE_BOX_RELAXATION','INCONCLUSIVE_BOX_ROW_LP');records.append({**record,'excluded':False})
        remaining=[dict(index=r['index'],negative=r['negative']) for r in records if not r['excluded']]
        results.append(dict(first_row=case['first_row'],second_row=case['second_row'],parent=case['parent'],cover=case['cover'],records=records,remaining=remaining,actual_parent_excluded=not remaining))
        print(json.dumps(dict(first=case['first_row'],second=case['second_row'],checked=len(records),remaining=remaining)),flush=True)
    for name in ('verify_cubic_parent_patterns.py','cubic_partial_scalar.py','test_cubic_partial_scalar.py','test_cubic_target_covers.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_COMPLETE_TWO_FIXED_ROW_CUBIC_INTERVAL_COVERS',global_status='UNRESOLVED',source=b.bind(source_path),
        actual_singleton_authority=source['actual_singleton_authority'],actual_pair_authority=source['actual_pair_authority'],geometry=g,core_mask=3,records=results,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
