# Attempt 015: independent review of the signed-star chain 1409 -> 1412 -> 1424 -> 1425/1431

Claude Code (Opus 5.5), 2026-10-23, at the user's request. New files only;
nothing in 006 or 009 was changed. This is an AI review (a different model
from the OpenAI Codex sessions that wrote the reviewed packets) plus fresh
finite computation. It is not human peer review or formal verification.

## Why

Attempt 014 certified all 24 open signed-star native contexts infeasible from
their raw rows. Those certificates prove infeasibility of the rows; whether
the rows are necessary consequences of the case hypotheses is the job of the
chain above. Each link was previously reviewed by a separate Codex session,
but two premises were inherited and never re-proved after cycle 1396:
completeness of the 006 sphere catalogs, and (by citation) the 1412 local
theorem's own guards. This attempt checks both, and re-derives the rows.

## 1. Catalog completeness and the 13-root domain (computed)

`spheres.py` enumerates triangulated 2-spheres by vertex splitting from K4
and deduplicates by a pynauty certificate of the 1-skeleton. It imports
nothing from 006, 1414 or 1424.

* Completeness rests on Steinitz-Rademacher (every sphere triangulation on
  more than four vertices has a contractible edge, so every class is a vertex
  split of a smaller class) and on Whitney (a 3-connected planar graph has a
  unique embedding, so the graph certificate is a complete invariant).
* Counts for n = 4..12: 1, 1, 2, 5, 14, 50, 233, 1249, 7595 (OEIS A000109).
* `audit.py` hash-checks each 006 catalog against the pin in
  `H/signed-star-full-geometry-result-cycle1422.json`, checks every record is a
  literal sphere on exactly n vertices with 2n-4 faces, and finds an exact
  bijection between records and enumerated classes for each order 7..12: no
  duplicate class, none missing, none extra.
* Re-applying the 1413 guards (degrees in 3..6; exactly three vertices of
  degree 3 or 6 with q = n6 in 1..3; every induced Euler characteristic in
  [-1, 3], by direct counting over all 2^n subsets) to the enumerated classes
  gives first failures 8965 degree support, 162 special count, 6 induced
  Euler, and 13 survivors. These equal the 1424 counts, and the 13 survivor
  classes are exactly the accepted native roots
  (7,0) (8,3) (8,7) (9,33) (9,35) (10,38) (10,113) (10,116) (10,180)
  (11,185) (11,257) (11,691) (12,1697).

Result: `audit-result.json`, status
`CATALOG_COMPLETENESS_AND_ROOT_DOMAIN_REPRODUCED`. This replaces the inherited
006 inverse-contraction cover premise for this branch by an independent
enumeration; it does not replay the 006 transitions.

Tests (`test_audit.py`, 12, pass normally and under `-O`; checks use an
explicit `require`, not `assert`): small-order counts; rejection of a torus,
a disconnected pair, a surface with boundary and a pinched surface; every
split of sampled n=8 classes is a sphere; certificate relabel invariance and
separation; the q=1 fixture survives with range [0,2]; octahedron and a
stacked sphere fail the right guards; a fourfold stacked K4 has induced
Euler 4; native record (11,761) fails only the Euler guard (max 4); a
catalog with a relabelled duplicate, a missing class, or a
corrupted record is rejected.

## 2. The 1412 local theorem (re-derived by hand)

Every step was re-derived from the stated hypotheses; all hold.

* Pair inversion 4m_J = a_J + s_J, with s_J the number of unit quartics
  containing J. Integral cubic monomial coefficients, equal to minus half the
  coface count, make every pair-link degree even. Baseline: s in {0,4,5}
  (s=1 has an odd vertex), so empty, C4 or C5. Plus one: s = 4m-1 forces
  m=1, C3. Minus two: s = 4m+2 forces m=1, s=6.
* Each occurring triangle contains a baseline pair (a star has no triangle),
  whose link is a cycle, so it has exactly two quartic cofaces. Hence every
  nonempty pair link is 2-regular, and a minus-two link is C6 or 2C3.
* At any vertex, the unit value gives A + P = 8 and summing pair inversions
  gives 4d = A + 3P, so P = 2d-4. A vertex link is then a closed surface
  union with characteristic d - (3d-6) + (2d-4) = 2.
* 2C3 at a private negative endpoint: splitting w gives characteristic 3 on
  at most 13 vertices, degrees 3 (the two copies) and 4/5. Positive
  curvature makes each component a sphere or a projective plane, and a
  characteristic-one component with degrees at most five has V <= 6 and
  E = 3(V-1) <= V(V-1)/2, so it is the 6-vertex K6 projective plane. Three of
  those need 18 vertices; so one sphere of at most 7 vertices holds both
  copies, which are nonadjacent with disjoint 3-neighbourhoods, needing 8.
* Center link L: vertex links C3/C4/C5/C6, total characteristic 2, every
  component has a vertex of degree at most 5 (an all-degree-6 component needs
  at least 7 such vertices). q = 0 leaves one sphere with 2n4 + n5 = 3:
  (3,3,3,4,5) has a degree 5 on five vertices, and (3,3,3,5,5,5) would need
  nine triangles on an 8-face sphere. For q >= 1 a disconnected L needs two
  projective planes of at least 6 and 7 vertices, exceeding 12. The profile
  follows from curvature 12.
* Bound (A): with p(1_X) = 1 - chi(K[X]), the w-derivative is
  chi(L[Y]) - 1 in [-2, 2].

## 3. The 1425/1431 rows (re-derived by hand)

From 16p = c + sum a_e chi_e + sum b_D chi_D: quartic monomial coefficient
b_D = x_D; cubic -(1/2)(cofaces) = -x_T; pair (a_e + v_e)/4 = x_e;
singleton -(A_i + Q_i)/8 = -1; constant 1. Hence p(1_X) = 1 - chi(K[X]) and
the 8100 induced-Euler rows 0 <= chi <= 2. Vertex rows Q_i = 2d_i - 4 and
T_i = 3d_i - 6; ordinary edge rows 0 <= v_e - 4x_e <= 1 from a_e in {-1,0};
special pairs x_e = 1 and v_e = 4 - a_e in {3, 6}, equal to the tip degree
in L. Global counts: T = 2Q, Q = E - 13 and, from p(0) = 1,
16 = c + 4E - 5Q, so E = 49 + c. Fixing all 298 through-center indicators to
the cone over L is exact, and placing L on coordinates 1..n is a relabeling
of a necessary case, valid because the local hypotheses are invariant under
coordinate permutation (the special pairs move with it).

## 4. The 1409 survivor enters the 1412 setting (checked)

For a free coordinate u, p = Delta_u f has 16 p_hat(S) = k_(S+u). The 1409
survivor's three cubics F+{x_i}, F = {u,v}, become the star {v, x_i} with
numerators -2 or +1; the constant is u's singleton numerator, 1 or 2; the
quartic numerators are quintics through u, which are 0 or 1 because u is
free; quadratic coefficients are f(J+u), Boolean. These are exactly the
1412 hypotheses with c in {1, 2}.

## Not reviewed here

1409's own inherited premises: the representative and selfdual reduction,
the defect accounting, and the old local exclusions in its guard table
(baseline 4,787-manifold classification, the one-positive whole-derivative
proof, the one-negative compact certificate with endpoint coverage, the
doubled-quartic proof, the two-exception local exclusions), plus its
two-free minus-three and doubled-quintic arguments. Those are the remaining
premises of the statement below.

## Combined status

Conditional on 1409 and its inherited premises, and on pynauty and two
classical theorems: in the selfdual existence representative, the case
"residual Fourier defect at most six with at least two negative-free
coordinates" has no Boolean function. The 26 native contexts are exhaustive
for it (section 1), their rows are necessary (sections 2 to 4), and every
context's rows are infeasible (014 LRAT certificates; two contexts by 009's
1476/1497). This closes that case only. It does not close any whole
negative-quintic pattern, the one-free or no-free cases, or residual defect
above six. The global problem is OPEN.
