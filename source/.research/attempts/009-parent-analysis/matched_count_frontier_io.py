"""Load an accepted count-search frontier without inferring mathematical status."""
from dataclasses import dataclass
import numpy as np
from gzip_certificate_io import read_certificate
from finite_function_csp import FunctionCSP
from matched_component_frontier import open_frontier


@dataclass
class CountFrontier:
    authority: dict
    geometry: dict
    solver: FunctionCSP
    tree: dict
    frontier: list


def load(bindings, authority_path):
    authority = bindings.read(authority_path)
    assert authority['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_COUNT_SEARCH'
    assert authority['search_status'] == 'UNKNOWN'
    source = bindings.read(authority['source']['path'], authority['source']['sha256'])
    proof = read_certificate(bindings, source['proof'])
    refinement = bindings.read(source['instance_authority']['path'], source['instance_authority']['sha256'])
    assert refinement['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT'
    quota = bindings.read(refinement['base_authority']['path'], refinement['base_authority']['sha256'])
    assert quota['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    instance = read_certificate(bindings, quota['instance']); extra = read_certificate(bindings, refinement['refinement'])
    tables = []
    for j, component in enumerate(instance['components']):
        values = np.load(component['values']['path'], allow_pickle=False)
        if j == quota['component_index']: values = values[quota['selected_row_indices']]
        counts = np.load(extra['columns'][j]['counts']['path'], allow_pickle=False)
        tables.append(np.column_stack((values, counts)))
    lookup = {(r['weight'], r['delta']): r['tuples'] for r in instance['relation_types']}
    relations = [lookup[x.bit_count(), 1-(x & 1)-((x >> 1) & 1)] for x in range(1024)]
    relations.append(extra['allowed_count_tuples'])
    order = [1024]+sorted(range(1024), key=lambda x: (min(x.bit_count(), 10-x.bit_count()), x))
    solver = FunctionCSP(tables, relations, order)
    tree = proof['answer']['tree']; frontier = open_frontier(solver, tree)
    assert len(frontier) == authority['unsearched_subtrees']
    return CountFrontier(authority, quota['geometry'], solver, tree, frontier)
