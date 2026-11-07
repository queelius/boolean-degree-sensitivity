# One-free Type I: the endpoint sphere does not exist

Alexander Richard Towell, with Claude Code (Anthropic) assistance. The local
theorem used is OpenAI Codex-assisted work (cycles 1395, 1513, 1523).
Proposed closure. Independently reviewed (REVIEW-typeI.md). No original magnitude
pattern is excluded.

## Claim

Type I of the 1513/1523 one-free residual-six trichotomy (c in {1,2}, the
sole residual departure a cubic -3 containing the free coordinate u) has
no realization.

## Proof

For Type I, p = Delta_u f on the other thirteen coordinates satisfies

    16p = c - 3 chi_A + sum_(J != A, |J|=2) a_J chi_J + sum_(|D|=4) b_D chi_D,
    c in {1,2}, a_J in {-1,0}, b_D in {0,1}, p in {-1,0,1}, p(0)=1, p(e_j)=0,

with A = {a,b} the pair of the -3 cubic minus u, and ordinary quadratic
coefficients m_J = f(J + u) in {0,1}. All other departures are absent
because Type I spends the whole residual budget on the -3 cubic, and no
negative quintic contains the free u.

This is literally the displayed local form of
`009-parent-analysis/minus-three-links-independent-review-cycle1395.md`
(lines 43-46). That review analyses one derivative at a time: its
exclusions of m_A = 0 and of the C3+C4 link, and its endpoint conclusion,
use only the single p: its origin and unit values (the constant
cancels), the pair inversion identity 4m_J = a_J + sum_(D contains J) b_D
(1395 equation (1)), cubic integrality, and surface counting. Its remarks
about three derivatives, the common exceptional graph and f(F) are not
used by the argument. 1513
section 3 records the same transfer ("This local conclusion does not need
a second free derivative"), and 1523 accepts its consequence (Type I
endpoint degrees 11/12). Its conclusion:

    the link of A is C7, and for each endpoint w of A the link L_w is a
    2-sphere on at most 12 vertices in which the other endpoint has
    degree 7 and every other vertex has degree 4 or 5.

(The other endpoint's degree in L_w is the valence of A, 7; any other
vertex y of L_w gives an edge wy of K, a baseline pair whose link is C4 or
C5, so its degree is 4 or 5.)

No such sphere exists, at any order.

Lemma. No triangulated 2-sphere has exactly one vertex v of degree 7 and
every other vertex of degree 4 or 5.

Proof. Let C = c_0..c_6 be the link of v and D the disk left by removing
the open star of v; its boundary is C and its other vertices form W, with
|W| = k. Each c_i has neighbours v, c_(i-1), c_(i+1) and one or two more.

No chords. Suppose D has a chord, and take a chord c_i c_j whose shorter
side D1 has the fewest boundary vertices, L in {3,4} (the two sides have
L + L2 = 9 boundary vertices). If c_i had no edge in D1 besides c_(i+1)
and the chord, then c_(i+1) c_i c_j would be a face of D1: for L = 3 it
fills D1 and c_(i+1) has degree 3; for L = 4 the edge c_(i+1) c_j is a chord
with a shorter side. Either way a contradiction, so c_i has a further edge
in D1, and that uses up its at most two extra neighbours. The same holds
for c_j. On the other side D2, c_i and c_j then have no edges besides
their boundary edges and the chord, so the unique D2 face on the chord is
both c_(i-1) c_i c_j and c_i c_j c_(j+1). Hence c_(i-1) = c_(j+1) and
L2 = 3, contradicting L2 >= 5.

Chordless D. The face of D on the boundary edge c_i c_(i+1) has its apex
y_i in W. At c_i the apexes y_(i-1), y_i agree when c_i has degree 4 and
differ when it has degree 5. Let beta be the number of degree-5 vertices
on C, the number of changes in the cyclic sequence y_0..y_6. A cyclic
sequence cannot change exactly once, and beta = 0 would make one apex
adjacent to all seven c_i, so beta >= 2. The beta maximal runs have
distinct apexes: an apex y of two runs would have at least four
neighbours on C in two arcs, and two such arcs cannot be adjacent in the
link of y (a C-edge between them already has its unique D face with
another apex, and there are no chords), so two further vertices separate
them and y has degree at least 6. Hence beta <= k. Curvature,
sum (6 - deg) = 12, gives -1 + (14 - beta) + (2k - gamma) = 12, that is
beta + gamma = 2k + 1, where gamma <= k counts the degree-5 vertices of W.
So beta >= k + 1 > k. Contradiction.

This proof was supplied by the independent reviewer (REVIEW-typeI.md)
and checked step by step by the parent. Two finite checks agree with it
and are kept as controls, not premises. `one_seven_spheres.py` filters
every 2-sphere on 4..12 vertices, from the 015 vertex-split enumeration
(counts equal OEIS A000109) and from the 006 catalogs (hashes pinned by
the 015 audit), and finds none. Allowing degree 3 as well finds one sphere
at each of orders 8, 9, 10, so the filter is not vacuous. The reviewer's
separate disk-filling search, sharing no code with either, reproduces
Brown's disk counts for 0..4 interior vertices and finds no such sphere
for up to 7 interior vertices, which is every order allowed by curvature
(at most 14). Curvature alone does not exclude the pattern: 2 n4 + n5 = 13
has solutions at every order 8..14.

Hence L_w cannot exist and Type I is impossible. In particular the
accepted 1513/1523 endpoint range (degree 11 or 12) has no instances,
which is consistent with it.

## Premises and scope

Conditional only on the 1395 local argument, used from its displayed
form onward; the displayed form itself is supplied here by the accepted
1513/1523 Type I classification and its premises, not by the 1393
three-free setting. The lemma above is proved by hand at every order, so
no sphere catalog or enumeration is a premise.

With TYPE-III-CLOSURE.md, if both are accepted, the one-free residual-six
case reduces to Type II (c in {1,2}, three distinct nonsingleton cost-two
departures all containing u). Type II, the no-free case and residual
defect above six remain open. No whole magnitude pattern changes. Global
status: OPEN.
