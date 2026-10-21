# A complete finite cover for three-exceptional constant-one singleton components

Alexander Richard Towell, 21 October 2026. Prepared with substantial OpenAI
Codex assistance. This is a written reduction plus exact finite computation,
not a proof-assistant formalization or human-reviewed theorem. Novelty has not
been established. The broader fourteen-variable Boolean question remains open.

## Statement

For a subset S of ten physical coordinates, put
`chi_S(x)=(-1)^(sum_{j in S} x_j)` on `{0,1}^10`. Let M be a simple family of
two-element subsets and P a simple family of four-element subsets. Suppose

    B(x) = 1 - sum_{e in M} chi_e(x) + sum_{F in P} chi_F(x),

has B(0)=0, all its1024 values divisible by8, and singleton values B(e_j)=−8
on exactly three coordinates E and0 on the other seven.

Then |M|=8 and |P|=7. There is a permutation of the ten physical coordinates
carrying E to{0,1,2} and carrying(M,P) to one of the **seventeen literal rows**
in `data/components.json`, printed in `CATALOG.md`. Conversely, every listed
row has exactly these properties, and so does each of its coordinate images.
When E is already{0,1,2}, the transporting permutation preserves E setwise.

This is a complete finite **cover**. The seventeen rows are not asserted to
be pairwise inequivalent under coordinate permutations; no minimal orbit
count is claimed or needed. All components have real degree4, value histogram
`{-8:64,0:768,8:192}`, and at least one inactive physical coordinate. Those
last properties are exact invariants checked on every covering row.

The theorem concerns the displayed component polynomial. It does not assert
that B is Boolean, that it extends to a fourteen-variable function, or that
the analogous constant-two components have been classified.

## 1. Exact incidence and parity equations

Write m=|M|, p=|P|; m_j,p_j count supports containing j, and m_ij,p_ij count
supports containing a fixed pair ij. Simplicity makes m_ij either0 or1.
Origin evaluation gives m−p=1. Singleton evaluation gives

    p_j - m_j = 4*1_E(j).

Summing over j gives4p−2m=12, hence p=7 and m=8.

Expand characters as `chi_S(x)=product_{j in S}(1-2x_j)` in real multilinear
monomials. The coefficient of x_i*x_j in B is4(p_ij−m_ij). Since H=B/8 is
integer-valued on the Boolean cube, each multilinear coefficient of H is an
integer: its coefficient on T is the alternating sum of H(1_U) over U⊆T.
Consequently

    p_ij = m_ij (mod2).

Equivalently, the XOR of the complete pair graphs on the selected quartets
is M. These equations are also sufficient for divisibility in the displayed
coefficient pattern. The constant coefficient is0; singleton coefficients
of H are−1_E; quadratic coefficients are(p_ij−m_ij)/2; cubic coefficients are
minus the number of quartets containing that triple; and quartic coefficients
are twice the quartet indicators. They are all integers, and no higher
coefficients occur. Thus exact cardinality, the vertex equations and pair
parity characterize this component problem without a numerical relaxation.

## 2. An elementary binary rank bound

Form the10-by15 binary incidence matrix G whose columns are the eight M
supports and seven P supports. Two different coordinate rows overlap in
m_ij+p_ij positions, an even number by pair parity. A row has weight
m_j+p_j=2m_j+4*1_E(j), also even. Its row span C is therefore self-orthogonal
in the nondegenerate binary dot-product space of length15. Hence

    dim C <= floor(15/2) = 7.

Row rank equals column rank, so the supports in M∪P have binary rank at most7.
Only elementary binary linear algebra is used; no Reed–Muller classification
or signed-lattice theorem is a premise.

Let the negative graph M have c connected components, including isolates.
Within a connected component, its edge vectors span all vectors of even
coordinate sum: paths from a chosen root generate every root-to-vertex pair.
Thus the edge span has rank10−c and is the kernel of the map sending a vector
to its intersection parities with the c graph components. Let D be the span
of the images of the positive quartets. Rank-nullity gives

    rank(M union P) = 10-c + dim D.

Every quartet has even size, so D lies in the(c−1)-dimensional even-parity
subspace of the component-parity space. Therefore c≥3 and dim D≤c−3. Also
c≤6: if c≥7 the graph rank r=10−c≤3; a graph with component ranks r_i has at
most `sum binom(r_i+1,2) <= binom(r+1,2) <= 6` edges, contradicting |M|=8.

For c=3,4,5,6, every allowed D extends to a subspace U of dimension c−3
inside that even space. Enumerating all such U is a complete, possibly
overlapping cover. It is a quotient-space argument, not a GL transformation
of the physical coordinates or of pair/quartet support sizes.

## 3. Guards that retain every valid family

The target number of selected quartets at j is `t_j=m_j+4*1_E(j)`, which cannot
exceed7. If c=3, D=0, so every selected quartet meets each graph component
evenly. An isolated coordinate is therefore absent from P and cannot be
exceptional. For a two-vertex edge component uv, every quartet contains both
endpoints or neither, giving p_u=p_v. Their exceptional statuses agree. If
both were ordinary, p_u=p_v=1, so a unique quartet uvab contains them. Its
cross pair ua then appears in exactly one selected quartet; pair parity would
force ua into M, contradicting that uv is an isolated component. Both endpoints
must therefore be exceptional. These tight guards apply only when c=3.

Fix one allowed maximal U. A target-zero coordinate appears in no selected
quartet, and a target-seven coordinate appears in all seven. The candidate
universe A consists of **all** four-subsets obeying those two rules and whose
component-parity image lies in U. For a valid P choose U⊇D; then P⊆A. Seven
distinct candidates can meet the target only if |A|≥7 and, for every j,

    #{F in A: j in F} >= t_j,
    #{F in A: j not in F} >= 7-t_j.

The checker regenerates every maximal subspace as a literal set, every one
of the210 possible quartets, and every capacity test. These tests alone do
not constitute a component; the remaining exact selection equations are
exhausted below.

## 4. Literal graph and coloring coverage certificates

The finite graph cover begins with the empty graph on ten named vertices.
For each grade, the augmentation certificate records, for **every** missing
edge of **every** retained predecessor, a destination next-grade graph and a
literal coordinate permutation carrying that extension to it. The checker
verifies every map and checks that the extension identities are exactly the
required set, with no omission or alias.

Induction proves coverage: remove an edge from an arbitrary next-grade graph,
transport the predecessor to a covered representative, and apply the recorded
map for its transported missing edge. No canonical-labeling algorithm or
claim of representative inequivalence is needed for this induction.

At grade8, every c≥3 representative has a checked literal frame-link map
into a raw graph in the historical graph catalog. Each raw graph contains all
120 exceptional three-subsets. A checked edge-and-color permutation sends
each marked graph to a recorded frame with E={0,1,2}. Composing these literal
maps covers every physical(M,E) satisfying the necessary graph condition.
Every graph guard, target, subspace and candidate list is then reconstructed
from that literal frame. No global function symmetry is imposed.

The verified inventory has graph grade sizes
`[1,1,2,5,11,26,66,165,428]`,329 eligible raw frames,39480 marked maps,
14343 colored frames,44901 maximal-subspace covers and19112 capacity-passing
instances. These are checked inventory sizes, not a necessary assumption of
minimal graph or coordinate-orbit enumeration.

## 5. Exhaustive exact quartet selection

For each of the19112 instances, the search chooses seven distinct quartets
from its reconstructed universe, with exact vertex targets and required XOR
clique boundary M. Its state consists of selected rows, still-available rows,
remaining quotas and boundary. Impossible quotas/capacity are rejected.
Appending a final parity bit to each quartet's boundary vector shows that
the required boundary and remaining cardinality parity must lie in the binary
span of available vectors; failure is a valid necessary pruning step.

Otherwise choose a vertex with positive remaining quota q. Every completion
selects exactly q of its available incident quartets. The algorithm branches
over **all** q-subsets and excludes all other incident quartets in that child.
These branches partition the completions. The choice of vertex minimizes a
binomial branch count only for speed; it omits no branch. A zero-slot leaf is
accepted exactly when all quotas and the residual boundary are zero.

This is the separately developed quota-vertex enumerator, distinct from the
original include/exclude producer. CPU, node and branch limits return explicit
OPEN frontiers. Completeness is reported only when every instance exhausts;
an OPEN result never acts as a negative certificate.

The recorded portable replay exhausts all19112 instances, compares the full
family set for **each** to the independent historical reference, and checks
that the union is exactly the seventeen literal(M,E,P) rows, with all53
source-cover occurrences accounted for. Thus every component allowed by the
written reductions is a coordinate image of a listed row. This finite step
is reproducible Python computation, not a proof-assistant certificate.

## 6. Converse and invariants

For each listed row the checker evaluates all1024 exact integer values and
checks origin0, the ten required singleton values, and divisibility8. It
independently transforms the value vector by an integer Walsh transform and
checks every Fourier coefficient: constant1, coefficient−1 precisely on M,
coefficient+1 precisely on P, zero elsewhere. This proves the converse and
real degree4. Every listed histogram is `{-8:64,0:768,8:192}`. The union of
nonzero support masks omits at least one physical coordinate in every row;
this is equivalent to that coordinate being inactive. These properties are
preserved by the literal coordinate transports.

The written deductions and finite replay together establish the stated cover.
Novelty, minimal orbit counts, a2 classification, full-function realizability,
formal verification, human peer review and the global existence question are
separate matters and are not claimed here.
