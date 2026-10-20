from cubic_degree_profiles import degree_profiles
from positive_profile_partition import positive_profile_groups


def test_zero_low_profiles_force_both_apices_out_of_the_positive_support():
    singletons=[[0,8],[0,8]]+[[-4]]*8
    assert degree_profiles(10,[13],singletons)==[]
    for negative,expected in [([7],[5]*7+[7]),([13,50],[5]*4+[7]*4)]:
        profiles=degree_profiles(10,negative,singletons);assert len(profiles)==1
        groups=positive_profile_groups(profiles)
        assert len(groups)==1 and groups[0]['active']==list(range(2,10)) and groups[0]['forced']==[]
        assert sorted(profiles[0]['degrees'][2:])==expected


def test_one_low_partition_separates_inactive_apices_and_covers_every_profile():
    profiles=degree_profiles(10,[13,50],[[0,8],[0,8],[4]]+[[-4]]*7)
    groups=positive_profile_groups(profiles)
    assert sorted(i for g in groups for i in g['profile_indices'])==list(range(len(profiles)))
    assert {tuple(i for i in (0,1) if i in g['active']) for g in groups}=={(),(0,),(1,),(0,1)}
    hard=[g for g in groups if len(g['high'])==9]
    assert len(hard)==1 and hard[0]['forced']==[2] and len(hard[0]['profile_indices'])==1
