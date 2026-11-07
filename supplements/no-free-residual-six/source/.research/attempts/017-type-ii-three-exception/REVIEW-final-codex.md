# Codex end-to-end audit of the 017 result

OpenAI Codex (codex-cli 0.163.0, read-only sandbox), 2026-10-23. Verbatim
final message. Applied after it: read_all.py matches the complete normalized
case; CERTIFICATES.md placement count corrected to 14,643; run_cover.py
derives pending c = 2 jobs from verified records; test_assembly.py added.

The supplied evidence supports the conditional exclusion. I found no mathematical counterexample, but the exact-case guarantee and one reported count need correction. The original restart bug is fixed for current records, with one legacy-record edge case remaining.

- **1. Aggregation: wrong as a literal exact-equality guarantee, with a reproduced counterexample.**

  [read_all.py:67](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/read_all.py:67) includes `faces`, `exceptions`, `order`, and `root_index` in its matching key, but omits `doubled` and `root_kind`.

  In memory, I changed `shape1_mmQ2-0138-c1.json` from `doubled=[[1,2,5,8]]` to `doubled=[[8,5,2,1]]`. The case dictionaries differed, their aggregation keys matched, and the real hardened reader still returned `CASE_ROWS_INFEASIBLE_VERIFIED`. The assembly accepted the corresponding record as `ALL_CASES_VERIFIED`.

  This is a counterexample to literal equality, **not to mathematical soundness**. The reader forces shape 1's doubled support to equal the union of its two disjoint negative pairs. Removing it or changing its mathematical support was rejected. All 3,184 case dictionaries in the saved result actually equal their matching cover cases in full.

  **Required fix:** canonicalize the complete case dictionary, rather than selecting fields, and add an aggregation regression test.

  The remaining aggregation logic is sound: all three covers are checked, only reader-verified records satisfy obligations, and each case requires both constants. In-memory controls produced 3,184 missing obligations after removing c = 2, and two after dropping or invalidating one certificate. Changing faces also produced two missing obligations.

  **Universe binding: sound for the supplied inputs.** I independently established a bijection between the 24 covered shapes and the frontier's 24 `OPEN` rows, preserving `-2`, `+1`, and `Q2`. Every one of the 3,184 cover cases belongs to its corresponding shape. Empty, incomplete, duplicated, and Q2-deleted universes were rejected.

- **2. Independent certificate sample: sound.**

  I ran `../../venv-exact/bin/python -B` with kernel-enforced read-only Landlock restrictions. Using `random.Random(20261023)`, I sampled two certificates per signed shape, in stored cover/shape order, from populations sorted by certificate path: **48 distinct `*-c1.json` certificates across all 24 shapes**.

  Every sampled certificate:
  - Matched its cover case exactly, including faces and doubled data.
  - Matched the certificate and artifact hashes recorded in the aggregate result.
  - Returned `CASE_ROWS_INFEASIBLE_VERIFIED`, `constants=[1,2]`, and `clause_soundness=PASS`.
  - Passed the real pinned LRAT checker with exit 20.
  - Contained no constant row.

  The sample included `triangle_mmm-0041-c1.json`, `triangle_mmm-0067-c1.json`, `shape1_mmQ2-0138-c1.json`, and `shape1_mmQ2-0154-c1.json`. It covered **11,104 core rows and 1,088,637 clauses**. No labels file was mistaken for a certificate.

- **3. Reported results: sound after correcting the main-cover placement count.**

  The saved result agrees with the principal certificate claims:

  | Cover | Shapes | Cases/certificates | Fresh cover-check placements |
  |---|---:|---:|---:|
  | `cover-cases.json` | 22 | 2,775 | **14,643** |
  | `triangle-cover.json` | 1 | 81 | 1,285 |
  | `shape1-cover.json` | 1 | 328 | 8,847 |

  [CERTIFICATES.md](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/CERTIFICATES.md) incorrectly gives **12,780** for the first placement count. Both the fresh cover reader and an independent count using signed-graph stabilizers gave **14,643**. All three cover checks passed.

  I confirmed 3,184 accepted records, zero rejected records, zero missing obligations, and `[1,2]` on every record. Totals match: **471,742 rows**, largest core **2,622**, and **43,863,984 clauses**. Referenced artifacts occupy approximately **13.315 GB**. All recorded frontier, catalog, cover, and reader hashes match current files.

  These are complete checks of the saved summary and coverage obligations. Fresh proof verification was sampled, not repeated over the entire collection.

- **4. Remaining mathematical scope: sound conditional on the stated premises.**

  The reader's reconstruction enforces the relevant restrictions:
  - Flag rows exclude the root, unsupported vertex types, triangle `---` exceptional vertices, and shape 1's doubled-quartic vertices.
  - `t2` occurs in reconstructed rows only on the exceptional negative triangle or the four triples inside the doubled quartic.
  - The doubled quartic is fixed and receives weight two through reconstruction and substitution.
  - Exact row comparison rejects additional unjustified terms.

  I independently checked these restrictions throughout the sample, including **4,099 flag rows** and **12 `t2` terms**, without finding a violation.

  The certificates establish infeasibility of necessary case rows. The written lemmas and enumeration premises justify necessity and exhaustive coverage. CP-SAT status strings alone establish neither. Nothing here proves an unconditional exclusion, integrates a candidate derivative into a global function, or resolves the remaining magnitude-pattern cases.

The earlier vertex-13, repeated-coordinate, malformed doubled-support, and negative-root-index defects are repaired and their counterexamples are rejected. The stated scope corrections and triangle-sign normalization are also present.

The restart repair in [run_cover.py:49](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/run_cover.py:49) correctly schedules c = 2 after a recorded c = 1 success with `constants:[1]`. However, a success record **without** `constants` is accepted into `done` through the fallback but never enters `needs_c2`; I reproduced an empty schedule. Derive pending c = 2 jobs from `done`. This does not affect the current complete collection.

All **41 existing tests passed normally and under `-O`**, with test scratch files virtualized in memory. Branch-aware coverage was 87% for the reader and 94% for the cover reader. Permanent aggregation and restart regression tests remain warranted.

No files were written; I did not read `../../log.md` or recursively list `.research`. This was a Codex audit, so it does not establish the requested different-model-family provenance.