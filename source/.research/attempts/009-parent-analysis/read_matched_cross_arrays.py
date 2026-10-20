"""Read accepted cross-refined arrays without importing producer construction."""
from dataclasses import dataclass
import numpy as np
from gzip_certificate_io import read_certificate


@dataclass
class CrossArrays:
    authority: dict
    quotient_reference: dict
    quota: dict
    tables: list
    relations: list


def load(bindings,authority_path):
    cross_authority=bindings.read(authority_path)
    assert cross_authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_ORDINARY_CROSS_REFINEMENT'and cross_authority['complete_actual_cover']is True
    safe_authority=bindings.read(cross_authority['base_refinement']['path'],cross_authority['base_refinement']['sha256'])
    assert safe_authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_SAFE_COUNT_REFINEMENT'and safe_authority['complete_actual_cover']is True
    count_authority=bindings.read(safe_authority['base_refinement']['path'],safe_authority['base_refinement']['sha256'])
    assert count_authority['status']=='INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT'and count_authority['complete_actual_cover']is True
    quota=bindings.read(count_authority['base_authority']['path'],count_authority['base_authority']['sha256'])
    assert quota['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT'and quota['complete_actual_cover']is True
    assert cross_authority['geometry_index']==safe_authority['geometry_index']==count_authority['geometry_index']==quota['geometry_index']
    instance=read_certificate(bindings,quota['instance']);counts=read_certificate(bindings,count_authority['refinement'])
    bounded=read_certificate(bindings,safe_authority['refinement']);cross=read_certificate(bindings,cross_authority['refinement'])
    assert cross['base_refinement']==cross_authority['base_refinement']and cross['quotient_authority']==count_authority['base_authority']
    assert bounded['base_refinement']==safe_authority['base_refinement']and counts['base_authority']==count_authority['base_authority']
    assert bounded['columns']==counts['columns']and bounded['source_point']==1024 and bounded['added_point']==1025
    assert cross['old_point_count']==cross_authority['old_point_count']==1026
    assert len(instance['components'])==len(counts['columns'])==len(cross['components'])==6
    tables=[]
    for j,component in enumerate(instance['components']):
        values=np.load(component['values']['path'],allow_pickle=False)
        if j==quota['component_index']:values=np.stack([values[i]for i in quota['selected_row_indices']])
        q=np.load(counts['columns'][j]['counts']['path'],allow_pickle=False)
        appended=np.load(cross['components'][j]['columns']['path'],allow_pickle=False)
        assert values.shape==(len(q),1024)and appended.shape==(len(q),cross_authority['added_points'])
        tables.append(np.concatenate((values,q[:,None],q[:,None],appended),axis=1))
    lookup={(r['weight'],r['delta']):r['tuples']for r in instance['relation_types']}
    relations=[lookup[x.bit_count(),1-(x&1)-((x>>1)&1)]for x in range(1024)]
    relations.extend([counts['allowed_count_tuples'],bounded['allowed_count_tuples']]);relations.extend(cross['relations'])
    assert len(relations)==tables[0].shape[1]
    return CrossArrays(cross_authority,count_authority['base_authority'],quota,tables,relations)
