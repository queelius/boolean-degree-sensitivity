# Three-exceptional constant-one singleton components

This self-contained packet establishes a complete finite cover for the exact
ten-variable component problem in [THEOREM.md](THEOREM.md):

    B = 1 - sum of eight distinct pair characters
          + sum of seven distinct quartet characters,

with origin0, exactly three singleton values−8, seven singleton values0, and
all cube values divisible by8. Every such component is a coordinate image of
one of the seventeen literal rows in [CATALOG.md](CATALOG.md). They form a
cover; no minimal coordinate-orbit count is claimed.

The written proof derives the binary rank bound and a complete graph/subspace
reduction. A **standard-library-only** Python checker verifies literal graph
augmentation/marking maps and independently exhausts all19112 quartet-selection
instances. It checks every listed component on all1024 inputs and Fourier
coefficients. The recorded run took38.82CPU seconds, with peak RSS160MiB.

**The fourteen-variable Boolean degree/sensitivity problem remains open.**
These components are not Boolean functions or full constructions. Constant-two
components are not classified here. Novelty, human peer review and formal
verification are not established. Substantial AI assistance is disclosed.

## Reproduce without package installation

Python3.10 or later is sufficient. No NumPy, nauty, SAT solver, network access,
original checkout or old667MB archive is needed:

```sh
python -S -m unittest -v
python -S verify_packet.py --output FRESH-VERIFICATION.json.gz --cpu-budget 120
```

Output paths must be fresh. The checker resolves its data relative to its own
location, so copying this directory elsewhere or running from an unrelated
working directory works. `-S` disables site-package loading and was used for
the recorded full replay. The unit controls also run under `python -O`.

The default CPU allowance is120 seconds, with10 reserved for output. Slower
machines may return an explicit incomplete report, including the pending
identity and any open search frontier; that report is not a proof. The full
recorded receipt is [verification.json.gz](verification.json.gz).

`data/manifest.json` pins the five local data files. The literal augmentation
certificate covers every missing-edge extension, so checking the cover does
not depend on canonical-labeling correctness or representative uniqueness.
The preparatory generator used a pinned nauty wrapper solely to discover
frame maps, which are now checked literally. Optional `prepare_sources.py`
documents that historical preparation and is **not** a replay dependency.

## Evidence and limits

The complete replay checks10720 augmentation maps,329 uncolored frame links,
39480 exceptional-set transports,14343 colored frames,44901 maximal subspaces
and19112 exhausted selection instances. Full family sets agree with the
independent historical quota-vertex enumeration: seventeen native rows,
53 overlapping source-cover occurrences. All listed histograms are
`{-8:64,0:768,8:192}` and each row has at least one inactive coordinate.

The tests include exact tiny positive/negative exhaustive searches, omitted
augmentation/bridge/candidate/family records, wrong coordinate/color maps,
changed component supports, aliased integer metadata, changed file pins and
path escapes, plus copied-directory entrypoint replay with site packages
disabled. Written completeness, finite enumeration, witness checks and prior
AI reviews are distinguished in [REVIEW_HISTORY.md](REVIEW_HISTORY.md).

This staging packet's portable replay is complete. Root acceptance and an
independent portable-packet review remain pending; historical independent
reviews do not automatically approve this new packaging. No formal proof
assistant or human signoff is claimed.

## Citation and publication readiness

This is an **unpublished local staging supplement**, not a new public release
or DOI. [CITATION.cff](CITATION.cff) intentionally has no DOI, release date or
new source commit. Existing version1.1.0, DOI10.5281/zenodo.23533427, archives
the earlier two-exceptional singleton classification and ten retained
conditional exclusions. It does **not** archive this three-exceptional result.
The existing concept family10.5281/zenodo.23496541 is the candidate archive
family for a substantive successor, subject to root publication review.

Canonical project: https://github.com/queelius/boolean-degree-sensitivity

Shared public catalog: https://github.com/queelius/research-records

Central ID: `boolean-degree-five-spectral-exclusions`.

Credit Alexander Richard Towell (ORCID0000-0001-6443-9897). OpenAI Codex
substantially assisted deductions, proof drafting, code, tests and separate
AI reviews. [PROVENANCE.json](PROVENANCE.json) preserves predecessor/source
credit and separates local preparation from public disclosure/archive dates.
Original code is MIT; original proof, data and metadata are CC-BY-4.0.
See [LICENSE.md](LICENSE.md). No external publication was performed here.
