"""Typed whole-candidate relation; allowed rows contain two local row indices."""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class BinaryRelation:
    left: int
    right: int
    allowed: np.ndarray
