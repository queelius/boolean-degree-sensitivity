"""Sharper necessary rows from the complete one-degree-three sphere filter.

This is a new model wrapper.  Earlier probes and their source remain unchanged.
"""
from dataclasses import asdict
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import time

from disjoint_cubic_complex import HERE, bind, instance
from negative_free_complex import masks
from exact_binary_row_propagation import propagate, replay


def positive_link_types():
    result = []
    for n in range(6, 13):
        source = json.loads((HERE / f"sphere-triangulations-{n:02d}.json").read_text())
        assert source["status"] == "COMPLETE_INVERSE_CONTRACTION_COVER" and source["order"] == n
        for row in source["classes"]:
            edges = {sum(1 << v for v in pair) for face in row["face_masks"]
                     for pair in combinations([v for v in range(n) if face >> v & 1], 2)}
            degrees = [sum(edge >> v & 1 for edge in edges) for v in range(n)]
            if degrees.count(3) == 1 and all(d in (3, 4, 5) for d in degrees):
                result.append({"order": n, "index": row["index"], "degree_vector": degrees})
    return result


def strengthened_instance(cover, second_pair, constant):
    model = instance(cover, second_pair, 1, constant)
    # The independently complete sphere cover yields only order seven.
    for vertex in range(13):
        if second_pair >> vertex & 1:
            model.add({edge: 1 for edge in masks(13, 2) if edge >> vertex & 1},
                      7, 7, "positive_endpoint_exact_order")
    return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=120)
    args = parser.parse_args()
    assert 0 < args.seconds <= 180
    cover_path = HERE / "disjoint-cubic-root-link-cover.json"
    prior_path = HERE / "disjoint-cubic-ordinary-full-interval-probe.json"
    target = HERE / "disjoint-mixed-degree-seven-interval-probe.json"
    covers = json.loads(cover_path.read_text())["covers"]
    previous = json.loads(prior_path.read_text())
    assert previous["status"] == "COMPLETE_INTERVAL_PROBES"
    pending = [row for row in previous["cases"]
               if row["second_value"] == 1 and row["status"] == "INTERVAL_FIXED_POINT_INCONCLUSIVE"]
    links = positive_link_types()
    assert len(links) == 1 and links[0]["order"] == 7
    sources = [bind(path) for path in (Path(__file__), cover_path, prior_path,
               HERE / "disjoint_cubic_complex.py", HERE / "two_mixed_cubic_complex.py",
               HERE / "independent-math-audit/disjoint-cubic-root-link-cover-independent-verification.json")]
    sources += [bind(HERE / f"sphere-triangulations-{n:02d}.json") for n in range(6, 13)]
    if target.exists():
        result = json.loads(target.read_text())
        assert result["sources"] == sources
    else:
        result = {"status": "RUNNING", "global_goal": "OPEN", "sources": sources,
                  "scope": "Necessary local models; independent compact-row reconstruction is pending.",
                  "positive_link_types": links, "cases": [], "runs": []}
    for old, expected in zip(result["cases"], pending):
        assert (old["root_index"], old["second_pair"]) == (expected["root_index"], expected["second_pair"])
    tick = time.monotonic()
    first = len(result["cases"])
    for original in pending[first:]:
        if time.monotonic() - tick >= args.seconds:
            break
        started = time.monotonic()
        model = strengthened_instance(covers[original["root_index"]], original["second_pair"], 1)
        proof = propagate(model.rows)
        replay(model.rows, proof)
        proof.update(root_index=original["root_index"], second_pair=original["second_pair"],
                     second_value=1, constant=1, original_case_index=original["case_index"],
                     row_digest=sha256(json.dumps([asdict(x) for x in model.rows], sort_keys=True).encode()).hexdigest(),
                     rows=len(model.rows), seconds=time.monotonic() - started)
        result["cases"].append(proof)
        target.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({k: v for k, v in proof.items() if k != "steps"}), flush=True)
    result["runs"].append({"first_case": first, "after_last_case": len(result["cases"]),
                           "seconds": time.monotonic() - tick, "budget_seconds": args.seconds})
    result.update(status="COMPLETE_DEGREE_SEVEN_INTERVAL_PROBES" if len(result["cases"]) == len(pending)
                  else "TERMINAL_BOUNDED_PARTIAL_PROBES", untested=len(pending) - len(result["cases"]))
    target.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
