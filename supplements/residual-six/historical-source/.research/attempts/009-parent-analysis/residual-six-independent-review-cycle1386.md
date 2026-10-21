# Independent review of the residual-six negative-support bound

Alexander Richard Towell; substantial OpenAI Codex assistance. 21 October 2026.

**Accepted under the explicit inherited local-theorem premises.** The reviewed
final proof is `residual6-negative-union-theorem-cycle1382.md`, SHA256
`677297733b1df5fb132ab7752f4a5c613ac73c818ff293387212dd8a687fea6f`.
This is an independent written mathematical review with separate exact small
controls. It is neither proof-assistant formalization nor human peer review.
The original fourteen-variable decision problem remains open.

The precise conclusion is: for the accepted selfdual empty-pair existence
representative, after fixing **all** negative quintic coefficients, residual
Fourier defect at most six implies that their supports cover at least eleven
coordinates. No assertion is made that every original solution is selfdual.
No symmetry of the unknown function or chosen support family is assumed.

## Normalization and complete exception cover

Write `g=1-2f` and `k_S=16*g_hat(S)`. The inherited exact normalization and
empty-profile budget give integer odd-level numerators and

`sum_i (k_i-1)(k_i-2) + sum_T k_T(k_T+1) + sum_Q k_Q(k_Q-1) = 28`.

Negative quintics contribute their entire costs before the residual budget is
formed. The remaining quintics are nonnegative. The five cost-two types are
singleton `0,3`, cubic `-2,1`, and quintic `2`; the five cost-six types are
singleton `-1,4`, cubic `-3,2`, and quintic `3`. There is no positive
single-coefficient cost four. Thus the allocations are exactly zero to three
cost-two departures, or one cost-six departure. Their multiset counts at costs
`0,2,4,6` are `1,5,15,40`, totaling 61. Repeated abstract types denote distinct
physical coefficients, not repeated copies or different values of one support.

If `v` avoids all negative quintics, the actual derivative `p=Delta_v f` has
thirteen variables, range `{-1,0,1}`, `p(0)=1`, and every unit value zero.
Differentiating the characters gives exactly

`16p = k_v + sum_A2 k_(A+v) chi_A + sum_D4 k_(D+v) chi_D`.

All quartic numerators here are nonnegative. The ordinary quadratic coefficient
is `m_ij=p(ij)-p(i)-p(j)+p(0)=f(vij)`, hence is zero or one. Fourier inversion
gives `4m_A=a_A+sum_(D contains A)b_D`, and cubic integrality gives an even
sum of `b_D` on each triple coface. These are necessary consequences of an
actual derivative, not freely selected coefficient conditions. The independent
basis controls check the scale, sign, and both inversion identities exactly.

## The tripled-quartic argument is sound

With baseline quadratic numerators, every weighted pair link has total size in
`{0,1,4,5}` and even weighted degrees. For a pair in the unique weight-three
quartic, size four would require one residual edge equal to the existing heavy
edge, which is forbidden. Size five requires two distinct unit edges. Their
odd-degree boundary must consist exactly of the heavy endpoints, so they form
a length-two path between those endpoints through a new vertex.

For heavy `abcd`, the `ab` path supplies `abcz,abdz`. The `ac` path shares the
already supplied edge `bz`, forcing the same middle vertex `z` and `acdz`.
The `bc` path similarly supplies `bcdz`. Consequently the ordinary `az` link
contains the unit triangle on `b,c,d`. It would need one or two further simple
edges to have allowed total size four or five. The triangle already has even
degrees; a nonempty simple even graph cannot have only one or two edges. This
is a contradiction. No bound on the constant, manifold catalog, or unproved
flag property is involved in this new local lemma.

The small controls enumerate 1,590 weighted links on six vertices (60 admissible
paths), all 171 triangle completions by one or two edges on seven vertices,
and 2,520 labeled forced-quartic configurations. Six and seven vertices suffice:
two residual edges use at most four endpoints beyond the fixed heavy edge or
triangle. Explicit controls show that allowing weighted size six, a positive
exceptional quadratic, or three added unit edges invalidates particular steps.
Those controls are arithmetic guard counterexamples, not ternary-polynomial
constructions outside the theorem's scope.

## The private-tip extension is genuinely local

I read the original `006/two-exception-positive-extension.md`, the prior
independent doubled-quartic audit, and the accepted special-edge extension's
independent audit. The latter already explicitly describes the calculation as
using only coefficients incident with the chosen vertex. Its use here is valid.

Let a derivative coordinate `w` belong to exactly one doubled quartic `D`;
all other quartics through `w` are binary and every quadratic through `w` is
baseline. A pair through `w` in `D` has residual unit link a triangle; a pair
through `w` outside `D` has empty, four-cycle, or five-cycle link. The original
two-pair argument forbidding a unit quartic through a triple of `D` containing
`w` uses only pairs containing `w`. Its forced contradiction is in a link
`{w,r}` outside `D`, so additional exceptional supports avoiding `w` cannot
change it.

The unit-tetrahedron link at `w` is therefore a disjoint union of closed
triangulated surfaces. It has exactly three degree-three vertices, the other
vertices of `D`, and every other degree is four or five. At most twelve
vertices occur. The two local equations

`A_w+P_w=8`, and `4d=A_w+3P_w`

give weighted incidence `P_w=2d-4`. Removing the doubled quartic subtracts
two, leaving `2d-6` unit triangles in the link and Euler characteristic three.
The first equation comes from `p(0)-p(e_w)`; all coefficients avoiding `w`
cancel, including the constant. This is the precise reason the extension
does not need a global bound on the number of nonincident exceptions.

For completeness, a connected closed surface with degrees at most five has
positive Euler characteristic, at most two. A characteristic-one component
has at least six vertices from `E=3(V-1)<=V(V-1)/2`, and at most six from
curvature; thus it has six degree-five vertices. Total characteristic three
on at most twelve vertices forces one such component and one characteristic-two
component. The latter contains all three degree-three vertices. Its curvature
equation is `9+2n4+n5=12`, with at most six vertices. The two possibilities
are `(n4,n5)=(1,1)` or `(0,3)`. The first demands degree five on only five
vertices. In the second, three universal vertices force nine distinct
triangles around the three degree-three vertices, but the surface has only
eight triangles. Both are impossible. This argument uses the elementary Euler
bound for a connected closed surface, not a small-surface enumeration.

Independent controls enumerate all 20 labeled graphs of degree sequence
`(3,3,3,5,5,5)` and all 900 eight-face candidates; none is a closed surface.
An octahedral sphere passes. A tetrahedral sphere plus a six-vertex projective
plane is a genuine characteristic-three countercontrol with **four**, rather
than three, degree-three vertices. A pinched pair of spheres fails the vertex
link condition despite each edge having two triangles. These prevent weaker
surface assumptions from being silently substituted.

## The four-coordinate selection exhausts the cases

Choose four distinct negative-free coordinates `F0`. With at most three
cost-two exceptions and at least one singleton exception, choose a coordinate
outside every exceptional singleton owner. It has constant one or two and sees
at most two nonsingleton exceptions. The same choice covers every allocation
of residual cost zero, two, or four. The older **global** residual-four covering
theorem is not a logical premise of this argument.

A sole cost-six singleton or cubic misses a coordinate of `F0`, yielding a
baseline derivative. A sole tripled positive quintic either misses one, or
gives the new tripled-quartic contradiction.

If all three cost-two exceptions are nonsingleton, every singleton is baseline.
Any coordinate of `F0` missing one exception would see at most two, so all three
supports must contain `F0`. A cubic cannot contain four distinct coordinates.
Hence the supports are three distinct doubled positive quintics `F0+{t_i}`
with distinct tips. Differentiating at any member of `F0` leaves each tip in
exactly one doubled quartic; the private-tip lemma just reviewed applies.

The independent finite incidence cover checks all 61 allocations against all
possible intersections with four chosen coordinates: 54,411 cases, after
discarding 1,784 impossible literal support aliases. Of these, 54,409 use an
old local theorem with constant one or two, one uses the tripled-quartic lemma,
and one uses the three-double private tip. This is a conservative support
incidence cover, not a realizability assertion. The source packet's exact 61
allocation rows are compared independently. Its 584 differently organized
single-coordinate templates are not claimed freshly replayed; they are
replaced for this gate by the complete four-coordinate incidence cover.

## Inherited guards and scope of acceptance

The authority and source audit bind these accepted local premises explicitly:

| Local context | Guard used here |
| --- | --- |
| Baseline or one quadratic `+1` | Thirteen variables, ternary range, correct origin/units, ordinary quadratic `0/1`, binary quartics, constant `1/2` (old bound `<=3`) |
| One quadratic `-2` | Same; the compact rows are constant-independent, but the structural reduction still requires `c<=3` |
| One doubled quartic | Baseline quadratics; ordinary `0/1`; the proof needs no constant bound |
| Two exceptional quadratics | Distinct pair supports; adjacent or disjoint; all sign combinations; constant `1/2` |
| Two nonsingleton exceptions including a double | Exact ordinary context; constant `1/2`; the private-coordinate proof is used |

No two-quadratic theorem is transferred to constant zero or three. The old
baseline/positive-quadratic proofs retain published complete small-valence
manifold classification; other local results retain their recorded small-sphere
coverage and finite certificates. I checked written guards and source pins,
not all historical classifications or certificate leaves afresh.

The connected-branch application is immediate: six five-sets connected by
intersection-four edges use at most `5+5=10` coordinates along a spanning tree.
Magnitude pattern `(3,1,1,1,1,1)` spends `12+5*2=22` of the empty budget 28,
leaving six. Thus this theorem excludes that connected branch. This argument
does **not** need the 496-class connected-support catalog or later local graph
tables. A whole-pattern exclusion still requires separate composition with the
accepted disconnected-branch theorem; this review changes no ledger and claims
no whole-pattern or global completion.

The final validation records eleven normal and eleven optimized-mode unit
controls, thirteen project tests, explicit `-O/-OO` CLI rejection, exact coverage,
source hashes and terminal output. The helper imports only Python's standard
library, never the producer or a solver. There is no new large enumeration,
Boolean-function search, publication, or mathematical novelty assessment.
