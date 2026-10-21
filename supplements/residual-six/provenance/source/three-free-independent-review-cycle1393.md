# Independent review: the three-negative-free-coordinate classification

Alexander Richard Towell; substantial OpenAI Codex assistance. 21 October 2026.

The main classification below is sound under the inherited local-theorem
premises. The accepted source version and exact pins are recorded separately
in the cycle1393 authority. This review covers only that classification; it
does not accept the subsequent proposed exclusions of ordinary coefficient
zero, a `C3+C4` link, or any asserted `C7`/manifold/sphere classification.

Let `f` be the accepted selfdual empty-pair existence representative on fourteen
variables, with real degree at most five, origin zero, and every singleton and
pair value one. Write `k_S=16*g_hat(S)`, `g=1-2f`. Subtract the entire defect
cost of **every negative quintic** and assume the residual is at most six. Let
`F` be the coordinates in none of those negative supports. Then:

> If `|F|>=3`, necessarily `|F|=3`, the one residual exception is
> `k_F=-3`, and every other unfixed coefficient is baseline: singleton
> numerators `1/2`, other cubic numerators `-1/0`, and nonnegative quintic
> numerators `0/1`.

This is a necessary classification of a possible survivor. It asserts neither
its existence nor its nonexistence. Fixed negative quintics are not called
baseline. The implication applies to the existence-preserving representative;
it is not a claim that an arbitrary original solution is selfdual.

## Exact coefficient cases and local guards

The accepted cost identity uses `(k-1)(k-2)`, `k(k+1)`, and `k(k-1)` at
levels one, three and five. The last is applied only to nonnegative quintics
after the fixed negatives are removed. Thus the ten possible exception types
and the 61 allocation multisets are exactly those already independently
checked in cycle1386: five cost-two types, five cost-six types, and no positive
individual cost four. Repeated abstract types represent distinct coefficients.

Select three distinct elements of `F`, called `F0`. For `v` in `F0`, the actual
derivative has the already checked scale-sixteen even Fourier form, thirteen
variables, ternary range, origin one, all units zero, and ordinary quadratic
coefficients zero or one. Its quartic numerators are nonnegative. It retains
exactly the nonsingleton exceptions containing `v`; its constant is `k_v`.

With zero, one, or two cost-two departures, choose `v` outside all exceptional
singleton owners. This is possible because at most two coordinates are
excluded. Its constant is one or two and it sees at most two nonsingleton
exceptions. The accepted baseline, one-exception, and complete two-exception
ordinary derivative exclusions apply with their exact domain and geometry
guards. The same argument works with three cost-two departures when one or
two of them are singletons.

The remaining singleton case is essential: all three departures might be
singletons occupying all of `F0`. Then every derivative has **no** nonsingleton
exception and its constant is zero or three. The independently accepted
baseline theorem explicitly allows `c<=3`, including both values. It therefore
excludes this case. No two-quadratic theorem is applied at constant zero or
three. If the three singleton owners do not cover `F0`, the earlier
baseline-constant argument already works.

## Three nonsingleton cost-two departures

All singleton constants are now baseline. If a coordinate of `F0` misses an
exception support, its derivative sees at most two and is excluded by the old
theorems. Thus every one of the three supports contains all of `F0`.

Two distinct cubic supports cannot both contain `F0`: each has size three and
would equal `F0`. This also forbids two different exceptional values being
assigned to that one coefficient. If there is exactly one cubic, the other
exceptions are two distinct doubled positive quintics `F0+A` and `F0+B`, where
`A,B` are distinct two-element subsets of the eleven outside coordinates.
The difference `A-B` is nonempty. Choose `w` in that difference and differentiate
at any `v` in `F0`. The exceptional quadratic is `F0-v`, which avoids `w`.
Exactly one of the two doubled quartics contains `w`. Every quadratic through
`w` is therefore baseline, and every other quartic through it is binary. These
are precisely the incident-only private-tip conditions accepted in cycle1386.
The other double and exceptional quadratic avoid `w`; their presence does not
affect the origin/unit difference or any pair/triangle equation used in that
proof. Hence this case is impossible.

If all three exceptions are doubled positive quintics, differentiate at any
`v` in `F0`. The baseline quadratic pair `F0-v` lies in three distinct doubled
quartics, so its weighted quartic incidence is at least six. Pair inversion
gives incidence `4m-a`, at most five for `m in {0,1}` and `a in {-1,0}`.
This contradiction requires the quadratic pair to be baseline. The budget
ensures it: all six residual units are already spent on the three doubles.

## A single cost-six departure

A singleton exception leaves another coordinate of `F0` with a fully baseline
derivative. A tripled positive quintic either misses a coordinate, giving a
baseline derivative, or produces the single-tripled-quartic obstruction
accepted in cycle1386. No new constant bound is needed for that obstruction.

For a cubic exception, any negative-free coordinate outside its support has a
baseline derivative. Consequently the entire free set `F` is contained in
that cubic support. Since `|F|>=3`, both are the same three-set. If the cubic
numerator is `+2`, the exceptional pair in a derivative has binary quartic
incidence `4m-2`. At `m=0` it is negative, impossible. At `m=1` it is two, but
cubic integrality forces all degrees of the simple pair-link graph to be even.
No simple graph with two distinct edges has even degrees. Binary quartics
are essential: a doubled edge would evade this parity obstruction, but another
exception cannot coexist with the cost-six cubic.

The only type not excluded is therefore the cubic `-3` on exactly `F`. It
already consumes six residual units, so every other residual coefficient must
have zero cost. This proves every part of the stated classification. No truth
value for `f(F)` is imposed by this review.

## Independent finite controls and limitations

The new helper imports no cycle1391 producer or solver. It reuses the frozen,
independently accepted cycle1386 cost/type and literal link/private-tip helpers,
with that reuse explicitly source-bound. Its new three-coordinate selection is
independent of the producer's allocation labels.

All 61 allocations are checked against all possible intersections with `F0`.
After discarding 484 impossible aliases of complete physical supports, there
are 9,805 incidence cases:

| Route | Cases |
| --- | ---: |
| Old local theorem, constant one or two | 9,775 |
| Baseline with an exceptional singleton constant zero or three | 24 |
| One cubic and two doubles, private tail | 2 |
| Three doubles, common-pair weight | 1 |
| Tripled-quartic obstruction | 1 |
| Cost-six positive cubic, two-edge parity obstruction | 1 |
| Remaining cubic `-3` on all of `F0` | 1 |

The literal tail controls cover all 2,970 ordered pairs of distinct two-sets
on eleven outside coordinates and all 8,910 derivative/private-tip checks.
They cover all 26,235 triples of distinct tails and all 78,705 derivative
common-pair checks. All fifteen simple two-edge graphs on four vertices fail
the required even-degree condition; four vertices suffice for any two-edge
graph. A triangle and a doubled edge are genuine parity-positive controls.
Alias, budget, signed-type, singleton-constant, and optimized-CLI guards are
also tested. These are conservative necessary-case controls, not a search for
an actual fourteen-variable function.

The baseline and other inherited local exclusions retain their published
small-valence manifold classification, small-sphere coverage, and exact finite
certificate premises. Those historical computations are not replayed here.
The cycle1386 private-tip and tripled-quartic arguments are accepted premises;
their large predecessor catalogs are not imported into the new elementary
common-pair or positive-two arguments.

No later cycle1391 topology argument is a premise of this result. In particular,
this gate neither excludes `f(F)=0`, nor forces a seven-cycle, nor licenses
using the old valence-six catalogs for a valence-seven link. No ledger, support
pattern status, solver model, publication, or global decision is changed. No
human peer review, formal verification, or novelty claim is asserted.
