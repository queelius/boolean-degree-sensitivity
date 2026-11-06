"""Small source-bound arithmetic checks; no function/catalog/solver search."""
import hashlib
import json
import math
import time
from collections import Counter
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def signed_star(c, r):
    require(type(c) is int and c in (1, 2), "constant domain")
    require(type(r) is int and r in (1, 2, 3), "signed-star domain")
    edges, quartics = 49 + c, 36 + c
    negative_ordinary = 23 + 2 * c - 3 * r
    require(6 * quartics == 4 * (edges - 3) + negative_ordinary
            + 3 * (3 - r) + 6 * r, "incidence identity")
    coefficients = ([c] + [-1] * negative_ordinary
                    + [1] * (3 - r) + [-2] * r + [1] * quartics)
    require(sum(coefficients) == 16, "origin identity")
    norm = sum(value * value for value in coefficients)
    require(norm == c * c + 3 * c + 62, "norm identity")
    complement = 256 - norm
    return dict(constant=c, negative_exceptional_pairs=r,
                active_edges=edges, ordinary_minus_one_count=negative_ordinary,
                ordinary_zero_active_edges=edges - 3 - negative_ordinary,
                positive_quartics=quartics, norm_P=norm, norm_Q=complement,
                integer_support_bound=complement,
                integer_amplitude_bound=math.isqrt(complement))


def main():
    started = time.process_time()
    h = Path(__file__).resolve().parent
    ledger = h.parent.parent / "findings/negative-quintic-pattern-cases.json"
    authority = h / "whole-pattern-exclusion-authority-cycle1388.json"
    historical = json.loads(ledger.read_text())["empty_pair"]
    exclusion = json.loads(authority.read_text())
    require(exclusion["whole_magnitude_pattern_excluded"] is True,
            "accepted inventory premise")
    old_open = [row for row in historical["patterns"] if row["status"] == "open"]
    removed = [row for row in old_open if row["negative_magnitudes"]
               == exclusion["negative_magnitudes"]]
    require(len(removed) == 1, "one separately excluded native inventory")
    current = [row for row in old_open if row not in removed]
    histogram = Counter()
    for row in current:
        magnitudes = row["negative_magnitudes"]
        cost = sum(m * (m + 1) for m in magnitudes)
        require(cost == row["negative_defect"], "negative-cost binding")
        require(28 - cost == row["remaining_defect"], "residual binding")
        histogram[28 - cost] += 1
    require(len(old_open) == 30 and len(current) == 29, "current scoped view")
    residual_six = [row["negative_magnitudes"] for row in current
                    if row["remaining_defect"] == 6]
    require(len(residual_six) == 3, "residual-six inventory count")
    signatures = []
    for magnitudes in residual_six:
        for c in range(4):
            singleton_twos = 3 - c
            q1 = 13 - singleton_twos + 4 * singleton_twos
            q3 = 84 - 2 * c
            minus_quintics = sum(magnitudes) + 68 - c
            q5 = sum(m * m for m in magnitudes) + minus_quintics
            require(q5 == 90 - c, "quintic inventory norm")
            require(q1 + q3 + q5 == 196 - 6 * c, "odd norm")
            require(256 - q1 - q3 - q5 == 60 + 6 * c, "even norm")
            signatures.append(dict(negative_magnitudes=magnitudes, constant=c,
                                   Q_level_norms=[q1, q3, q5],
                                   norm_Q=q1 + q3 + q5, norm_P=60 + 6 * c))
    stars = [signed_star(c, r) for c in (1, 2) for r in (1, 2, 3)]
    corrected = signed_star(2, 1)
    require(corrected["ordinary_minus_one_count"] == 24
            and corrected["norm_P"] == 72 and corrected["norm_Q"] == 184,
            "root-seven correction")
    require(corrected["norm_P"] != 96 and corrected["norm_Q"] != 160,
            "old erroneous norm rejected")
    rejects = []
    for args in ((True, 1), (2, True), (0, 1), (2, 4)):
        try:
            signed_star(*args)
        except ValueError:
            rejects.append(list(args))
        else:
            raise ValueError("invalid arithmetic metadata accepted")
    refs = []
    for path in (Path(__file__).resolve(), ledger, authority):
        refs.append(dict(path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    result = dict(status="ARITHMETIC_AND_STRUCTURED_SOURCE_CHECKS_PASSED",
                  scope="No existence, topology, local exclusion, or whole-pattern proof is certified by these arithmetic checks.",
                  historical_open_count=len(old_open), effective_open_count=len(current),
                  residual_budget_histogram=dict(sorted(histogram.items())),
                  residual_six_inventories=residual_six, signed_star_checks=stars,
                  one_free_signature_checks=signatures, invalid_metadata_rejected=rejects,
                  sources=refs, cpu_seconds=time.process_time() - started,
                  target_solver_calls=0, target_catalog_enumerations=0)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
