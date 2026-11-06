# 018: no-free residual six (union 14)

Claude Code (Opus 5.5), 2026-10-23, for Alexander Richard Towell. Codex
reviewed L1. **Nothing here is accepted or frozen.** Global status: OPEN.

## Goal

After checkpoint 1533, every residual <= 6 instance has negative-support
union 14 (`no-free-frontier.json`): 22 of the 29 open magnitude patterns.
The first target is lemma L1 (`L1.md`). If it is certified, it excludes the
whole patterns (2^4) and (2^4,1), the first whole patterns closed since the
frontier was set.

## Reading order

1. `PLAN.md`: why this front, steps (a) to (d).
2. `L1.md`: the lemma, the counting that closes (2^4) and (2^4,1), the
   cover's lemmas and the cover design. `REVIEW-L1-codex.md`: Codex review
   (all fixes applied).
3. `NOTES.md`: working notes and probes (CP-SAT verdicts only). Its cover
   section is the earlier proposal; `L1.md` is the final design.
4. `SCOPING.md`: subagent report, unreviewed. `CONTROLS.md`: n = 13
   positive controls.

## Files by role

| Role | Producer | Independent check |
|---|---|---|
| Frontier of the 22 patterns | `make_frontier.py` -> `no-free-frontier.json` | `frontier_reader.py`, `test_frontier.py` |
| Positive controls | `controls_n13.py` -> `controls-n13.json` | `test_model018.py` |
| L1 cover (2221 cases) | `cases018.py` -> `l1-cover.json` | `cover_reader018.py` (every labelled placement, about 19 min) |
| Row model | `model018.py` | `reader018.py` rebuilds rows from keys; `test_reader018.py` |
| Certificates | `certify018.py` (CP-SAT core, 014 CNF, CaDiCaL LRAT, pinned lrat-trim), driven by `run018.py` | `reader018.py` per certificate |
| Assembly | | `read_all018.py`: every (case, m) covered and bound to its cover case |
| Progress | `status018.py` (reads `certs/results.jsonl`) | |

`pilot_neg.py` is exploration. `fixtures/` holds two small certificates
used by the tests.

## Running

Producers need OR-Tools (environment `uv-search` in `../../environments.json`);
readers and tests use `venv-exact`. From this directory:

```sh
# progress (cheap)
../../venv-exact/bin/python -B status018.py
# resume or finish the certificate run (resumable; skips done obligations)
cd ../../.. && uv run --extra search python -B .research/attempts/018-no-free-residual-six/run018.py --jobs 8 --core-seconds 900 --seed-core 3; cd -
# assembly check, after the run
../../venv-exact/bin/python -B read_all018.py read-all-l1.json --jobs 6
# tests, normal and -O
../../venv-exact/bin/python -B -m unittest test_frontier test_model018 test_reader018
../../venv-exact/bin/python -O -B -m unittest test_frontier test_model018 test_reader018
```

Acceptance would be `read_all018.py` reporting `ALL_L1_CASES_VERIFIED`
(0 rejected, 0 missing). Freezing a checkpoint 1534 is the user's decision.

## State on 2026-10-23 (about 22:45 local)

- The run was launched in a Claude Code session with 8 jobs. If that
  session ends the run may stop; it resumes from `certs/results.jsonl`.
  After about 3 hours: 425 certificates, 974 of 4442 obligations done
  (variants let one certificate cover several (type, m) obligations).
  Median job 41 s.
- **Case 754, m = 1: failed once, now certified.** CP-SAT's core from
  the full model needed a 253-term value row, and CaDiCaL did not refute
  it within 3600 s (recorded as `ERROR`). Its partial proof is compressed
  in `certs/l1-00754-m1.lrat.failed-timeout.zst`; it is not evidence.
  Following the Codex consultation `consultations/case754-strategy`, the
  case was redone with `certify(..., seed_k=3, seed_core=True)`. That takes
  a CP-SAT core inside the structural subset (every non-value row, plus the
  value rows with |X| <= 3). The core has 1,437 rows and no constant row;
  CaDiCaL refutes it in 20 s. `reader018` verifies
  `certs/l1-00754s3-m1.json` in normal and `-O` mode, with variants none,
  c0 and c3 at m = 1. It is logged in `certs/results-extra.jsonl`, which
  `run018.py` and `status018.py` also read. Use the same route for any
  other timeout.
- **Seed-core mode (from about 23:45).** After 476 certificates, the pair
  departure cases were taking about 450 s each. Nearly all of that went to
  the full-model CP-SAT core and the deletion pass; CaDiCaL itself took 1
  to 200 s. Three pending pm cases benchmarked with the case-754 route
  (`seed_k=3, seed_core=True`) took about 8 s each, and reader018 verified
  one of them in both modes. The run was restarted with `--seed-core 3`,
  which falls back to the full-model core if the structural subset is
  feasible. Earlier certificates are unchanged. Certificates from both
  routes are checked by the same reader.
- **Run finished 2026-10-24 00:59.** `status018.py`: 4442 of 4442
  obligations done, 3664 logged results (3663 `LRAT_VERIFIED_CORE_UNSAT`
  plus the superseded case-754 `ERROR`), 3662 certificate JSONs (754s3 is
  logged twice under one stem). Median job 10.6 s; `certs/` is 85 GB. This
  is producer bookkeeping only.
- **Assembly passes (01:37).** After the Codex audit
  (`REVIEW-l1-assembly-audit-codex.md`; all should-fix items applied),
  `read_all018.py` was rerun on a write-protected `certs/`:
  `ALL_L1_CASES_VERIFIED`, 3662 certificates, 0 rejected, 0 missing, cover
  and frontier readers pass, targets exact (`read-all-l1.json`, read-only).
  `read-all-l1.preliminary-pre-audit-fix.json` is the earlier pass with
  the old code and is not evidence. `make_acceptance_1534.py` has been
  dry-run only; writing the 1534 ledger and acceptance and freezing the
  checkpoint wait for the user's approval. About 24 GB of disk is free.
- **Disk.** The proofs average about 44 MB, some 1 to 2 GB. The disk had
  about 89 GB free after the compression, and the remaining run may need
  about 65 GB. A watchdog in the launching session stops the run
  (resumably) below 15 GB free, logging to `certs/disk-watchdog.log`.
  Before a restart, consider storing verified proofs compressed. The
  readers currently need plain `.lrat` paths, so that change needs a
  reader update and review.
