# Positive obstruction locality in free 124-edge 3-graphs

This **verified source supplement** proves the graph lemma in [THEOREM.md](THEOREM.md), relative to Markström–Talbot's published classification count: in every fourteen-vertex 3-uniform hypergraph with124 edges and at most two edges in each four-set, a five-set contains at most one missing triple whose addition creates an obstruction and whose **every** obstruction lies in that five-set. It also proves the minimum-six-repair corollary.

All75 literal graphs and their complete obstruction/window certificate are included. Two distinct standard-library Python algorithms independently check freeness, actual invariant-tuple distinction, and positive locality. The classification's count75 is an explicit external theorem, not a newly repeated GLPK/nauty exhaustion. The paper's unrestricted Figure1 is used, not its2-colourable Figure2. The primary PDF is cited and hash-identified, not redistributed.

The fourteen-variable Boolean existence problem remains **OPEN**. This is a graph statement, not a Boolean function or a complete nonexistence proof. The dependent Boolean application in [APPLICATION.md](APPLICATION.md) requires additional premises not packaged here. Novelty, human peer review and proof-assistant formalization are not established. The stronger locality property already appears in earlier project history.

## Reproduce without installation

Python3.10+ is sufficient. From this directory:

```sh
python -S -m unittest -v
python -S verify_union.py --output FRESH-UNION.json
python -S verify_quartet.py --output FRESH-QUARTET.json
```

Use fresh output names. Expected complete status is `VERIFIED_RELATIVE_TO_EXTERNAL_CLASSIFICATION` from **both** verifiers, with75 graphs,18,000 missing triples and maximum positive locality1. A budget-limited `INCOMPLETE` receipt proves no complete cover. `--cpu-budget` defaults to60 CPU seconds; slower machines may use a larger finite allowance. Copying the directory elsewhere or invoking either script from another working directory works. No network, NumPy, graph canonicalizer, SAT solver, original repository or previous archive is required. Network isolation was not enforced in the recorded tests.

`verify_union.py` uses missing-triple obstruction unions and enumerates all five-set completions. `verify_quartet.py` distributes saturated quartets to their missing faces and directly scans all2,002 five-sets per graph. They accumulate the same incidence invariant differently and compare full tuples, not just their displayed hashes. Only strict relative-path I/O is shared. [data/manifest.json](data/manifest.json) pins all mathematical inputs; [MANIFEST.json](MANIFEST.json) records the complete publication edition.

Attribution, source transformations and review limits are in [PROVENANCE.json](PROVENANCE.json) and [REVIEW_HISTORY.md](REVIEW_HISTORY.md). Credit Alexander Richard Towell, ORCID0000-0001-6443-9897, with substantial OpenAI Codex assistance; Markström and Talbot retain credit for their classification. Original code is MIT; original notes/data are CC-BY-4.0, under the owning project's policy.

Cite exact archive version **1.3.0**, DOI [10.5281/zenodo.23539867](https://doi.org/10.5281/zenodo.23539867). This source edition carries the verified graph supplement; the record's public state establishes archive publication. The source-disclosure and public-file receipts in the owning project's verification directory record exact commit and observation times separately from the archive date. No earlier public disclosure is inferred from local preparation.

The existing concept family is10.5281/zenodo.23496541. Earlier version1.2.0, DOI10.5281/zenodo.23536478, archives the retained exclusions and singleton results and does **not** contain this graph supplement. The parent portable-packet gate accepted both algorithms and fresh copied-directory replays. It is AI review, not human peer review or proof-assistant verification. Historical preparation receipts remain unchanged and are identified as historical in REVIEW_HISTORY.md.
