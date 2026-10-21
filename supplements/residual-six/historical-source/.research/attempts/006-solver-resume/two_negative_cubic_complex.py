"""Necessary models for two adjacent valence-six edges, with proof traces."""
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
from exact_binary_row_propagation import propagate, replay
from one_six_edge_complex import six_edge_model
from negative_free_complex import masks


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
            if degrees.count(6) == 2 and set(degrees) <= {4, 5, 6}:
                records.append({"order": n, "index": row["index"], "face_masks": row["face_masks"],
                                "degree_vector": degrees,
                                "exceptional_vertices": [v for v, degree in enumerate(degrees) if degree == 6]})
    return records, sources


def instance(link, constant):
    endpoints = [v + 1 for v in link["exceptional_vertices"]]
    root_link = tuple(face << 1 for face in link["face_masks"])
    data = six_edge_model(13, 49 + constant, root_link,
                          {1 | (1 << v) for v in endpoints}, exceptional_links_flag=False)
    for vertex in endpoints:
        data.add({edge: 1 for edge in masks(13, 2) if edge >> vertex & 1},
                 9, 11, "private_endpoint_one_six_link_order")
        for tetrahedron in masks(13, 4):
            if not tetrahedron >> vertex & 1:
                continue
            faces = {tetrahedron ^ (1 << v): 1 for v in range(13)
                     if tetrahedron >> v & 1 and v != vertex}
            faces[tetrahedron] = -1
            data.add(faces, -1, 2, "private_endpoint_one_six_link_flag")
    return data


def main():
    target = HERE / "two-negative-cubic-ordinary-interval-probe.json"
    assert not target.exists(), "preserve completed probe"
    links, sources = link_types()
    result = {"status": "RUNNING", "global_status": "UNRESOLVED",
              "scope": "Necessary local derivative models. Contradictions require independent model and coverage audit.",
              "link_types": links, "sources": sources + [bind(path) for path in
                  (Path(__file__), HERE / "two-negative-cubic-ordinary-derivative.md",
                   PARENT / "one_six_edge_complex.py", PARENT / "negative_free_complex.py",
                   PARENT / "exact_binary_row_propagation.py")], "cases": []}
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
