# Three exceptions: triangle --- and the doubled-quartic shape 1

Alexander Richard Towell, with Claude Code (Anthropic) assistance. Proposed
structural notes for the two shapes the main cover leaves out. Reviewed
by Codex (OpenAI; REVIEW-special-codex.md): sound after the wording fixes
applied here. No original magnitude pattern is excluded.

Both shapes are rooted at an ordinary vertex, so neither needs a
classification of its exceptional vertex links.

## Triangle --- (-2 on ab, bc, ca)

1. Triangle incidence. By VERTEX-TYPES.md Lemma 1, abc is the only
   triangle that may lie in four tetrahedra; every other present triangle
   lies in exactly two. The model gives abc a second binary t2 (incidence
   2 (t + t2)), with cubic coefficient -(t + t2).
2. Degrees. P_x = 2d - 4 and pair inversion give d >= 6 + n(-2) - n(+1)/2,
   so a, b, c each have at least 8 neighbours (REVIEW-vertex-types.md).
3. Ordinary links. CROSS-EDGES.md covers triangle --- (its F1 uses only
   item 2), so every ordinary link is a sphere with degrees 4 and 5, one of
   the six deltahedra (NEAR-FLAG.md), all flag.
4. Root. a has at least 8 neighbours, at most two of them exceptional, so
   it has an ordinary neighbour w. Label w as 0, its link by a deltahedron
   in `deltahedra.json`, a as a link vertex, b and c as link vertices or
   non-neighbours. `cases.py --triangle` lists 81 cases up to Aut(L) and
   non-neighbour relabelling; `cover_reader.py` checks that they cover all
   1285 labelled placements.
5. Model rows: the exact rows, flag rows at every ordinary vertex except
   the root, none at a, b, c (their links may split or pinch), implied rows.

## Shape 1 (-2 on {0,1} and {2,3}, doubled quartic D0 = {0,1,2,3})

1. Pair links (TYPE-II-RIGID-SHAPES.md (W), (P)). The pairs 02, 03, 12, 13
   have m = 1, k = -1 and link the doubled edge plus a unit triangle; 01 and
   23 have link the doubled edge plus nothing (m = 0) or a unit C4 (m = 1).
   Every pair not inside D0 has a unit link.
2. Triangle incidence. A triple inside D0 has weighted incidence 2 or 4
   (the doubled quartic plus 0 or 2 unit ones), encoded by t + t2. Any
   other triple T has incidence 0 or 2: if |T meet D0| <= 1 all its pairs
   are baseline with unit links that are empty, C4 or C5; if T = {d1, d2, y} with y outside
   D0, the incidence is the unit degree of y in the link of d1d2, which is
   a unit C4, a unit triangle or empty. Every quartic containing T contains
   y, so is unit.
3. Degrees. At x in D0, 3 P_x = sum over r of the weighted link size of xr
   = 6d - 12, where a partner contributes 4 or 5, xr inside D0 with
   k = -1 contributes 5, the -2 pair contributes 6 (m = 1) or 2 (m = 0,
   not a partner). Either way 6d - 12 >= 4d + 4, so d >= 8.
4. Ordinary links. A vertex outside D0 meets no exception and no doubled
   quartic, so all its pair links are unit C4 or C5, its unit link is a
   union of closed surfaces with chi = 2 (P_v = 2D_v - 4) and degrees 4, 5.
   The identities still give E = 49 + c (weights included). If the link of
   such a w were two six-vertex projective planes on A and B, then as in
   CROSS-EDGES.md M = 7 + c <= 9, D_v = 6 + cross(v) and each side sums to
   M. The vertices of D0 have cross >= 2 by item 3. An ordinary v has
   cross >= 1 (cross 0 needs degree-3 link vertices, F2) and cross 1 forces
   a vertex of cross 6 on the other side (F3; the link of v is then a
   sphere on 7 vertices with degrees 4, 5). If every ordinary vertex has cross >= 2 the
   two sides sum to at least 24 > 18; otherwise one side has a cross-6
   vertex and five more of cross >= 1, at least 11 > 9. So every ordinary
   link is a deltahedron, hence flag.
5. Root. 0 has at least 8 neighbours, at most 3 in D0, so it has an
   ordinary neighbour w. Label w as 0 (so D0 is relabelled), its link a
   deltahedron, the old vertex 0 a link vertex, the rest of D0 link
   vertices or non-neighbours. `cases.py --shape1` lists 328 cases;
   `cover_reader.py` checks they cover all 8847 labelled placements and
   that each case's doubled quartic is the union of its two -2 pairs.
6. Model rows: l_D0 = 2 (a variable fixed to 1 with coefficient 2), t2 on
   the four triples inside D0, flag rows at ordinary vertices except the
   root, none at D0, implied rows. `reader017.py` rebuilds these from the
   case alone.

Global status: OPEN.
