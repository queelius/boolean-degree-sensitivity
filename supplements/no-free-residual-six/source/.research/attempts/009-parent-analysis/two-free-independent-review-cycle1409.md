# Independent two-free residual-six classification

Alexander Richard Towell; substantial OpenAI Codex assistance. 21 October 2026.

The main necessary classification proposed in
`two-free-residual6-review-cycle1405.md`, SHA256
`b722030e267ca32e8f5a64bdb8a5e4234bcdebc803c5e49e31f866e53a6d292c`,
is valid under the inherited representative, integrality, defect and local
classification premises below. Its formerly pending two-free minus-three
step is proved explicitly here. The separate all-positive sign refinement is
reviewed in `positive-star-independent-review-cycle1409.md`; it is not folded
silently into the main type authority.

**Main conclusion.** In the selfdual empty-pair existence representative on
fourteen variables, suppose that subtracting the complete cost of all
negative quintics leaves Fourier defect at most six and that at least two
coordinates avoid those quintics. Then the full set of such coordinates is
exactly a pair `F={u,v}`. The only residual departures are three distinct
cubics `F+{x1}, F+{x2}, F+{x3}`, each with Fourier numerator minus two or plus
one. The singleton numerators are one or two, all other cubic numerators are
minus one or zero, and all nonnegative quintic numerators are zero or one.
The three departures use the full residual budget six. Before the separate
sign refinement, all eight signings of the three distinct tips are retained.

This is a necessary classification, not the construction or exclusion of its
remaining types. It neither assumes selfduality of an arbitrary original
function nor changes a pattern ledger. The original existence problem is
open. Historical classifications and certificates are explicit premises,
not newly replayed computations.

## Setting and exact inherited local guards

Write `g=1-2f`, `k_S=16*g_hat(S)`. The accepted representative has real degree
at most five, `f(0)=0`, and every singleton and pair truth equal to one. Its
Fourier support has odd degrees one, three and five, with integer numerators.
Every negative quintic is fixed before computing the residual budget. A
coordinate is *free* here only if it belongs to none of those fixed negative
quintics.

For a free coordinate `v`, the derivative `p=Delta_v f` on the remaining
thirteen coordinates has values in `{-1,0,1}`, origin one, units zero, and
scale-sixteen Fourier degrees zero, two and four. Its ordinary quadratic
coefficient on a pair `J` equals the actual Boolean truth `f(J+v)`, hence is
zero or one. This follows from the origin, singleton and pair truths, and is
not an optional relaxation. Baseline derivative coefficients have constant
one or two, quadratic numerators minus one or zero, and quartic numerators
zero or one. No negative quartic can occur at a free derivative.

The accepted old local exclusions used here have the following exact guards.

| Incident nonsingleton departures | Allowed constant in the inherited exclusion | Essential premise |
| --- | --- | --- |
| None | `c<=3` | Baseline written reduction and complete 4,787-manifold classification |
| One quadratic `+1` | `c<=3` | Whole-derivative one-positive proof and its classification premises |
| One quadratic `-2` | `c<=3` | Structural reduction, complete endpoint coverage, later compact certificate audit |
| One doubled positive quartic | No extra constant bound | Elementary doubled-quartic proof with the stated coefficient domains |
| Two nonsingleton cost-two departures | `c in {1,2}` only | Accepted two-exception local exclusions |

In particular, the two-exception theorem is never used with `c=0` or `c=3`.
The singleton-departure cases that need those constants have at most one
incident nonsingleton departure.

The negative-quadratic guard deserves a precise distinction. The older six
case audit tested constants one and two. The later
`one-negative-quadratic-compact-exclusion-audit.md` explicitly accepts every
`c<=3` for which its structural reduction applies. Its separately accepted
report has three contradictions, 230 retained rows and 228 deductions, with
no retained global face-count row. The independent row constructor's only
three loads of `edge_count` are in its global face-count loop. The compact
rows therefore do not depend on that parameter. The structural use of
`E=49+c<=52` and the endpoint catalog coverage remain essential. This review
rehashes and reads that accepted evidence and its scope; it does not rerun
the 228 deductions, endpoint coverage or historical manifold catalog. The
old six-case receipt alone would not justify the larger constant range.

The old one-positive proof is a whole-derivative theorem. Its global cross-edge
and catalog arguments cannot be reused merely because a private endpoint has
one positive incident pair. The separate sign review gives an explicit local
countercontrol against that stronger inference. Likewise the one-negative
230-row certificates are not transferred to three negative quadratic pairs.

## A genuinely two-free minus-three obstruction

Suppose the sole residual departure is a cubic `k_T=-3`, where `T={u,v,w}`
contains two genuinely free coordinates `u,v`. The third coordinate `w`
need not be free. All singleton numerators are one or two, every other cubic
is baseline, and every nonnegative quintic is binary.

At each of the two available derivatives `Delta_u f`, `Delta_v f`, the local
form is exactly

```
16p = c - 3 chi_A + sum_(J != A, |J|=2) a_J chi_J
                    + sum_(|D|=4) b_D chi_D,
c in {1,2}, a_J in {-1,0}, b_D in {0,1},
p in {-1,0,1}, p(0)=1, p(e_j)=0,
ordinary quadratic coefficients m_J in {0,1}.
```

Here `A=T` minus the derivative coordinate. These are precisely the local
hypotheses of the argument written in the accepted cycle1395 review. The
cycle1395 global authority was stated under the three-free classification;
we do not widen that authority by assertion. Instead we reapply its local
proof, checking which hypotheses it uses:

1. Pair inversion gives `4m_J=a_J+sum_(D contains J)b_D`; triple integrality
   makes pair links even. Baseline links are empty, `C4`, or `C5`. Every
   tetrahedral triangle contains a baseline pair and hence has two cofaces.
2. The exceptional link has `4m_A+3` edges and degree two at each vertex.
   It is `C3` for `m_A=0`, or `C7`/disjoint `C3+C4` for `m_A=1`.
3. At an exceptional endpoint, the actual origin/unit identities yield
   `A_x+P_x=8`, `4d_m=A_x+3P_x`, and `P_x=2d_m-4`. The local sphere/count
   arguments excluding `m_A=0` and split `C3+C4` use only these identities,
   the listed coefficient domains and at most twelve endpoint-link vertices.
   They do not use a derivative at the third core coordinate.
4. The remaining endpoint link is a sphere with one degree-seven vertex and
   all other degrees four or five. Its order is nine through twelve. This
   is the elementary endpoint conclusion, with no whole-complex manifold,
   flagness, Walkup or catalog premise added.

For clarity, the local contradictions in step 3 retain the exact degree
guards. The zero case is a surface union of characteristic three with one
degree-three vertex. It would be a small sphere plus a six-vertex
characteristic-one component; the sphere would have degrees `(3,4,4,4,4,5)`,
contradicted by the pentagon obtained on deleting its universal vertex.
The split `C3+C4` case has characteristic three on at most thirteen vertices.
Both split copies lie in the sphere, are nonadjacent, and have disjoint
neighbor sets of sizes three and four; together with the required six-vertex
other component this needs at least fifteen vertices. These are local
arguments even when `w` belongs to a negative quintic elsewhere.

It follows that `f(T)=1` and that the literal graph `C` whose edge `xy`
means `k_(T+x+y)=1` is a seven-cycle. Both derivatives see the same actual
coefficient, not an isomorphic replacement selected independently.

For each core pair `B` in `T`, define a triangle complex `D_B` on coordinates
outside `T` by the triangles `Y` for which `k_(B+Y)=1`. Every core pair
meets `{u,v}`. Realize all three complexes as follows:

| Disk | Available derivative | Exceptional endpoint |
| --- | --- | --- |
| `D_uv` | `Delta_u f` | `v` |
| `D_uw` | `Delta_u f` | `w` |
| `D_vw` | `Delta_v f` | `w` |

The remaining member of `T` has link `C` in that endpoint sphere. Removing
its open star gives the actual antistar disk `D_B`. Boundary vertices have
disk degrees three or four, and interior vertices retain degrees four or
five. All three boundaries are the same literal cycle on the same seven
coordinates. All possible interiors lie in the same four-set
`R=[14] minus (T union V(C))`. Every quintic used in any disk or the common
cycle contains `u` or `v`, so it cannot be negative. The possible negative
quintics through `w` alone are irrelevant to these constructions.

The accepted pure disk lemma1399, independently proved in1401, requires at
least three interior vertices in each such disk. We recall why its scope is
independent of freeness: in a seven-boundary triangulated disk, an empty
side of a boundary chord has a whole-disk degree-two ear. With no interiors
there is an ear, and with one there are no chords and the interior has
degree seven. With two interiors, the ten nonboundary edges are chords,
spokes and possibly their mutual edge. Adjacent interiors force no chords
and degree sum eleven. Nonadjacent interiors permit at most two chords;
zero chords give too few faces, one forces a degree-five chord endpoint,
and two force a degree-six shared endpoint of the empty middle triangle.
Each contradicts the disk degree guards. Thus all three actual disks require
at least nine interior incidences.

At an off-cycle unit `z=e_r`, `r in R`, the full-core Fourier block is

```
B_T(z) = -3 + sum_(xy in C) chi_xy(z) = 4.
```

Its exact eight-point core normalization is
`B_T=-4 sum_(X subset T) (-1)^|X| f(X,z)`. The four truths for `X` empty or
singleton equal one by the original singleton/pair layers. Therefore, writing
`s_B=f(B+r)` and `h=f(T+r)`,

```
sum_(B a pair in T) s_B - h = 1.
```

Booleanity allows at most two of the three `s_B` to be one. For each pair
`B`, choose its free derivative as in the table. Its pair inversion is

```
4s_B = k_(B+r) + sum_(Q quintic containing B+r) k_Q.
```

The cubic is baseline; the quintics are binary and nonnegative because `B`
contains a true free coordinate. A contributing quintic containing all of
`T` would give a cycle edge through `r`, impossible off-cycle. The sum thus
counts triangles of `D_B` incident with `r`. If `s_B=0`, there are zero or
one such triangles; the simple even link cannot have one edge, so `r` is
absent. If `s_B=1`, there are four or five and `r` is an interior vertex.
Thus `s_B` is exactly its disk-interior indicator. Four possible coordinates
with at most two incidences each give at most eight, contradicting nine.

This establishes the needed two-free minus-three exclusion without assuming
the third core coordinate free, or an entire tetrahedral complex to be a
manifold. The negative sign, scale four and off-cycle restriction are the
same exact identities independently controlled in1401; one free coordinate
alone would not realize all three disks and is outside this argument.

## Complete residual allocation and incidence reduction

The integer coefficient costs are `(k-1)(k-2)`, `k(k+1)`, and `k(k-1)` at
the singleton, cubic, and nonnegative-quintic levels. Up to budget six, the
five cost-two departures are singleton zero/three, cubic minus-two/plus-one,
and quintic two. The five cost-six departures are singleton minus-one/four,
cubic minus-three/plus-two, and quintic three. There is no cost-four single
departure. These give 61 unordered abstract allocations, including the
empty allocation. Repeated abstract types still mean distinct physical
coefficients. Partial incidences with the chosen free pair are conservative
supersets; only collisions that specify an entire identical support are
discarded.

For at most two cost-two departures, choose a free coordinate with baseline
singleton and at most two incident nonsingleton departures, unless both
free coordinates are exceptional singleton owners. In that case no
nonsingleton remains and the `c<=3` baseline theorem suffices.

With three cost-two departures, one singleton owner can be avoided, leaving
at most two nonsingleton departures and a baseline constant. If two singleton
owners cover the free pair, either coordinate has constant zero/three and
at most one nonsingleton departure, exactly the guard proved above; if they
do not, choose a missed baseline coordinate. With three singleton owners
there are no nonsingleton departures and each actual constant is at most
three. Thus the only possible cost-two escape is three nonsingleton
departures, each containing both free coordinates. If one missed a free
coordinate, the derivative there would have baseline constant and at most
two incident departures.

A sole cost-six departure missing one chosen free coordinate leaves a
baseline derivative. A singleton necessarily misses one. A quintic three
containing both gives the previously accepted tripled-quartic contradiction.
A cubic plus-two gives a pair link of size `4m-2`, either negative or two;
a simple nonnegative even graph cannot have two edges. A cubic minus-three
containing both is excluded by the preceding new two-free argument.

The independent incidence control enumerates all 61 allocations against the
two labeled free coordinates: 1,746 incidences after 134 impossible complete
support aliases. It finds 1,718 old-local uses, 15 missed-cost-six baseline
uses, one tripled quartic, one positive-cubic parity case, one newly justified
minus-three case, six doubled mixtures and four abstract cubic-sign
multisets. Among the old-local uses, 362 select the legitimate constant-zero
or constant-three guards. The four sign multisets encode all eight physical
signings; they are neither four functions nor four global cases.

## Eliminating every doubled-quintic mixture

The remaining departures share `F={u,v}`. Write cubics as `F+{x}` and doubled
quintics as `F+Y`, `|Y|=3`, with distinct full supports.

With two cubic tips and one triple tail, the tail has a vertex outside those
tips. With one cubic tip and two distinct triple tails, their symmetric
difference has at least two vertices and cannot be covered by that one tip.
Choose a difference vertex outside it. In either case the selected vertex
belongs to exactly one doubled quartic and no exceptional quadratic in an
available free derivative. The accepted incident-only private-tip argument
applies: every equation it uses contains that vertex, while the other
exceptions avoid it. Its actual quadratic domains, one doubled incident
quartic and baseline incident pairs are preserved; this is not the invalid
private-positive inference.

With three distinct triple tails, a vertex of multiplicity one gives the
same private-tip obstruction. Otherwise the nine tail incidences occupy at
most four vertices and at least four by distinctness. The tails are three
of the four triples of a four-set, with a common vertex `x`. In `Delta_u f`
the baseline pair `{v,x}` lies in all three doubled quartics, with weight at
least six. Baseline pair inversion allows at most `4*1-(-1)=5`; every other
quartic contribution is nonnegative. This is impossible.

The independent controls include all unions up to the largest relevant sizes
after relabeling: 100 two-tip/one-tail choices on five vertices, 4,165
one-tip/two-tail choices on seven, and 95,284 three-tail choices on nine.
The last divide into 94,780 private-tip and 504 common-pair cases. For every
private witness, the literal incident supports and avoidance of all
exceptional pairs are checked in both free derivatives. These are complete
finite controls of the elementary tail cases, not a Boolean-function catalog.

## Survivor and independent evidence

Only three distinct common-pair cubics remain, each numerator minus two or
plus one. Any additional free coordinate outside `F` meets at most one of
them, because their tips are distinct. Its singleton is baseline and its
derivative has zero or one exception, which the old local guard excludes.
Thus the full free set is exactly `F`, and the negative quintic union has
size twelve in this necessary type. The budget is exactly six.

The new helper imports only the previously accepted independent1386
allocation/literal helpers, not the1405 producer, a solver, a catalog
enumerator or the old compact deduction engine. It also checks all sixty
choices of a three-core and two true-free coordinates on six labeled
coordinates; every core pair is realized using an actually free derivative.
The test rejects one-free or outside-core substitutions. The 1,760 literal
tip/sign choices are `choose(12,3)*8` and are controls of support/sign
inventory only. They make no existence assertion.

Nine normal and nine optimized tests pass, including explicit `-O` and
`-OO` command-line rejection before output creation, invalid/bool support
aliases, excess budget, duplicate tails, misuse of the two-exception
constant guard, the private-positive countercontrol and separate tiny
all-positive surface check. Thirteen project tests pass. The owned helper
has 163/163 statements and 46/46 branches covered by the units and actual
CLI. Coverage measures exercised implementation paths, not formal proof.
The actual full control pass is preserved under coverage and repeated with
an explicitly observed terminal exit zero; all mathematical fields agree.

The written proof and controls are suitable for a conditional publication
packet with their exact inherited local/classification premises. This audit
does not publish, establish novelty, provide human peer review or formal
verification, replay all historical certificates, run a new target solver,
or change a canonical status. Mixed-sign endpoint geometry, a common-link
sphere catalog, and the separately proposed1412 result are outside its scope.
