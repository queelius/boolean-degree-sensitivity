# Independent adversarial review of TYPE-I-CLOSURE.md (2026-10-23)

Reviewer: a fresh Claude subagent given the note, its checker and the 1395,
1513 and 1523 sources, and asked to break each step, in particular to check
the nonexistence claim with a method independent of 015 and 006. AI review,
not human review. Verdict: SOUND; three low-severity suggestions.

## What the reviewer independently did

- Wrote its own disk-filling search (no 015/006 code or catalogs): fill the
  disk left by removing the degree-7 star from its 7-cycle boundary inward,
  generating each boundary-labelled disk once; rebuild every result as a
  sphere and check closedness, cyclic links and Euler characteristic;
  count classes with pynauty.
  - Unconstrained control: 42, 330, 2310, 16170, 115500 disks for 0..4
    interior vertices, equal to Brown's (1964) formula. Post-filtering all
    134,352 without pruning gives 0 targets; the relaxed filter (degree 3
    allowed) gives exactly one sphere at each of orders 8, 9, 10, matching
    the note's control, so the pruning is not over-eager.
  - Constrained search: no target for up to 7 interior vertices, which is
    every order allowed by curvature (n <= 14).
- Supplied a short human proof valid at every order (no chords, then a
  run-counting and curvature argument in the chordless case). The parent
  checked it step by step; it is now the note's primary proof.
- Confirmed that Type I's derivative has exactly 1395's displayed form
  (c = k_u in {1,2}; -3 on A; other pairs -1/0 because the budget is
  spent; quartics 0/1 because u is free and there is no quintic departure;
  m_J = f(J+u) in {0,1}).
- Went through 1395's equation (1), cubic integrality, the baseline-link
  step, P_w = 2d_m - 4, the m_A = 0 exclusion, the C3+C4 split and the
  sphere conclusion: all use only the single derivative. The
  three-derivative remarks are not used.
- Confirmed the degrees in L_w are exactly 7 (other endpoint) and 4/5
  (baseline edges, C4/C5 links), and |L_w| <= 12.

## Suggestions and response

1. Remove the catalog premise by adding the human proof. Done; the
   enumeration and the reviewer's search are recorded as controls.
2. Name the identities used instead of "pair-inversion identities", and
   do not call two cross-checked catalog filters fully independent. Done.
3. Say "the accepted 11/12 range has no instances" instead of "vacuous",
   and test `has_pattern` on a synthetic positive. Done.
