# Review: VERTEX-TYPES.md (017 steps 1 to 4)

Adversarial review by Claude Code (Anthropic), 2026-10-23, for Alexander
Richard Towell. Inputs reviewed: VERTEX-TYPES.md, PLAN.md, vertex_types.py,
surfaces.py, test_surfaces_vertex_types.py, 015 spheres.py, and the cited
background (006 two-negative, two-mixed, disjoint notes; 016
TYPE-II-RIGID-SHAPES.md "Setting and tools", identities W, P, U). No
existing file was modified. Scratch checks (not pinned, not evidence by
themselves):

- /tmp/claude-1000/-home-spinoza-github-math-theory/5b9124f3-8322-467a-bb3d-8f1c7e442523/scratchpad/review017/indep.py
- /tmp/claude-1000/-home-spinoza-github-math-theory/5b9124f3-8322-467a-bb3d-8f1c7e442523/scratchpad/review017/noconstraint.py
- /tmp/claude-1000/-home-spinoza-github-math-theory/5b9124f3-8322-467a-bb3d-8f1c7e442523/scratchpad/review017/step4.py

The 017 test file passes (7 tests) in normal and -O mode.

## Verdict summary

| Claim | Verdict |
|---|---|
| Setup (pair inversion, link shapes C4/C5, C3, C6/2C3/bowtie) | sound |
| Lemma 1 (triangle incidence, bowtie only in triangle with three -2) | sound; two wording fixes |
| Lemma 2 setup (chi = 2 + s, d + s vertices, degrees, copy rules, chi >= 1, order bounds) | sound; every constraint is necessary, none too strong |
| vertex_types.py implements the stated combination problem | sound; independent re-implementation agrees on all 19 types |
| surfaces.brute is a complete enumeration | sound (proof sketch below), plus census agreement |
| Corollary (split pairs 2-regular, hence triangle of -2) | sound |
| Step 4 count (19 of 23 contradicted, four tight at c = 2) | numbers reproduced exactly; the triangle (-,-,-) row is sound only after a stated fix |

Category reminder. Lemma 2 is a necessary condition on vertex links (a
catalog of the links that can occur). Its empty rows are local exclusions
of vertex types, conditional on the identities W, P, U, the constant-free
relations quoted from 006, and the sphere/RP2 catalogs. The step-4 count is
an exclusion of one subcase only (every ordinary non-centre vertex with
cross degree at least 2); it excludes no shape. No original magnitude
pattern is excluded by anything here.

## 1. Setup and Lemma 1

Pair inversion with weight 4m_A - k_A and even link degrees: m = 0 gives
weight 0 or 1 for baseline pairs, so the link is empty; m = 1 gives 4 or 5
edges, and the only even simple graphs are C4 and C5. A +1 pair has weight
4m - 1, so m = 1 and the link is C3. A -2 pair has weight 4m + 2; m = 0
would give two edges, which no even simple graph has; m = 1 gives six
edges, and the even simple graphs with six edges are exactly C6, 2C3 and
the bowtie (two triangles sharing an edge has degree-3 vertices). Sound.

Lemma 1. A tetrahedron {a,b,y,z} containing triangle aby is exactly an edge
yz of link(ab) at y, so the incidence equals deg_y link(ab) (all quartic
weights are 1 here), and by symmetry deg_b link(ay) and deg_a link(by).
In C3..C6 and in 2C3 every degree is 0 or 2; in the bowtie only the centre
has degree 4. Incidence 4 therefore forces all three of ab, ay, by to be
six-edge links, hence -2 pairs, each a bowtie centred at the opposite
vertex. Conversely, any bowtie forces such a triangle, so G must be a
triangle with three -2 pairs. Sound.

Wording fixes (no change of substance):
- "In a single cycle it is 0 or 2" should read "in C3, C4, C5, C6 or 2C3";
  2C3 is not a single cycle but also has degrees 0 or 2, and the lemma needs
  it.
- Define "present triangle" as a triangle lying in at least one
  tetrahedron (so incidence is exactly 2, not 0 or 2).

## 2. Lemma 2 setup

Checked each step:

- Vertices of U_x. Every partner r (m_xr = 1) has a nonempty link, and a
  non-partner has an empty link, so U_x has exactly d vertices, d <= 12.
- chi. P_x = 2d - 4 follows from U (A_x + P_x = 8 and 4d = A_x + 3P_x) and
  uses no link structure. Faces of U_x are the P_x tetrahedra at x; an edge
  rs of U_x is the triangle xrs, which by Lemma 1 lies in exactly two
  tetrahedra, so E = 3F/2 and chi = d - (d - 2) = 2.
- Splitting. For a 2C3 partner r, every vertex t adjacent to r lies in
  exactly one triangle of link(xr), so both faces of U_x through the edge rt
  go to the same copy; each vertex link stays a single cycle, and this
  remains true when t is split too. V rises by s, E and F do not change:
  chi = 2 + s on d + s vertices. Sound.
- Degrees 6 / 3 / 3 / 4-or-5. Sound.
- Copy rules. Copies are non-adjacent (r is not in link(xr)) and their
  neighbourhoods are the vertex sets of the two disjoint triangles. Both are
  necessary. The code applies them to split labels; the true condition is on
  merged originals and is stronger (also forbids r' ~ t' and r'' ~ t'' for
  a split t). I re-ran the search with the merged condition (no common
  merged neighbour, no multi-edge after merging): identical result for
  every type. So the weaker form used in the code is safe and loses nothing.
- chi >= 1. At most three degree-6 vertices and at least four vertices per
  surface give each component a vertex of degree <= 5, so
  sum(6 - deg) = 6 chi > 0. Sound.
- Order bounds. A component's vertices cover at least n - floor(n3/2)
  originals, so n - floor(n3/2) <= 12. With n = 12 - 2 n3 - n4 + n6 and
  n6 <= 3 this gives n <= 12 for n3 = 0, 1 and n <= 11 for n3 >= 2. RP2:
  n = 6 - 2 n3 - n4 + n6 <= 9. Sound. The note states "curvature bounds
  sphere components by 12 vertices" without the merge step; the docstring
  has it, and the note should too, since the bare curvature bound for n3 = 0
  is 15 and only the budget d <= 12 brings it to 12.
- Budget. The code checks sum(n) - s <= 12, which is exactly d <= 12.

No constraint is too strong. Two of them are load-bearing, so their
derivation matters (noconstraint.py): dropping the copy rules makes
(0,1,0), (0,1,2), (0,2,1), (0,3,0), (1,1,0), (1,1,1), (2,1,0) nonempty;
dropping the budget makes (0,1,0) and (2,1,0) nonempty and lets two-RP2
links into (2,0,0) and (3,0,0). Both constraints are derived correctly above.

Minor wording: the table entry "(0,2,0) two spheres (orders 5, 6, 8 each)"
should list the pairs: (5,5), (5,6), (5,8), (6,6), (6,8). The pair (8,8) is
excluded by the budget. For (1,2,0) the pairs are (5,7), (5,8), (6,7),
(6,8).

## 3. Code (vertex_types.py)

Read line by line. component_types: degree filter {3,4,5,6}, n6 <= 3,
n3 <= 6, all necessary. max_internal_pairs returns the maximum matching
size among compatible degree-3 pairs (correct; matchings of every smaller
size exist). realizable: sums n6 = c6 and n3 = p + 2s, any number of
internal pairs up to that maximum, external copies pairable across distinct
components iff max part <= half the total (correct criterion for a perfect
matching in a complete multipartite graph); the final remainder check is
then automatically equal to p. The summary tuple (chi, n, n6, n3, max
pairs) is a sufficient statistic because all non-paired degree-3 vertices
play interchangeable roles. classify allows 1 to 2 + s components with
replacement. No bug found that could empty a type.

Independent re-implementation (indep.py): enumerate multisets of actual
component surfaces (76 relevant classes, no summarising), build the
labelled disjoint union, and search every matching of size s among the
degree-3 vertices under the copy rules, in both the label form and the
merged form. Result: per-type component patterns identical to
vertex-types-result.json for all 19 types, including every empty row and
both split rows.

## 4. Catalog completeness (surfaces.brute and 015)

surfaces.brute is complete. Proof sketch: fix any connected closed surface
S on n vertices and a face of it labelled {0,1,2}. The search always holds a
labelled subcomplex P of S. Its least open edge ab lies in exactly two faces
of S, one in P; the other's third vertex is either already labelled (tried
among the old labels) or unlabelled (gets the next label). The prunes never
cut a branch inside S: no edge of S lies in more than two faces, and a
vertex link of P is a subgraph of a cycle, hence paths or the whole cycle,
which is exactly what _ok_partial accepts. P grows strongly connected; when
it has no open edge, any face of S outside P would put a third face on an
edge of P, and S is strongly connected, so P = S and used = n. The
certificate (vertex/face incidence graph with a two-colouring) is a complete
invariant of the complex.

Census check: spheres 1, 1, 2, 5, 14, 50, 233, 1249, 7595 at orders 4 to 12
and RP2 1, 3, 16, 134 at orders 6 to 9, both equal to the published Lutz
census. Since the classes are distinct and every one is verified to be a
surface of the right type, the catalogs are complete.

## 5. Corollary

The link of pair xb is one graph, so "split" is a property of the pair and
holds at both endpoints. By Lemma 2 (s = 1 and s = 3 rows empty, together
with (0,2,1) and (2,1,0) empty), each vertex of H has H-degree 0 or 2. A
2-regular simple graph with at most three edges is empty or a triangle, and
a triangle of split pairs is a triangle of -2 pairs, i.e. G = triangle
(-,-,-). Sound. Hence outside that shape every -2 link is C6 and every
exceptional vertex link is a single sphere with the stated degrees (s = 0
rows are single spheres only).

## 6. Step 4 count

step4.py enumerates the 23 shapes by orbit under the graph automorphisms
(triangle 4, star 3 after removing +++, P4 6, P3+K2 6, 3K2 4) and computes
2(12 - e) + sum over exceptional v of max(minorder(v) - 6, 0), with minimum
orders >= 6 taken from the independent search: (1,0,0) 9, (0,0,1) 7,
(1,0,1) 8, (2,0,0) 8, (0,0,2) 6, (2,0,1) 8, (1,0,2) 7, (3,0,0) 9.
D_v = 6 + cross(v) is correct (w plus five side-mates), and 2M = 2(7 + c)
is 16 or 18.

Result: 19 shapes give at least 22, so they are contradicted at both
constants; triangle +++, P4 +++, P3+K2 +++ and 3K2 +++ give exactly 18,
contradicted at c = 1 and tight at c = 2. This matches the note.

Gap, with fix. The triangle (-,-,-) shape is counted among the 19 using the
Lemma 2 minimum (2,0,0) = 8, but Lemma 2 and the Corollary are stated to
exclude that shape (bowties, and split triangles of -2 pairs, are possible
there). The conclusion survives with an elementary bound that needs no link
classification: from P_x = 2d - 4 and pair inversion,
sum_r |link(xr)| = 3 P_x = 6d - 12, with 4 or 5 per baseline partner, 6 per
-2 partner and 3 per +1 partner, so

    2d - 12 = n_(k=-1) + 2 n_(-2) - n_(+1),   hence   d >= 6 + n_(-2) - n_(+1)/2.

Each vertex of the triangle (-,-,-) has d >= 8 and cross degree at least 2,
giving 18 + 6 = 24 > 18. With this sentence added the step-4 count is sound
for all 19 shapes. (The elementary bound alone does not reproduce the other
rows; there the Lemma 2 minima are needed.)

Scope notes for step 4 (not errors, since the note claims only this
subcase): the complement "some ordinary vertex has cross degree at most 1"
includes cross degree 0, which 006 handled by the six-vertex-link
obstruction; when step 4 is completed, that obstruction should be re-checked
with up to six exceptional vertices on the sides, and the universal-neighbour
argument must handle the (0,0,2) vertices with cross degree 0, as the note
already says.

## Remaining dependencies

Identities W, P, U and E = 49 + c, M = 7 + c are taken from accepted
notes and were not re-derived here. The 015 sphere catalog and the RP2
catalog are inputs; their completeness rests on the census agreement and
the brute-force argument above. Global status: OPEN.
