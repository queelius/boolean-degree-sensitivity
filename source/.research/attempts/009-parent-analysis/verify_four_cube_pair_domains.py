"""Independent scalar replay of finite row-domain / Boolean cube deductions.

No new domain, Walsh transform, vectorized relation, or search producer is
imported. Cube relations are rebuilt from integer Boolean truth words; pair
values are evaluated directly by parity sums of the literal catalog rows.
"""
from functools import lru_cache
from itertools import combinations
from verify_coupled_two_positive import PairChecker, layout


@lru_cache(None)
def literal_relations(pairs):
    slices = []
    for pair in pairs:
        assert 0 < pair < 16 and pair.bit_count() == 2
        i, j = [v for v in range(4) if pair >> v & 1]
        rest = [v for v in range(4) if not pair >> v & 1]
        slices.append(tuple((base, base | (1 << i), base | (1 << j), base | pair)
                            for base in (0, 1 << rest[0], 1 << rest[1], (1 << rest[0]) | (1 << rest[1]))))
    result = {(w, d): set() for w in range(11) for d in (-1, 0, 1)}
    for word in range(65536):
        values = []
        delta = None
        for block in slices:
            derivatives = [((word >> ij) & 1) + ((word >> x) & 1)
                           - ((word >> i) & 1) - ((word >> j) & 1) for x, i, j, ij in block]
            a, b, c, e = derivatives
            this_delta = b - a
            if a != e or b != c or this_delta not in (-1, 0, 1) or (delta is not None and this_delta != delta):
                break
            delta = this_delta
            values.append(a)
        if len(values) != len(pairs): continue
        for outside_weight in range(11):
            valid = True
            for point in range(16):
                w = outside_weight + point.bit_count()
                value = (word >> point) & 1
                if (w in (0, 12, 13) and value != 0) or (w in (1, 2, 14) and value != 1):
                    valid = False
                    break
            if valid: result[outside_weight, delta].add(tuple(values))
    return result


class LiteralCubeChecker:
    def __init__(self, rows):
        self.rows = rows
        self.pairs = PairChecker(rows)
        self.terms = []
        for row in rows:
            terms = [(q, 1) for q in row['unit_faces']] + [(13, 2), (14, 2)]
            terms += [(1 << v, k) for v, k in enumerate(row['linear_numerators']) if k]
            self.terms.append(terms)
        self.values = {}

    def at(self, point):
        assert 0 <= point < 1024
        if point not in self.values:
            x = sum(1 << (v if v < 2 else v + 2) for v in range(10) if point >> v & 1)
            values = []
            for terms in self.terms:
                numerator = -sum(k * (-1 if (q & x).bit_count() % 2 else 1) for q, k in terms)
                assert numerator % 8 == 0 and -16 <= numerator <= 16
                values.append(numerator // 8)
            self.values[point] = tuple(values)
        return self.values[point]

    @staticmethod
    def coordinates(geometry):
        p, r = geometry['positive_doubles']
        core = p & r
        vs = [v for v in range(14) if core >> v & 1]
        assert len(vs) == 4
        local_pairs = tuple(sum(1 << i for i, v in enumerate(vs) if pair >> v & 1)
                            for pair in geometry['eligible_pairs'])
        a, = [v for v in range(14) if (p ^ core) >> v & 1]
        c, = [v for v in range(14) if (r ^ core) >> v & 1]
        outside = [a, c] + sorted(set(range(14)) - set(vs) - {a, c})
        return local_pairs, outside

    def reductions(self, live, local_pairs, point):
        values = self.at(point)
        possibilities = [{values[i] for i in rows} for rows in live]
        delta = 1 - (point & 1) - ((point >> 1) & 1)
        allowed = literal_relations(local_pairs)[point.bit_count(), delta]
        extendible = [t for t in allowed if all(v in s for v, s in zip(t, possibilities))]
        support = [{t[j] for t in extendible} for j in range(len(live))]
        return [{i for i in rows if values[i] in support[j]} for j, rows in enumerate(live)]

    def replay(self, initial, geometry, proof):
        known = dict(initial)
        pairs = geometry['eligible_pairs']
        assert len(pairs) == len(set(pairs)) and pairs
        local_pairs, outside = self.coordinates(geometry)
        live = [set(range(len(self.rows))) for _ in pairs]
        position = {pair: i for i, pair in enumerate(pairs)}
        for step in proof['steps']:
            method = step['method']
            if method == 'coefficient_filter':
                j = position[step['pair']]
                updated = live[j] & set(self.pairs.live(geometry, pairs[j], known))
                assert updated != live[j] and len(updated) == step['remaining_rows']
                live[j] = updated
            elif method == 'four_cube_filter':
                updated = self.reductions(live, local_pairs, step['point'])
                expected = [dict(pair=pair, remaining_rows=len(rows)) for j, (pair, rows) in enumerate(zip(pairs, updated))
                            if rows != live[j]]
                assert expected and expected == step['cuts'] and all(updated)
                live = updated
            elif method == 'coefficient_forces':
                j = position[step['pair']]
                assert live[j] and step['forces']
                columns = {q: (local, sign) for q, local, sign in layout(tuple(geometry['positive_doubles']), pairs[j])}
                for q, k in step['forces']:
                    assert q not in known
                    local, sign = columns[q]
                    bit = sign * k
                    assert bit in (0, 1)
                    assert all(((self.pairs.spectra[i] >> local) & 1) == bit for i in live[j])
                    known[q] = k
            else: raise AssertionError('unrecognized finite-domain proof step')
        assert proof['known'] == [list(x) for x in sorted(known.items())]
        if proof['status'] == 'EXACT_FOUR_CUBE_PAIR_DOMAIN_CONTRADICTION':
            if 'contradiction_pair' in proof:
                assert not live[position[proof['contradiction_pair']]]
            else:
                point = proof['contradiction_point']
                assert proof['outside_point'] == sum(1 << v for i, v in enumerate(outside) if point >> i & 1)
                assert not any(self.reductions(live, local_pairs, point))
            return dict(excluded=True, known=known)
        assert proof['status'] == 'NECESSARY_FOUR_CUBE_PAIR_DOMAIN_FIXED_POINT'
        assert all(live)
        assert proof['domains'] == [dict(pair=pair, rows=sorted(rows)) for pair, rows in zip(pairs, live)]
        return dict(excluded=False, known=known, domains=proof['domains'])
