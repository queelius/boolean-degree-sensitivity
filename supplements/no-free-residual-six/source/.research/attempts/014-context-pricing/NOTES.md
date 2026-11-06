# Attempt 014: pricing and certifying the signed-star native contexts

Started 2026-10-21 by Claude Code (Opus 5.5) at the user's request, following
the handoff's recommended continuation ("price one meaningful
proof-producing SAT experiment"). New files only; nothing in 009 was changed.

## Scope

The 26 native contexts of the conditional branch "residual defect <= 6 with
at least two negative-free coordinates" (`H/two-free-independent-review-cycle1409.md`,
frontier `H/signed-star-genuine-frontier-cycle1510.json`: 2 excluded, 24 open).
Closing every context closes that branch only. It does not settle any whole
negative-quintic pattern (29 open), the one-free / no-free residual cases, or
residual defect above six.

Two row systems per context:

* **raw**: the 12512 original rows (common block 1432 + context rows), under
  the 1431 row authority;
* **extended**: raw plus the 1518/1519 accepted added rows, which also rest on
  the 1515/1517 topology premises (and inherited cover transitions).

A raw exclusion depends on strictly fewer premises than an extended one.

## Assembly checks

* `models.py` assembles every model through 009's own pinned, hash-checked
  readers (`native_sat_pilot_io_cycle1457`), from the sources pinned in
  `H/tip-interval-parent-authorization-cycle1520.json`.
* For o8-i3-c1 the assembled extended model's `binding()` (rows, variables,
  header SHA-256) is identical to the binding pinned by the accepted 1521 run.
* Term entries are (face mask, coefficient); masks map to positions in the
  common block's 1079-variable list (bijective, asserted).

## Pipeline

1. `price.py`: bounded CP-SAT per context. Verdicts are untrusted. Any
   assignment returned is checked exactly against every row.
2. `core.py`: untrusted candidate infeasible row subset (assumption core, then
   deletion).
3. `certify.py`: decision-diagram CNF of exactly those rows (`encode.py`),
   CaDiCaL 3.0.1 LRAT, pinned `lrat-trim --forward --no-trim` (SHA-256
   179d041f...).
4. `verify_core.py`: independent reader. It rebuilds the rows from the pinned
   JSON directly, checks that every CNF clause holds under the canonical
   extension "aux (r,k,s) = first k terms of row r sum to s" of any
   row-satisfying x (so CNF UNSAT implies the rows are infeasible), then reruns
   lrat-trim.

Tests: `test_encode.py` (CNF projection equals the row's solution set,
exhaustively, on 40 random rows; conjunction controls), `test_verify_core.py`
(genuine encodings accepted; added units, arbitrary clauses, wrong-branch
steps and false dead-end claims rejected).

## Results (2026-10-22)

**All 24 open contexts: raw rows infeasible, LRAT-certified, independently
verified.** Summary with SHA-256 of every CNF, proof, label map, core and
verify record, plus the pipeline sources: `signed-star-raw-certificates.json`.

Pricing (untrusted): every one of the 26 models is INFEASIBLE under CP-SAT in
both row systems (`price-all-120s.jsonl` extended, `price-raw-300s.jsonl`
raw; raw walls 0.8 s to 125 s, hardest o7/o8/o9). Controls: Euler-row
ablation gives feasible models whose assignments pass the exact re-check
(`ablation.jsonl`, `controls.jsonl`).

| idx | context | assumption core | minimized core rows | CNF clauses | LRAT MB | core search s |
|---|---|---|---|---|---|---|
| 2 | o8-i3-c1 | 1145 | 376 | 26477 | 4.2 | 716 |
| 3 | o8-i3-c2 | 1243 | 445 | 37339 | 10.3 | 1739 |
| 4 | o8-i7-c1 | 2873 | 1949 | 378287 | 35.3 | 80644 |
| 5 | o8-i7-c2 | 1910 | 473 | 66966 | 29.9 | 26807 |
| 6 | o9-i33-c1 | 1664 | 580 | 54673 | 13.3 | 3363 |
| 7 | o9-i33-c2 | 1870 | 1187 | 90008 | 20.9 | 47067 |
| 8 | o9-i35-c1 | 1708 | 434 | 30389 | 5.1 | 1285 |
| 9 | o9-i35-c2 | 2032 | 670 | 80408 | 22.3 | 21430 |
| 10 | o10-i38-c1 | 1136 | 361 | 37052 | 7.6 | 695 |
| 11 | o10-i38-c2 | 996 | 360 | 35872 | 5.2 | 359 |
| 12 | o10-i113-c1 | 555 | 222 | 10421 | 1.4 | 145 |
| 13 | o10-i113-c2 | 688 | 254 | 18985 | 2.7 | 200 |
| 14 | o10-i116-c1 | 744 | 381 | 29947 | 3.6 | 216 |
| 15 | o10-i116-c2 | 953 | 321 | 23896 | 4.0 | 288 |
| 16 | o10-i180-c1 | 582 | 233 | 24888 | 2.6 | 151 |
| 17 | o10-i180-c2 | 808 | 234 | 8753 | 0.2 | 190 |
| 18 | o11-i185-c1 | 441 | 159 | 8825 | 0.3 | 100 |
| 19 | o11-i185-c2 | 104 | 83 | 3089 | 0.1 | 33 |
| 20 | o11-i257-c1 | 195 | 134 | 5188 | 0.1 | 33 |
| 21 | o11-i257-c2 | 457 | 174 | 8364 | 0.2 | 103 |
| 22 | o11-i691-c1 | 1085 | 239 | 14482 | 2.2 | 261 |
| 23 | o11-i691-c2 | 676 | 184 | 6677 | 0.2 | 122 |
| 24 | o12-i1697-c1 | 205 | 137 | 6188 | 0.2 | 37 |
| 25 | o12-i1697-c2 | 137 | 100 | 4825 | 0.1 | 34 |

Each row: CaDiCaL exit 20, `lrat-trim --forward --no-trim` prints
`s VERIFIED`, `verify_core.py` clause soundness PASS. "Minimized" means after
one deletion pass, not minimal. Row 25 was verified by hand before the batch
and re-verified into `certs/raw-25.verify.json` afterwards.

Root-7 replication controls (indices 0, 1; already excluded in 009 by
1476 and 1476+1497) were still in deletion when this was written; they are
not needed for the claim.

### What this does and does not establish

* Established, conditional on the 1431 row authority (that every row is a
  valid consequence of the context hypotheses): no Boolean assignment of the
  1079 face variables satisfies the raw rows of any of the 24 contexts. With
  the two 009 exclusions, all 26 native contexts of the two-free,
  residual <= 6 signed-star branch are excluded.
* Not established: any whole negative-quintic pattern (29 open), the
  one-free and no-free residual cases, residual defect above six. The
  problem is OPEN.
* Not yet done: an independent review of the 1431 row derivations by this
  attempt (inherited, not rechecked), and acceptance into the checkpoint
  chain (`H/save_research_checkpoint_v2.py`). The status in the JSON is
  therefore CANDIDATE_RESULT_NOT_ACCEPTED_INTO_CHECKPOINT_CHAIN.

## Review and hardening (2026-10-23)

An independent adversarial subagent found the clause checking sound but
three binding gaps (label not derived from the model, raw scope not
enforced, row ids not range checked); see `REVIEW-verifier.md`. All three
are fixed in `verify_core.py`, with regression tests (99 pass). Every
certificate was re-verified with `--require-raw` into
`certs/raw-<i>.verify2.json`, and `make_summary.py` rebuilt
`signed-star-raw-certificates.json` from those records (all RAW scope).
The premise chain is reviewed in `../015-sphere-catalog-audit/REVIEW.md`.

Checkpoint drafts, not yet frozen: `checkpoint-1531/` holds the acceptance
authority, the successor frontier (26/26 contexts, 13/13 roots genuinely
excluded; raw rows 25/26, o7-i0-c2 still needs the 1497 units) and the
state summary.
