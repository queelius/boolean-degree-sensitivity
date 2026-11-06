"""Derive labeled theorem constraints, without propagation or feasibility queries.

The written theorems and complete native context domain are external accepted
premises. These routines derive their literal mask/row instantiations only.
"""
from collections import Counter
from itertools import combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(model_id):
    require(type(model_id) is dict and set(model_id) == {'native_identity', 'constant'},
            'model identity fields')
    native = model_id['native_identity']
    require(type(native) is dict and set(native) == {'catalog_sha256', 'order', 'original_index'},
            'native identity fields')
    digest = native['catalog_sha256']
    require(type(digest) is str and len(digest) == 64 and
            all(c in '0123456789abcdef' for c in digest), 'catalog digest')
    require(all(type(native[k]) is int and native[k] >= 0 for k in ('order', 'original_index'))
            and type(model_id['constant']) is int and model_id['constant'] in (1, 2),
            'typed model identity')
    return digest, native['order'], native['original_index'], model_id['constant']


def derive_context(context, variables):
    n, root = context['n'], context['root']
    require(type(n) is int and 8 <= n <= 13 and type(root) is int and 0 <= root < n,
            'dimension or root')
    expected_variables = [sum(1 << i for i in c) for k in (2, 3, 4)
                          for c in combinations(range(n), k)]
    require(all(type(v) is int for v in variables) and variables == expected_variables,
            'complete ordered native variable masks')
    variable_index = {v: i for i, v in enumerate(variables)}
    faces = context['root_link']
    root_mask = 1 << root
    require(type(faces) is list and len(faces) == len(set(faces)) and faces and
            all(type(f) is int and 0 < f < (1 << n) and f.bit_count() == 3 and
                not f & root_mask for f in faces), 'distinct root-link triangles')
    vertices = sorted({v for f in faces for v in range(n) if f >> v & 1})
    embedding = context['source_to_physical']
    require(all(type(v) is int for v in embedding) and len(set(embedding)) == len(embedding)
            and sorted(embedding) == vertices, 'source embedding')
    degrees = {v: sum(bool(f >> v & 1) for f in faces) for v in vertices}
    edges = Counter(e for f in faces for e in variables if e.bit_count() == 2 and e & f == e)
    require(all(count == 2 for count in edges.values()) and
            len(vertices) - len(edges) + len(faces) == 2, 'closed Euler-two link guards')
    require(all(d in (3, 4, 5, 6) for d in degrees.values()), 'root-link degree profile')
    special = [dict(pair_mask=root_mask | (1 << v), valence=d, quadratic_numerator=4-d)
               for v, d in degrees.items() if d in (3, 6)]
    require(all(type(e) is dict and set(e) == {'pair_mask', 'valence', 'quadratic_numerator'}
                and all(type(value) is int for value in e.values())
                for e in context['special_edges']) and context['special_edges'] == special,
            'literal exceptional star/signs')
    positive_tips = []
    for tip, degree in degrees.items():
        if degree != 3:
            continue
        tip_mask = 1 << tip
        opposite_edges = sorted(f ^ tip_mask for f in faces if f & tip_mask)
        opposite = 0
        for edge in opposite_edges:
            opposite |= edge
        require(opposite.bit_count() == 3 and len(set(opposite_edges)) == 3 and
                opposite_edges == sorted(opposite ^ (1 << v) for v in range(n)
                                          if opposite >> v & 1), 'triangular positive edge link')
        require(not opposite & (root_mask | tip_mask) and
                all(not edge & root_mask for edge in opposite_edges), 'ordinary opposite edges')
        incident_edges = sorted(root_edge for root_edge in variables
                                if root_edge.bit_count() == 2 and root_edge & tip_mask)
        require(len(incident_edges) == n-1, 'complete incident degree variables')
        positive_tips.append(dict(tip=tip, tip_mask=tip_mask,
            positive_edge_mask=root_mask | tip_mask, opposite_triangle_mask=opposite,
            opposite_edge_masks=opposite_edges,
            native_triangle_variable_index=variable_index[opposite],
            degree_edge_masks=incident_edges,
            native_degree_variable_indices=[variable_index[e] for e in incident_edges]))
    added_rows = [dict(key=dict(family='POSITIVE_OPPOSITE_TRIANGLE_ABSENT',
                              subject=p['opposite_triangle_mask'], detail=0),
                       terms=[[p['opposite_triangle_mask'], 1]], lower=0, upper=0)
                  for p in positive_tips]
    added_rows += [dict(key=dict(family='POSITIVE_TIP_DEGREE_LOWER_BOUND',
                                subject=p['tip_mask'], detail=0),
                         terms=[[e, 1] for e in p['degree_edge_masks']], lower=7, upper=n-1)
                   for p in positive_tips]
    require(len({(r['key']['family'], r['key']['subject'], r['key']['detail'])
                 for r in added_rows}) == len(added_rows), 'duplicate appended row keys')
    return dict(n=n, root=root, root_mask=root_mask,
                source_to_physical=embedding, root_link=faces, special_edges=special,
                positive_tips=positive_tips, added_rows=added_rows)


def inventory(common, packet, gate, frontier):
    contexts, expected = packet['contexts'], packet['expected_model_ids']
    keys = [identity(c['model_id']) for c in contexts]
    require(len(keys) == len(set(keys)) and keys == [identity(m) for m in expected],
            'complete original context order/identity')
    require(packet['pending'] == 0 and packet['completed'] == len(keys) == gate['models_compared'],
            'complete accepted context count')
    require(keys == [identity(c['model_id']) for c in gate['contexts']] and
            gate['variable_count'] == len(common['variables']), 'accepted row gate identities')
    front_keys = [identity(e['model_id']) for e in frontier['entries']]
    require(len(front_keys) == len(set(front_keys)) and set(front_keys) == set(keys),
            'exact frontier context coverage')
    front = dict(zip(front_keys, frontier['entries']))
    records = []
    for c, accepted, key in zip(contexts, gate['contexts'], keys):
        require(c['n'] == common['n'] and c['row_count'] == accepted['rows'], 'native row layout')
        f = front[key]
        require(f['genuine_context_status'] in ('OPEN', 'EXCLUDED') and
                f['raw_row_model_status'] in ('OPEN', 'EXCLUDED'), 'frontier status')
        require((f['genuine_exclusion_authority'] is not None) ==
                (f['genuine_context_status'] == 'EXCLUDED'), 'exclusion authority scope')
        r = derive_context(c, common['variables'])
        original = common['row_count'] + c['row_count']
        records.append(dict(r, model_id=c['model_id'],
            genuine_context_status=f['genuine_context_status'],
            raw_row_model_status=f['raw_row_model_status'],
            skip_future_queries=(f['genuine_context_status'] == 'EXCLUDED'),
            genuine_exclusion_authority=f['genuine_exclusion_authority'],
            original_row_count=original, extended_row_count=original+len(r['added_rows']),
            added_row_native_ids=list(range(original, original+len(r['added_rows'])))))
    return dict(contexts=records, model_count=len(records),
                genuine_context_counts=dict(Counter(r['genuine_context_status'] for r in records)),
                raw_row_counts=dict(Counter(r['raw_row_model_status'] for r in records)),
                positive_tip_count=sum(len(r['positive_tips']) for r in records),
                added_row_count=sum(len(r['added_rows']) for r in records))
