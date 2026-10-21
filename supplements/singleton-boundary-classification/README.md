# Ten-variable divisible singleton boundary classification

This self-contained supplement proves a component classification:
under the precise hypotheses in [THEOREM.md](THEOREM.md), the constant
coefficient is 1 and the polynomial is

    (1-chi_uv)(1-sum_{e in C5}chi_e).

There are 30,240 forms on ten labeled coordinates. A complete written
proof excludes constant coefficient 2. Exact standalone scripts reproduce
the catalog and verify all 30,965,760 cube values and equally many integer
Walsh coefficients. The verifier independently enumerates cycle forms and
does not import the generator or any research checkout.

**The fourteen-variable Boolean degree/sensitivity problem remains open.**
These components are not fourteen-variable Boolean functions. No novelty,
human peer review, or formal verification is claimed. Substantial AI
assistance and separate AI proof reviews are disclosed below.

## Reproduce

Use Python 3.10 or later and the single pinned dependency in requirements.txt:

```sh
python -m pip install -r requirements.txt
python -m unittest -v
python generate_catalog.py --output reproduced-catalog.json
python verify_catalog.py reproduced-catalog.json --output reproduced-verification.json
```

Output paths must be fresh. Included catalog.json and verification.json
record one exact run. No old archive, solver, network connection, original
absolute path, or external research file is needed after dependency setup.
The unit suite includes complete positive checks, omitted/aliased/invalid
row and coefficient tampering, scope-promotion rejection, small graph
lemmas, unrelated-working-directory replay, and optimized-Python failures.

The compact mask catalog is a few MiB. Verification uses 256-row batches;
it does not store a giant full-value table. Cube bit i represents coordinate
i, and Fourier characters are `(-1)^popcount(mask & input)`.

## What is and is not verified

THEOREM.md proves completeness using incidence, integer Mobius parity,
and a finite exhaustive graph case split in written mathematics. The
portable finite checker establishes the complete five-cycle family,
its converse, all cube guards, and exact Fourier spectra. It does not
enumerate every possible six-quartic family or replace the a=2 proof.
Review history, source pins, and limits are in REVIEW_HISTORY.md and
PROVENANCE.json. QA results and their precise environment are recorded
separately. There is no proof-assistant certificate or human signoff.

## Citation and archive readiness

This source supplement is prepared for the existing Boolean degree/sensitivity
archive family. It has no archival DOI or assigned archive version. Cite an
exact public source commit until an archived version is available. CITATION.cff
intentionally has no DOI field. The existing archive
version 10.5281/zenodo.23496542 contains ten earlier geometry 34 exclusions;
it does not archive this classification. Concept 10.5281/zenodo.23496541
is the candidate family. The parent independently copied the packet to an unrelated directory, passed
all12 normal and12 optimized controls, regenerated the catalog byte for byte,
and replayed the full cube/Walsh check. The written graph case split was also
reviewed. See qa/root-portable-replay.json. Archive metadata and public file
verification remain separate publication steps.

Canonical owning source: https://github.com/queelius/boolean-degree-sensitivity
Central catalog: https://github.com/queelius/research-records
Catalog identifier: `boolean-degree-five-spectral-exclusions`.

Alexander Richard Towell (ORCID 0000-0001-6443-9897) is credited for this
research record. OpenAI Codex substantially assisted deductions, code,
drafting, exact checks, and independent AI review. Earlier project and
predecessor contributions are retained in the provenance record.

Original code is MIT licensed; proof, notes, catalog data and metadata are
CC-BY-4.0. See LICENSE.md and LICENSES/. Dependencies retain their own licenses.
