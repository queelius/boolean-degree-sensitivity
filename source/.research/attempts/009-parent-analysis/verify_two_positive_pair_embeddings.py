"""Independent literal-map and exhaustive injection audit; no producer imports."""
from argparse import ArgumentParser
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings

H=Path(__file__).resolve().parent


def moved(mask,mapping):
    result=0
    for i,target in enumerate(mapping):
        if mask&(1<<i):result|=1<<target
    return result


def catalog():return json.loads((H/'two-positive-pair-catalog.json').read_text())


def check_geometries(data):
    original=catalog()['placements']
    source={(r['class_index'],r['placement_index']):r for r in original}
    assert len(source)==len(data['maps'])
    targets={r['index']:r for r in data['representatives']}
    assert len(targets)==len(data['representatives'])
    reached=set();seen=set()
    for witness in data['maps']:
        key=witness['class_index'],witness['placement_index']
        assert key in source and key not in seen;seen.add(key)
        row=source[key];mapping=witness['map']
        assert sorted(mapping)==list(range(14))
        target=targets[witness['representative']];reached.add(target['index'])
        for field in ('negative_supports','positive_doubles'):
            assert sorted(moved(q,mapping) for q in row[field])==target[field]
    assert seen==set(source) and reached==set(targets)
    for target in targets.values():
        expected=[]
        for i,j in combinations(range(14),2):
            q=(1<<i)|(1<<j)
            if all(s&q==q for s in target['positive_doubles']) and all(s&q!=q for s in target['negative_supports']):
                expected.append(q)
        assert target['eligible_pairs']==expected and target['selected_pair'] in expected
    return len(seen)


def check_domain(data):
    templates=catalog()['rows'];domain=data['domain'];lookup={}
    for index,row in enumerate(domain['rows']):
        assert row['index']==index and 0<=row['template']<len(templates)
        template=templates[row['template']];mapping=row['source_to_row']
        assert sorted(mapping)==list(range(12))
        assert sorted(moved(q,mapping) for q in template['double_faces'])==[13,14]
        faces=tuple(sorted(moved(q,mapping) for q in template['unit_faces']))
        linear=[0]*12
        for source,k in enumerate(template['linear_numerators']):linear[mapping[source]]=k
        assert list(faces)==row['unit_faces'] and linear==row['linear_numerators']
        signature=faces,tuple(linear)
        assert signature not in lookup;lookup[signature]=index
    seen=set();raw=0
    # Different traversal from the producer: choose the image subset first,
    # then order it; derive protected vertices directly from the face degrees.
    for template in templates:
        n=template['surface_order']
        ds=[sum(bool(q&(1<<v)) for q in template['unit_faces']) for v in range(n)]
        protected=[v for v in range(n) if ds[v]==3]
        ordinary=[v for v in range(n) if ds[v]!=3]
        assert len(protected)==2
        for chosen in combinations(range(4,12),len(ordinary)):
            for ordering in permutations(chosen):
                for swap in (False,True):
                    mapping=[0]*n
                    mapping[protected[0]],mapping[protected[1]]=(1,0) if swap else (0,1)
                    for v,target in zip(ordinary,ordering):mapping[v]=target
                    faces=tuple(sorted(moved(q,mapping) for q in template['unit_faces']))
                    linear=[0]*12
                    for v,d in enumerate(ds):linear[mapping[v]]=-(d%2)
                    signature=faces,tuple(linear)
                    assert signature in lookup
                    seen.add(lookup[signature]);raw+=1
    assert seen==set(range(len(domain['rows'])))
    assert raw==domain['raw_maps']
    assert {str(k):v for k,v in Counter(r['template'] for r in domain['rows']).items()}==domain['domain_counts']
    return raw


def verify(path):
    b=Bindings();data=b.read(path)
    authority=b.read(H/'two-positive-pair-catalog-independent-manifest.json',
                     '07e4d0a2b8f910d30a811b30a81f1f93a1782307ea5b3b8e842a9543f3aaa742')
    assert authority['status']=='INDEPENDENTLY_ACCEPTED_COMPLETE_ADJACENT_TWO_POSITIVE_PAIR_CATALOG'
    placements=check_geometries(data);raw=check_domain(data)
    assert data['whole_support_exclusion'] is False and data['global_status']=='UNRESOLVED'
    for path in (Path(__file__),H/'test_verify_two_positive_pair_embeddings.py'):
        b.bind(path)
    return dict(status='INDEPENDENTLY_ACCEPTED_COMPLETE_TWO_POSITIVE_GEOMETRY_AND_PAIR_EMBEDDING_COVER',
                global_status='UNRESOLVED',whole_support_exclusion=False,producer_imports=False,
                placements=placements,geometries=len(data['representatives']),raw_maps=raw,
                pair_domain_rows=len(data['domain']['rows']),domain_counts=data['domain']['domain_counts'],
                source_binding_checks=b.checks,
                files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();assert not args.output.exists()
    report=verify(args.input)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','placements','geometries','raw_maps','pair_domain_rows','domain_counts')}))
