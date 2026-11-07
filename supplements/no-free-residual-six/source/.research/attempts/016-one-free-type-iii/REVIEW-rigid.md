# Independent adversarial review of TYPE-II-RIGID-SHAPES.md (2026-10-23)

Reviewer: a fresh Claude subagent given the note, its sphere-fact checker,
the shape enumeration and the 1513 and doubled-quartic sources. AI review,
not human review. Verdict: SOUND_WITH_FIXES. Shapes 6, 2, 3, 7, 5 sound as
written; shape 4 missed one sub-case; shape 1 correctly left open.

## What the reviewer independently did

- Checked the identities behind (W), (P), (U) numerically with exact
  rationals on 200 random instances (n = 7): pair inversion, the cubic
  coefficient as minus half the weighted quartic incidence (so (P) holds
  with weights 2), A_x + P_x = 8 and 4d = A_x + 3P_x for any c.
- Enumerated even simple graphs with 1..6 edges: 3, 4, 5 edges give only
  C3, C4, C5; 1 or 2 edges give none; 6 edges give C6, two triangles, or
  the bowtie.
- Recomputed every degree set, tetrahedron count, chi = 3, decomposition
  and vertex bound in shapes 4, 5, 7, and the split cases.
- Verified (S3), (S4), (S6) by hand, and enumerated all connected closed
  surfaces on 4..6 vertices (the only chi = 1 one is the six-vertex
  all-degree-5 surface).
- Re-derived the shape list by its own brute force (7 covered shapes,
  matching type2_shapes.py and the note's labels); confirmed no excluded
  shape borrows a fact from another; confirmed shape 1 does not close
  locally (bipyramid plus six-vertex RP^2 fits in 11 vertices).
- Ran test_rigid_shape_facts in normal and -O mode.

## Issues and response

1. Shape 4: the six-edge link of J can also be a bowtie. Fixed: the shared
   vertex w would put the triangle {0,1,w} in four tetrahedra, while the
   baseline pair {0,w} has a cycle link, so every triangle on it lies in
   exactly two.
2. Shape 4, C6: show that a chi = 1 component containing the degree-6
   vertex holds no degree-3 vertex. Added (at least seven vertices, all
   others degree 5).
3. Tool (U): the six-vertex lower bound for chi = 1 needs
   E = 3(V - 1) <= V(V - 1)/2. Added.
4. Cosmetic: (U) now lists C6 among single-cycle links; (S3) is no longer
   called pure curvature.
