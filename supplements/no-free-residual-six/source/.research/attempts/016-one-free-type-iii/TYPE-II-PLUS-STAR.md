# Type II: three +1 pairs at one vertex

Alexander Richard Towell, with Claude Code (Anthropic) assistance. Proposed
written local argument. Independently reviewed (REVIEW-star.md).

Shape: three +1 pair numerators on {x,a}, {x,b}, {x,c} (the pair-only star
K_(1,3) among the five "three +1" shapes of TYPE-II-PRICING.md), no doubled
quartic, everything else baseline.

At x: a +1 pair has link weight 4m - 1 = 3 (m = 1), a baseline pair 4 or 5
(m = 1) or 0 (m = 0; weight 1 is excluded by parity (P)). So every pair
link is empty or a single cycle C3, C4, C5, and
there are no doubled tetrahedra. With tools (U) of TYPE-II-RIGID-SHAPES.md,
P_x = 2d - 4 and U_x is a disjoint union of closed surfaces on d <= 12
vertices with chi = d - (2d - 4)/2 = 2, in which a, b, c have degree 3 and
every other vertex degree 4 or 5. Components have chi >= 1. Two chi = 1
components would need six vertices each, hence all twelve vertices, and a
six-vertex chi = 1 surface has 3(6 - 1) = 15 edges, so it is K6 with all
degrees 5, leaving no room for a, b, c. So U_x is a sphere with exactly
three degree-3 vertices and all others of degree 4 or 5. Curvature gives
9 + 2 n4 + n5 = 12, so it is (3,3,3,5,5,5) on six vertices or has five
vertices with a degree-5 vertex. A five-vertex sphere has maximum degree 4,
and in (3,3,3,5,5,5) the three degree-5 vertices are universal, so the
graph contains K_(3,3) and is not planar (S3, also checked by
`rigid_shape_facts.py`). Contradiction.

`vertex_type_screen.py` screens the other ways a vertex can meet pair
exceptions (one to three of them, -2 with a C6 link counted as degree 6,
+1 as degree 3) and finds spheres in every other case. Its orders agree
with the orders the accepted sources report (one -2: 9..11; one +1: 7;
adjacent -2,+1: 8, 9), compared with their written statements, not with
their catalog files. The screen ignores split -2 links and non-sphere
unit links, which cannot matter here: a nonempty row only shows that
one-vertex counting does not decide that case. So one-vertex counting
removes only this shape, leaving 23 pair-only shapes and rigid shape 1.

Caution for the remaining shapes (from REVIEW-star.md): the shape-4 bowtie
argument of TYPE-II-RIGID-SHAPES.md does not carry over when two -2 pairs
share a vertex, so those shapes must treat bowtie links explicitly.
