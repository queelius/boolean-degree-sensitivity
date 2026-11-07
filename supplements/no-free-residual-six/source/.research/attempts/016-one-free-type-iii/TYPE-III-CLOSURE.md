# One-free Type III at constants zero and three

Alexander Richard Towell, with Claude Code (Anthropic) assistance. The
source theorems and their finite certificates are OpenAI Codex-assisted
work. Proposed written closure, assembled from accepted local theorems.
Independently reviewed (REVIEW-closure.md). No original magnitude pattern is excluded.

## The case

In the 1513/1523 one-free residual-six trichotomy, Type III has c = k_u in
{0,3}, the singleton at u, and exactly two distinct cost-two nonsingleton
departures, both containing u. Each is a cubic with numerator -2 or +1 or
a positive quintic with numerator 2. For p = Delta_u f these become two
departures of the thirteen-coordinate ternary derivative: a pair numerator
-2 or +1, or a doubled quartic l_D = 2. Every other pair numerator is -1/0,
every other quartic 0/1, ordinary quadratic coefficients 0/1, p(0)=1 and
p(e_v)=0 (1513 section 1). Two departures are two pairs (adjacent or
disjoint, signs (-2,-2), (-2,+1) or (+1,+1)), or at least one doubled
quartic. These alternatives are exhaustive.

## Subcase by subcase

Common facts of the pair theorems, all constant-free (re-derived in each
audit): Q_v = 2D_v - 4 at every vertex, E = 49 + c, every triangle lies in
zero or two tetrahedra, and vertex links are closed surfaces with chi = 2
(at a -2 endpoint only after the accepted C6 / no-two-C3 step). In their
disconnected-link step, two six-vertex projective planes at an ordinary w
force 42 edges, so the cross-edge count is M = E - 42 = 7 + c, which is 10
at c = 3. In the parts used, this is the only constant-dependent step,
apart from the (+1,+1) closing scan range E = 49 + c <= 52, tight at
c = 3. The full models also contain face-count rows that depend on c; the
selected certificate rows do not use them. The source's special
coefficient-two branch (E = 48 + c) does need c <= 2 but is not used,
since ordinary quadratic coefficients are 0/1 for every one-free
derivative.

| Departures | Accepted at | c = 0 | c = 3 |
|---|---|---|---|
| adjacent -2,-2 | 1526/1527 for c = 0..3 | accepted | accepted |
| two +1 (adjacent or disjoint) | c <= 2, `006/two-positive-cubic-free-derivative.md` | inside source scope | new argument, `EXTENSION-plus-plus-c3.md` |
| adjacent -2,+1 | c = 1,2, `006/two-mixed-cubic-accepted-manifest.json` | bounds stronger | bounds still contradict |
| disjoint -2,-2 or -2,+1 | c = 1,2, `006/two-disjoint-cubic-ordinary-accepted-manifest.json` | bounds stronger | bounds still contradict |
| doubled quartic with a quartic or a pair | m_e = 1 part of `009/two-exception-positive-quartic-special-edge-manifest.json` | c not used | c not used |

Adjacent -2,+1 (`two-mixed-cubic-derivative.md` lines 31-43). Endpoint
cross degrees are at least 1, 3, 1: the degrees are at least 7 (link(a) is
a sphere with one degree-three vertex, source lines 18-24), 9 (the
one-six-edge filter gives orders 9..11) and 7 (y_x = 2D_x - 13 >= 0),
against five same-side neighbours plus w, six in all. If all nine good vertices have cross degree at least
two, 2M >= 18 + 5 = 23, so M >= 12 > 10. Otherwise a good cross-degree-one
vertex makes its neighbour universal to the opposite side and the other
five vertices on that side each need a cross edge: M >= 11 > 10.

Disjoint pairs (`disjoint-cubic-local-reduction.md` lines 17-24). Negative
endpoints have cross degree at least 3 (sphere links of order 9..11),
positive endpoints at least 1. If all eight good vertices have cross degree
at least two, 2M >= 24 (mixed) or 28 (two negatives), so M >= 12 > 10.
Otherwise the universal neighbour gives 6 cross edges and, since every
vertex needs a cross edge and no vertex lies in two exceptions, the other
five on its side add 5: M >= 11 > 10, with no slack at c = 3. This breaks
at c = 4, which Type III does not need.

At c = 0 both bounds read M <= 7 and the written proofs apply verbatim.
After the ordinary links are spheres, the remaining steps of both pair
theorems (endpoint sphere catalogs, root-link cover, placements) are
constant-free, and their finite certificates use no constant-dependent row:
the accepted reports record `global_face_count_rows_used = 0` and
`constant_independent_selected_rows = true` (mixed), and the disjoint
compact verifier rejects face-count rows as constant-sensitive while the
branch proofs are built with face-count rows removed. Their stated scope
c in {1,2} is inherited framing, which their own audits say does not
extend by itself; this note supplies the missing structural step.

Doubled quartic. The proof for ordinary coefficient m_e = 1
(`006/two-exception-positive-extension.md`, accepted in
`006/independent-math-audit/connected-six-unit-exclusion-audit.md`) works
at a private vertex x of the doubled quartic, outside the other departure.
There A_x + P_x = 8 and 4d = A_x + 3P_x give a link with Euler
characteristic 3, which the surface lemma excludes. The accepted audit
states that this "does not require a bound on c" (lines 53-55); the
special-edge note says the same of its m_e = 2 part. The "1 or 2" in the
manifest refers to m_e, not to c.

## Conclusion and premises

If accepted, Type III is excluded at c = 0 and c = 3, so the one-free
residual-six case reduces to Types I and II (both c in {1,2}). Conditional
on: the accepted local premises of each source theorem (the one-six-edge
and one-three-edge arguments, the six-vertex and pentagon lemmas, the
endpoint sphere catalogs and their inherited inverse-cover completeness),
the 76-record scan and the published edge-valence-five catalog (Frick 2015,
Theorem 3.10) for the (+1,+1) case, the 1526/1527 acceptance, and the 015
sphere enumeration for the L7/L8 lemmas.

What was replayed (REVIEW-closure.md): an AI reviewer rebuilt the models at
c = 0 and c = 3 and confirmed that the selected rows are identical at their
original indices, then replayed them, for both mixed compact proofs (at
c = 0..3), all 66 disjoint compact proofs and all 69 disjoint branch leaves.
Branch-tree coverage and the per-row literal-necessity reconstruction are
inherited from the accepted verifiers, and the replay scripts are scratch
files, not a frozen successor checker.

Types I and II, the no-free case and residual defect above six remain
open. No whole magnitude pattern changes. Global status: OPEN.
