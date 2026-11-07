"""Independent necessary-row recognition and compact replay for cycle1527.

Only the retained 945 rows are reconstructed. No full model, sphere catalog
enumeration, solver call, or import of a producer/previous verifier occurs.
All checks remain active under Python optimization.
"""
from collections import Counter
from enum import Enum
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import signal
import time

ROOT = Path(__file__).resolve().parents[3]
H = ROOT / ".research/attempts/009-parent-analysis"
S = ROOT / ".research/attempts/006-solver-resume"
HANDOFF = H / "adjacent-two-negative-extension-handoff-cycle1526.json"
HANDOFF_SHA = "e6bb82b7832d7e9298c9b7aeb6602d04e32bb925670cfadefb1b785727a4a5cf"
OLD_AUTHORITY = S / "two-adjacent-negative-cubic-accepted-manifest.json"
OLD_AUTHORITY_SHA = "47a0c56e5d0f345d02d7a095dd6fb4de49a802935fe0d80cb2cfa8e42eb2b94b"


class AuditError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


class Kind(str, Enum):
    DOWNWARD = "downward"
    COFACES = "triangle_two_tetrahedra"
    ROOT = "root_link"
    EULER = "induced_euler"
    VALENCE = "ordinary_edge_four_or_five"
    ORDINARY_FLAG = "ordinary_vertex_link_flag"
    PRIVATE_FLAG = "private_endpoint_one_six_link_flag"
    PRIVATE_ORDER = "private_endpoint_one_six_link_order"
    INDEPENDENCE = "no_independent_triple"


def vertices(mask):
    require(type(mask) is int and 0 <= mask < (1 << 13), "invalid face mask")
    return frozenset(i for i in range(13) if mask & (1 << i))


def subsets(items, size):
    return [frozenset(t) for t in combinations(sorted(items), size)]


def connected(adjacency):
    if not adjacency:
        return False
    seen, todo = set(), [next(iter(adjacency))]
    while todo:
        u = todo.pop()
        if u not in seen:
            seen.add(u)
            todo.extend(adjacency[u] - seen)
    return seen == set(adjacency)


def check_root(link):
    """Validate each of the nine supplied literals, without generating a cover."""
    require(set(link) == {"order", "index", "face_masks", "degree_vector", "exceptional_vertices"},
            "unexpected root fields")
    n, index = link["order"], link["index"]
    require(type(n) is int and 8 <= n <= 12 and type(index) is int and index >= 0, "root identity")
    facets = [vertices(m) for m in link["face_masks"]]
    require(len(facets) == len(set(facets)) == 2*n-4, "root face multiplicity/count")
    require(all(len(t) == 3 and t <= set(range(n)) for t in facets), "root face labels")
    edges = Counter(e for t in facets for e in subsets(t, 2))
    require(len(edges) == 3*n-6 and set(edges.values()) == {2}, "root edge incidences")
    adjacency = {v: set() for v in range(n)}
    for e in edges:
        u, v = sorted(e)
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(connected(adjacency), "disconnected root")
    degrees = [len(adjacency[v]) for v in range(n)]
    require(link["degree_vector"] == degrees and degrees.count(6) == 2 and set(degrees) <= {4, 5, 6},
            "root degree metadata")
    exceptional = [v for v, d in enumerate(degrees) if d == 6]
    require(link["exceptional_vertices"] == exceptional, "root exceptional labels")
    for v in range(n):
        cycle = {u: set() for u in adjacency[v]}
        for t in facets:
            if v in t:
                u, w = sorted(t - {v})
                cycle[u].add(w)
                cycle[w].add(u)
        require(all(len(neighbors) == 2 for neighbors in cycle.values()) and connected(cycle),
                "root vertex link not a circle")
    return {"order": n, "index": index, "private_vertices": [x+1 for x in exceptional],
            "faces": len(facets), "edges": len(edges), "chi": n-len(edges)+len(facets)}


def validate_row(row):
    require(isinstance(row, dict) and set(row) == {"terms", "lower", "upper", "reason"}, "row schema")
    require(type(row["lower"]) is int and type(row["upper"]) is int and row["lower"] <= row["upper"],
            "row endpoints")
    require(type(row["reason"]) is str and isinstance(row["terms"], list), "row labels/terms")
    terms = row["terms"]
    require(bool(terms) and all(isinstance(t, list) and len(t) == 2 for t in terms), "term schema")
    require(all(type(v) is int and type(c) is int and 2 <= len(vertices(v)) <= 4 and c != 0
                for v, c in terms), "noninteger/invalid term")
    require(terms == sorted(terms) and len({v for v, _ in terms}) == len(terms), "unordered/duplicate term")
    return {vertices(v): c for v, c in terms}


def recognize(row, link):
    """Reconstruct the row as a set formula, ignoring saved original indices."""
    terms = validate_row(row)
    try:
        kind = Kind(row["reason"])
    except ValueError as error:
        raise AuditError("unsupported or constant-dependent row family") from error
    positive = [f for f, c in terms.items() if c > 0]
    negative = [f for f, c in terms.items() if c < 0]
    private = {v+1 for v in link["exceptional_vertices"]}
    exceptional = {frozenset((0, v)) for v in private}
    ground = set(range(13))
    if kind == Kind.DOWNWARD:
        require(len(positive) == len(negative) == 1, "downward signs")
        top, bottom = positive[0], negative[0]
        require(bottom < top and len(top) == len(bottom)+1, "downward support")
        expected, low, high = {top: 1, bottom: -1}, -1, 0
    elif kind == Kind.COFACES:
        require(len(negative) == 1 and len(negative[0]) == 3, "triangle anchor")
        triangle = negative[0]
        expected = {triangle | {v}: 1 for v in ground - triangle}
        expected[triangle] = -2
        low = high = 0
    elif kind == Kind.ROOT:
        require(len(terms) == 1, "root row length")
        face = next(iter(terms))
        require(0 in face, "root center missing")
        root_triangles = [frozenset(v+1 for v in vertices(m)) for m in link["face_masks"]]
        value = int(any(face - {0} <= t for t in root_triangles))
        expected, low, high = {face: 1}, value, value
    elif kind == Kind.EULER:
        domain = frozenset().union(*terms)
        require(len(domain) >= 3, "Euler domain too small")
        expected = {face: (1 if size == 3 else -1)
                    for size in (2, 3, 4) for face in subsets(domain, size)}
        low, high = -len(domain), 2-len(domain)
    elif kind == Kind.VALENCE:
        require(len(negative) == 1 and len(negative[0]) == 2, "ordinary edge anchor")
        edge = negative[0]
        require(edge not in exceptional, "ordinary row on exceptional edge")
        expected = {edge | pair: 1 for pair in subsets(ground - edge, 2)}
        expected[edge] = -4
        low, high = 0, 1
    elif kind in (Kind.ORDINARY_FLAG, Kind.PRIVATE_FLAG):
        require(len(negative) == 1 and len(negative[0]) == 4 and len(positive) == 3, "flag support sizes")
        tetra = negative[0]
        center = frozenset.intersection(*positive)
        require(len(center) == 1 and center <= tetra, "flag center")
        v = next(iter(center))
        require(v in private if kind == Kind.PRIVATE_FLAG else v not in private | {0},
                "flag used at unclassified/common root link")
        expected = {center | edge: 1 for edge in subsets(tetra - center, 2)}
        expected[tetra] = -1
        low, high = -1, 2
    elif kind == Kind.PRIVATE_ORDER:
        center = frozenset.intersection(*terms)
        require(len(center) == 1 and next(iter(center)) in private, "private degree center")
        expected = {center | {v}: 1 for v in ground - center}
        low, high = 9, 11
    else:
        domain = frozenset().union(*terms)
        require(kind == Kind.INDEPENDENCE and len(domain) == 3, "independence domain")
        expected = {edge: 1 for edge in subsets(domain, 2)}
        low, high = 1, 3
    require(terms == expected and (row["lower"], row["upper"]) == (low, high),
            f"row is not the necessary {kind.value} formula")
    return kind.value


def interval(row, fixed):
    validate_row(row)
    require(all(type(v) is int and type(x) is int and x in (0, 1) for v, x in fixed.items()),
            "nonbinary assignment")
    # Center/radius derivation differs from the predecessor's termwise min/max code.
    center = radius = 0
    for v, coefficient in row["terms"]:
        if v in fixed:
            center += 2*coefficient*fixed[v]
        else:
            center += coefficient
            radius += abs(coefficient)
    require((center-radius) % 2 == 0 and (center+radius) % 2 == 0, "interval parity")
    return (center-radius)//2, (center+radius)//2


def contradictory(row, bounds):
    return bounds[1] < row["lower"] or bounds[0] > row["upper"]


def replay(rows, steps, terminal):
    for row in rows:
        validate_row(row)
    require(type(terminal) is int and 0 <= terminal < len(rows), "terminal index")
    fixed = {}
    for step in steps:
        require(isinstance(step, dict) and set(step) == {"variable", "value", "row"}, "step schema")
        variable, value, rid = step["variable"], step["value"], step["row"]
        require(type(variable) is int and type(value) is int and type(rid) is int,
                "step fields must be integers")
        require(value in (0, 1) and variable not in fixed and 0 <= rid < len(rows), "step domain/order")
        row = rows[rid]
        require(variable in dict(row["terms"]), "step variable absent from reason")
        opposite = {**fixed, variable: 1-value}
        require(contradictory(row, interval(row, opposite)), "opposite value not contradicted")
        fixed[variable] = value
    final = interval(rows[terminal], fixed)
    require(contradictory(rows[terminal], final), "terminal row is not contradictory")
    return {"deductions": len(fixed), "final_interval": list(final),
            "allowed_interval": [rows[terminal]["lower"], rows[terminal]["upper"]]}


def check_cover(cases, roots):
    expected = {(r["order"], r["index"]): r for r in roots}
    require(len(expected) == len(roots), "duplicated inherited root")
    keys = [(c["link"]["order"], c["link"]["index"]) for c in cases]
    require(len(keys) == len(set(keys)) and set(keys) == set(expected), "missing/duplicated root case")
    for case, key in zip(cases, keys):
        require(case["link"] == expected[key], "root labels differ from inherited literal cover")
    return True


def cross_degree_controls():
    # Nine good minima 2; private endpoint minima 1 each; common minimum 2.
    minima = [2]*9 + [1, 1, 2]
    lower = (sum(minima)+1)//2
    # One universal cross-neighbor has six edges; the other five vertices
    # on its side each need an edge not incident to it.
    universal_lower = 6+5
    upper = [49+c - (12+2*15) for c in range(4)]
    require(all(m < lower and m < universal_lower for m in upper), "cross-edge contradiction lost")
    moments = []
    for c in range(4):
        b = (13*8 - 2*(16-c))//2
        a = 16-c-b
        edges = (a+6*b)//4
        moments.append({"c": c, "quadratic_sum": a, "tetrahedra": b,
                        "edges": edges, "triangles": 2*b})
        require((b, edges, 2*b) == (36+c, 49+c, 72+2*c), "face-vector arithmetic")
    return {"good_vertices": 9, "private_vertices": 2, "common_vertices": 1,
            "minimum_if_nine_good_at_least_two": lower,
            "universal_neighbor_minimum": universal_lower,
            "cross_upper_by_constant": upper, "moments": moments}


def pin(path, expected):
    path = Path(path).resolve()
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    require(digest == expected, f"source digest mismatch: {path}")
    return {"path": str(path), "sha256": digest, "bytes": len(data)}


def run():
    started = time.process_time()
    bindings = [pin(HANDOFF, HANDOFF_SHA), pin(OLD_AUTHORITY, OLD_AUTHORITY_SHA)]
    handoff = json.loads(HANDOFF.read_text())
    for ref in handoff["sources"]:
        actual = pin(ref["path"], ref["sha256"])
        require(type(ref["bytes"]) is int and ref["bytes"] == actual["bytes"], "source byte length")
        bindings.append(actual)
    files = {Path(r["path"]).name: Path(r["path"]) for r in handoff["sources"]}
    inherited = json.loads(files["two-adjacent-negative-cubic-independent-verification.json"].read_text())
    require(inherited["status"] == "VERIFIED_TWO_ADJACENT_NEGATIVE_CUBIC_ORDINARY_DERIVATIVE_EXCLUSION",
            "inherited report not accepted")
    require(inherited["global_face_count_rows_used"] == 0 and inherited["constant_independent_selected_rows"] is True,
            "inherited constant independence claim missing")
    # This accepted report supplies completeness; its target catalogs are not traversed.
    cover_name = "d10-normalization-spheres-independent-verification.json"
    cover_refs = [r for r in inherited["dependencies"] if Path(r["path"]).name == cover_name]
    require(len(cover_refs) == 1, "complete sphere-cover dependency")
    bindings.append(pin(cover_refs[0]["path"], cover_refs[0]["sha256"]))
    compact = json.loads(files["two-negative-cubic-ordinary-compact-proofs.json"].read_text())
    cases = compact["cases"]
    check_cover(cases, inherited["root_link_types"])
    require(len(cases) == 9, "expected complete nine-case cover")
    counts = Counter()
    reports = []
    for case in cases:
        root = check_root(case["link"])
        require(case["constant"] == 1 and case["uses_global_face_count"] is False,
                "compact source metadata")
        require(case["status"] == "EXACT_INTERVAL_CONTRADICTION", "compact case status")
        for row in case["rows"]:
            counts[recognize(row, case["link"])] += 1
        result = replay(case["rows"], case["steps"], case["contradiction_row"])
        result.update({"root": root, "literal_rows": len(case["rows"]),
                       "row_SHA256": hashlib.sha256(json.dumps(case["rows"], sort_keys=True).encode()).hexdigest()})
        reports.append(result)
    require(dict(counts) == inherited["selected_row_reasons"], "fresh semantic-family counts")
    require(sum(counts.values()) == 945 and sum(r["deductions"] for r in reports) == 1111,
            "fresh retained-proof totals")
    return {"schema_version": 1, "status": "PASS_INDEPENDENT_RETAINED_ROW_RECOGNITION_AND_REPLAY",
            "author": "Alexander Richard Towell", "AI_assistance": "Substantial OpenAI Codex independent review; no human/formal claim.",
            "bindings": bindings, "cases": reports, "row_families": dict(sorted(counts.items())),
            "literal_rows": sum(counts.values()), "deductions": sum(r["deductions"] for r in reports),
            "structural_arithmetic": cross_degree_controls(),
            "new_constants": [0, 3], "unchanged_old_constants": [1, 2],
            "retained_global_count_rows": 0, "full_model_constructed": False,
            "old_original_row_indices_used_as_mathematical_premises": False,
            "complete_sphere_cover_inherited_not_reenumerated": True,
            "opposite_value_replay_active_under_optimization": True,
            "old_verifier_imported_or_executed": False, "target_queries": 0,
            "limits": {"CPU_seconds": 5, "wall_seconds": 15, "address_space_bytes": 512*1024*1024},
            "CPU_seconds": time.process_time()-started, "global_goal_complete": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    signal.alarm(15)
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"status": result["status"], "rows": result["literal_rows"],
                      "deductions": result["deductions"], "CPU_seconds": result["CPU_seconds"]}))


if __name__ == "__main__":
    main()
