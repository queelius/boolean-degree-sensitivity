"""Finite pair-domain consistency against exact Boolean four-cube relations.

Each safe pair has derivative values (t,t+d,t+d,t) on the other two
common-core bits. Here d=(z_a+z_b)/2 is shared by every safe pair and t
is a catalog-row function of the ten outside bits. All arithmetic is exact.
Passing these necessary, separately consistent restrictions is not a witness.
"""
from dataclasses import dataclass, field
from functools import lru_cache
from itertools import combinations
import numpy as np

from two_positive_pair_domains import make_domains, compatible_rows
from two_positive_three_cubes import walsh_rows, coordinates


@lru_cache(None)
def relation(pairs, outside_weight, delta):
    assert 0 <= outside_weight <= 10 and delta in (-1, 0, 1)
    assert pairs and len(pairs) == len(set(pairs))
    words = np.arange(65536, dtype=np.uint32)
    truth = ((words[:, None] >> np.arange(16)) & 1).astype(np.int8)
    live = np.ones(65536, dtype=bool)
    for point in range(16):
        weight = outside_weight + point.bit_count()
        if weight in (0, 12, 13): live &= truth[:, point] == 0
        elif weight in (1, 2, 14): live &= truth[:, point] == 1
    cols = []
    for pair in pairs:
        assert 0 < pair < 16 and pair.bit_count() == 2
        i, j = [v for v in range(4) if pair >> v & 1]
        rest = [v for v in range(4) if not pair >> v & 1]
        values = []
        for point in range(4):
            base = sum(1 << v for k, v in enumerate(rest) if point >> k & 1)
            values.append(truth[:, base | pair] + truth[:, base]
                          - truth[:, base | (1 << i)] - truth[:, base | (1 << j)])
        t = values[0]
        live &= (values[3] == t) & (values[1] == t + delta) & (values[2] == t + delta)
        cols.append(t)
    return tuple(sorted(set(map(tuple, np.stack(cols, axis=1)[live].tolist()))))


def supported_values(allowed, available):
    supports = [0] * len(available)
    for values in allowed:
        assert len(values) == len(available)
        if all(bits & (1 << (value + 2)) for bits, value in zip(available, values)):
            for i, value in enumerate(values): supports[i] |= 1 << (value + 2)
    return tuple(supports)


@dataclass
class CubeIndex:
    table: np.ndarray
    masks: dict = field(default_factory=dict)

    @classmethod
    def build(cls, rows):
        full = walsh_rows(rows)
        points = np.arange(1024, dtype=np.int16)
        indices = (points & 3) | ((points >> 2) << 4)
        base = full[:, indices]
        delta = np.array([1, 0, 0, -1], dtype=np.int8)[points & 3]
        assert np.array_equal(full[:, indices | 12], base)
        assert np.array_equal(full[:, indices | 4], base + delta)
        assert np.array_equal(full[:, indices | 8], base + delta)
        return cls(base)

    def partitions(self, point):
        if point not in self.masks:
            values = self.table[:, point]
            self.masks[point] = tuple(int.from_bytes(np.packbits(values == k, bitorder='little').tobytes(), 'little')
                                     for k in range(-2, 3))
        return self.masks[point]


def setup(geometry):
    core = geometry['positive_doubles'][0] & geometry['positive_doubles'][1]
    vs = [v for v in range(14) if core >> v & 1]
    pairs = tuple(sum(1 << i for i, v in enumerate(vs) if pair >> v & 1)
                  for pair in geometry['eligible_pairs'])
    outside = None
    for pair in geometry['eligible_pairs']:
        image = coordinates(geometry, pair)
        this = image[:2] + image[4:]
        if outside is None: outside = this
        else: assert outside == this
    assert len(outside) == 10 and set(outside) == set(range(14)) - set(vs)
    return pairs, outside


def propagate(initial, geometry, index, cubes):
    domains = make_domains(geometry, index)
    pairs, outside = setup(geometry)
    live = [(1 << index.size) - 1 for _ in domains]
    known = dict(initial)
    steps = []

    def finish(status, **kwargs):
        return dict(status=status, steps=steps, known=sorted(known.items()), **kwargs)

    # Weight-one and weight-two guards are cheap and usually informative first.
    points = sorted(range(1024), key=lambda p: (min(p.bit_count(), 10-p.bit_count()), p))
    while True:
        changed = False
        for j, domain in enumerate(domains):
            reduced = live[j] & compatible_rows(domain, known)
            if reduced != live[j]:
                live[j] = reduced
                steps.append(dict(method='coefficient_filter', pair=domain.pair, remaining_rows=reduced.bit_count()))
                changed = True
            if not reduced: return finish('EXACT_FOUR_CUBE_PAIR_DOMAIN_CONTRADICTION', contradiction_pair=domain.pair)
        for point in points:
            partitions = cubes.partitions(point)
            available = tuple(sum(1 << i for i, mask in enumerate(partitions) if mask & rows) for rows in live)
            delta = (1, 0, 0, -1)[point & 3]
            allowed = relation(pairs, point.bit_count(), delta)
            supports = supported_values(allowed, available)
            if not all(supports):
                return finish('EXACT_FOUR_CUBE_PAIR_DOMAIN_CONTRADICTION',
                              contradiction_point=point, outside_point=sum(1 << v for i,v in enumerate(outside) if point >> i & 1))
            cuts = []
            for j, (support, possible) in enumerate(zip(supports, available)):
                if support == possible: continue
                keep = 0
                for i, mask in enumerate(partitions):
                    if support >> i & 1: keep |= mask
                live[j] &= keep
                cuts.append(dict(pair=domains[j].pair, remaining_rows=live[j].bit_count()))
            if cuts:
                steps.append(dict(method='four_cube_filter', point=point, cuts=cuts))
                changed = True
        for j, domain in enumerate(domains):
            forces = []
            for q, sign, ones in domain.columns:
                if q in known: continue
                values = live[j] & ones
                if not values or values == live[j]:
                    known[q] = sign * int(bool(values))
                    forces.append([q, known[q]])
            if forces:
                steps.append(dict(method='coefficient_forces', pair=domain.pair, forces=forces))
                changed = True
        if not changed:
            return finish('NECESSARY_FOUR_CUBE_PAIR_DOMAIN_FIXED_POINT',
                          domains=[dict(pair=domain.pair, rows=[i for i in range(index.size) if rows >> i & 1])
                                   for domain, rows in zip(domains, live)])
