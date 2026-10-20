# Degree-five Boolean functions with sensitivity fourteen

**Status: open problem; verified partial exclusions.**

We are investigating whether a Boolean multilinear polynomial on 14 variables
can have real degree at most five, satisfy `f(0)=0`, and satisfy `f(e_i)=1`
for every coordinate. This repository does not contain a construction or a
proof of nonexistence for that full problem.

The first curated contribution consists of **ten exact conditional
exclusions** within one signed Fourier geometry, together with source code,
explicit case definitions, controls, and reproducible certificate checking.
The cases are specified in [CASES.json](CASES.json); their integer
contradictions and mathematical assumptions are described in
[REPORT.md](REPORT.md).

Author: **Alexander Richard Towell**, Southern Illinois University
Edwardsville, [ORCID 0000-0001-6443-9897](https://orcid.org/0000-0001-6443-9897).
Substantial OpenAI Codex assistance is disclosed in the report.

## What is proved

Each specified case has a complete necessary linear model. An independent
implementation reconstructs its equations and checks an integer
combination that yields a contradiction. The proof applies to that entire
conditional case. It does not exclude the whole geometry or all possible
14-variable Boolean functions.

The evidence uses exact finite computation and written mathematical
arguments. It has not been formalized in a proof assistant, and human peer
review and external acceptance are not claimed. Numerical solver timeouts
and UNKNOWN results are not treated as proofs.

## Code and reproduction

The `source/` tree preserves the research files' bytes and layout, including
the inherited mathematical notes and verification code. The complete data
packet also includes the frozen catalogs, arrays and certificates. Download
the complete packet from the [v1.0.0 release](https://github.com/queelius/boolean-degree-sensitivity/releases/tag/v1.0.0).

The complete staged packet passed an isolated, network-disabled replay:
all ten case checks, domain deletions, and 138 controls passed. See the
[verification receipt](verification/REPLAY-RECEIPT.json) and
[packaging history](verification/REPLAY-HISTORY.json).
All eight release assets, including the 667 MB data archive, were downloaded
without authentication and checked against their SHA-256 hashes. See the
[public download receipt](verification/PUBLIC-RELEASE.json).
The same evidence packet is archived on Zenodo at
[10.5281/zenodo.23496542](https://doi.org/10.5281/zenodo.23496542).
All 48 public files—the 40 archive parts and eight metadata files—were
downloaded without authentication and verified by SHA-256. Concatenating
the public parts reproduced the original archive exactly.
[The publication receipt](verification/PUBLIC-ZENODO.json) records the
completed metadata, file, and archive checks.
[REPRODUCE.md](REPRODUCE.md) describes the full packet's Docker verification;
it requires the complete data packet, not just this source checkout.

For the small exact-arithmetic and scope controls in this checkout:

```bash
python -m pip install -r runtime/requirements.txt
python run_controls.py
```

These 138 tests include feasible and infeasible examples, changed categorical
bases, large integers, missing proof checks, and scope mismatches. Passing
them is distinct from checking the ten large certificates.

## Citation and public record

Use [CITATION.cff](CITATION.cff) to cite the exact archived version:
Alexander Richard Towell (2026), *Exact spectral exclusion certificates for
degree-five Boolean candidates*, version **1.0.0**,
[doi:10.5281/zenodo.23496542](https://doi.org/10.5281/zenodo.23496542).
The archive was published on 20 October 2026 and pins source commit
`43ddb9a8a360bf84451b81a27fb67a001b4c4e16`. The separate GitHub v1.0.0
release includes later explanatory documentation at commit
`00e60302ac9900530f523b8b43f88fac523302bf`.
Substantive future updates will use the same archive family, rather than
a separate DOI for each experiment.

The cross-project public index is
[queelius/research-records](https://github.com/queelius/research-records).
The [project record](https://github.com/queelius/research-records/tree/main/records/boolean-degree-five-spectral-exclusions)
tracks the source commit, archival status, public disclosure date,
verification scope and limitations.
Its stable central ID is `boolean-degree-five-spectral-exclusions`,
recorded in [CONTRIBUTION.json](CONTRIBUTION.json). Detailed research
tracking stays with the owning project; the central entry describes the
frozen ten-case contribution.

The curated source was first publicly verified on 20 October 2026 at
[commit 43ddb9a](https://github.com/queelius/boolean-degree-sensitivity/commit/43ddb9a8a360bf84451b81a27fb67a001b4c4e16).
No journal or arXiv submission has been made for this contribution.

The broader motivation is Epoch AI's
[degree–sensitivity problem](https://epoch.ai/frontiermath/open-problems/degree-sensitivity-boolean).
The report credits earlier work by Smotrovs, Zaicevs and Stepanovs. Novelty
of these partial exclusions is not established by the bounded literature
review or by obtaining a DOI.

Original code is MIT licensed; original notes and data are CC BY 4.0.
Third-party notices are retained. See [LICENSE.md](LICENSE.md).
