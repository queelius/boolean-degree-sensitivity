# Two positive pair exceptions at constant three

Alexander Richard Towell, with Claude Code (Anthropic) assistance; the
source theorem and its finite inputs are OpenAI Codex-assisted work.
Proposed written extension of an accepted local theorem. Independently
reviewed (REVIEW-plus-plus-c3.md). No original magnitude pattern is excluded.

## Statement

Let p on thirteen Boolean coordinates have range {-1,0,1}, p(0)=1 and
p(e_v)=0 for every v. Write

    16p = c + sum_(|A|=2) k_A chi_A + sum_(|D|=4) l_D chi_D

with every l_D in {0,1}, exactly two distinct pairs with k_A=+1, every other
k_A in {-1,0}, and every ordinary (monomial) quadratic coefficient of p in
{0,1}. If c=3, no such p exists.

The accepted source `006-solver-resume/two-positive-cubic-free-derivative.md`
(audit `009-parent-analysis/two-positive-cubic-parent-audit.md`, manifest
`009-parent-analysis/local-audits-cycle64-manifest.json`) proves this for
c<=2. Its second part, a special ordinary coefficient two, is not used or
extended here. This note changes only the disconnected-link step, the one
place where c=3 breaks the source's counting.

## 1. Constant-free facts (re-derived, as in the source)

Let K be the complex of quartets with l_D=1 and m_A the monomial coefficient
of the pair A. Pair inversion gives 4m_A = k_A + #(tetrahedra on A). Unit
evaluation gives, at each v, sum_(A at v) k_A + P_v = 8, where P_v counts
tetrahedra at v. Summing pair inversion over the pairs at v gives
4D_v = (8 - P_v) + 3P_v, so P_v = 2D_v - 4, and with z incident +1 pairs
the number of incident -1 pairs is y_v = 2D_v - 12 + z >= 0. Hence D_v >= 6
except at a common endpoint of two adjacent exceptions (D_v >= 5). Summing
P_v and the origin identity gives Q = E - 13 and E = 49 + c. None of this
bounds c.

Pair inversion and cubic integrality make every pair link an even simple
graph with 4m_A - k_A edges: empty, C4 or C5 at a baseline pair, C3 at a +1
pair. Every pair link is thus empty or a cycle, so a present triangle lies
in exactly two tetrahedra, and
p(1_X) = 1 - chi(K[X]). Each vertex link is a closed surface with
chi = D_v - P_v/2 = 2 and link degrees in {3,4,5}. At a GOOD vertex (in
neither exceptional pair) every incident edge is baseline, so its link
degrees are in {4,5}. Components of a vertex link have positive Euler
characteristic, since sum(6 - deg) = 6 chi with all degrees at most five;
a chi=1 component therefore has all degrees five and six vertices (the
projective plane), so a disconnected link is two such planes.

Two inherited local facts, both constant-free and accepted in the source:
a good vertex and a vertex in exactly one exception each have a cross
neighbour in the configuration below (the second by the pentagon lemma).

## 2. The disconnected link at c=3

Suppose lk(w) is two projective planes on six-sets A, B. All link degrees
at w are five, so no edge at w has the valence three of a +1 pair: w is
good. A and B span complete graphs, and {w}, A, B are all thirteen
vertices, so these with the star of w give 42 edges and the number of
cross edges between A and B is exactly M = E - 42 = 10.
At c<=2 the source has M <= 9; both of its contradictions used M >= 10.

Two link lemmas, checked exhaustively by `link_lemmas.py` over every
7- and 8-vertex sphere from the independent 015 enumeration:

- L7. A 7-vertex sphere with all degrees in {4,5} is the pentagonal
  bipyramid; for each degree-5 vertex w, its unique non-neighbour is
  adjacent to every neighbour of w.
- L8. An 8-vertex sphere with all degrees in {4,5} is the snub
  disphenoid; for each degree-5 vertex w, at least 7 edges join its two
  non-neighbours to its neighbours.

Link position. Let x in A be good with cross neighbours N_B(x). Then
lk(xw) is lk_(lk(w))(x), the 5-cycle on A\x. So in the sphere lk(x), w has
degree 5 with neighbours exactly A\x, and the vertices N_B(x) are its
non-neighbours. A link edge from b in N_B(x) to a in A\x is a triangle xab,
hence a cross edge ab, and distinct link edges give distinct cross edges.
The same holds with A and B exchanged.

Counting. Every good vertex has cross degree at least 1. With disjoint
exceptions there are 8 good and 4 singly bad vertices in A union B; with
adjacent exceptions there are 9 good, 2 singly bad and the doubly bad common
endpoint t, which may have cross degree 0. Exactly one of the following
holds.

(a) Every good vertex has cross degree at least 2. Then the cross degree
sum is at least 20, so M = 10 with equality throughout: good vertices have
cross degree exactly 2, singly bad ones exactly 1, t (if present) 0. A has
at most four bad vertices, so pick a good x in A, with cross neighbours
b1, b2. Here D_x = 8, lk(x) is a sphere (two projective planes need twelve
vertices), and its degrees lie in {4,5}, so L8 applies with root w: at
least 7 link edges join {b1,b2} to A\x. Adding the edges x b1, x b2, the
cross degrees of b1 and b2 sum to at least 9. Equality allows at most
2 + 2 = 4. Contradiction.

(b) Some good y has cross degree 1, say y in A with neighbour z in B. As in
the source (and L7, since D_y = 7 and lk(y) has degrees in {4,5}), z is
adjacent to all of A: six cross edges. Each vertex of B\z other than t
needs a further cross edge, distinct from those six. If t is not in B\z
this gives M >= 11 > 10. Otherwise M = 10 exactly, and the four vertices
of B\{z,t} have cross degree exactly 1 while t has 0. At most two of those
four are bad (the singly bad endpoints), so some good b in B\{z,t} has a
single cross neighbour a. By L7 applied to lk(b), a is adjacent to every
vertex of B\b, including t. But t has cross degree 0. Contradiction.

So every vertex link is a sphere, as at c<=2.

## 3. Closing step, unchanged

K is connected (every component has at least seven vertices), hence a
closed 13-vertex combinatorial 3-manifold with E = 52 and all edge
valences at most five. The accepted scan behind the source
(`009-parent-analysis/one-positive-quadratic-derivative.md`,
`small_valence_euler_obstructions.py`) checks all 4,787 records of the
published list of such manifolds (Frick 2015, Theorem 3.10); exactly 76
have thirteen vertices and E <= 52, and each has an induced subcomplex
with Euler characteristic outside {0,1,2}. E = 52 is inside that range, so
p(1_X) leaves {-1,0,1} for some X. Contradiction.

## Application and scope

In the 1513/1523 one-free trichotomy, Type III (c in {0,3}, the singleton
at u plus two cost-two nonsingleton departures through u) has a subcase
where both departures are cubic +1. Its derivative p = Delta_u f satisfies
the statement above. Its ordinary quadratic coefficients are in {0,1}
for every one-free derivative, not only Type III: by Mobius inversion the
monomial coefficient of x_a x_b in Delta_u f is f(1_{u,a,b}), given f(0)=0
and truth value one on all singletons and pairs (1513 section 1). This
also rules out the source's special coefficient-two branch, which does
need c <= 2. The source covers c=0; this note covers c=3. If accepted, the
(+1,+1) subcase of Type III is excluded at both constants, conditional on:
the source theorem's accepted local premises, the pentagon lemma, the
76-record scan and the completeness of the published catalog (not
regenerated), and the 015 sphere enumeration for L7/L8.

Type I, Type II and the other Type III subcases stay open, and no whole
magnitude pattern changes. Global status: OPEN.
