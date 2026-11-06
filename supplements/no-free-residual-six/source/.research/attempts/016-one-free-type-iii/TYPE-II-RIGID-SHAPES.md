# Type II: the covered doubled-quartic shapes

Alexander Richard Towell, with Claude Code (Anthropic) assistance. Proposed
written local arguments. Independently reviewed (REVIEW-rigid.md). No original magnitude
pattern is excluded.

## Setting and tools

p = Delta_u f for a one-free Type II case (TYPE-II-PRICING.md): range
{-1,0,1}, p(0)=1, p(e_v)=0, ordinary quadratic coefficients m_A in {0,1},
c in {1,2}, and exactly three departures among pair numerators -2/+1 and
doubled quartics l_D = 2, everything else baseline (pairs -1/0, quartics
0/1). The seven shapes below are the ones where every vertex of every
doubled quartic lies in another departure, so the private-vertex argument
does not apply. Labels as in TYPE-II-PRICING.md.

Write the link of a pair A as the weighted graph with an edge D\A of weight
l_D for each quartic D containing A. Then:

- (W) Weight. Pair inversion gives total weight 4m_A - k_A. For a baseline
  pair this is at most 5, and it is 4 or 5 when m_A = 1.
- (P) Parity. Cubic integrality makes every weighted vertex degree of a
  pair link even. So a baseline pair in exactly one doubled quartic has,
  besides the doubled edge, a unit triangle (weight 2 or 3 remains, and only
  3 supports a nonempty even simple graph), and a baseline pair in two
  doubled quartics has no unit edge at all (weight at most 1 remains).
- (U) Unit link at a vertex x. Let U_x be the link of x in the complex of
  unit tetrahedra. Origin and unit values give A_x + P_x = 8 with P_x the
  weighted quartic count at x, and summing pair inversion gives
  4d = A_x + 3P_x, where d = sum_r m_(xr). So P_x = 2d - 4 for any c.
  Each vertex r of U_x has as its link the unit part of the link of xr;
  when that is a single cycle for every r (C3, C4, C5, or C6 at a -2
  partner), U_x is a disjoint union of closed surfaces with
  chi(U_x) = (number of its vertices) - (unit tetrahedra at x)/2. Also
  |U_x| <= 12. With all degrees at most 5, sum(6 - deg) = 6 chi gives every
  component chi >= 1, and a chi = 1 component at most six vertices; a
  closed surface with chi = 1 has E = 3(V - 1) <= V(V - 1)/2 edges, so at
  least six vertices. Hence a chi = 1 component then has exactly six
  vertices, all of degree 5, and contains no degree-3 vertex.

Small-sphere facts, checked exhaustively up to 12 vertices by
`rigid_shape_facts.py` (S4 and S6 also follow from curvature alone; S3
needs in addition that the three degree-5 vertices of a (3,3,3,5,5,5)
sphere are universal, forcing nine triangles against eight): (S4) a sphere with
degrees in {3,4,5} and four degree-3 vertices is the tetrahedron boundary;
(S3) no sphere has three degree-3 vertices and all others of degree 5, and
no 5-vertex sphere has a degree-5 vertex; (S6) a sphere with one degree-6
vertex, three pairwise non-adjacent degree-3 vertices and all others of
degree 4 or 5 has exactly 7 vertices.

## Shapes excluded

Shape 6: Q2 on {0,1,2,3}, {0,1,2,4}, {0,1,3,4}. The baseline pair {0,1}
lies in all three, so its link weight is at least 6 > 5, contradicting (W).

Shapes 2 and 3: a +1 pair J inside the doubled quartic D = J + J'. The link
of J has total weight 4m_J - 1 = 3 (m_J = 0 would give -1), of which the
doubled edge J' takes 2. One unit edge remains, giving two odd weighted
degrees, contradicting (P).

Shape 7: Q2 on D1 = {0,1,2,3}, D2 = {0,1,4,5}, D3 = {2,3,4,5}. Each of the
pairs {0,1}, {2,3}, {4,5} lies in two doubled quartics, so by (P) none lies
in a unit tetrahedron. At x = 0: by (W) m_01 = 1 but 1 is isolated in U_0;
the pairs 02, 03 (in D1 only) and 04, 05 (in D2 only) have unit triangles,
so 2, 3, 4, 5 have degree 3 in U_0; every other vertex has degree 4 or 5.
There are 2d - 8 unit tetrahedra at 0 (two doubled tetrahedra weigh 4)
and d - 1 vertices in U_0, so chi(U_0) = (d - 1) - (2d - 8)/2 = 3.
Three chi = 1 components need 18 vertices, so U_0 is a sphere plus a
six-vertex all-degree-5 component; the sphere holds all four degree-3
vertices and by (S4) is the tetrahedron boundary on {2,3,4,5}. Its edge 23
gives a unit tetrahedron containing {2,3}. Contradiction.

Shape 5: +1 on J = {0,1}, Q2 on D1 = {0,2,3,4}, D2 = {1,2,3,4}. Pairs
inside {2,3,4} lie in D1 and D2, so by (P) no unit tetrahedron contains
two of 2, 3, 4. At x = 0: J lies in no doubled quartic, so its link is a
unit C3 (weight 4m - 1 = 3) and 1 has degree 3 in U_0; pairs 02, 03, 04 lie
in D1 only and have unit triangles, so 2, 3, 4 have degree 3; others have
degree 4 or 5. There are 2d - 6 unit tetrahedra and d vertices, so
chi(U_0) = 3. As in shape 7, U_0 is a sphere plus a six-vertex component,
and the sphere is the tetrahedron boundary on {1,2,3,4}. Its edge 23 gives
a unit tetrahedron containing {2,3}. Contradiction.

Shape 4: -2 on J = {0,1}, Q2 on D1 = {0,2,3,4}, D2 = {1,2,3,4}. Again no
unit tetrahedron contains two of 2, 3, 4. The link of J has weight
4m_J + 2, and m_J = 0 would leave two unit edges, which no even simple
graph has, so m_J = 1 and the link is six unit edges forming an even
simple graph: C6, two disjoint triangles, or a bowtie (two triangles
sharing a vertex w). The bowtie is impossible: w would put the triangle
{0,1,w} in four tetrahedra, but {0,w} is a baseline pair whose unit link
is a single cycle (C3 if w is in {2,3,4}, else C4 or C5), so every
triangle on it lies in exactly two. This leaves C6 or two disjoint
triangles. At x = 0, 2, 3, 4 have degree 3 in U_0 (unit triangles of
02, 03, 04), others 4 or 5, and chi(U_0) = 3 as in shape 5 (all of 0's
pairs have m = 1).
- C6: 1 has degree 6 in U_0. Components still have chi >= 1 (each has a
  vertex of degree at most 5 and degree 6 contributes 0). Three components
  need more than 12 vertices, so U_0 has a sphere and a chi = 1 component.
  A chi = 1 component containing the degree-6 vertex 1 has at least seven
  vertices, and sum(6 - deg) = 6 then forces all its other vertices to
  degree 5, so it contains none of 2, 3, 4. If the sphere omits 1, it
  therefore has exactly the three degree-3 vertices 2, 3, 4 and
  2 n4 + n5 = 3, so it is (3,3,3,5,5,5) on six vertices or has five
  vertices with a degree-5 vertex, both impossible by (S3). So the sphere
  contains 1, with 2, 3, 4 pairwise non-adjacent, and by (S6) has 7
  vertices; the chi = 1 component avoids 1 and so has six vertices of
  degree 5. That is 13 vertices in U_0, more than 12. Contradiction.
- Two triangles: split 1 into two copies, one per triangle (as in 1395).
  This preserves edges and faces and gives closed surfaces with chi = 4 on
  at most 13 vertices and five degree-3 vertices (the copies and 2, 3, 4),
  all others of degree 4 or 5. Four chi = 1 components need 24 vertices,
  and a single sphere holds at most four degree-3 vertices
  (3 n3 <= 12), so U_0 is two spheres, holding the five degree-3
  vertices as 4 + 1 or 3 + 2. A sphere with four of them is a tetrahedron
  boundary (S4) and contains two of 2, 3, 4, which are then adjacent.
  A sphere with exactly three is impossible by (S3). Contradiction.

## Shape left open

Shape 1: -2 on {0,1}, -2 on {2,3}, Q2 on {0,1,2,3}. The links of 01 and 23
consist of the doubled edge plus either nothing (m = 0) or a unit 4-cycle
(m = 1). At x = 0 the unit link has chi = 3 with only 2 and 3 of degree 3,
and the forced sphere (two degree-3 vertices, 2 n4 + n5 = 6) exists, so
the one-vertex count does not decide it. It needs the global treatment of
the pair-only shapes.

## Consequence

If accepted, Type II reduces to the 24 pair-only shapes and shape 1. These
are local statements about one derivative, independent of c except where
c in {1,2} is inherited from the Type II definition. Global status: OPEN.
