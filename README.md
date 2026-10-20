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
packet also includes the frozen catalogs, arrays and certificates. Those
large data files will be distributed through the archival deposit rather
than Git.

The complete staged packet passed an isolated, network-disabled replay:
all ten case checks, domain deletions, and 138 controls passed. See the
[verification receipt](verification/REPLAY-RECEIPT.json) and
[packaging history](verification/REPLAY-HISTORY.json).
The data archive is uploading to Zenodo. Its DOI will be recorded here
after publication and public-download verification.
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

Use [CITATION.cff](CITATION.cff) and an exact repository commit while the
archive is pending. Once deposited, cite the **specific version DOI** of the
evidence packet. Substantive future updates will use the same archive family.
There will not be a separate DOI for each experiment.

The cross-project public index is
[queelius/research-records](https://github.com/queelius/research-records).
The [project record](https://github.com/queelius/research-records/tree/main/records/boolean-degree-five-spectral-exclusions)
tracks the source commit, archival status, public disclosure date,
verification scope and limitations.

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
