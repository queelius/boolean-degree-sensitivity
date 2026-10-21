"""Small exact checks for the proposed two-positive quadratic derivative lemma."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def cycle_data(cycle):
    n = len(cycle)
    edge = lambda x, y: (1 << x) | (1 << y)
    return {"cycle": list(cycle),
            "edges": {edge(cycle[i], cycle[(i + 1) % n]) for i in range(n)},
            "boundary": {edge(cycle[i], cycle[(i + 2) % n]) for i in range(n)},
            "faces": {sum(1 << cycle[(i + j) % n] for j in range(3)) for i in range(n)}}


def roots(n):
    boundary = cycle_data(tuple(range(n)))["boundary"]
    answer = []
    for tail in permutations(range(1, n)):
        if tail[0] > tail[-1]:
            continue
        data = cycle_data((0,) + tail)
        if data["boundary"] == boundary:
            answer.append(data)
    return answer


def root_controls():
    report = []
    for n in (7, 8, 9):
        group = roots(n)
        histogram = Counter()
        allowed = []
        for left in group:
            for right in group:
                common = left["faces"] & right["faces"]
                exceptional = []
                for face in common:
                    contained = [edge for edge in left["boundary"] if edge & face == edge]
                    assert len(contained) == 1
                    exceptional += contained
                assert len(set(exceptional)) == len(exceptional)
                shared_edges = len(left["edges"] & right["edges"])
                histogram[len(common), shared_edges] += 1
                if len(common) <= 2:
                    assert n == 8 and shared_edges <= 4
                    allowed.append(shared_edges)
        report.append({"vertices": n, "roots": len(group),
                       "ordered_root_pairs": len(group) ** 2,
                       "common_face_edge_histogram": [{"faces": k[0], "edges": k[1], "count": v}
                                                       for k, v in sorted(histogram.items())],
                       "pairs_with_at_most_two_common_faces": len(allowed),
                       "maximum_shared_edges_in_allowed_pairs": max(allowed, default=None)})
    return report


def pentagon_controls():
    diagonals = [pair for pair in combinations(range(5), 2)
                 if (pair[1] - pair[0]) not in (1, 4)]
    def crosses(first, second):
        if set(first) & set(second):
            return False
        a, b = first
        c, d = second
        return ((a < c < b) != (a < d < b))
    pairs = list(combinations(diagonals, 2))
    noncrossing = [pair for pair in pairs if not crosses(*pair)]
    disjoint = [pair for pair in noncrossing if not set(pair[0]) & set(pair[1])]
    assert noncrossing and not disjoint
    return {"diagonal_pairs": len(pairs), "noncrossing_positive_controls": len(noncrossing),
            "noncrossing_disjoint_pairs": len(disjoint)}


def cross_edge_controls():
    # Count lower bounds only; no hidden enumeration of potential manifolds.
    # The residual degree cost may be concentrated at the common bad vertex.
    records = []
    for adjacent in (False, True):
        good = 9 if adjacent else 8
        singly_bad = 2 if adjacent else 4
        minimum_twice_cross_edges = 2 * good + singly_bad
        assert minimum_twice_cross_edges > 18
        after_universal = 4 if adjacent else 5
        assert 6 + after_universal > 9
        records.append({"adjacent_exceptions": adjacent,
                        "minimum_cross_degree_if_no_good_degree_one": minimum_twice_cross_edges,
                        "cross_edge_lower_bound_after_universal": 6 + after_universal})
    assert 37 + 14 > 48 + 2
    return records


def build():
    return {"status": "CANDIDATE_LOCAL_THEOREM_FINITE_CONTROLS",
            "cycle_roots": root_controls(), "six_vertex_link_obstruction": pentagon_controls(),
            "cross_degree_arithmetic": cross_edge_controls(),
            "scope": "Small finite ingredients only; independent mathematical audit and inherited catalog binding are separate."}


if __name__ == "__main__":
    result = build()
    (HERE / "two-positive-cubic-controls.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
