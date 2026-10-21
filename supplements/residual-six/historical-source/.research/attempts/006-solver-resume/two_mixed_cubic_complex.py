"""Exact necessary local models for adjacent +1/-2 quadratic numerators."""
from dataclasses import asdict
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import sys
import time

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "009-parent-analysis"
sys.path.insert(0, str(PARENT))
from negative_free_complex import build, closure, masks
from exact_binary_row_propagation import propagate, replay


def bind(path):
    return {"path": str(path), "sha256": sha256(path.read_bytes()).hexdigest()}


def link_types():
    records, sources = [], []
    for n in range(6, 13):
        source = HERE / f"sphere-triangulations-{n:02d}.json"
        data = json.loads(source.read_text())
        assert data["status"] == "COMPLETE_INVERSE_CONTRACTION_COVER" and data["order"] == n
        sources.append(bind(source))
        for row in data["classes"]:
            edges = {sum(1 << v for v in pair) for face in row["face_masks"]
                     for pair in combinations([v for v in range(n) if face >> v & 1], 2)}
            degrees = [sum(edge >> v & 1 for edge in edges) for v in range(n)]
            if degrees.count(3) == degrees.count(6) == 1 and set(degrees) <= {3, 4, 5, 6}:
                records.append({"order": n, "index": row["index"], "face_masks": row["face_masks"],
                                "degree_vector": degrees,
                                "positive_vertex": degrees.index(3), "negative_vertex": degrees.index(6)})
    return records, sources


def valence_model(n, edge_count, root_link, exceptional_valences, all_euler=True):
    assert all(e.bit_count() == 2 and e < 1 << n and v in (3, 6)
               for e, v in exceptional_valences.items())
    data = build(n, edge_count, 0, root_link, all_euler=all_euler)
    data.rows = [row for row in data.rows if row.reason != "edge_four_or_five"]
    edges, tetrahedra = masks(n, 2), masks(n, 4)
    bad_vertices = {v for e in exceptional_valences for v in range(n) if e >> v & 1}
    for e in edges:
        incident = {q: 1 for q in tetrahedra if q & e == e}
        if e in exceptional_valences:
            data.add({e: 1}, 1, 1, "exceptional_edge_present")
            valence = exceptional_valences[e]
            data.add(incident, valence, valence, "exceptional_edge_valence")
        else:
            data.add({**incident, e: -4}, 0, 1, "ordinary_edge_four_or_five")
    for q in tetrahedra:
        vertices = [v for v in range(n) if q >> v & 1]
        for v in vertices:
            if v in bad_vertices:
                continue
            terms = {q ^ (1 << w): 1 for w in vertices if w != v}
            terms[q] = -1
            data.add(terms, -1, 2, "ordinary_vertex_link_flag")
    if all_euler:
        for triple in combinations(range(n), 3):
            data.add({sum(1 << v for v in pair): 1 for pair in combinations(triple, 2)},
                     1, 3, "no_independent_triple")
    return data


def instance(link, constant):
    plus, minus = link["positive_vertex"] + 1, link["negative_vertex"] + 1
    root_link = tuple(face << 1 for face in link["face_masks"])
    data = valence_model(13, 49 + constant, root_link, {1 | 1 << plus: 3, 1 | 1 << minus: 6})
    edges, tetrahedra = masks(13, 2), masks(13, 4)
    for v in range(13):
        lower, upper = (9, 11) if v == minus else ((7, 10) if v == plus else (6, 12))
        data.add({e: 1 for e in edges if e >> v & 1}, lower, upper, "vertex_link_order")
    for q in tetrahedra:
        if q >> minus & 1:
            terms = {q ^ (1 << v): 1 for v in range(13) if q >> v & 1 and v != minus}
            terms[q] = -1
            data.add(terms, -1, 2, "negative_private_endpoint_flag")
    return data


def main():
    target = HERE / "two-mixed-cubic-ordinary-interval-probe.json"
    assert not target.exists(), "preserve completed probe"
    links, sources = link_types()
    result = {"status": "RUNNING", "global_status": "UNRESOLVED",
              "scope": "Necessary local models; independent mathematical and literal row audit required.",
              "sources": sources + [bind(path) for path in (Path(__file__),
                  HERE / "two-mixed-cubic-derivative.md", PARENT / "negative_free_complex.py",
                  PARENT / "exact_binary_row_propagation.py")],
              "link_types": links, "cases": []}
    for link in links:
        for constant in (1, 2):
            start = time.monotonic()
            data = instance(link, constant)
            proof = propagate(data.rows)
            replay(data.rows, proof)
            proof.update(link_order=link["order"], link_index=link["index"], constant=constant,
                         row_count=len(data.rows),
                         row_digest=sha256(json.dumps([asdict(row) for row in data.rows], sort_keys=True).encode()).hexdigest(),
                         seconds=time.monotonic() - start)
            result["cases"].append(proof)
            target.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps({key: value for key, value in proof.items() if key != "steps"}), flush=True)
    result["status"] = "TERMINAL_EXACT_INTERVAL_PROBE"
    target.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
