"""Complete marked root-link coverage for two disjoint cubic exceptions."""
from dataclasses import asdict
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import time

from two_mixed_cubic_complex import HERE, PARENT, bind, valence_model
from negative_free_complex import masks
from exact_binary_row_propagation import propagate, replay


def mapped(mask, permutation):
    return sum(1 << permutation[v] for v in range(len(permutation)) if mask >> v & 1)


def automorphisms(n, faces):
    faces = frozenset(faces)
    edges = {sum(1 << v for v in pair) for face in faces
             for pair in combinations([v for v in range(n) if face >> v & 1], 2)}
    degrees = [sum(e >> v & 1 for e in edges) for v in range(n)]
    blocks = [[v for v in range(n) if degrees[v] == d] for d in sorted(set(degrees))]
    result = []
    for choices in product(*(permutations(block) for block in blocks)):
        permutation = list(range(n))
        for block, images in zip(blocks, choices):
            for v, image in zip(block, images):
                permutation[v] = image
        if all(mapped(e, permutation) in edges for e in edges) and {mapped(f, permutation) for f in faces} == faces:
            result.append(tuple(permutation))
    assert tuple(range(n)) in result
    return result


def source_links():
    links, sources = [], []
    for n in range(6, 13):
        path = HERE / f"sphere-triangulations-{n:02d}.json"
        source = json.loads(path.read_text())
        assert source["status"] == "COMPLETE_INVERSE_CONTRACTION_COVER" and source["order"] == n
        sources.append(bind(path))
        for row in source["classes"]:
            edges = {sum(1 << v for v in pair) for f in row["face_masks"]
                     for pair in combinations([v for v in range(n) if f >> v & 1], 2)}
            degrees = [sum(e >> v & 1 for e in edges) for v in range(n)]
            if degrees.count(6) == 1 and set(degrees) <= {4, 5, 6}:
                links.append({"order": n, "index": row["index"], "face_masks": row["face_masks"],
                              "degree_vector": degrees, "negative_vertex": degrees.index(6)})
    return links, sources


def marked_cover(link):
    n = link["order"]
    root_link = {f << 1 for f in link["face_masks"]}
    group = []
    for local in automorphisms(n, link["face_masks"]):
        for outside in permutations(range(n + 1, 13)):
            perm = [0] + [v + 1 for v in local] + list(outside)
            assert sorted(perm) == list(range(13))
            assert {mapped(f, perm) for f in root_link} == root_link
            group.append(perm)
    first = 1 | (1 << (link["negative_vertex"] + 1))
    available = [v for v in range(13) if not first >> v & 1]
    records, representatives = [], {}
    for pair in combinations(available, 2):
        mask = sum(1 << v for v in pair)
        best, witness = min((mapped(mask, perm), perm) for perm in group)
        if best not in representatives:
            representatives[best] = len(representatives)
        records.append({"pair": mask, "representative_pair": best,
                        "class_index": representatives[best], "permutation": witness})
    assert len(records) == 55
    return {"link": link, "first_exception": first, "group_order": len(group),
            "second_pairs": sorted(representatives), "coverage": records}


def instance(cover, second, second_value, constant):
    assert second in cover["second_pairs"] and second_value in (-2, 1)
    first = cover["first_exception"]
    assert first & second == 0
    link = cover["link"]
    specs = {first: 6, second: 6 if second_value == -2 else 3}
    data = valence_model(13, 49 + constant, tuple(f << 1 for f in link["face_masks"]), specs)
    negative = {v for e, valence in specs.items() if valence == 6 for v in range(13) if e >> v & 1}
    positive = {v for e, valence in specs.items() if valence == 3 for v in range(13) if e >> v & 1}
    edges, tetrahedra = masks(13, 2), masks(13, 4)
    for v in range(13):
        lower, upper = (9, 11) if v in negative else ((7, 10) if v in positive else (6, 12))
        data.add({e: 1 for e in edges if e >> v & 1}, lower, upper, "vertex_link_order")
    for v in sorted(negative):
        for q in tetrahedra:
            if q >> v & 1:
                terms = {q ^ (1 << w): 1 for w in range(13) if q >> w & 1 and w != v}
                terms[q] = -1
                data.add(terms, -1, 2, "negative_endpoint_flag")
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--limit", type=int, default=6)
    args = parser.parse_args()
    links, sources = source_links()
    covers = [marked_cover(link) for link in links]
    cover_path = HERE / "disjoint-cubic-root-link-cover.json"
    cover = {"status": "COMPLETE_CANDIDATE_MARKED_ROOT_COVER", "covers": covers,
             "sources": sources + [bind(Path(__file__)), bind(HERE / "disjoint-cubic-local-reduction.md")]}
    if cover_path.exists():
        assert json.loads(cover_path.read_text()) == cover
    else:
        cover_path.write_text(json.dumps(cover, indent=2) + "\n")
    print(json.dumps({"types": len(covers), "marked_pairs": [len(x["second_pairs"]) for x in covers],
                      "literal_pairs": sum(len(x["coverage"]) for x in covers)}), flush=True)
    if not args.probe:
        return
    path = HERE / f"disjoint-cubic-interval-pilot-{args.limit}.json"
    assert not path.exists(), "preserve completed probe"
    output = {"status": "RUNNING", "scope": "Necessary ordinary-coefficient local models only; no coverage or row audit yet.",
              "sources": [bind(cover_path), bind(Path(__file__)), bind(HERE / "two_mixed_cubic_complex.py")], "cases": []}
    cases = [(i, second, value) for i, c in enumerate(covers) for second in c["second_pairs"] for value in (-2, 1)]
    for index, (i, second, value) in enumerate(cases[:args.limit]):
        start = time.monotonic()
        data = instance(covers[i], second, value, 1)
        proof = propagate(data.rows)
        replay(data.rows, proof)
        proof.update(case_index=index, root_index=i, second_pair=second, second_value=value, constant=1,
                     rows=len(data.rows), row_digest=sha256(json.dumps([asdict(x) for x in data.rows], sort_keys=True).encode()).hexdigest(),
                     seconds=time.monotonic() - start)
        output["cases"].append(proof)
        path.write_text(json.dumps(output, indent=2) + "\n")
        print(json.dumps({k: v for k, v in proof.items() if k != "steps"}), flush=True)
    output.update(status="TERMINAL_EXACT_INTERVAL_PILOT", tested=len(output["cases"]), untested=len(cases)-len(output["cases"]))
    path.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
