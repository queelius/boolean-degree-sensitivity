"""Small independent arithmetic/source audit of the frozen cycle1513 proposal.

No producer imports, solver, target complex enumeration, or theorem discovery.
The local exclusion guards used below remain inherited mathematical premises.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
import hashlib
from itertools import combinations, combinations_with_replacement, product
import json
from math import comb, isqrt
from pathlib import Path
import resource
import time


ROOT = Path(__file__).resolve().parents[3]
H = ROOT / ".research/attempts/009-parent-analysis"
PINS = {
    "one-free-source-handoff-cycle1513.json":
        "b53cc1c87160b14800c0f66ffdec7c81ea253e68a6f86ad5c8cbfaff1cf9f163",
    "one-free-source-manifest-cycle1513.json":
        "e41c57eb57ffd4226dd9c88efc1823c36546f1af7c32fdd9c5388f0dbcac66b9",
    "one-free-residual-six-and-extension-audit-cycle1513.md":
        "e30a88eae5d15641bc4566938380702baab415ced2b0226295a541a8d4f08c22",
}


class AuditError(ValueError):
    """An exact check failed; deliberately independent of Python assertions."""


def require(condition, message):
    if not condition:
        raise AuditError(message)


def integer(value, label):
    require(type(value) is int, f"{label}: expected a genuine integer")
    return value


def reference(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data)}


def verify_reference(ref):
    require(isinstance(ref, dict), "reference is not an object")
    require(type(ref.get("path")) is str and type(ref.get("sha256")) is str,
            "reference has no path/digest")
    actual = reference(ref["path"])
    require(actual["sha256"] == ref["sha256"], f"digest mismatch: {ref['path']}")
    if "bytes" in ref:
        require(integer(ref["bytes"], "reference length") == actual["bytes"],
                f"length mismatch: {ref['path']}")
    return actual


def references(value):
    """Read structured source references; do not parse paths out of prose."""
    if isinstance(value, dict):
        if "path" in value and "sha256" in value:
            yield value
        for child in value.values():
            yield from references(child)
    elif isinstance(value, list):
        for child in value:
            yield from references(child)


class Level(IntEnum):
    SINGLETON = 1
    CUBIC = 3
    QUINTIC = 5


def cost(level, value):
    integer(value, "coefficient")
    require(isinstance(level, Level), "unrecognized coefficient level")
    if level == Level.SINGLETON:
        return (value - 1) * (value - 2)
    if level == Level.CUBIC:
        return value * (value + 1)
    require(value >= 0, "negative quintics are fixed before residual accounting")
    return value * (value - 1)


@dataclass(frozen=True, order=True)
class Departure:
    level: Level
    value: int

    @property
    def defect(self):
        return cost(self.level, self.value)


def departures():
    # The quadratic costs exceed six outside [-4,5], with monotone tails.
    return tuple(Departure(level, k) for level in Level for k in range(-4, 6)
                 if (level != Level.QUINTIC or k >= 0)
                 and 0 < cost(level, k) <= 6)


def old_guard(constant, incident):
    """Exactly the inherited local guards, never widened to two at c=0/3."""
    require(all(d.level != Level.SINGLETON for d in incident),
            "singleton cannot be an incident nonsingleton")
    if not incident and constant <= 3:
        return "OLD_BASELINE"
    if len(incident) == 1:
        d = incident[0]
        if d.level == Level.CUBIC and d.value in (-2, 1) and constant <= 3:
            return "OLD_ONE_QUADRATIC"
        if d.level == Level.QUINTIC and d.value == 2:
            return "OLD_ONE_DOUBLE"
    if constant in (1, 2) and len(incident) == 2 and all(d.defect == 2 for d in incident):
        return "OLD_TWO_AT_BASELINE_CONSTANT"
    return None


def allocation_route(allocation, hits, baseline_constant):
    require(len(allocation) == len(hits), "incidence length mismatch")
    require(all(type(x) is bool for x in hits), "incidence must be Boolean")
    require(baseline_constant in (1, 2), "invalid baseline constant")
    require(sum(d.defect for d in allocation) <= 6, "allocation exceeds budget")
    owned = [d for d, hit in zip(allocation, hits)
             if hit and d.level == Level.SINGLETON]
    require(len(owned) <= 1, "two singleton departures cannot own one coordinate")
    c = owned[0].value if owned else baseline_constant
    incident = tuple(d for d, hit in zip(allocation, hits)
                     if hit and d.level != Level.SINGLETON)
    inherited = old_guard(c, incident)
    if inherited:
        return c, inherited
    if owned and owned[0].value == 4:
        require(len(allocation) == 1 and 4 + 13 > 16, "singleton-four level sum")
        return c, "GLOBAL_SINGLETON_SUM"
    if len(incident) == 1 and incident[0].defect == 6:
        d = incident[0]
        if d.level == Level.QUINTIC:
            return c, "ACCEPTED_TRIPLED_QUARTIC"
        if d.value == 2:
            require([4 * m - d.value for m in (0, 1)] == [-2, 2], "plus-two link sizes")
            return c, "SIMPLE_EVEN_GRAPH_PARITY"
        require(d.value == -3 and c in (1, 2), "uncovered cost-six case")
        return c, "TYPE_I"
    require(sum(d.defect for d in allocation) == 6, "uncovered smaller budget")
    require(all(hits), "a retained allocation misses the free coordinate")
    if c in (1, 2):
        require(len(incident) == len(allocation) == 3, "invalid Type II")
        return c, "TYPE_II"
    require(c in (0, 3) and len(incident) == 2 and len(owned) == 1, "invalid Type III")
    return c, "TYPE_III_PENDING_TWO_EXCEPTION_EXTENSION"


def allocation_control():
    ds = departures()
    two = tuple(d for d in ds if d.defect == 2)
    six = tuple(d for d in ds if d.defect == 6)
    require(len(two) == len(six) == 5, "cost-domain count")
    allocs = [a for n in range(4) for a in combinations_with_replacement(two, n)]
    allocs += [(d,) for d in six]
    routes = Counter()
    retained = set()
    invalid_owned = 0
    cases = 0
    for allocation in allocs:
        for hits in product((False, True), repeat=len(allocation)):
            if sum(hit and d.level == Level.SINGLETON for d, hit in zip(allocation, hits)) > 1:
                invalid_owned += 1
                continue
            constants = (1,) if any(hit and d.level == Level.SINGLETON
                                    for d, hit in zip(allocation, hits)) else (1, 2)
            for c in constants:
                actual_c, route = allocation_route(allocation, hits, c)
                routes[route] += 1
                cases += 1
                if route.startswith("TYPE_"):
                    retained.add((route, actual_c))
    require(retained == {("TYPE_I", 1), ("TYPE_I", 2), ("TYPE_II", 1),
                         ("TYPE_II", 2), ("TYPE_III_PENDING_TWO_EXCEPTION_EXTENSION", 0),
                         ("TYPE_III_PENDING_TWO_EXCEPTION_EXTENSION", 3)}, "trichotomy guard coverage")
    return {"allocations": len(allocs), "incidence_constant_cases": cases,
            "impossible_multiple_owner_masks": invalid_owned,
            "cost_histogram": dict(sorted(Counter(sum(d.defect for d in a) for a in allocs).items())),
            "routes": dict(sorted(routes.items())),
            "retained_types_and_constants": sorted(retained),
            "all_nonsingleton_supports_are_distinct_physical_coefficients": True,
            "incidence_control_is_a_conservative_superset_not_a_function_search": True}


def moments(c):
    integer(c, "constant")
    # Solve c+A+B=16 and 2A+4B=13*8, independently of the proposal's formulas.
    top_sum = (13 * 8 - 2 * (16 - c)) // 2
    quadratic_sum = 16 - c - top_sum
    require(2 * quadratic_sum + 4 * top_sum == 13 * 8, "summed unit equation")
    edge_numerator = quadratic_sum + 6 * top_sum
    require(edge_numerator % 4 == 0, "ordinary edge sum integrality")
    return quadratic_sum, top_sum, edge_numerator // 4


def star_counts(c, r):
    require(type(c) is int and c in (1, 2), "signed-star constant guard")
    require(type(r) is int and 0 <= r <= 3, "signed-star negative count")
    a_sum, top_count, edge_count = moments(c)
    special = (-2,) * r + (1,) * (3 - r)
    n_minus = sum(special) - a_sum
    n_zero = edge_count - len(special) - n_minus
    require(n_minus >= 0 and n_zero >= 0, "negative edge counts")
    incidence = 5 * n_minus + 4 * n_zero + 6 * r + 3 * (3 - r)
    require(incidence == 6 * top_count, "quartet-edge incidence")
    p_norm = c * c + n_minus + sum(a * a for a in special) + top_count
    q_norm = 16 * 16 - p_norm
    return {"c": c, "r_negative": r, "top_quartets": top_count,
            "edges": edge_count, "ordinary_minus_one": n_minus,
            "ordinary_zero": n_zero, "P_norm": p_norm, "Q_norm": q_norm,
            "support_bound": q_norm, "amplitude_bound": isqrt(q_norm)}


def complement_counts(c, negative_magnitudes):
    require(type(c) is int and c in (0, 1, 2, 3), "incident-allocation constant guard")
    require(all(type(m) is int and m > 0 for m in negative_magnitudes), "negative magnitudes")
    negative_cost = sum(m * (m + 1) for m in negative_magnitudes)
    require(negative_cost == 22, "residual-six negative cost")
    a_sum, top_sum, _ = moments(c)
    levels = (c - 16, -(-104 - a_sum), -(104 - top_sum))
    n_twos = -levels[0] - 13
    singleton = [-2] * n_twos + [-1] * (13 - n_twos)
    n_cubics = levels[1]
    n_negative_top = sum(negative_magnitudes) - levels[2]
    norm_parts = (sum(x*x for x in singleton), n_cubics,
                  sum(x*x for x in negative_magnitudes) + n_negative_top)
    q_norm = sum(norm_parts)
    require(sum(singleton) == levels[0], "outside singleton sum")
    return {"c": c, "negative_magnitudes": list(negative_magnitudes),
            "outside_level_sums": list(levels), "minus_two_singletons": n_twos,
            "unit_cubics": n_cubics, "minus_one_quintics": n_negative_top,
            "Q_norm_by_level": list(norm_parts), "Q_norm": q_norm,
            "P_norm": 256 - q_norm}


def fiber_controls():
    rows = []
    for f0, f1 in product((0, 1), repeat=2):
        p, q = f1 - f0, f0 + f1 - 1
        require(p*q == 0 and p*p + q*q == 1, "Boolean fiber identity")
        for t in (0, 1):
            require(1 - 2 * (f0 if t == 0 else f1) == (1 - 2*t)*p - q,
                    "sign in h=z*p-q")
        # A selfdual partner fiber has complementary reversed endpoints.
        partner = (1 - f1, 1 - f0)
        require(partner[1] - partner[0] == p and sum(partner) - 1 == -q,
                "selfdual p-even/q-odd signs")
        rows.append({"fiber": [f0, f1], "p": p, "q": q})
    return {"four_fibers": rows, "unrestricted_indices": sum(comb(13, k) for k in range(6)),
            "odd_indices": sum(comb(13, k) for k in (1, 3, 5))}


def endpoint_controls():
    # This checks only the arithmetic AFTER the inherited disk lemma, not a disk catalog.
    available = set(range(4))
    sets = [set(s) for n in (3, 4) for s in combinations(available, n)]
    intersections = Counter()
    degree_pairs = Counter()
    for left, right in product(sets, repeat=2):
        degrees = (1 + 7 + len(left), 1 + 7 + len(right))
        require(set(degrees) <= {11, 12}, "endpoint degree after disk lemma")
        require(len(left & right) >= 2, "shared off-cycle count")
        intersections[len(left & right)] += 1
        degree_pairs[degrees] += 1
    return {"subset_pairs": len(sets)**2, "shared_off_cycle_histogram": dict(sorted(intersections.items())),
            "degree_pairs": [{"degrees": list(k), "count": v} for k, v in sorted(degree_pairs.items())],
            "earlier_9_10_endpoint_orders_are_excluded_by_inherited_disk_lemma": True,
            "whole_complex_manifold_assumed": False}


def source_control():
    checked = {}
    def check(ref):
        actual = verify_reference(ref)
        checked[actual["path"]] = actual
        return actual
    for name, digest in PINS.items():
        check({"path": str(H / name), "sha256": digest})
    manifest = json.loads((H / "one-free-source-manifest-cycle1513.json").read_text())
    for ref in references(manifest):
        check(ref)
    handoff = json.loads((H / "one-free-source-handoff-cycle1513.json").read_text())
    correction = json.loads(Path(handoff["norm_correction"]["path"]).read_text())
    for ref in references(correction):
        check(ref)
    # Only these selected mathematical reviews/receipts are dependencies of this audit.
    for filename in ("minus-three-links-independent-authority-cycle1395.json",
                     "three-disks-independent-authority-cycle1401.json",
                     "two-free-independent-authority-cycle1409.json"):
        authority = json.loads((H / filename).read_text())
        check(authority["review"])
    two_free = json.loads((H / "two-free-independent-authority-cycle1409.json").read_text())
    check(two_free["source_audit"])
    guard_audit = json.loads(Path(two_free["source_audit"]["path"]).read_text())
    require(guard_audit["two_exception_c0_c3_transfer_permitted"] is False,
            "old authority unexpectedly widens the two-exception guard")
    wanted = {"negative-free-derivative-catalog-audit.md",
              "one-positive-quadratic-derivative-independent-audit.md"}
    for ref in guard_audit["references"]:
        if Path(ref["path"]).name in wanted:
            check(ref)
    # Inspect the existing source graph of the accepted native proof; never invoke it.
    lrat = json.loads((H / "independent-lrat-authority-cycle1501.json").read_text())
    for key in ("review", "source_audit"):
        check(lrat[key])
    native_audit = json.loads(Path(lrat["source_audit"]["path"]).read_text())
    native_refs = list(references(native_audit)) + list(references(lrat))
    old_examples = {ref["path"] for ref in correction["superseded_source_examples"]}
    require(not old_examples.intersection(ref["path"] for ref in native_refs),
            "old source-only norm example occurs in native source audit")
    # Rehash the unchanged CNF/proof, but no parser/native verifier/solver runs here.
    check(lrat["sources"]["CNF"])
    check(lrat["sources"]["proof"])
    require(lrat["status"] == "EXCLUDED_GENUINE_ROOT7_C2_CONTEXT", "native authority scope")
    ledger = json.loads((ROOT / ".research/findings/negative-quintic-pattern-cases.json").read_text())["empty_pair"]
    whole = json.loads((H / "whole-pattern-exclusion-authority-cycle1388.json").read_text())
    require(whole["whole_magnitude_pattern_excluded"] is True, "missing independent whole-pattern authority")
    historical = [row for row in ledger["patterns"] if row["status"] == "open"]
    effective = [row for row in historical if row["negative_magnitudes"] != whole["negative_magnitudes"]]
    require(len(historical) == 30 and len(effective) == 29, "read-only effective ledger view")
    residual_six = []
    for row in effective:
        residual = ledger["defect_budget"] - sum(m*(m+1) for m in row["negative_magnitudes"])
        require(residual == row["remaining_defect"], "ledger residual arithmetic")
        if residual == 6:
            residual_six.append(row["negative_magnitudes"])
    return {"checked_sources": sorted(checked.values(), key=lambda r: r["path"]),
            "source_hashes_are_not_old_certificate_replay": True,
            "native_proof_replayed": False, "native_files_rehashed_unchanged": True,
            "old_norm_examples_in_native_dependency_references": False,
            "historical_open_rows": len(historical), "effective_open_rows": len(effective),
            "residual_six_inventories": residual_six}


def run():
    before = time.process_time()
    sources = source_control()
    stars = [star_counts(c, r) for c in (1, 2) for r in range(4)]
    norms = [complement_counts(c, inventory) for inventory in sources["residual_six_inventories"]
             for c in range(4)]
    require({(x["c"], x["P_norm"], x["Q_norm"]) for x in stars} == {(1, 66, 190), (2, 72, 184)},
            "corrected signed-star norms")
    require(all(x["P_norm"] == 60 + 6*x["c"] and x["Q_norm"] == 196 - 6*x["c"] for x in norms),
            "incident-allocation norm formula")
    return {"schema_version": 1, "status": "PASS_INDEPENDENT_SMALL_CONTROLS_AND_SOURCE_BINDINGS",
            "author": "Alexander Richard Towell", "assistance": "Substantial OpenAI Codex assistance; independent AI audit, not human/formal review.",
            "sources": sources, "signed_star_correction": stars, "one_free_allocation": allocation_control(),
            "complement_counts": norms, "fiber_and_index_controls": fiber_controls(),
            "endpoint_controls": endpoint_controls(), "CPU_seconds": time.process_time() - before,
            "limits": {"CPU_seconds": 3, "address_space_bytes": 512*1024*1024},
            "target_solver_queries": 0, "target_catalog_enumerations": 0, "native_checker_invocations": 0,
            "canonical_status_changed": False, "global_goal_complete": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    report = run()
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "sources": len(report["sources"]["checked_sources"]),
                      "CPU_seconds": report["CPU_seconds"], "output": str(args.output)}))


if __name__ == "__main__":
    main()
