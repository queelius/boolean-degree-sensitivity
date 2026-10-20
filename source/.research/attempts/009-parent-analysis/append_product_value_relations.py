"""Append exact product values while preserving every original column and row."""
from numbers import Integral
import numpy as np


def append_product_values(tables, relations, points, pairs, targets):
    assert tables and all(t.ndim == 2 and t.shape[1] == len(relations) for t in tables)
    assert len(points) == len(set(points)) and all(0 <= x < len(relations) for x in points)
    assert all(0 <= i < len(tables) and 0 <= j < len(tables) and i != j for i, j in pairs)
    assert len(targets) == len(pairs) and all(len(t) == len(points) for t in targets)
    assert all(isinstance(v, Integral) for row in targets for v in row)
    added = [[tuple(row) for row in relations[x]
              if all(int(row[i]) * int(row[j]) == int(targets[k][p]) for k, (i, j) in enumerate(pairs))]
             for p, x in enumerate(points)]
    return [np.concatenate((t, t[:, points]), axis=1) for t in tables], list(relations) + added
