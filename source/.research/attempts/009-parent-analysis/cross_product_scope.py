"""Bind a product join to exactly the accepted ordinary-cross refinement."""


def require_cross_source(join, cross, quotient_reference, refinement_reference):
    assert join['status']=='INDEPENDENTLY_VERIFIED_MATCHED_VANISHING_SLICE_PRODUCT_JOIN'
    assert cross['status']=='INDEPENDENTLY_VERIFIED_MATCHED_ORDINARY_CROSS_REFINEMENT'
    assert cross['complete_actual_cover'] is True
    assert cross['geometry_index']==join['geometry_index']
    assert quotient_reference==join['quotient_authority']
    assert refinement_reference==join['refinement_authority']
