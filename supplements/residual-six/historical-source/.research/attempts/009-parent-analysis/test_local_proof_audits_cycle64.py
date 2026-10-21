import pytest

import audit_endpoint_d11 as d11
import audit_two_positive_cubic as positive


def test_d11_full_independent_catalog_and_strip_replay():
    report = d11.evaluate()
    assert report['counts']['all_records'] == 4787
    assert len(report['witnesses']) == 4
    assert report['strip_controls'][0]['normalized_sphere_links'] == 8


def test_positive_join_and_duplicate_negative_control():
    first = [(i+1, (i+1) % 4+1) for i in range(4)]
    second = [(i+5, (i+1) % 5+5) for i in range(5)]
    facets = tuple(sorted(tuple(sorted(a+b)) for a in first for b in second))
    checked = d11.inspect(0, facets)
    assert checked['f_vector'] == [9, 29, 40, 20]
    assert set(checked['edge_valences']) == {4, 5}
    assert d11.eligible(facets) is None
    with pytest.raises(AssertionError):
        d11.inspect(0, facets + (facets[0],))
    with pytest.raises(AssertionError):
        d11.inspect(0, facets[:-1])


def test_two_positive_pair_finite_controls():
    report = positive.evaluate()
    assert [row['roots'] for row in report['cycle_roots']] == [1, 8, 1]
    assert len(report['pentagon_disk_positive_controls']) == 5


def test_structured_catalog_invalid_record_rejected():
    with pytest.raises(AssertionError):
        list(d11.records('manifold_lex_d3_deg5_#2=[[1,2,3,4]]'))
    with pytest.raises(AssertionError):
        list(d11.records('manifold_lex_d3_deg5_#1=[[1,2,3]]'))
