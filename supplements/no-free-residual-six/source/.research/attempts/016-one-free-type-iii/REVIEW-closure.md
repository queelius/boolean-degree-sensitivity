# Independent adversarial review of TYPE-III-CLOSURE.md (2026-10-23)

Reviewer: a fresh Claude subagent given the closure note and every cited
source, and asked to break each claim. It did not re-review the internals
of EXTENSION-plus-plus-c3.md (reviewed separately, REVIEW-plus-plus-c3.md).
AI review, not human review. Verdict: SOUND_WITH_FIXES; nothing fatal.

Before this review, three read-only subagent audits had located the
constant-dependent steps of the mixed, disjoint and doubled-quartic sources;
the parent re-read each cited passage before drafting the note.

## What the reviewer independently did

- Translation: P_S = k_(u union S) from h = 1 - 2f alone; c = k_u; cubic
  numerators through u become pair numerators of p, positive quintic 2
  becomes l_D = 2; no negative quintic meets the free u; ordinary quadratic
  coefficients are f(1_uab) by Mobius inversion. The nine subcases (two
  pairs adjacent or disjoint with three sign patterns, three doubled-quartic
  combinations) are exhaustive and all in the table.
- Cross-edge counts at c = 3 for the mixed and disjoint theorems, with the
  source of every degree bound; found no other constant dependence (catalog
  filters, root link covers, placement quotients, vertex-order, flag and
  induced-Euler rows are link-degree derived; in the producer only
  face_count uses edge_count).
- Certificates: rebuilt the models at c = 0, 1, 2, 3 and confirmed the
  selected rows identical at their original indices, then replayed: both
  mixed compact proofs, all 66 disjoint compact proofs (47 of -2,-2 and 19
  mixed), and all 69 disjoint branch leaves across 28 cases. Branch-tree
  coverage was not re-checked (inherited, constant-free). Scripts are in
  the session scratchpad, not frozen.
- Doubled quartic: re-derived the private-vertex argument (chi = 3 link,
  surface split forces (3,3,3,4,5) or (3,3,3,5,5,5), the latter needs nine
  faces on eight); it uses only data incident to x, not c, the special pair
  e or the six-unit context; it covers J meeting D since |D minus J| >= 2.
- Adjacent -2,-2: the 1527 authority's scope is constant [0,1,2,3] with the
  same hypotheses.

## Issues and response

1. Wording: "six same-side neighbours plus w" should be five plus w, and the
   degree bounds 7, 9, 7 need their sources. Fixed.
2. Wording: "the only constant-dependent step" overstated; the (+1,+1)
   closing scan range E <= 52, the unused coefficient-two branch and the
   models' face-count rows also involve c. Restated precisely.
3. Wording: the common facts hold for the pair theorems (and at a -2
   endpoint only after the C6 step), not for the doubled-quartic link at x.
   Restricted.
4. Precision: the replay statement now says exactly what was rebuilt and
   replayed, what is inherited, and that the scripts are not frozen.
5. Citation: lines 53-55, not 50-55. Fixed.
