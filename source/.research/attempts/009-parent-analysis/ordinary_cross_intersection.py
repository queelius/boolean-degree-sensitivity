"""Exact ordinary cubic supports and their complementary-pair relations."""
from itertools import combinations
import numpy as np


def ordinary_features(values):
    assert values.ndim == 2 and values.shape[1] == 1024 and np.issubdtype(values.dtype, np.integer)
    # Local outside bits 0 and 1 are the apices. Average them out exactly.
    averaged = values.astype(np.int32).reshape(len(values), 256, 4).sum(axis=2)
    spectrum = averaged.copy()
    for width in (1, 2, 4, 8, 16, 32, 64, 128):
        block = spectrum.reshape(len(values), -1, 2*width)
        left = block[:, :, :width].copy(); right = block[:, :, width:].copy()
        block[:, :, :width] = left + right; block[:, :, width:] = left - right
    triples = [sum(1 << i for i in c) for c in combinations(range(2, 10), 3)]
    numerator = spectrum[:, [mask >> 2 for mask in triples]]
    assert np.all((numerator == 0) | (numerator == 1024))
    return triples, (numerator == 1024).astype(np.int8)


def cross_relations(features, core_pairs, triples):
    assert len(core_pairs) == len(features) and len(set(core_pairs)) == len(core_pairs)
    assert all(f.ndim == 2 and f.shape[1] == len(triples) and np.all((f == 0) | (f == 1)) for f in features)
    assert len(set(triples)) == len(triples) and all(t.bit_count() == 3 for t in triples)
    core = 0
    for pair in core_pairs: core |= pair
    partners = [(j, k) for j in range(len(features)) for k in range(j+1, len(features))
                if core_pairs[j] ^ core_pairs[k] == core and core_pairs[j] & core_pairs[k] == 0]
    assert partners
    descriptions = [dict(left=j, right=k, triple=t) for j,k in partners for t in triples]
    columns = [np.zeros((len(f), len(descriptions)), dtype=np.int8) for f in features]
    relations = []
    for x, item in enumerate(descriptions):
        j, k, t = item['left'], item['right'], item['triple']
        columns[j][:,x] = features[j][:,triples.index(t)]
        disjoint = [i for i,s in enumerate(triples) if not s & t]
        columns[k][:,x] = np.any(features[k][:,disjoint], axis=1)
        zero = [0]*len(features); left = zero.copy(); right = zero.copy(); left[j] = 1; right[k] = 1
        relations.append([zero, left, right])
    return columns, relations, descriptions
