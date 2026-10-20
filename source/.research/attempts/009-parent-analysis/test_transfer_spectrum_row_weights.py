"""Transfer must handle changed omitted categories without adding assumptions."""
import importlib
import importlib.util
import pytest


def api():
    assert importlib.util.find_spec('transfer_spectrum_row_weights') is not None
    return importlib.import_module('transfer_spectrum_row_weights').transfer


def category(value):
    return dict(kind='slice_tuple_distribution',block=0,point=2,features=[3],value=[value])


def target():
    reasons=[dict(kind='joint_word_normalization',outside_point=2),
             dict(kind='slice_pattern_normalization',block=0),category(2),category(3)]
    partitions=[dict(block=0,point=2,features=[3],omitted=[1],
                     groups=[dict(value=[v],word_count=1,pattern_count=1) for v in (1,2,3)])]
    return reasons,partitions


def test_explicit_category_maps_by_identity_despite_reordering():
    reasons,partitions=target()
    assert api()([category(3),category(2)],[5,-2],reasons,partitions)==[0,0,-2,5]


def test_omitted_category_is_recovered_from_two_normalizations():
    reasons,partitions=target()
    assert api()([category(1)],[7],reasons,partitions)==[7,-7,-7,-7]


def test_absent_category_is_identically_zero_on_target_domains():
    reasons,partitions=target()
    assert api()([category(4)],[10**40],reasons,partitions)==[0,0,0,0]


def test_identity_and_omitted_contributions_accumulate_exactly():
    reasons,partitions=target()
    assert api()([reasons[0],category(1),category(2)],[5,7,9],reasons,partitions)==[12,-7,2,-7]


def test_single_category_partition_still_uses_both_normalizations():
    reasons,partitions=target()
    partitions[0]['groups']=partitions[0]['groups'][:1]
    assert api()([category(1)],[-3],reasons[:2],partitions)==[-3,3]


def test_other_row_metadata_is_matched_structurally():
    a=dict(kind='bounded_spectrum_value',feature=0,point=7)
    b=dict(kind='bounded_spectrum_total',total=0)
    assert api()([a,b],[10**40,-9],[b,a],[])==[-9,10**40]


def test_missing_noncategorical_identity_is_rejected():
    with pytest.raises(ValueError):
        api()([dict(kind='bounded_spectrum_value',feature=1,point=7)],[1],[],[])


@pytest.mark.parametrize('weights', [[],[.5],[True]])
def test_invalid_weight_vector_is_rejected(weights):
    reasons,partitions=target()
    with pytest.raises(ValueError):
        api()([category(1)],weights,reasons,partitions)


def test_missing_partition_is_rejected_instead_of_dropping_a_row():
    reasons,_=target()
    with pytest.raises(ValueError):
        api()([category(1)],[1],reasons,[])


def test_duplicate_target_identity_is_rejected():
    reasons,partitions=target()
    with pytest.raises(ValueError):
        api()([category(1)],[1],reasons+[reasons[0]],partitions)


def test_missing_explicit_distribution_is_rejected():
    reasons,partitions=target()
    with pytest.raises(ValueError):
        api()([category(1)],[1],reasons[:-1],partitions)


@pytest.mark.parametrize('mutation', ['missing_omitted','duplicate_value','duplicate_partition'])
def test_invalid_partition_metadata_is_rejected(mutation):
    reasons,partitions=target()
    if mutation=='missing_omitted': partitions[0]['omitted']=[99]
    elif mutation=='duplicate_value': partitions[0]['groups'].append(partitions[0]['groups'][0])
    else: partitions.append(partitions[0])
    with pytest.raises(ValueError):
        api()([category(1)],[1],reasons,partitions)
