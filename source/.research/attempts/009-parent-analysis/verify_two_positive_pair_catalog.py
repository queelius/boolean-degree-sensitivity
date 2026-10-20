"""Producer-free audit: literal support quantifiers and integer Walsh transforms."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

from compose_class40_same_b_acceptance import Bindings

H=Path(__file__).resolve().parent
P=H.parent/'006-solver-resume'
A=P/'independent-math-audit'


def check_placements(data):
    original=json.loads((P/'four-double-positive-cover.json').read_text())
    expected={}
    for cl in original['classes']:
        for i,(p,r) in enumerate(cl['cover']['two_positive_doubles']['placements']):
            assert p!=r and (p&r).bit_count()==4
            choices=[]
            for a,b in combinations(range(14),2):
                pair=(1<<a)|(1<<b)
                if p&pair==r&pair==pair and all(q&pair!=pair for q in cl['negative_supports']):
                    choices.append(pair)
            assert choices
            expected[cl['class_index'],i]=(cl['negative_supports'],[p,r],choices)
    assert len(data['placements'])==len(expected)
    actual={}
    for item in data['placements']:
        key=item['class_index'],item['placement_index']
        assert key not in actual
        actual[key]=(item['negative_supports'],item['positive_doubles'],item['eligible_pairs'])
    assert actual==expected
    assert data['counts']['selected_pairs']==sum(len(item[2]) for item in expected.values())
    return len(expected)


def check_rows(data):
    expected={}
    for n in range(5,9):
        surface=json.loads((P/f'sphere-triangulations-{n:02d}.json').read_text())
        for entry in surface['classes']:
            degrees=[sum(bool(f&(1<<v)) for f in entry['face_masks']) for v in range(n)]
            if all(d in (3,4,5) for d in degrees) and degrees.count(3)==2:
                expected[n,entry['index']]=(entry['face_masks'],degrees)
    assert len(data['rows'])==len(expected)
    seen=set()
    for i,row in enumerate(data['rows']):
        key=row['source_order'],row['source_index']
        assert row['index']==i and key in expected and key not in seen
        seen.add(key)
        faces,degrees=expected[key]
        n=key[0]
        assert row['surface_order']==n and row['active_order']==n+2
        assert row['unit_faces']==faces and len(faces)==2*n-4
        # Independently recover all coefficients, then transform in place.
        vector=[0]*4096
        shared=(1<<n)+(1<<(n+1))
        doubles=[shared+(1<<v) for v,d in enumerate(degrees) if d==3]
        linears=[-(d%2) for d in degrees]+[0]*(12-n)
        assert row['linear_numerators']==linears and row['double_faces']==doubles
        for q in faces: vector[q]=1
        for q in doubles: vector[q]=2
        for v,k in enumerate(linears): vector[1<<v]=k
        step=1
        while step<len(vector):
            for start in range(0,len(vector),2*step):
                for j in range(start,start+step):
                    left,right=vector[j],vector[j+step]
                    vector[j],vector[j+step]=left+right,left-right
            step*=2
        assert vector[0]==8 and set(vector)<={-16,-8,0,8,16}
        assert row['range']['status']=='NECESSARY_RANGE_VALID'
        assert Counter(vector)=={int(k):v for k,v in row['range']['value_histogram'].items()}
    assert seen==set(expected)
    return [row['surface_order'] for row in data['rows']]


def verify(path):
    b=Bindings()
    data=b.read(path)
    authority_path=P/'four-double-positive-cover-accepted-manifest.json'
    b.bind(authority_path,'e16d80d932a80611d3073029ba226c60838599b65ab34e285a4cd69cd793fd45')
    authority=json.loads(authority_path.read_text())
    # This historical manifest predates absolute paths: its references are
    # relative to the project root, not to the invocation's working directory.
    for reference in authority['files']:
        dependency=Path(reference['path'])
        if not dependency.is_absolute():
            dependency=H.parents[2]/dependency
        b.bind(dependency,reference['sha256'])
    assert authority['status']=='ACCEPTED_NECESSARY_POSITIVE_DOUBLE_COVER'
    component_path=A/'d2-component-inventory-independent-manifest.json'
    b.bind(component_path,'846e3f4a33b8ecf761cac5c7d7a8a9b5e478f7a6d4c32effeb2aeb84bcbda653')
    accepted=json.loads(component_path.read_text())
    assert accepted['status']=='INDEPENDENTLY_ACCEPTED_COMPLETE_COMPATIBLE_D2_COMPONENT_AND_ARRANGEMENT_COVER'
    sources={Path(r['path']).resolve():r['sha256'] for r in accepted['dependencies']}
    for n in range(5,9):
        source=(P/f'sphere-triangulations-{n:02d}.json').resolve()
        assert source in sources
        b.bind(source,sources[source])
    n=check_placements(data)
    orders=check_rows(data)
    assert data['whole_support_exclusion'] is False and data['global_status']=='UNRESOLVED'
    for f in (Path(__file__),H/'test_verify_two_positive_pair_catalog.py'):
        b.bind(f)
    return dict(status='INDEPENDENTLY_ACCEPTED_COMPLETE_ADJACENT_TWO_POSITIVE_PAIR_CATALOG',
                global_status='UNRESOLVED',producer_imports=False,
                whole_support_exclusion=False,placements=n,rows=len(orders),
                surface_orders=orders,exact_spectral_inputs=4096*len(orders),
                inherited_completeness='Accepted sphere catalogs through order eight and the companion surface lemma',
                source_binding_checks=b.checks,
                files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    assert not args.output.exists()
    result=verify(args.input)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','placements','rows','surface_orders','exact_spectral_inputs','source_binding_checks')}))
