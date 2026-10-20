"""Precompute exact simplex bounds for every fixed marked-component row."""
from dataclasses import dataclass
from numbers import Integral
import numpy as np
from condition_core_word_scores import minima_by_feature


@dataclass(frozen=True)
class CaseBound:
    candidate_index: int
    empty_points: tuple[int, ...]
    lower_bound: int | None
    gap: int | None

    @property
    def candidate_contradiction(self):
        return bool(self.empty_points) or self.gap > 0


@dataclass(frozen=True)
class ConditionalScores:
    pattern_costs: tuple[tuple[int, ...], ...]
    word_minima: tuple[dict[int, int], ...]
    fixed_lower_bound: int
    bounds: tuple[CaseBound, ...]


def integer(value):
    return isinstance(value, Integral) and not isinstance(value, (bool, np.bool_))


def build(functional, tables, features, pools, flags, marked):
    points = len(pools)
    if not points or not tables or len(tables) != len(features):
        raise ValueError("Require matching nonempty components and face points.")
    if not integer(marked) or not 0 <= marked < len(tables):
        raise ValueError("Marked component index is invalid.")
    if any(not integer(f) or f < 0 for f in features) or len(set(features)) != len(features):
        raise ValueError("Require distinct nonnegative integer features.")
    if not integer(functional.rhs) or any(not integer(c) for c in flags):
        raise ValueError("Require integer RHS and flag costs.")
    values = []
    pattern_costs = []
    for block, (table, feature) in enumerate(zip(tables, features)):
        table = np.asarray(table)
        if (table.ndim != 2 or not len(table) or table.shape[1] < points
                or not np.issubdtype(table.dtype, np.integer)):
            raise ValueError("Require nonempty integer component tables covering every point.")
        face = table[:, :points]
        values.append(face)
        costs = functional.pattern_scores(block, face[:, :, None], (feature,))
        if len(costs) != len(face) or any(not integer(c) for c in costs):
            raise ValueError("Require an exact integer cost for each complete pattern.")
        pattern_costs.append(tuple(map(int, costs)))
    word_minima = []
    for point, words in enumerate(pools):
        if any(len(word) <= max(features) or any(not integer(v) for v in word) for word in words):
            raise ValueError("Require integer words covering every component feature.")
        unary = {feature: set(map(int, np.unique(table[:, point])))
                 for feature, table in zip(features, values)}
        costs = [functional.word_score(point, word) for word in words]
        word_minima.append(minima_by_feature(words, costs, unary, features[marked]))
    fixed = sum(min(costs) for block, costs in enumerate(pattern_costs) if block != marked)
    fixed += sum(min(0, int(c)) for c in flags)
    bounds = []
    for index, (pattern, cost) in enumerate(zip(values[marked], pattern_costs[marked])):
        empty = tuple(x for x, value in enumerate(pattern) if int(value) not in word_minima[x])
        lower = None if empty else fixed + cost + sum(word_minima[x][int(v)] for x, v in enumerate(pattern))
        bounds.append(CaseBound(index, empty, lower, None if lower is None else lower-int(functional.rhs)))
    return ConditionalScores(tuple(pattern_costs), tuple(word_minima), fixed, tuple(bounds))
