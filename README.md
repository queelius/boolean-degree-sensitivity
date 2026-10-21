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

## Standalone singleton component classification

A [self-contained supplement](supplements/singleton-boundary-classification/README.md)
classifies ten-coordinate divisible singleton Fourier components under explicit
hypotheses. Every component is a five-cycle form; there are 30,240 labeled forms.
The written proof excludes the second constant case. An independently reproduced
portable checker verifies every cube value and Fourier coefficient, with positive
and tamper controls. Substantial AI assistance and review are disclosed.

This is a completed component lemma within the still-open investigation. It is
not a fourteen-variable Boolean construction or a global nonexistence proof.
Version **1.1.0**, [10.5281/zenodo.23533427](https://doi.org/10.5281/zenodo.23533427),
archives this supplement together with the ten earlier exclusions. All 52 public
files have been downloaded without authentication and verified by exact hashes;
see [the receipt](verification/PUBLIC-ZENODO-v1.1.0.json). The frozen supplement
retains its original pre-archive metadata as historical evidence. Novelty and
human peer review are not established.

## Three-exceptional singleton component cover

A [second self-contained supplement](supplements/singleton-ell3-classification/README.md)
classifies the constant-one ten-coordinate singleton components with three
exceptional unit inputs. The complete cover has seventeen listed families;
no minimal coordinate-orbit count is claimed. Written rank and graph reductions,
literal coverage maps, and exhaustive quartet selection establish completeness.

The [portable replay](verification/SINGLETON-ELL3-PORTABLE.json) uses only the
Python standard library. Root replay from a copied directory exhausted all
19,112 selection instances, checked all listed cube values and Fourier
coefficients, and passed 11 normal and 11 optimized controls. The frozen packet
retains its preparation-time publication and review notes; this root notice
records the subsequent portable acceptance and public source release.

Version **1.2.0**, [10.5281/zenodo.23536478](https://doi.org/10.5281/zenodo.23536478),
archives this second supplement together with the retained earlier evidence.
Neither v1.0.0 nor v1.1.0 includes it. The constant-two classification and
original fourteen-variable question remain open. Substantial AI assistance is disclosed; human review, formal verification
and mathematical novelty are not established.

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

Use [CITATION.cff](CITATION.cff) to cite the current exact archive, version
**1.3.0**, [10.5281/zenodo.23539867](https://doi.org/10.5281/zenodo.23539867),
published on 21 October 2026. It pins the graph supplement at commit
`81e6f434d44ee67610a88aab18a2ed7438510bfc` and retains the earlier evidence.
The [public verification receipt](verification/PUBLIC-ZENODO-v1.3.0.json) records
four new files freshly downloaded without authentication and both full proof
replays from the downloaded archive. The 56 retained entries passed earlier-body
SHA-256/MD5 rehash and successor MD5/size continuity. This does not claim 60 fresh
downloads. The graph lemma inherits the published Markström–Talbot 75-class count;
the Boolean application has additional unbundled premises. Later research and a
global solution are outside this archive.

Version **1.2.0**, [10.5281/zenodo.23536478](https://doi.org/10.5281/zenodo.23536478),
remains the earlier exact archive for the ell3 cover and retained exclusions/ell2
classification, pinning source `54644197be81024d1cfd18f74235a093cbcaf3a4`.
Its [receipt](verification/PUBLIC-ZENODO-v1.2.0.json) preserves the four-new/52-retained
verification protocol. Version 1.1.0 remains the earlier exact archive for the ten
exclusions and ell2 classification. None of these earlier versions contains the
graph supplement.

For the earlier ten-exclusion-only archive, the exact citation remains:
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


## Positive-obstruction locality graph supplement

The [verified portable graph supplement](supplements/g124-positive-locality/README.md) proves the positive-locality lemma for free124-edge fourteen-vertex3-graphs, relative to the explicitly cited Markström–Talbot75-class count, and the minimum-six-repair corollary. Two distinct standard-library algorithms and literal75-graph data are included. The Boolean application has additional unbundled premises; the original existence problem remains open. The graph supplement is archived in exact version1.3.0, [10.5281/zenodo.23539867](https://doi.org/10.5281/zenodo.23539867). Four new files were fully downloaded anonymously and both verifiers reran from the public archive;56 retained entries passed predecessor-body rehash and successor MD5/size continuity. [The public receipt](verification/PUBLIC-ZENODO-v1.3.0.json) states this scope without claiming60 fresh downloads. Earlier versions and their original disclosure dates remain preserved.
