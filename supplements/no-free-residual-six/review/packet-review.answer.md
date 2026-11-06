**Do not publish this exact staged packet yet.** I found three blocking defects and a pending release gate. Confidence is high in these findings; confidence in full reproducibility remains provisional because I did not run the full replay.

**BLOCKING**

1. **The headline and citation abstract overstate the result.** [CITATION.cff:16](/home/spinoza/github/math-theory/.research/publication-staging/residual6-no-free-v1.5-cycle1534/packet/CITATION.cff:16) says “residual Fourier defect at most six is closed.” The REPORT and README titles also say “residual six closed.” This contradicts the acceptances and ledger: **20 residual-≤6 patterns remain open**. What 1531–1533 close is the branch with at least one negative-free coordinate. Use wording such as “Residual-six branches with free coordinates excluded; two whole patterns excluded.” Correct the Zenodo metadata too.

2. **The bundled checker’s license and source are missing.** [LICENSE.md:12](/home/spinoza/github/math-theory/.research/publication-staging/residual6-no-free-v1.5-cycle1534/packet/LICENSE.md:12) claims both are included, but the staged `lrat-trim/` directory contains only the executable. I inspected the upstream checkout’s LICENSE: it explicitly requires inclusion of its copyright and permission notice. Include that exact license, plus the matching checker source and build files for an auditable trusted checker. Towell’s original-code MIT notice does not supply Biere’s notice.

3. **The packet does not preserve one checkpoint-pinned artifact.** Both the 1534 acceptance and checkpoint manifest pin `018-no-free-residual-six/README.md` to SHA-256 beginning `00a0b9b8…`; the staged file hashes to `62ed85dd…`. No source-manifest entry contains the expected bytes. All 570 files nevertheless match the packet’s newly generated manifest—demonstrating that this check alone does not establish checkpoint fidelity. Restore the accepted bytes, keep updated navigation separately, and validate authority/checkpoint pins during staging. This is an archival identity defect; I found no corresponding changed mathematical reader.

4. **Pending publication gate:** `packet/verification/` was empty when inspected. The report already describes a staged receipt and measured runtime. Wait for the running replay, include its receipt and logs, then build and checksum the final packet. I recognize that this work is already underway.

**SHOULD-FIX**

5. **Make the premise summary explicit enough to audit.** The results table substantially matches all four acceptance statements, and the report incorporates their full conditions by reference. However, its premise bullets are not an exhaustive rendering of them. In particular, 1532 names the 1526/1527 acceptance, 76-record scan, inherited endpoint inverse-cover completeness, the 1395 displayed-form argument, and small-sphere facts S3/S4/S6. List these directly or provide a per-checkpoint premise table. Point readers to accepted `L1.md` for definitions; `SCOPING.md` labels itself unreviewed and unaccepted.

6. **Document the actual platform and resource assumptions.** The bundled checker is a dynamically linked **x86-64 ELF** executable; “Linux with Docker” is insufficient for native ARM execution. Specify supported architecture or an explicit emulation route. The mount arrangement and venv shim look consistent by inspection, but I did not test Docker. Scratch usage also scales with jobs: the largest listed certificate input set is about 3 GB, so “one certificate at a time” means per worker. Quote the `mkdir` paths for installation directories containing spaces.

7. **The archived Docker helper has a broken packet path.** In `packet/build/docker_replay.sh`, `dirname "$0"/../packet` resolves to `packet/packet`, which does not exist. The documented direct Docker command avoids this bug. Fix the helper to locate the packet parent directory, or clearly identify it as a historical, non-runnable staging script.

8. **Describe controls at their actual scope.** The missing-certificate control exercises `missing()` using archived result dictionaries and then calls `status()` with fabricated passing cover/frontier verdicts. It meaningfully tests assembly bookkeeping, but does not rerun discovery and assembly after deleting a real certificate. The 014 negative controls also accept any subprocess failure; recording the specific rejection or checker outcome would distinguish intended rejection from an unrelated error. I found no demonstrated false-positive control.

**MINOR**

9. README promises `CONTRIBUTION.json`, which is absent. Include it or remove the reference. This would also be a useful place to distinguish original public disclosure dates/URLs from the DOI publication date.

10. REPORT groups the assembly behavior too loosely: 017 checks constants `c=1,2` and binds the 24 frontier shapes; 018 checks magnitudes `m=1,2`, runs its frontier reader, and requires the two exact target patterns.

**What I verified myself**

- All **570 source-file hashes** match `SOURCE-MANIFEST.json`; the historical interpreter symlink has the documented target.
- Authority data contains **26 contexts, 13 roots**, and **136 Type-II classes with 24 open**.
- The 017 covers contain **24 shapes and 3,184 cases** and bind to the frontier. The 018 cover contains **2,221 cases / 4,442 obligations**.
- Eligible certificate filenames exactly match the **3,184** and **3,662** receipt entries. Every receipt-referenced certificate/input has a matching manifest hash, including aliases.
- The ledger has **73 patterns, 27 open: 20 at residual ≤6 and seven above six**.
- Four bundled fixture CNF/proof pairs pass the bundled lrat-trim with exit 20 and `s VERIFIED`; their input pins match.
- Removing the first 018 archived result creates a missing obligation; optimized-mode assembly also returns `INCOMPLETE`.

**What I inspected but did not fully execute**

The materialization wrapper appears sound: it checks decompressed hashes, calls the original per-certificate function, and removes inputs afterward. The frozen readers actually invoke lrat-trim and require its success. Receipt comparisons bind certificate hashes, cases, variants/constants, and input pins; they are not vacuous. The 014 comparison is meaningful because the reader independently rebuilds rows and emits their identity, raw scope, checker result, and input hashes.

I found no apparent certificate-skipping route or missing receipt-referenced certificate input. The limited closure rule is adequate only when supported by the completed offline replay and original-pin validation; it is not a general dependency-closure guarantee.

I only **read** `verify-tar.json`, acceptance/review claims, and staged replay logs. I did not independently hash the entire certificate store, rerun tar verification, execute the complete tests/controls, or re-prove the written reductions. The AI-assistance and review-kind disclosures otherwise accurately distinguish certificate checking from mathematical formalization and human review.