"""Bounded, constant-independent exact case splits for mixed fixed points."""
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
import argparse
import json
import time

from disjoint_mixed_degree_seven import HERE, bind, strengthened_instance
from binary_branch_certificates import solve, verify
from one_six_edge_compact_proofs import compact
from negative_free_complex import Row


def compact_tree(rows, tree):
    if tree["status"] == "EXACT_INTERVAL_CONTRADICTION":
        full_rows = rows + [Row(((v, 1),), value, value, "branch_assumption")
                            for v, value in tree["assumptions"]]
        chosen, proof = compact(full_rows, tree)
        proof.update(rows=[asdict(row) for row in chosen], assumptions=tree["assumptions"])
        return proof
    if tree["status"] == "EXACT_BRANCH_CONTRADICTION":
        return {"status": tree["status"], "variable": tree["variable"],
                "assumptions": tree["assumptions"],
                "zero": compact_tree(rows, tree["zero"]), "one": compact_tree(rows, tree["one"])}
    return tree


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--case-seconds", type=float, default=15)
    parser.add_argument("--nodes", type=int, default=31)
    args = parser.parse_args()
    assert 0 < args.seconds <= 180 and 0 < args.case_seconds <= 60 and 1 <= args.nodes <= 255
    cover_path = HERE / "disjoint-cubic-root-link-cover.json"
    original_path = HERE / "disjoint-cubic-ordinary-full-interval-probe.json"
    target = HERE / "disjoint-mixed-constant-independent-branch-proofs.json"
    covers = json.loads(cover_path.read_text())["covers"]
    pending = [row for row in json.loads(original_path.read_text())["cases"]
               if row["second_value"] == 1 and row["status"] == "INTERVAL_FIXED_POINT_INCONCLUSIVE"]
    sources = [bind(path) for path in (Path(__file__), cover_path, original_path,
              HERE / "disjoint_mixed_degree_seven.py", HERE / "binary_branch_certificates.py",
              HERE / "exact_binary_gap_propagation.py")]
    if target.exists():
        result = json.loads(target.read_text())
        assert result["sources"] == sources
    else:
        result = {"status": "RUNNING", "global_goal": "OPEN", "sources": sources,
                  "scope": "Necessary local ordinary-coefficient models. No global face-count rows. Independent row/branch replay pending.",
                  "constants": [1, 2], "cases": [], "runs": []}
    for old, expected in zip(result["cases"], pending):
        assert (old["root_index"], old["second_pair"]) == (expected["root_index"], expected["second_pair"])
    started = time.monotonic()
    first = len(result["cases"])
    for original in pending[first:]:
        if time.monotonic() - started >= args.seconds:
            break
        model = strengthened_instance(covers[original["root_index"]], original["second_pair"], 1)
        model.rows = [row for row in model.rows if row.reason != "face_count"]
        proof = solve(model.rows, max_nodes=args.nodes, seconds=args.case_seconds)
        verify(model.rows, proof)
        proof["tree"] = compact_tree(model.rows, proof["tree"])
        proof.update(root_index=original["root_index"], second_pair=original["second_pair"], second_value=1,
                     row_digest=sha256(json.dumps([asdict(row) for row in model.rows], sort_keys=True).encode()).hexdigest(),
                     uses_global_face_count=False)
        result["cases"].append(proof)
        target.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({k: v for k, v in proof.items() if k != "tree"}), flush=True)
    result["runs"].append({"first_case": first, "after_last_case": len(result["cases"]),
                           "seconds": time.monotonic() - started, "budget_seconds": args.seconds})
    result.update(status="COMPLETE_BOUNDED_BRANCH_PROBES" if len(result["cases"]) == len(pending)
                  else "TERMINAL_BOUNDED_PARTIAL_PROBES", untested=len(pending) - len(result["cases"]))
    target.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
