"""Exact positive and degree-violating controls for coupled slice coefficients."""
from dataclasses import replace
import importlib
import numpy as np
import pytest
from exact_box_row_lp import solve,verify_certificate


def module():return importlib.import_module('core_slice_degree_lp')


def literal_pools(outside_bits,sign_function):
    pools=[]
    for y in range(1<<outside_bits):
        values=[sign_function(y,z) for z in range(16)]
        assert set(values)<={-1,1}
        spectrum=tuple(sum(values[z]*(-1 if (q&z).bit_count()%2 else 1) for z in range(16)) for q in range(16))
        pools.append([spectrum])
    return pools


def sign(x,mask):return -1 if (x&mask).bit_count()%2 else 1


def prepare_fixed(pools,degree=5):
    api=module();pairs=tuple(q for q in range(16) if q.bit_count()==2)
    values=np.array([[[pool[0][q] for q in pairs] for pool in pools]],dtype=np.int16)
    caps=[api.DegreeCap(q,degree-q.bit_count()) for q in range(16) if q.bit_count()<=1]
    return api.prepare(pools,[api.PatternBlock(pairs,values)],caps)


def test_degree_five_function_preserves_its_complete_exact_assignment():
    pools=literal_pools(6,lambda y,z:sign(y,15)*sign(z,1))
    model=prepare_fixed(pools)
    rows=list(model.rows());assignment=[1]*model.variable_count
    assert all(row.lower<=sum(assignment[i]*v for i,v in row.terms)<=row.upper for row in rows)
    assert solve(rows,model.variable_count,seconds=5)['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'


def test_omitted_core_coordinate_can_vary_with_outside_input():
    pools=literal_pools(6,lambda y,z:sign(z,3) if not y&1 else sign(z,12))
    model=prepare_fixed(pools)
    assert solve(list(model.rows()),model.variable_count,seconds=5)['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'


@pytest.mark.parametrize('function,violating_feature,violating_character',[
    (lambda y,z:sign(y,63),0,63),
    (lambda y,z:sign(y,31)*sign(z,1),1,31)])
def test_forbidden_constant_and_linear_degrees_have_exact_contradictions(function,violating_feature,violating_character):
    model=prepare_fixed(literal_pools(6,function));rows=list(model.rows())
    special=[row for row in rows if row.reason.get('kind')=='slice_degree' and
             row.reason['feature']==violating_feature and row.reason['character']==violating_character]
    assert len(special)==1 and sum(v for _,v in special[0].terms)!=0
    result=solve(rows,model.variable_count,seconds=5)
    assert result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
    assert verify_certificate(rows,model.variable_count,result['certificate'])<0


def test_relaxing_the_degree_five_singleton_equations_loses_the_negative_control():
    pools=literal_pools(6,lambda y,z:sign(y,31)*sign(z,1))
    model=prepare_fixed(pools,degree=6)
    assert solve(list(model.rows()),model.variable_count,seconds=5)['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'


def test_shared_word_weights_reject_incompatible_marginals_and_accept_real_ones():
    api=module();pools=[[(0,4,0,0),(0,0,4,0)]]*2
    good=api.PatternBlock((1,2),np.array([[[4,0],[0,4]]],dtype=np.int16))
    bad=replace(good,values=np.array([[[4,4],[4,4]]],dtype=np.int16))
    for block,want in ((good,'NUMERICALLY_FEASIBLE_BOX_RELAXATION'),(bad,'EXACT_BOX_ROW_LP_CONTRADICTION')):
        model=api.prepare(pools,[block],[])
        assert solve(list(model.rows()),model.variable_count,seconds=5)['status']==want


def test_complete_patterns_share_one_weight_across_all_inputs():
    api=module();pools=[[(16,)], [(-16,)]]
    block=api.PatternBlock((0,),np.array([[[16],[16]],[[-16],[-16]]],dtype=np.int16))
    model=api.prepare(pools,[block],[])
    result=solve(list(model.rows()),model.variable_count,seconds=5)
    assert result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'


def test_inventory_is_exact_before_materializing_sparse_rows():
    api=module();pools=[[(0,4,0,0),(0,0,4,0)]]*2
    block=api.PatternBlock((1,2),np.array([[[4,4],[4,4]]],dtype=np.int16))
    model=api.prepare(pools,[block],[api.DegreeCap(1,0)])
    inventory=model.inventory()
    assert inventory['variables']==5 and inventory['rows']==8 and inventory['nonzeros']==15
    assert inventory['degree_rows']==1 and inventory['word_variables']==4 and inventory['pattern_variables']==1
    assert inventory['estimated_peak_bytes']>=512*15


@pytest.mark.parametrize('fault',['empty_pool','noncube','wrong_width','float_pattern','wrong_points',
    'empty_patterns','repeated_feature','overlapping_blocks','bad_cap','duplicate_cap'])
def test_inconsistent_structured_inputs_are_rejected(fault):
    api=module();pools=[[(0,4,0,0)]]*2
    blocks=[api.PatternBlock((1,),np.array([[[4],[4]]],dtype=np.int16))]
    caps=[api.DegreeCap(1,0)]
    if fault=='empty_pool':pools=[[],[(0,4,0,0)]]
    elif fault=='noncube':pools=pools+[pools[0]]
    elif fault=='wrong_width':pools=[[(0,4,0,0)],[(0,4)]]
    elif fault=='float_pattern':blocks=[replace(blocks[0],values=blocks[0].values.astype(float))]
    elif fault=='wrong_points':blocks=[replace(blocks[0],values=blocks[0].values[:,:1])]
    elif fault=='empty_patterns':blocks=[replace(blocks[0],values=blocks[0].values[:0])]
    elif fault=='repeated_feature':blocks=[api.PatternBlock((1,1),np.zeros((1,2,2),dtype=np.int16))]
    elif fault=='overlapping_blocks':blocks=blocks*2
    elif fault=='bad_cap':caps=[api.DegreeCap(4,0)]
    elif fault=='duplicate_cap':caps=caps*2
    with pytest.raises(AssertionError):api.prepare(pools,blocks,caps)
