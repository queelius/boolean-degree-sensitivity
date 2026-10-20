"""Construct the unchanged old instance followed by one accepted relation."""
import numpy as np
from gzip_certificate_io import read_certificate
from append_repeated_relation import append_relation


def load(bindings, refinement_path):
    refinement = bindings.read(refinement_path)
    assert refinement['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_SAFE_COUNT_REFINEMENT' and refinement['complete_actual_cover'] is True
    base = bindings.read(refinement['base_refinement']['path'], refinement['base_refinement']['sha256'])
    assert base['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT' and base['complete_actual_cover'] is True
    quota = bindings.read(base['base_authority']['path'], base['base_authority']['sha256'])
    assert quota['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    assert refinement['geometry_index'] == base['geometry_index'] == quota['geometry_index']
    instance = read_certificate(bindings, quota['instance']); extra = read_certificate(bindings, base['refinement'])
    added = read_certificate(bindings, refinement['refinement'])
    assert added['columns'] == extra['columns'] and added['source_point'] == 1024 and added['added_point'] == 1025
    tables = []
    for j, component in enumerate(instance['components']):
        values = np.load(component['values']['path'], allow_pickle=False)
        if j == quota['component_index']: values = values[quota['selected_row_indices']]
        counts = np.load(extra['columns'][j]['counts']['path'], allow_pickle=False)
        assert counts.shape == (len(values),)
        tables.append(np.column_stack((values, counts)))
    lookup = {(r['weight'], r['delta']): r['tuples'] for r in instance['relation_types']}
    relations = [lookup[x.bit_count(), 1-(x & 1)-((x >> 1) & 1)] for x in range(1024)] + [extra['allowed_count_tuples']]
    tables, relations = append_relation(tables, relations, added['source_point'], added['allowed_count_tuples'])
    return refinement, quota, tables, relations
