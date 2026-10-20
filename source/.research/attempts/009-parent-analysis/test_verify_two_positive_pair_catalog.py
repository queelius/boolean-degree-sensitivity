from copy import deepcopy
from pathlib import Path
import json
import pytest

from verify_two_positive_pair_catalog import check_placements, check_rows

H=Path(__file__).resolve().parent


def data():
    return json.loads((H/'two-positive-pair-catalog.json').read_text())


def test_full_catalog():
    source=data()
    assert check_rows(source)==[5,6,8]
    assert check_placements(source)==333


@pytest.mark.parametrize('mutation', ['missing','coefficient','face','source'])
def test_changed_row_rejected(mutation):
    source=data()
    if mutation=='missing': source['rows'].pop()
    if mutation=='coefficient': source['rows'][0]['linear_numerators'][0]=0
    if mutation=='face': source['rows'][0]['unit_faces'].pop()
    if mutation=='source': source['rows'][0]['source_index']=1
    with pytest.raises(AssertionError): check_rows(source)


@pytest.mark.parametrize('mutation', ['missing','pairs','positive','duplicate'])
def test_changed_support_coverage_rejected(mutation):
    source=data()
    if mutation=='missing': source['placements'].pop()
    if mutation=='pairs': source['placements'][0]['eligible_pairs'].pop()
    if mutation=='positive': source['placements'][0]['positive_doubles'][0]^=1
    if mutation=='duplicate': source['placements'].append(deepcopy(source['placements'][0]))
    with pytest.raises(AssertionError): check_placements(source)
