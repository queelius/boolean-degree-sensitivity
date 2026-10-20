"""Explicit geometry quotient and complete labeled three-template pair domains."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import json
import time

from class40_pair_placement_orbits import canonical
from two_positive_pair_catalog import eligible_pairs

H=Path(__file__).resolve().parent


def vertices(mask): return [v for v in range(mask.bit_length()) if mask>>v&1]


def remap(mask,image): return sum(1<<image[v] for v in vertices(mask))


def geometry_cover(placements):
    keys,representatives,maps={},{},[]
    for entry in placements:
        terms={q:-2 for q in entry['negative_supports']}|{q:2 for q in entry['positive_doubles']}
        key,image=canonical(terms,14,0)
        if key not in keys:
            i=len(keys);keys[key]=i
            negatives=sorted(q for q,k in key[1] if k==-2)
            positives=sorted(q for q,k in key[1] if k==2)
            pairs=eligible_pairs(negatives,positives)
            assert pairs
            representatives[i]=dict(index=i,source_class=entry['class_index'],
                                    negative_supports=negatives,positive_doubles=positives,
                                    eligible_pairs=pairs,selected_pair=min(pairs))
        i=keys[key]
        assert sorted(image)==list(range(14))
        assert sorted(remap(q,image) for q in entry['negative_supports'])==representatives[i]['negative_supports']
        assert sorted(remap(q,image) for q in entry['positive_doubles'])==representatives[i]['positive_doubles']
        maps.append(dict(class_index=entry['class_index'],placement_index=entry['placement_index'],
                         representative=i,map=image))
    return dict(representatives=list(representatives.values()),maps=maps)


def local_domains(templates):
    """Doubled faces are {0,2,3} and {1,2,3}; enumerate every remaining label."""
    registry,rows={},[]
    count=0
    for template in templates:
        n=template['surface_order']
        common=template['double_faces'][0]&template['double_faces'][1]
        special=[vertices(q^common)[0] for q in template['double_faces']]
        shared=vertices(common)
        ordinary=[v for v in range(n) if v not in special]
        unused=[v for v in range(12) if v not in special+shared+ordinary]
        for apex_image in permutations((0,1)):
            for chosen in permutations(range(4,12),len(ordinary)):
                count+=1
                image=[None]*12
                for src,dst in zip(special+shared+ordinary,list(apex_image)+[2,3]+list(chosen)):
                    image[src]=dst
                for src,dst in zip(unused,sorted(set(range(4,12))-set(chosen))):
                    image[src]=dst
                assert sorted(image)==list(range(12))
                faces=tuple(sorted(remap(q,image) for q in template['unit_faces']))
                linear=[0]*12
                for src,k in enumerate(template['linear_numerators']): linear[image[src]]=k
                key=faces,tuple(linear)
                if key not in registry:
                    registry[key]=len(rows)
                    rows.append(dict(index=len(rows),template=template['index'],source_to_row=image,
                                     unit_faces=list(faces),linear_numerators=linear))
    return dict(rows=rows,raw_maps=count,domain_counts=dict(Counter(r['template'] for r in rows)))


def embed(row,geometry):
    b=geometry['selected_pair']
    negatives,positives=geometry['negative_supports'],geometry['positive_doubles']
    assert b.bit_count()==2 and all(q&b==b for q in positives)
    assert not any(q&b==b for q in negatives)
    common=positives[0]&positives[1]
    assert common.bit_count()==4
    image=vertices(positives[0]^common)+vertices(positives[1]^common)+vertices(common^b)
    image+=sorted(set(range(14))-set(vertices(b))-set(image))
    assert len(image)==len(set(image))==12
    unit={b|remap(q,image) for q in row['unit_faces']}
    fixed={b|sum(1<<v for v in triple):int(b|sum(1<<v for v in triple) in unit)
           for triple in combinations(image,3)}
    for q in positives:
        assert fixed[q]==0
        fixed[q]=2
    for q in negatives:
        assert q not in fixed
        fixed[q]=-2
    cubics={b|(1<<image[v]):-k for v,k in enumerate(row['linear_numerators'])}
    assert len(cubics)==12 and set(cubics.values())<={0,1}
    return fixed,cubics


def run():
    start=time.monotonic()
    source=H/'two-positive-pair-catalog.json'
    data=json.loads(source.read_text())
    geometries=geometry_cover(data['placements'])
    domain=local_domains(data['rows'])
    paths=[Path(__file__),H/'test_two_positive_pair_embeddings.py',source,
           H/'two-positive-pair-catalog-independent-manifest.json',
           H/'class40_pair_placement_orbits.py',H/'two_positive_pair_catalog.py']
    return dict(status='PROPOSED_COMPLETE_TWO_POSITIVE_GEOMETRIES_AND_PAIR_EMBEDDINGS',
                global_status='UNRESOLVED',whole_support_exclusion=False,
                independent_audit='PENDING',**geometries,domain=domain,
                elapsed_seconds=time.monotonic()-start,
                sources=[dict(path=str(p),sha256=sha256(p.read_bytes()).hexdigest()) for p in paths])


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    assert not args.output.exists()
    report=run()
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(geometries=len(report['representatives']),placements=len(report['maps']),
                         domain_rows=len(report['domain']['rows']),domain_counts=report['domain']['domain_counts'],
                         raw_maps=report['domain']['raw_maps'],elapsed_seconds=report['elapsed_seconds'])))
