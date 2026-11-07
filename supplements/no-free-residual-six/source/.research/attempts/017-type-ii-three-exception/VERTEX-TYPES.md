# Three exceptions: triangle incidence and exceptional vertex links

Alexander Richard Towell, with Claude Code (Anthropic) assistance. Proposed
written lemmas with an exact check (PLAN.md steps 1 to 3). Independently
reviewed by Claude (REVIEW-vertex-types.md) and by Codex (OpenAI;
REVIEW-vertex-types-codex.md): sound after the fixes below. No original magnitude pattern is excluded.

## Setting

A pair-only open Type II shape (PLAN.md): p = Delta_u f on thirteen
coordinates, c in {1,2}, p(0)=1, p(e_v)=0, ordinary quadratic coefficients
m in {0,1}, quartic numerators 0/1, pair numerators -1/0 except three
exceptional pairs with numerator -2 or +1. Let G be the graph of the
exceptional pairs. Write the link of a pair A as the graph of quartics
D containing A (edge D minus A), all of weight one here.

Pair inversion 4m_A = k_A + |link A| and even link degrees (cubic
integrality) give: a baseline edge (m = 1) has link C4 or C5; a +1 pair
has m = 1 and link C3; a -2 pair has m = 1 (m = 0 would leave two edges)
and a six-edge even simple graph: C6, two disjoint triangles (split) or
two triangles sharing one vertex (bowtie).

## Lemma 1 (triangle incidence)

The number of tetrahedra containing a triangle {a,b,y} is the degree of y
in the link of ab (all quartic weights are one), and equally of b in the
link of ay. In a C3, C4, C5, C6 or two disjoint triangles it is 0 or 2. It can be 4 only at the centre of a bowtie, so only if all
three of ab, ay, by are -2 pairs with bowtie links centred at the third
vertex. Hence outside the shape "G a triangle, all three -2" there is no
bowtie and every present triangle (one lying in at least one tetrahedron)
lies in exactly two tetrahedra.

## Lemma 2 (unit links at an exceptional vertex)

Outside the triangle --- shape, fix a vertex x and split every -2 partner
of x whose link is split into two copies, one per triangle. As in the
two-exception theorems, P_x = 2d - 4 (d partners) gives a disjoint union
of closed surfaces U_x with chi = 2 + s on d + s vertices, d <= 12, s the
number of split partners. Degrees: 6 at a C6 partner, 3 at a +1 partner
and at each split copy, 4 or 5 elsewhere; the two copies of one partner
are non-adjacent with disjoint neighbourhoods. Every component has a
vertex of degree at most 5, so chi >= 1 and components are spheres or
projective planes. A sphere component has n = 12 - 2 n3 - n4 + n6 vertices
by curvature, of which at most n3 / 2 copy pairs merge; with n6 <= 3 and
at most d <= 12 merged vertices this gives n <= 12 (curvature alone would
allow 15). Projective planes have at most 6 + n6 <= 9 vertices.

`vertex_types.py` takes every sphere on at most 12 vertices (015
enumeration) and every projective plane on at most 9 (`surfaces.brute`,
a closing search with no classification theorem, cross-checked against
vertex splitting from the orders 6 and 7 and the census 1, 3, 16, 134),
and lists all multisets of components with a consistent assignment of
the special vertices, for every type (c6, s, p) with 1 <= c6 + s + p <= 3.
Result (sphere orders of a single-sphere link; "none" means no
configuration at all):

| c6, split, +1 | links |
|---|---|
| 1,0,0 | sphere, 9..11 (accepted three-type classification) |
| 0,0,1 | sphere, 7 (accepted) |
| 1,0,1 | sphere, 8, 9 (accepted adjacent -2,+1 root) |
| 2,0,0 | sphere, 8..12 |
| 0,0,2 | sphere, 5, 6, 8 |
| 2,0,1 | sphere, 8..11 |
| 1,0,2 | sphere, 7, 8 |
| 3,0,0 | sphere, 9..12 |
| 0,0,3 | none (016 star) |
| 0,2,0 | two spheres, orders (5,5), (5,6), (5,8), (6,6), (6,8) |
| 1,2,0 | two spheres, orders (5,7), (5,8), (6,7), (6,8) |
| every other type with a split | none |

So a split occurs only at a vertex with exactly two split partners, and
the link of an exceptional vertex with no split partner is always a
single sphere (ordinary vertices are type (0,0,0), not classified here;
see CROSS-EDGES.md). In `vertex-types-result.json`, `configurations`
counts combinations of component signatures, not sphere classes, and
`only_single_sphere` is vacuously true on an empty row. The copy rule is
checked before merging; checking disjointness after all merges is
stronger and only removes candidates (Codex checked that every listed
order pair keeps valid witnesses).

## Corollary

Outside the triangle --- shape every -2 link is C6 and every exceptional
vertex link is a sphere with the degrees above. Proof: the link of a pair
xb is the same graph seen from x and from b, so a split pair is split at
both endpoints. The split pairs form a subgraph H of G in which, by
Lemma 2, every vertex has degree exactly 2. A nonempty such H with at
most three edges is a triangle of -2 pairs, which is the excluded shape.

The rows 1,0,0, 0,0,1, 1,0,1 and the empty rows 0,1,0 and 0,0,3 reproduce
the accepted two-exception statements and 016; they are controls, not
premises.

## Disconnected ordinary links (first count, PLAN.md step 4)

At an ordinary w whose link is two six-vertex projective planes on A and
B, every other vertex v has D_v = 6 + cross(v) and the cross edges number
M = 7 + c <= 9. Using the minimum sphere order at least 6 allowed above
for each exceptional vertex, the case "every ordinary vertex has cross
degree at least 2" gives a cross-degree sum above 2M for 19 of the 23
shapes at both constants. The four +1-heavy shapes (triangle +++, P4 +++,
P3+K2 +++, 3K2 +++) meet 2M = 18 exactly at c = 2, and the universal-
neighbour case needs a refinement wherever an exceptional vertex can
have cross degree 0 (a +1,+1 vertex with the six-vertex link). These
remain to be done; they are not claimed here. The triangle --- row does
not use Lemma 2 (which excludes that shape): P_x = 2d - 4 with pair
inversion gives d >= 6 + n(-2) - n(+1)/2 directly, so each of its
vertices has d >= 8 and the bound is 24 > 18. When the cross-degree 0
and 1 cases are done, the 006 six-vertex-link obstruction must be
re-checked with up to six exceptional vertices present.

## Scope

Lemma 2 assumes no bowtie, so the triangle --- shape and the doubled-
quartic shape 1 need separate treatment. Conditional on the 015 sphere
enumeration (Steinitz-Rademacher, pynauty) and the identities above.
Global status: OPEN.
