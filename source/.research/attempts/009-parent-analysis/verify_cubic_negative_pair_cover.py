"""Literal complete pair-cover audit and actual signed-geometry restriction."""
from argparse import ArgumentParser
from itertools import combinations
from collections import defaultdict
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_four_cube_pair_domains import LiteralCubeChecker
from verify_two_positive_conditional_orbits import relabel

H=Path(__file__).resolve().parent


def signature(pattern,apices):
    assert len(pattern)==2 and len(apices)==2
    apex_mask=sum(1<<v for v in apices)
    parts=[sum(1<<i for i,v in enumerate(apices) if q>>v&1) for q in pattern]
    common=(pattern[0]&pattern[1]&~apex_mask).bit_count()
    swapped=[((q&1)<<1)|((q&2)>>1) for q in parts]
    return min(tuple(sorted(parts))+(common,),tuple(sorted(swapped))+(common,))


def verify_cover(data):
    g=data['geometry'];known=dict(data['initial_known']);pairs,outside=LiteralCubeChecker.coordinates(g)
    assert data['outside']==outside and data['coordinate_marks']==g['eligible_pairs']
    assert data['negative_count']==2 and data['core_mask']==3 and 3 not in pairs
    expected=set(combinations([q for q in range(1024) if q.bit_count()==3],2))
    actual=[tuple(m['pattern']) for m in data['maps']]
    assert len(actual)==len(set(actual))==data['literal_positions']==len(expected)==7140 and set(actual)==expected
    reps=data['representatives'];assert [r['index'] for r in reps]==list(range(len(reps))) and data['representative_count']==len(reps)
    assert len({tuple(r['pattern']) for r in reps})==len(reps) and all(tuple(r['pattern']) in expected for r in reps)
    seen=set();checked=set()
    for witness in data['maps']:
        image=tuple(witness['map']);assert sorted(image)==list(range(10));target=witness['representative'];assert type(target) is int and 0<=target<len(reps);seen.add(target)
        if image not in checked:
            full=list(range(14))
            for i,v in enumerate(outside):full[v]=outside[image[i]]
            full=tuple(full);assert sorted(full)==list(range(14))
            assert {relabel(q,full):k for q,k in known.items()}==known
            assert all(relabel(q,full)==q for q in g['eligible_pairs'])
            assert {relabel(q,full) for q in g['positive_doubles']}==set(g['positive_doubles']);checked.add(image)
        moved=sorted(sum(1<<image[i] for i in range(10) if q>>i&1) for q in witness['pattern'])
        assert moved==reps[target]['pattern'] and signature(witness['pattern'],[0,1])==signature(moved,[0,1])
    assert seen==set(range(len(reps)));return len(reps)


def actual_patterns(data,frames):
    evidence=[];hist=defaultdict(list)
    for frame in frames:
        index=frame['geometry'];g=data['representatives'][index];p,r=g['positive_doubles'];core=p&r
        vertices=[v for v in range(14) if core>>v&1];apices=[(p^core).bit_length()-1,(r^core).bit_length()-1]
        missing=[sum(1<<v for v in pair) for pair in combinations(vertices,2) if sum(1<<v for v in pair) not in g['eligible_pairs']]
        assert len(missing)==2 and missing[0]&missing[1]==0
        counts=[]
        for pair in missing:
            negative=[q^pair for q in g['negative_supports'] if q&core==pair];assert negative and all(q.bit_count()==3 for q in negative);counts.append(len(negative))
            if len(negative)==2:evidence.append(dict(geometry=index,core_pair=pair,negative_outside=negative,apices=apices,signature=list(signature(negative,apices))))
        hist[tuple(sorted(counts))].append(index)
    return evidence,[dict(counts=list(k),geometries=v) for k,v in sorted(hist.items())]


def run(output):
    b=Bindings();path=H/'cubic-two-negative-position-cover-cycle108.json';source=b.read(path)
    assert source['status']=='PROPOSED_COMPLETE_CONDITIONAL_CUBIC_TWO_NEGATIVE_POSITION_COVER'
    authority=b.read(source['authority']['path'],source['authority']['sha256']);assert authority['status']=='INDEPENDENTLY_VERIFIED_CONDITIONAL_CUBIC_ONE_NEGATIVE_EXCLUSION'
    assert source['parent']==authority['parent'] and source['geometry']==authority['geometry']
    parent=read_certificate(b,source['parent']);assert source['initial_known']==parent['known'];verify_cover(source)
    frames_path=H/'safe-four-cycle-first-second-covers-independent-manifest.json';frames=b.read(frames_path,'7aaaed46c192db0cf0a5886378778dd9c1c877e1154e504b7fd0c9570c53d0de')
    assert frames['status']=='INDEPENDENTLY_VERIFIED_SAFE_FOUR_CYCLE_FIRST_AND_SECOND_COVERS_WITH_SCOPED_PILOT' and frames['geometry']==source['geometry']
    data=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b');evidence,hist=actual_patterns(data,frames['actual_frames'])
    allowed={tuple(r['signature']) for r in evidence};kept=[r for r in source['representatives'] if signature(r['pattern'],[0,1]) in allowed]
    kept_literals=sum(signature(r['pattern'],[0,1]) in allowed for r in source['maps'])
    for name in ('verify_cubic_negative_pair_cover.py','test_verify_cubic_negative_pair_cover.py','actual-four-cycle-negative-pair-restriction-cycle108.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_COMPLETE_CUBIC_TWO_NEGATIVE_COVER_WITH_ACTUAL_FILTER',global_status='UNRESOLVED',
        source=b.bind(path),authority=source['authority'],frames_authority=b.bind(frames_path),geometry=source['geometry'],parent=source['parent'],
        core_mask=3,negative_count=2,allowed_signatures=[list(s) for s in sorted(allowed)],actual_evidence=evidence,actual_missing_diagonal_counts=hist,
        representatives=kept,retained_literal_positions=kept_literals,retained_representatives=len(kept),full_literal_positions=7140,full_representatives=source['representative_count'],
        scope='Remaining actual exact-four-cycle signed geometries from the accepted frontier',
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(full=source['representative_count'],retained=len(kept),retained_literals=kept_literals,signatures=result['allowed_signatures'],counts=hist)),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
