# Root-7 c = 2: raw rows infeasible without the 1497 units

Claude Code (Anthropic), 2026-10-23, for Alexander Richard Towell. Successor
to ROOT7-CONTROL.md (pinned by checkpoint 1532, so not edited), which
recorded this run as unfinished.

Context o7-i0-c2 (root-7 sphere, c = 2) was already excluded by 009
(1476/1497/1501), but only with the 1497 unit clauses added; the 1531
frontier records its raw rows as open ("raw rows 25 excluded / 1 open").
The 014 raw pipeline has now excluded the raw rows alone:

| item | value |
|---|---|
| core | 3,987 of the raw rows (`cores/raw-1.json`, sha256 1a5afe83...; minimisation wall 121,589 s) |
| CNF | 3,482,391 clauses (`certs/raw-1.cnf`, sha256 b6da042d...) |
| proof | CaDiCaL 3.0.1 LRAT (`certs/raw-1.lrat`, 278 MB, sha256 b858748b...) |
| check | pinned lrat-trim exit 20, s VERIFIED |
| reader | `verify_core.py`: clause soundness PASS, row scope RAW, ROWS_INFEASIBLE_VERIFIED (`certs/raw-1.verify.json`, sha256 88a4fac3...) |

Certificate record `certs/raw-1.json` (sha256 25c83a65...). The row
families in the core: downward closure 1971, induced Euler 1612, triangle
cofaces 264, root fixings 66, edge valence 61, and a few others; all are
raw rows of the 009 native model (no 1518/1519 added rows, no 1497 units).

Consequence, if accepted: the signed-star frontier becomes raw rows 26/26
excluded, so the 1497 unit-clause premise is no longer needed for this
branch. It changes no genuine-context or root count (all were already
excluded) and no magnitude pattern. Not frozen; global status OPEN.
