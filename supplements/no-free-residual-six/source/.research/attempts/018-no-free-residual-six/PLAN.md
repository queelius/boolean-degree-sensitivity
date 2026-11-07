# 018: the no-free (union 14) residual <= 6 case

Claude Code (Anthropic), 2026-10-23, for Alexander Richard Towell. Plan
after checkpoint 1533, on the user's go-ahead ("I defer to your
judgement"). Global status: OPEN.

## Why this front

SCOPING.md (subagent report, claims cited to sources; not yet reviewed)
shows that, conditional on the accepted chain (residual-four support
constraints, 1401/1404, 1531, 1533), every residual <= 6 instance has
negative-support union 14. In the canonical ledger
`findings/negative-quintic-pattern-cases-cycle1388.json` (empty_pair,
budget 28) this covers 22 of the 29 open magnitude patterns (checked
directly: remaining defect 0, 2, 4, 6 for 7, 6, 6, 3 open patterns; the
other 7 have remaining defect 8 to 12). Closing it would close whole
patterns for the first time since the frontier was set.

It needs new structure: with no free coordinate every derivative Delta_u f
has negative quartics, so the nonnegative quartic complex behind 014 to 017
is unavailable (1513 lines 11 and 60).

## Steps

(a) Typed frontier for the 22 rows with an independent reader that rederives
    the 39 / 17 / 22 split from the cost table and the ledger, binding the
    reasons union 14 is forced and pinning the existing partial reductions
    ((2^4): 52 of 67 classes excluded; (2^4,1); (3,2,1^5) branches).
(b) Positive controls from the 012 n = 13 witnesses: done, CONTROLS.md.
(c) The key lemma: at a coordinate u in exactly one negative quintic, with
    little other incident residual, no ternary derivative. First as an exact
    row model (Fourier-side variables, as in 017 `model.py`, with l_Q = -m and
    integer cubic coefficients), piloted with CP-SAT, then structure.
(d) Placement enumeration for N <= 7 supports, only after (c).

Unit-heavy inventories (9 or more supports) are expected to need a global
argument; no per-placement case trees there.
