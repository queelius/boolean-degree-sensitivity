# Three-free classification at residual defect at most six

This written argument is the independently accepted1391/1393 classification,
restated with its inherited assumptions explicit. All original proof/review
pins are retained in PROVENANCE.json and provenance/source/. It is a necessary
classification, not an existence assertion. No new catalog or solver is used.

Use the setting and exact costs of THEOREM.md, with g=1-2f and k=16*g_hat in
the accepted selfdual-empty existence representative. All negative quintics
are fixed before the residual budget is formed. OLD_LOCAL_012 assumes the old
ordinary derivative exclusions with at most two nonsingleton cost-two
departures at constant1/2. We additionally name **BASELINE_LE3**: the older
baseline derivative exclusion with constant c<=3, ordinary quadratic0/1,
quadratic Fourier numerators-1/0 and quartic numerators0/1. The latter retains
its published complete small-valence-manifold and finite-scan premises; this
packet does not regenerate them. It does not broaden the two-exception theorem
to constants0/3.

Suppose at least three coordinates avoid every negative quintic and choose
three of them, F0. The cost-two departures are singleton0/3, cubic-2/+1 and
positive quintic2; the cost-six departures are singleton-1/4, cubic-3/+2 and
positive quintic3. There is no single cost-four departure. Repeated abstract
types always mean distinct physical coefficients.

With at most two cost-two departures, choose a member of F0 avoiding every
exceptional singleton owner. Its actual singleton constant is1/2 and at most
two nonsingleton departures are incident. OLD_LOCAL_012 excludes its ordinary
derivative. The same argument covers three cost-two departures with one or
two singleton owners. If all three are singleton departures, there are no
nonsingleton departures and each free derivative has constant at most three,
even if all three chosen coordinates are owners. BASELINE_LE3 excludes it.
This is the only c0/3 fallback; no per-coordinate defect charging is used.

Now consider three nonsingleton cost-two departures. A member of F0 missing
one support would see at most two departures at a baseline constant. Thus all
three supports contain F0. Two distinct cubic departures cannot both contain
F0: a cubic has exactly three coordinates and a physical coefficient cannot
count twice or take two values. If there is one cubic, it is F0; the other
departures are doubled quintics F0+A and F0+B with distinct two-element tails.
Choose w in A minus B. In the derivative at v in F0, w lies in exactly one
doubled quartic and avoids the exceptional quadratic F0 minus{v}. The
incident-only private-tip lemma in THEOREM.md excludes it. If all three
departures are doubled quintics, their derivative quartics all contain the
baseline pair F0 minus{v}. Their weight is at least six, exceeding the
ordinary inversion bound4m-a<=5. Hence this case is also impossible.

For a single cost-six singleton, choose a different member of F0; its derivative
is baseline. A tripled positive quintic either misses a free coordinate or
gives exactly the tripled quartic excluded in THEOREM.md. A cost-six cubic
must contain every member of F0, or a missed derivative is baseline. Its support
is therefore exactly F0. If its numerator is+2, the exceptional unit link has
size4m-2: negative for m=0 and two for m=1. A nonnegative simple even graph
cannot have two edges, so+2 is impossible. The only remaining value is-3.
An additional free coordinate outside F0 would miss that sole departure and
again have a baseline derivative, so the entire free set is exactly F0.

Consequently the only remaining case with at least three free coordinates is

    F has exactly three coordinates, k_F=-3 is the sole departure,
    every singleton is1/2, every other cubic is-1/0,
    every nonnegative quintic is0/1.

The actual derivative at any v in F has thirteen coordinates, origin1, units0,
ternary range and ordinary quadratic coefficient f(vij) in{0,1}. No negative
quartic is present because v avoids every negative quintic. This gives the
precise input to ENDPOINT.md. The classification has not constructed a
derivative or a Boolean function. Its written proof, not a new portable
9,805-case classification replay, establishes this reduction. The packet's
61-allocation controls are supporting evidence, and the older local theorem
assumptions remain explicit in CLAIMS.json.
