"""Compose the accepted group and support covers into a necessary zero rule."""
from pathlib import Path
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate

H=Path(__file__).resolve().parent


def run():
    output=H/'matched-g34-first58-full-slice-zero-independent-manifest-cycle471.json';assert not output.exists()
    b=Bindings();support_path=H/'matched-g34-first58-group0-support-sum-independent-manifest-cycle469.json'
    support=b.read(support_path)
    assert support['status']=='INDEPENDENTLY_VERIFIED_MATCHED_SUPPORT_SUM_JOIN' and support['complete_sum_cover'] is True
    groups=b.read(support['group_authority']['path'],support['group_authority']['sha256'])
    assert groups['status']=='INDEPENDENTLY_VERIFIED_MATCHED_PRODUCT_GROUP_SEARCH' and groups['complete_exact_group_cover'] is True
    assert groups['geometry_index']==support['geometry_index'] and groups['first_row']==support['first_row']
    assert groups['quotient_authority']==support['quotient_authority']
    group=support['group_index'];assert [r['group_index'] for r in groups['groups']]==list(range(groups['group_count']))
    for row in groups['groups']:
        if row['group_index']!=group:assert row['search_status']=='UNSAT' and row['unsearched_subtrees']==0
        else:assert row['zero_product'] is True
    source=b.read(support['source']['path'],support['source']['sha256']);proof=read_certificate(b,source['proof'])
    assert proof['group_authority']==support['group_authority'] and proof['group_index']==group
    def array(ref):
        b.bind(ref['path'],ref['sha256']);a=np.load(ref['path'],allow_pickle=False)
        assert list(a.shape)==ref['shape'] and str(a.dtype)==ref['dtype'];return a
    matches=array(proof['matches']);assert len(matches)>0
    for side,column in enumerate((0,2)):
        vectors=array(proof['vectors'][side]);assert not np.any(vectors[np.unique(matches[:,column])])
    targets=array(proof['targets']);assert not np.any(targets[np.unique(matches[:,1])])
    assert sorted(proof['support_points']+proof['zero_slice_points'])==list(range(2,1024,4))
    joined_authority=b.read(proof['product_join_authority']['path'],proof['product_join_authority']['sha256'])
    joined_source=b.read(joined_authority['source']['path'],joined_authority['source']['sha256'])
    joined=read_certificate(b,joined_source['proof'])
    assert joined['points']==proof['zero_slice_points'] and not np.any(array(joined['full_join']['signatures'])[group])
    pairs=proof['pairs']+[joined['safe_pair']]
    assert sorted(i for pair in pairs for i in pair)==list(range(6))
    for name in ('verify_first58_zero_products_cycle471.py','matched_full_zero_case_cycle471.md'):b.bind(H/name)
    result=dict(schema_version=1,status='INDEPENDENTLY_VERIFIED_FIRST_CASE_SELECTED_SLICE_ZERO_PRODUCTS',
        global_status='UNRESOLVED',geometry_index=groups['geometry_index'],first_row=groups['first_row'],
        quotient_authority=groups['quotient_authority'],product_group_authority=support['group_authority'],
        support_sum_authority=b.bind(support_path),complete_first_case_necessary_restriction=True,
        complementary_component_pairs=pairs,selected_apex_bits=[0,1],selected_slice_points=256,
        all_complementary_products_zero_on_selected_slice=True,other_apex_orientation_claimed=False,
        retained_domain_sizes=proof['counts']['retained_domain_sizes'],whole_first_case_excluded=False,
        whole_geometry_excluded=False,global_goal_complete=False,leaf_enumerations_reexecuted=False,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('geometry_index','first_row','selected_slice_points',
        'all_complementary_products_zero_on_selected_slice','whole_first_case_excluded')}),flush=True)


if __name__=='__main__':run()
