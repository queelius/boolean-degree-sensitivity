"""Independent first/second cover and scalar pilot replay for the safe four-cycle."""
from argparse import ArgumentParser
from collections import Counter
from itertools import combinations,permutations
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_coupled_two_positive import literal_embedding,PairChecker
from verify_four_cube_pair_domains import LiteralCubeChecker
from verify_abstract_safe_star import check_first_cover
from verify_core_fourier_envelope_certificate import literal_words
from verify_two_positive_conditional_orbits import relabel

H=Path(__file__).resolve().parent


def check_cycle(g):
    assert g['negative_supports']==[]
    p,r=g['positive_doubles'];core=p&r;assert p.bit_count()==r.bit_count()==5 and core.bit_count()==4
    pairs=g['eligible_pairs'];assert len(pairs)==len(set(pairs))==4 and g['selected_pair'] in pairs
    assert all(q.bit_count()==2 and q&core==q for q in pairs)
    assert all(sum(bool(q&(1<<v)) for q in pairs)==2 for v in range(14) if core>>v&1)


def check_second(rows,g,known,domains,cover):
    pair=cover['second_pair'];assert pair in g['eligible_pairs'] and pair!=g['selected_pair']
    expected=sorted(set(PairChecker(rows).live(g,pair,known))&set(next(d['rows'] for d in domains if d['pair']==pair)))
    assert cover['initial_known']==[list(x) for x in sorted(known.items())]
    assert cover['input_rows']==expected and cover['raw_rows']==len(expected)
    reps=cover['representatives'];assert [r['index'] for r in reps]==list(range(len(reps)))
    assert len(reps)==cover['representative_count'] and len({r['row'] for r in reps})==len(reps)
    assert all(r['row'] in expected for r in reps) and [m['source_row'] for m in cover['maps']]==expected
    targets={r['index']:literal_embedding(rows[r['row']],g,pair) for r in reps};seen=set();checked=set()
    for witness in cover['maps']:
        image=tuple(witness['map']);assert sorted(image)==list(range(14));target=witness['representative'];assert target in targets;seen.add(target)
        if image not in checked:
            assert relabel(pair,image)==pair and relabel(g['selected_pair'],image)==g['selected_pair']
            assert {relabel(q,image):k for q,k in known.items()}==known
            assert {relabel(q,image) for q in g['eligible_pairs']}==set(g['eligible_pairs'])
            assert {relabel(q,image) for q in g['positive_doubles']}==set(g['positive_doubles']);checked.add(image)
        source=literal_embedding(rows[witness['source_row']],g,pair)
        assert {relabel(q,image):k for q,k in source.items()}==targets[target]
    assert seen==set(targets);return len(reps)


def actual_frames(data,indices,target):
    def vertices(q):return [v for v in range(14) if q>>v&1]
    tp,tr=target['positive_doubles'];tc=tp&tr;tv=vertices(tc);results=[]
    for index in indices:
        g=data['representatives'][index];p,r=g['positive_doubles'];core=p&r;vs=vertices(core)
        safe=[sum(1<<v for v in pair) for pair in combinations(vs,2) if not any(q&sum(1<<v for v in pair)==sum(1<<v for v in pair) for q in g['negative_supports'])]
        assert safe==g['eligible_pairs']
        is_cycle=len(safe)==4 and all(sum(q>>v&1 for q in safe)==2 for v in vs)
        if not is_cycle:continue
        missing=set(sum(1<<v for v in pair) for pair in combinations(vs,2))-set(safe)
        assert len(missing)==2 and not (lambda a,b:a&b)(*missing)
        witnesses=[{q for q in g['negative_supports'] if q&pair==pair} for pair in missing]
        assert all(witnesses) and witnesses[0].isdisjoint(witnesses[1])
        single=[sum(q&core==1<<v for q in g['negative_supports']) for v in vs];assert sum(single)<=2
        image=None
        for perm in permutations(tv):
            trial=[None]*14
            for old,new in zip(vs,perm):trial[old]=new
            for left,right in ((vertices(p^core),vertices(tp^tc)),(vertices(r^core),vertices(tr^tc)),(vertices(16383^(p|r)),vertices(16383^(tp|tr)))):
                for old,new in zip(left,right):trial[old]=new
            mapping=tuple(trial)
            if {relabel(q,mapping) for q in safe}==set(target['eligible_pairs']):image=mapping;break
        assert image is not None and sorted(image)==list(range(14))
        assert {relabel(q,image) for q in g['positive_doubles']}==set(target['positive_doubles'])
        results.append(dict(geometry=index,map=list(image),single_core_negative_counts=single,
                            outside_pair_negative_count=sum((q&core).bit_count()==2 for q in g['negative_supports'])))
    return results


def run(output):
    b=Bindings();source_path=H/'abstract-safe-four-cycle-second-pilot-cycle105.json';source=b.read(source_path)
    assert source['status']=='COMPLETE_SCOPED_SAFE_FOUR_CYCLE_SECOND_PILOT'
    first=b.read(source['first_source']['path'],source['first_source']['sha256']);assert first['status']=='PROPOSED_ABSTRACT_SAFE_FOUR_CYCLE_FIRST_SCREEN'
    assert source['geometry']==first['geometry'];g=source['geometry'];check_cycle(g)
    data=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b');rows=data['domain']['rows']
    ca=b.read(H/'two-positive-pair-embeddings-independent-manifest.json','997d16b0bb5a88078ab2627692505250dc1bc144355a1230d5ab1157fcbf16e3')
    assert ca['status']=='INDEPENDENTLY_ACCEPTED_COMPLETE_TWO_POSITIVE_GEOMETRY_AND_PAIR_EMBEDDING_COVER'
    first_cover=b.read(first['first_cover']['path'],first['first_cover']['sha256']);check_first_cover(rows,g,first_cover)
    assert [r['first_row'] for r in source['records']]==[r['first_row'] for r in first['records']]==first_cover['representative_rows']
    checker=LiteralCubeChecker(rows);pairs,_=checker.coordinates(g);words=literal_words(pairs,0)
    assert len(words)==first['core_words'] and {str(k):v for k,v in Counter(w[1] for w in words).items()}==first['words_by_delta']
    for word,_,_,_ in words:
        for mask in (7,11,13,14):assert sum((1-2*((word>>x)&1))*(-1 if (x&mask).bit_count()%2 else 1) for x in range(16))==0
    for row in rows:assert row['linear_numerators'][2:4]==[0,0] and all(q&12==0 for q in row['unit_faces'])
    results=[]
    for record,original in zip(source['records'],first['records']):
        assert record['parent']==original['proof'];parent=read_certificate(b,record['parent'])
        initial=literal_embedding(rows[record['first_row']],g,g['selected_pair']);checked=checker.replay(initial,g,parent);assert not checked['excluded']
        cover=b.read(record['cover']['path'],record['cover']['sha256'])
        assert cover['parent']==record['parent'] and cover['first_row']==record['first_row'] and cover['second_pair']==record['second_pair']
        count=check_second(rows,g,checked['known'],checked['domains'],cover)
        assert record['literal_second_rows']==cover['raw_rows'] and record['second_representatives']==count
        chosen={}
        for r in cover['representatives']:chosen.setdefault(rows[r['row']]['template'],r['row'])
        assert [r['second_row'] for r in record['records']]==list(chosen.values())
        children=[]
        for child in record['records']:
            more=literal_embedding(rows[child['second_row']],g,record['second_pair'])
            assert all(q not in checked['known'] or checked['known'][q]==k for q,k in more.items())
            proof=read_certificate(b,child['proof']);answer=checker.replay(checked['known']|more,g,proof)
            assert proof['status']==child['status']
            assert child['domain_sizes']==[dict(pair=d['pair'],rows=len(d['rows'])) for d in answer.get('domains',[])]
            children.append({**child,'independently_excluded':answer['excluded']})
        results.append(dict(first_row=record['first_row'],parent=record['parent'],second_pair=record['second_pair'],cover=record['cover'],
                            literal_second_rows=cover['raw_rows'],second_representatives=count,pilot_records=children))
        print(json.dumps(dict(first_row=record['first_row'],representatives=count,pilot_cases=len(children))),flush=True)
    ledger_path=H/'two-positive-signed-geometry-frontier-cycle104.json';ledger=b.read(ledger_path)
    frames=actual_frames(data,ledger['remaining_geometries'],g)
    for name in ('verify_four_cycle_pilot.py','test_verify_four_cycle_pilot.py','disjoint-safe-pair-core-lemma.md','four-cycle-negative-budget-lemma.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_SAFE_FOUR_CYCLE_FIRST_AND_SECOND_COVERS_WITH_SCOPED_PILOT',global_status='UNRESOLVED',
        source=b.bind(source_path),first_source=source['first_source'],geometry=g,first_cover=first['first_cover'],records=results,
        actual_frames=frames,ledger=b.bind(ledger_path),single_core_negative_budget=2,core_words=len(words),
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
