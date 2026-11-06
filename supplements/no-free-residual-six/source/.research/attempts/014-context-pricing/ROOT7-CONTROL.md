# Root-7 controls through the 014 raw pipeline

Claude Code (Anthropic), 2026-10-23, for Alexander Richard Towell. A control
run, not new frontier evidence: both root-7 contexts were already excluded
by 009 (1476 for c = 1; 1476/1497/1501 for c = 2). This file is new; the
pinned NOTES.md and certificate summary are unchanged.

| index | context | result |
|---|---|---|
| 0 | o7-i0-c1 | `certs/raw-0.json`: core of 3,377 of 12,512 raw rows, 1,678,694 clauses, CaDiCaL UNSAT, pinned lrat-trim exit 20, independent reader `verify_core.py` ROWS_INFEASIBLE_VERIFIED |
| 1 | o7-i0-c2 | CP-SAT reports the raw rows INFEASIBLE under assumptions (`cores/raw-1.log`), core minimisation still running after 30 hours; no CNF, proof or reader verdict, so nothing is claimed |

Index 0 reproduces the 1476 raw-row exclusion with a different pipeline
(native 014 encoder, decision-diagram CNF, separate reader). Index 1, if
it finishes, would show that the c = 2 root-7 raw rows are infeasible
without the 1497 unit clauses, which the 1531 frontier records as needed.
Until a verified certificate exists, the 1531 statement stands.
