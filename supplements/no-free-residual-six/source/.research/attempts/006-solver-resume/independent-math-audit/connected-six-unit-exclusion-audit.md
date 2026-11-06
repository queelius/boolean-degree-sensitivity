# Independent audit: connected six negative units

**PASS.** The proof in `../connected-six-unit-exclusion.md` excludes all
connected exact-six-unit negative-quintic families in the selfdual
one-zero-pair representative. It does not exclude the remaining disconnected
families and does not resolve the full Boolean existence problem.

The final executable check is
[`verify_connected_six_unit_exclusion.py`](verify_connected_six_unit_exclusion.py),
with source hashes and results in
[`connected-six-unit-exclusion-independent-verification.json`](connected-six-unit-exclusion-independent-verification.json).
The separate uniform-repair replay is
[`verify_six_unit_ten_family_repair.py`](verify_six_unit_ten_family_repair.py),
reported in
[`six-unit-ten-family-codegree11-independent-verification.json`](six-unit-ten-family-codegree11-independent-verification.json).
Neither checker imports a producer or launches a research solver.

## The new local derivative step

The two-exception proof is valid with its explicit guard `f(e+u)=0`.
For a negative-free nonendpoint `u`, the derivative `p=Delta_u f` has
`p(0)=1`, zero singleton values, integral monomial coefficients, and ordinary
quadratic coefficients in `{0,1}`. In fact the latter coefficient at `A`
equals `f(u+A)+1[A=e]`, so the guard is exactly what controls the special
pair. Omitting this guard would not justify the argument.

Write `16p=c+sum a_A chi_A+sum b_D chi_D`. The following local statement
suffices for both new lemmas: choose a vertex `x` whose incident quadratic
Fourier coefficients are all `-1/0`, and whose incident quartic coefficients
are `0/1` except exactly one doubled tetrahedron `D`.

For a pair `A` through `x`, monomial inversion gives weighted top-link size
`4m_A-a_A` in `{0,1,4,5}`. Integrality at cubic monomials makes each weighted
link degree even. If the pair is outside `D`, its nonempty unit link is a
single four- or five-cycle. If it is inside `D`, subtracting the doubled
edge leaves a simple even graph with two or three edges; only the triangle
case is possible. Its ordinary coefficient is one and its quadratic
Fourier numerator is minus one.

Consequently the simplicial link at `x` made from **unit** tetrahedra has
one cycle as every vertex link. It is directly a disjoint union of closed
triangulated surfaces. Exactly the three vertices in `D minus {x}` have
degree three; all others have degree four or five. This direct route also
avoids needing any statement about pair links away from `x`. The producer's
additional forbidden-triple argument uses only pairs through `x` and is
consistent, but is unnecessary for this independent proof.

Let `d` be the number of vertices in this unit link and `P_x` the weighted
quartic incidence at `x`. Every occurring pair has ordinary coefficient
one, and every nonoccurring pair coefficient zero. The origin/unit
equations give `A_x+P_x=8`; summing pair inversion gives
`4d=A_x+3P_x`. Therefore `P_x=2d-4`, and the unit link has `2d-6`
triangles. Its Euler characteristic is `d-(2d-6)/2=3`. This calculation
does not require a bound on `c` or restrictions on coefficients not incident
with `x`.

Each component has positive Euler characteristic, because all vertex
degrees are below six; a connected closed surface has characteristic at
most two. A characteristic-one component here has exactly six vertices,
all degree five: curvature gives at most six vertices, while edge
simplicity excludes fewer. There are at most twelve vertices in total,
so characteristic three requires one characteristic-two component and
one such six-vertex component. The first contains all three degree-three
vertices. Its curvature equation leaves degree sequences `(3,3,3,4,5)`
on five vertices, impossible because of degree five, or
`(3,3,3,5,5,5)` on six vertices. In the latter graph, the three degree-five
vertices are universal and each degree-three vertex forces three distinct
faces. Those nine faces exceed the eight faces required by characteristic
two. This contradiction proves the local statement.

For two distinct doubled quartics, choose `x` in one but not the other.
For one doubled quartic `D` and one exceptional quadratic `J`, choose
`x` in `D minus J`. These choices establish exactly the required incident
hypotheses. Thus both two-double and mixed local derivatives are impossible.
All remaining local cases were covered by the accepted baseline and
one-exception derivative obstructions.

The independent finite controls check 65,536 simple unit graphs for the
pair-link claims, all 714 relative placements of a second doubled quartic,
and all 78 placements of an exceptional quadratic. They check all 900
labelled possible eight-face selections in the final six-vertex graph,
with no closed surface. A disjoint tetrahedral sphere and six-vertex
projective-plane triangulation is a genuine positive control of total
characteristic three; it has **four** degree-three vertices, showing why
the exact degree-three count matters.

## Repair coverage and codegree

The final input file is bound directly to the accepted 496-class support
catalog and the current ten-family/190-pair ledger. Every listed permission
has capacity one and every retained pair lies in no permission. The
independent C++ replay checks every actual-bad subset with more than five
members, and every consistent choice of its unique absent triple. It
rejects cross-created forbidden quartets and uses a separately controlled
set-cover search for deletions. All 203 subsets pass in 1,501 replay nodes.
There are also 12,000 set-cover controls, a valid uniform-repair example,
and a genuine repair-six counterexample. The producer's 1,361-node traversal
is a different algorithmic count and is not used as proof evidence.

From `H` with 138 zero triples, delete the `d` triples through the zero
pair, then at most five further triples. The resulting free graph has at
least `133-d` edges. Its common link contains an independent set of size
`d`: two restored star triples and both common-link triples would otherwise
make a full quartet through the zero pair, requiring a permission that the
literal pair check excludes. Extra edge deletions preserve this independence
and the zero pair shadow.

The published extremal bound 126 excludes `d<=6`. For `d=7,8,9`, a
124-edge subgraph contradicts the accepted common-link independence bound
six. For `d=10`, a 123-edge subgraph contradicts the bound seven. Baseline
endpoint numerators exclude `d=12` by `66-6d+k_a+k_b>=0`. Hence `d=11`.
The G126 common-link result is optional corroboration; G124/G123 suffice
for the final proof.

## Exhaustion of the final cases

The earlier accepted refinement forces singleton defect zero and exactly
two cost-two nonsingleton exceptions. If either exception is a positive
quintic of numerator two, the new local lemmas force every negative-free
nonendpoint to be a positive extension. If both are cubics, a nonpositive
free vertex must belong to both distinct cubic supports, so there are at
most two such vertices.

Nine final classes have at least four free nonendpoints at every retained
pair; codegree eleven allows only one positive extension, which contradicts
both alternatives. Class 126 has five pairs with four free vertices and
ten with three. Its outside hitting cap at the literal vertex 6 is one;
baseline singleton values force equality, making vertex 6 the unique
positive extension. It is in the negative-support union, so all three
free vertices would have to lie in both cubic supports. That is impossible.

The source accounting is exact: 396 incidence exclusions, 21 localization
exclusions, 56 guarded-covering exclusions, 13 singleton/intersection
exclusions, and these ten final exclusions total 496. All literal retained
pairs are checked; no original-function invariance is assumed. Missing or
altered families, pairs, permissions, caps and statuses are rejected by
the finite binding controls.

The published extremal result and complete G124/G123 catalogs remain
explicit external dependencies. The earlier baseline and one-exception
derivative theorems retain their accepted small-valence manifold census
dependency. The **new** private-vertex argument uses only elementary
closed-surface Euler characteristic and the checked small degree case.
The disconnected six-unit ledger is unchanged.
