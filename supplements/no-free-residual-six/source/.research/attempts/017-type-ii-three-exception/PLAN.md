# 017: the 24 open Type II shapes (three exceptions)

Claude Code (Anthropic), 2026-10-23, for Alexander Richard Towell.
Plan only. Started on the user's request after checkpoint 1532. Global
status: OPEN.

## Target

The 24 OPEN rows of `H/one-free-residual6-frontier-cycle1532.json`. Each
is a local problem about one ternary derivative p = Delta_u f on thirteen
coordinates: c in {1,2}, p(0)=1, p(e_v)=0, ordinary quadratic
coefficients 0/1, quartic numerators 0/1 except as stated, pair
numerators -1/0 except three departures. Twenty-three shapes have three
exceptional pairs (numerators -2 or +1); one has -2 on {0,1}, -2 on
{2,3} and a doubled quartic on {0,1,2,3}.

The 23 pair-only shapes, by the graph G of the exceptional pairs:

| G | sign classes | open |
|---|---|---|
| triangle | ---, --+, -++, +++ | 4 |
| star K(1,3) | ---, --+, -++ (+++ excluded in 016) | 3 |
| path P4 | middle - or +, ends --, -+, ++ | 6 |
| path P3 plus disjoint edge | path --, -+, ++; edge - or + | 6 |
| matching 3K2 | ---, --+, -++, +++ | 4 |

## What carries over from the two-exception theorems

Pair inversion makes every exceptional pair an edge (m = 1) with a
six-edge even link (-2) or a C3 (+1); baseline edges have C4 or C5
links. The identities Q_v = 2D_v - 4, E = 49 + c, T = 72 + 2c and
p(X) = 1 - chi(K[X]) for X in the support are constant-free and do not
depend on the number of exceptions. The disconnected ordinary-link
picture (two six-vertex projective planes, 42 forced edges, M = 7 + c
<= 9 cross edges) depends only on the ordinary centre.

## What has to be redone

1. Triangle incidence. With two exceptions every triangle has a baseline
   pair, so every present triangle lies in exactly two tetrahedra. Here a
   triangle can have three exceptional pairs, only when G is a triangle.
   A +1 pair's link is C3, so such a triangle still has incidence 0 or 2
   unless all three pairs are -2. Only the triangle --- shape can have a
   triangle in four tetrahedra (three mutually centred bowties).
2. Split -2 links. The accepted one-six-edge argument excludes a 2C3
   link at a -2 pair with a private endpoint. In P4 with a -2 middle, the
   triangle shapes and the star centre, neither endpoint is private, so
   the splitting count has to be redone with the other exceptions present.
3. Exceptional vertex links. A vertex meeting z exceptions has z special
   vertices in its unit link (degree 6 for a C6 partner, 3 for a +1
   partner, two degree-3 copies for a split partner). Classify every
   possible union of closed surfaces with chi = 2 + (number of splits) on
   at most 12 vertices after merging copies. Spheres come from the 015
   enumeration; projective-plane components have at most six plus the
   number of degree-6 vertices, so at most nine vertices, and need an
   enumeration of RP2 triangulations to nine vertices.
4. Disconnected ordinary links. Redo the cross-edge count with up to six
   exceptional vertices, using the degree lower bounds from step 3 (the
   cross degree of v is at least D_v - 6), plus the universal-neighbour
   case.
5. Root and placements. Root at the vertex with the most constrained
   link (the star centre, a P4 middle vertex, a triangle vertex). The
   root link catalog comes from step 3. Place the remaining exceptions
   around the root up to the root link's automorphisms, with every
   permutation checked on the full face set, as in the disjoint theorem.
6. Models. Face indicators, downward closure, two tetrahedra per
   triangle (four allowed only where step 1 allows), pair valences, flag
   rows where accepted, every induced Euler bound 0 <= chi <= 2, the
   fixed root link. A successor to the 014 row reader for the new rows.
7. Certificates. 014 pipeline: CP-SAT core, CNF, CaDiCaL LRAT, pinned
   lrat-trim, independent clause-soundness reader.
8. Shape 1 (two -2 pairs and their doubled quartic): the pair links are
   the doubled edge plus nothing or a unit C4, so its local structure
   differs and it gets its own structural note.

Steps 1 to 4 are written arguments with small exact checks, as in 016.
Steps 5 to 7 are the large build. Each step gets a fresh AI review before
it is used.

## Status (2026-10-23)

- Steps 1 to 3: VERTEX-TYPES.md. Outside triangle --- every -2 link is C6
  and every exceptional vertex link a sphere. Reviewed by Claude and Codex
  (sound after wording fixes).
- Step 4: CROSS-EDGES.md. Every ordinary vertex link is a sphere in all 23
  shapes at c = 1, 2 (exact search `step4_count.py`). Reviewed by Codex
  (sound after one code fix and two proof details, applied).
- Near-flag rows: NEAR-FLAG.md (`near_flag.py`). Ordinary links are the six
  deltahedra (all flag); links of types (0,1), (0,2), (1,0), (1,1), (2,0)
  are near-flag. Reviewed by Codex with SPECIAL-SHAPES.md.
- Step 5: `cases.py`: 2775 cases over 22 shapes, plus 81 (triangle ---)
  and 328 (shape 1) rooted at an ordinary vertex (SPECIAL-SHAPES.md).
  `cover_reader.py` checks all three covers.
- Steps 6 and 7: `model.py`, `certify017.py`, `reader017.py` (hardened
  after REVIEW-chain-codex.md). Positive control: the 16-cell at n = 8.
- Result: CERTIFICATES.md. All 3184 cases of the three covers (24 shapes)
  certified at c = 1 and 2; `read_all.py` ALL_CASES_VERIFIED.
