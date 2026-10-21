"""Extract literal necessary rows from the nine interval contradictions."""
from dataclasses import asdict
from pathlib import Path
from hashlib import sha256
import json

from two_negative_cubic_complex import HERE, PARENT, instance
from one_six_edge_compact_proofs import compact


def bind(path):
    return {"path": str(path), "sha256": sha256(path.read_bytes()).hexdigest()}


def build():
    source = HERE / "two-negative-cubic-ordinary-interval-probe.json"
    original = json.loads(source.read_text())
    result = {"status": "NINE_EXACT_COMPACT_CONTRADICTIONS_RECONSTRUCTION_PENDING",
              "scope": "Proposed local adjacent-two-negative-pair derivative exclusion; mathematical coverage and independent row rebuild are separate.",
              "sources": [bind(path) for path in (source, Path(__file__),
                  HERE / "two_negative_cubic_complex.py", HERE / "two-negative-cubic-ordinary-derivative.md",
                  PARENT / "one_six_edge_compact_proofs.py", PARENT / "exact_binary_row_propagation.py")],
              "cases": []}
    for link in original["link_types"]:
        model = instance(link, 1)
        source_case = next(row for row in original["cases"]
                           if row["link_order"] == link["order"] and
                           row["link_index"] == link["index"] and row["constant"] == 1)
        rows, proof = compact(model.rows, source_case)
        proof.update(link=link, constant=1, rows=[asdict(row) for row in rows],
                     uses_global_face_count=any(row.reason == "face_count" for row in rows))
        result["cases"].append(proof)
    return result


if __name__ == "__main__":
    result = build()
    (HERE / "two-negative-cubic-ordinary-compact-proofs.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"cases": len(result["cases"]),
                      "rows": sum(len(row["rows"]) for row in result["cases"]),
                      "steps": sum(len(row["steps"]) for row in result["cases"]),
                      "global_face_count_used": sum(row["uses_global_face_count"] for row in result["cases"])}))
