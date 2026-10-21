"""Extract two short exact contradictions from the mixed-cubic probe."""
from dataclasses import asdict
from hashlib import sha256
import json

from two_mixed_cubic_complex import HERE, PARENT, instance
from one_six_edge_compact_proofs import compact


def build():
    source = HERE / "two-mixed-cubic-ordinary-interval-probe.json"
    original = json.loads(source.read_text())
    sources = (source, HERE / "compact_two_mixed_cubic.py", HERE / "two_mixed_cubic_complex.py",
               HERE / "two-mixed-cubic-derivative.md", PARENT / "one_six_edge_compact_proofs.py",
               PARENT / "exact_binary_row_propagation.py")
    result = {"status": "TWO_EXACT_COMPACT_CONTRADICTIONS_AUDIT_PENDING",
              "sources": [{"path": str(p), "sha256": sha256(p.read_bytes()).hexdigest()} for p in sources],
              "global_goal": "OPEN", "cases": []}
    for link in original["link_types"]:
        data = instance(link, 1)
        full = next(x for x in original["cases"] if x["constant"] == 1 and
                    x["link_order"] == link["order"] and x["link_index"] == link["index"])
        rows, proof = compact(data.rows, full)
        proof.update(link=link, constant=1, rows=[asdict(row) for row in rows],
                     uses_global_face_count=any(row.reason == "face_count" for row in rows))
        result["cases"].append(proof)
    return result


if __name__ == "__main__":
    result = build()
    (HERE / "two-mixed-cubic-ordinary-compact-proofs.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"cases": len(result["cases"]),
                      "rows": sum(len(x["rows"]) for x in result["cases"]),
                      "steps": sum(len(x["steps"]) for x in result["cases"]),
                      "global_face_count_used": sum(x["uses_global_face_count"] for x in result["cases"])}))
