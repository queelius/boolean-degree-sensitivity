# Review: case 754 certification strategy (Codex consultation)

Source: `consultations/case754-strategy.{prompt,answer,log,json}`, Codex
session 01a16c1f-d237-7f20-93da-814123893986, read-only, 2026-10-23. This is
AI review, not acceptance.

## What Codex found (and what Claude Code checked)

- The stored core (464 rows) depends on one value row over X = {1..9}, with
  253 terms and about half of the CNF's auxiliary variables. Removing that
  row makes the rest satisfiable: Codex evaluated the assignment against
  the other 463 rows. So deletion over the saved core cannot help. The row
  is easy for CP-SAT's linear reasoning and hard for CaDiCaL through the
  decision-diagram encoding. That mechanism is Codex's inference.
- It found no case-specific mistake in the cover or the model:
  - the root matches catalog index 3 (order 9, V, E, F = 9, 21, 14);
  - the CNF reproduces byte for byte;
  - the reader rebuilt all 464 rows.
- Its proposed fix: a core taken inside the seed_k = 3 structural subset.
  In its proof-free test that core had 1,437 rows and CaDiCaL refuted it
  in 2.7 s. It needs no reader change. Splitting the case would need
  conditional certificates and new assembly rules (described in the
  answer); not needed.

## What was done

- Added `seed_core` to `certify018.certify`, producer only, with the
  default unchanged.
- Certified the case: 1,437 rows (matching Codex's count), no constant row,
  CaDiCaL 20 s including LRAT.
- `reader018.read` gives CASE_ROWS_INFEASIBLE_VERIFIED in normal and `-O`
  mode, with variants (none, 1), (c0, 1) and (c3, 1).
- Logged in `certs/results-extra.jsonl`, which `run018.py` and
  `status018.py` now read.

Not done: Codex's CaDiCaL option portfolio (not needed) and the conditional
split design (kept in the answer for future cases).
