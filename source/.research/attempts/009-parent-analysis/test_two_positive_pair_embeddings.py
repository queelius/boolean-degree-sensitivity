from itertools import combinations
import json
from pathlib import Path
import pytest

from two_positive_pair_embeddings import embed, geometry_cover, local_domains, remap

H=Path(__file__).resolve().parent


def data(): return json.loads((H/'two-positive-pair-catalog.json').read_text())


def test_bipyramid_domain_all_rim_three_sets():
    row=data()['rows'][0]
    result=local_domains([row])
    assert len(result['rows'])==56
    assert result['raw_maps']==672
    actual=set()
    for candidate in result['rows']:
        support=0
        for face in candidate['unit_faces']: support|=face
        actual.add(support&~3)
    assert actual=={sum(1<<v for v in triple) for triple in combinations(range(4,12),3)}


def test_full_geometry_maps_preserve_signed_supports():
    result=geometry_cover(data()['placements'])
    assert len(result['maps'])==333 and len(result['representatives'])==87
    for item,entry in zip(result['maps'],data()['placements']):
        target=result['representatives'][item['representative']]
        assert sorted(remap(q,item['map']) for q in entry['negative_supports'])==target['negative_supports']
        assert sorted(remap(q,item['map']) for q in entry['positive_doubles'])==target['positive_doubles']


def test_embedding_includes_every_zero_and_each_exception():
    source=data()
    rep=geometry_cover(source['placements'])['representatives'][0]
    row=local_domains(source['rows'][:1])['rows'][0]
    fixed,cubics=embed(row,rep)
    b=rep['selected_pair']
    assert len(cubics)==12
    assert sum(q&b==b for q in fixed)==220
    assert len(fixed)==224
    assert {q:k for q,k in fixed.items() if k not in (0,1)}==(
        {q:-2 for q in rep['negative_supports']}|{q:2 for q in rep['positive_doubles']})
    assert set(cubics.values())<={0,1}


def test_unsafe_pair_rejected():
    source=data();rep=geometry_cover(source['placements'])['representatives'][0]
    row=local_domains(source['rows'][:1])['rows'][0]
    rep['selected_pair']=rep['negative_supports'][0]
    with pytest.raises(AssertionError): embed(row,rep)
