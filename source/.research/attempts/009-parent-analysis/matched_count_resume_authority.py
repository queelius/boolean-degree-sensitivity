"""Validate unchanged instances when extending accepted partial count searches."""


def validate_previous(previous, source, refinement, refinement_reference):
    assert previous['search_status'] == 'UNKNOWN'
    assert previous['geometry_index'] == source['geometry_index'] == refinement['geometry_index']
    if previous['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_SEARCH':
        assert source['instance_authority'] == refinement['base_authority']
    else:
        assert previous['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_COUNT_SEARCH'
        assert source['instance_authority'] == refinement_reference
