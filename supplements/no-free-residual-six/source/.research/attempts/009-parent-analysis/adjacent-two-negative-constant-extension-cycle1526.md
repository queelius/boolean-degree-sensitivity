# Extending the adjacent two-negative-pair obstruction to constants zero and three

Alexander Richard Towell, with substantial OpenAI Codex assistance.
Proposed written extension of an accepted local theorem. Independent review and
a fresh compact-certificate replay are pending; no original pattern is excluded.

## Exact proposed theorem

Let p on thirteen Boolean variables have range {-1,0,1}, p(0)=1 and
p(e_i)=0 for every coordinate. Suppose

    16p = c + sum_(|A|=2) k_A chi_A + sum_(|Q|=4) h_Q chi_Q,

where c is in {0,1,2,3}, every h_Q is zero or one, exactly two distinct
adjacent pairs have k_A=-2, and every other pair has k_A in {-1,0}.
Require every ordinary quadratic coefficient of p to be zero or one.
Then no such p exists, conditional on the accepted complete sphere cover
and the nine independently checked compact contradictions cited below.

The previous theorem explicitly accepts only c=1,2. We do not silently
widen its statement. This note supplies the missing structural step for
c=0,3 and explains why its computational certificates transfer unchanged.
There is no special ordinary coefficient two, disjoint exceptional pair,
additional exception, or arbitrary original-function selfduality claim.

## 1. Constant-independent local reductions

Use the exact coefficient inversion 4m_A=k_A+sum_(Q contains A) h_Q and
the even pair-link degree identity. Baseline pair links are empty/C4/C5.
Exceptional pairs have m_A=1 and a six-edge link, since m_A=0 would give
a two-edge nonempty simple even graph. Every triangle has a baseline
pair, so triangle coface counts are zero or two. Thus the ordinary
polynomial is p(X)=1-chi(K[X]) for the simplicial complex K of its
unit quartics, and every induced Euler characteristic is in [0,2].

The origin and unit identities, with no bound on c, give

    Q=36+c, E=49+c, T=72+2c, Q_v=2D_v-4.

If v meets z exceptional pairs, valence counting gives D_v>=6+z.
These formulas do not require a whole-complex manifold or sphere.

The accepted local splitting argument makes both exceptional pair links
C6. The private endpoint links and the common endpoint link are spheres:
the relevant disjoint positive-curvature component bounds are independent
of c. Specifically, splitting a disconnected exceptional edge would need
at least eight vertices in a sphere and six in a projective-plane component
on at most thirteen available split vertices. At the common endpoint,
separating its two degree-six vertices invokes the one-six obstruction;
putting them together needs at least seven plus six vertices, exceeding
the twelve available. These are the same local premises as in the accepted
structural audit, not applications of its restricted final theorem.

## 2. The only structural use of the larger constant bound

It remains to rule out a disconnected ordinary vertex link. As in the
accepted proof, it must consist of two six-vertex projective planes on
sets A,B, with the ordinary center w outside them. Their complete skeletons
and the center already account for 42 graph edges. Hence the number M of
cross edges between A and B satisfies

    M <= E-42 = 7+c <= 10.

There are nine good vertices, two private exceptional endpoints, and one
common exceptional endpoint among A union B. Every good vertex needs a
cross neighbor by the six-vertex-link obstruction. Each private endpoint
needs one, and the common endpoint needs at least two, because its graph
degree is at least eight while its own six-set plus w supplies only six.

If every good vertex had cross degree at least two, the total cross degree
would be at least 9*2+2*1+2=22, so M>=11. This contradicts M<=10.
Therefore some good vertex has cross degree exactly one.

Its seven-vertex ordinary sphere link is the pentagonal bipyramid. The
accepted local argument then forces its cross neighbor to meet all six
vertices on the opposite side, accounting for six cross edges. Each of
the other five vertices on that neighbor's side still needs a cross edge;
these five edges are distinct and not among those six. Thus M>=11, again
contradicting M<=10. This replaces the old M<=9 bound by M<=10 without
changing either contradiction. All vertex links are consequently spheres.

This proves exactly the structural premises needed by the old certificates
for c=0 and c=3. No Walkup theorem, whole-complex S3 assertion, solid-torus
claim, or geometric realization is needed here.

## 3. The unchanged finite cover and literal certificates

The accepted independent sphere cover yields exactly nine possible common
root links, with native (order,index)

    (8,12), (9,32), (10,74), (10,75), (10,168),
    (11,499), (11,764), (12,2537), (12,5741).

Ordinary sphere links are the accepted six flag types, and each private
one-six sphere link is one of the three flag types of orders9,10,11.
These are local link statements; no global flagness is assumed.

The nine saved compact certificates have 945 literal rows and 1,111 exact
binary deductions. Their independently accepted report explicitly records
zero retained global face-count rows and constant-independent selected
rows. The row families are downward inclusion, triangle coface counts,
fixed root values, induced Euler bounds, ordinary edge valences, ordinary
and private link flag conditions, private degree9..11, and no independent
triple. Every family remains a necessary consequence of Section1/2 at
c=0,3. The retained row formulas and all compact deduction steps are
therefore unchanged; their old selected indices are provenance only.

A fresh independent review must recheck the structural transfer, literal
necessity of these families, complete nine-case cover, and every retained
opposite-value interval deduction/final contradiction. It need not build
a new full model or search for contradictions. The 179583 inverse-cover
transitions are an explicitly inherited completeness premise, not a claim
of fresh transition replay. The old theorem and files remain immutable.

## Sources and application boundary

Primary local sources (all local, source pins in the companion receipt):

- attempts/006-solver-resume/independent-math-audit/two-adjacent-negative-cubic-audit.md
- attempts/006-solver-resume/independent-math-audit/two-adjacent-negative-cubic-independent-verification.json
- attempts/006-solver-resume/two-negative-cubic-ordinary-compact-proofs.json
- attempts/006-solver-resume/independent-math-audit/verify_two_adjacent_negative_cubic.py
- attempts/009-parent-analysis/two-adjacent-negative-cubic-structural-audit.md

If accepted, this removes the adjacent-minus-two/minus-two subcase of
TypeIII in1513 at c=0,3. It does not remove its disjoint or mixed-sign
subcases, and it does not complete any of the29 original magnitude patterns.
The all-input Boolean14 construction/nonexistence goal remains OPEN.
The extension is a source-bound strengthening of an existing computational
local obstruction; no mathematical novelty, formal verification or human
review is asserted.
