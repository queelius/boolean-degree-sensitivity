"""Extract exact small contradictions, retaining literal authoritative case keys."""
from dataclasses import asdict
import argparse
import json
from pathlib import Path
import time

from disjoint_cubic_complex import HERE, PARENT, bind, instance
from one_six_edge_compact_proofs import compact
from exact_binary_row_propagation import replay


def extract(cover, original, builder=instance):
    model = builder(cover, original["second_pair"], original["second_value"], 1)
    rows, proof = compact(model.rows, original)
    alternative = builder(cover, original["second_pair"], original["second_value"], 2)
    selected_alternative = [alternative.rows[index] for index in proof["original_row_indices"]]
    constant_independent = rows == selected_alternative
    if constant_independent:
        replay(selected_alternative, proof)
    proof.update(root_index=original["root_index"], second_pair=original["second_pair"],
                 second_value=original["second_value"], root_link=cover["link"],
                 first_exception=cover["first_exception"], rows=[asdict(row) for row in rows],
                 constants=[1, 2] if constant_independent else [1],
                 uses_global_face_count=any(row.reason == "face_count" for row in rows))
    return proof


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=120)
    args = parser.parse_args()
    assert 0 < args.seconds <= 180
    original_path = HERE / "disjoint-cubic-ordinary-full-interval-probe.json"
    cover_path = HERE / "disjoint-cubic-root-link-cover.json"
    target = HERE / "disjoint-cubic-ordinary-compact-proofs.json"
    original = json.loads(original_path.read_text())
    assert original["status"] == "COMPLETE_INTERVAL_PROBES"
    cases = [case for case in original["cases"] if case["status"] == "EXACT_INTERVAL_CONTRADICTION"]
    covers = json.loads(cover_path.read_text())["covers"]
    sources = [bind(path) for path in (Path(__file__), original_path, cover_path,
        HERE / "disjoint_cubic_complex.py", HERE / "two_mixed_cubic_complex.py",
        PARENT / "negative_free_complex.py", PARENT / "one_six_edge_compact_proofs.py",
        PARENT / "exact_binary_row_propagation.py")]
    if target.exists():
        result = json.loads(target.read_text())
        assert result["sources"] == sources
    else:
        result = {"status": "RUNNING", "global_goal": "OPEN", "sources": sources,
                  "scope": "Compact contradictions only; independent row audit pending.",
                  "authoritative_case_key": ["root_index", "second_pair", "second_value"],
                  "cases": [], "runs": []}
    for record, case in zip(result["cases"], cases):
        assert all(record[key] == case[key] for key in result["authoritative_case_key"])
    started = time.monotonic()
    first = len(result["cases"])
    for original in cases[first:]:
        if time.monotonic() - started > args.seconds:
            break
        proof = extract(covers[original["root_index"]], original)
        result["cases"].append(proof)
        target.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"root": proof["root_index"], "pair": proof["second_pair"],
                          "sign": proof["second_value"], "rows": len(proof["rows"]),
                          "steps": len(proof["steps"]), "constants": proof["constants"]}), flush=True)
    result["runs"].append({"first_case": first, "after_last_case": len(result["cases"]),
                           "seconds": time.monotonic() - started, "budget_seconds": args.seconds})
    result.update(status="COMPLETE_COMPACT_CONTRADICTIONS_AUDIT_PENDING" if len(result["cases"]) == len(cases)
                  else "TERMINAL_BOUNDED_PARTIAL_EXPORT", unexported=len(cases) - len(result["cases"]))
    target.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
