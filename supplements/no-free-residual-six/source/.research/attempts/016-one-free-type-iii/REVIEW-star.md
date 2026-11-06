# Independent adversarial review of TYPE-II-PLUS-STAR.md (2026-10-23)

Reviewer: a fresh Claude subagent given the note, the rigid-shapes tools,
the Type II setting, and (as a follow-up) the private-vertex reduction as
used with three departures. AI review, not human review. Verdict: SOUND;
two minor fixes.

## What the reviewer independently did

- Link shapes at x: +1 pairs have weight 3 and a simple link, so C3;
  baseline weights 0, 1, 4, 5 with 1 failing parity, and even simple graphs
  with 4 or 5 edges are only C4, C5 (non-cycle even graphs need 6 edges,
  which only a -2 pair has). Vertices of U_x are exactly the r with
  m_xr = 1, so d <= 12.
- Re-derived A_x + P_x = 8, 4d = A_x + 3P_x, P_x = 2d - 4 (no c), chi = 2;
  components chi >= 1, so one sphere or two RP^2, and the K6 argument
  excludes the latter.
- Hand proof of (S3): (1,1) needs a degree-5 vertex on five vertices;
  (3,3,3,5,5,5) contains K_(3,3).
- Its own screen with the 015 enumerator (OEIS counts checked): only the
  three-+1 case is empty; orders as in the note.
- Private-vertex reduction with three departures: went through lines 38-82
  of 006/two-exception-positive-extension.md; every step reads only
  coefficients on sets containing x plus p(0), p(e_x), so a third
  departure elsewhere, even touching D's other vertices, cannot interfere,
  at any c. `private_quartic()` implements exactly "some doubled quartic
  has a vertex outside the union of the other two departures".
- Ran test_type2_shapes and test_rigid_shape_facts in both modes. Did not
  re-count the 136 shapes or the 105 exclusions independently (relied on
  REVIEW-rigid.md's brute force and the pair-only test).

## Issues and response

1. The closing screen cited no script. Fixed: `vertex_type_screen.py` with
   `test_vertex_type_screen.py` (normal and -O).
2. "Matching the accepted catalogs" was checked only against their written
   orders. Reworded.
3. The five-vertex case needs only maximum degree 4. Reworded, with the
   K_(3,3) argument for (3,3,3,5,5,5).

Caution recorded in the note: bowtie links of a -2 pair are not excluded
automatically when two -2 pairs share a vertex.
