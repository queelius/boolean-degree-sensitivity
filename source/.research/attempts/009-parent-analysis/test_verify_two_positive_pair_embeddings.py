from copy import deepcopy
from pathlib import Path
import json
import pytest
from verify_two_positive_pair_embeddings import check_domain, check_geometries

H=Path(__file__).resolve().parent


def data(): return json.loads((H/'two-positive-pair-embeddings.json').read_text())


def test_complete_domain_and_geometry():
    source=data()
    assert check_geometries(source)==333
    assert check_domain(source)==44352


@pytest.mark.parametrize('mutation',['missing','coefficient','witness'])
def test_corrupt_domain_rejected(mutation):
    source=data()
    if mutation=='missing':source['domain']['rows'].pop()
    if mutation=='coefficient':source['domain']['rows'][0]['linear_numerators'][0]=0
    if mutation=='witness':source['domain']['rows'][0]['source_to_row'][0]=3
    with pytest.raises(AssertionError): check_domain(source)


@pytest.mark.parametrize('mutation',['missing','color','map','unsafe'])
def test_corrupt_geometry_rejected(mutation):
    source=data()
    if mutation=='missing':source['maps'].pop()
    if mutation=='color':source['representatives'][0]['positive_doubles'].reverse()
    if mutation=='map':source['maps'][0]['map'][0]=source['maps'][0]['map'][1]
    if mutation=='unsafe':source['representatives'][0]['selected_pair']=0
    with pytest.raises(AssertionError): check_geometries(source)
