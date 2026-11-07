# Independent cycle1523 review of the one-free residual-six packet

Alexander Richard Towell; substantial OpenAI Codex assistance. 21 October 2026.

The frozen cycle1513 proposal passes this independent mathematical review and
the small exact controls described below. This accepts necessary reductions,
not existence or nonexistence of their remaining cases. All 29 whole
magnitude patterns remain open, and the original Boolean14 problem is open.

The reviewed handoff SHA256 is
`b53cc1c87160b14800c0f66ffdec7c81ea253e68a6f86ad5c8cbfaff1cf9f163`;
the source manifest is
`e41c57eb57ffd4226dd9c88efc1823c36546f1af7c32fdd9c5388f0dbcac66b9`;
the written proof is
`e30a88eae5d15641bc4566938380702baab415ced2b0226295a541a8d4f08c22`.
Those files and all other predecessor files are unchanged. This review owns
only new cycle1523 artifacts in attempt008.

## Scope and inherited premises

The setting is the proved existence-preserving selfdual empty-pair
representative, not a claim that an arbitrary original solution is selfdual.
It has fourteen variables, degree at most five, origin truth zero, all
singleton/pair truths one, and integer odd Fourier numerators
`k_S=16*(1-2f)_hat(S)`. The level sums are `16,-104,104`; total squared
numerator norm is 256. Every negative quintic is fixed before calculating
the residual defect. A free coordinate belongs to none of those quintics.

The inherited local exclusions retain their exact historical premises:

* Baseline and one quadratic `+1` or `-2` allow `c<=3`.
* One doubled positive quartic uses its stated ordinary-quadratic and
  incident-domain guards and needs no added constant bound.
* Two nonsingleton cost-two departures are accepted here only at `c=1,2`.
* The tripled-quartic parity lemma is accepted by the cycle1386 authority.

The cycle1409 written guard audit and its predecessor authorities were read,
not replaced by an imagined constant-free theorem. The baseline audit
explicitly allows every `c<=3`, including `-1`; its historical complete
manifold classification remains an external premise. Other inherited small
sphere/certificate premises are also retained. None of those historical
catalogs or certificate computations was rerun in this audit.

## Corrected signed-star norm

Write `16p=c+sum a_J chi_J+sum b_D chi_D`, and let `A=sum a_J`,
`B=sum b_D`. The origin and thirteen unit values give, independently of
any edge-count interpretation,

```
c+A+B=16,       2A+4B=13*8,
B=36+c,        A=-20-2c.
```

Pair inversion is `4m_J=a_J+sum_(D contains J)b_D`. Summing it gives
`4 sum m_J=A+6B=196+4c`. For a signed three-star every active pair has
ordinary coefficient one, hence `E=49+c`. With `r` special numerators
`-2` and `3-r` numerators `+1`, their sum is `3-3r`. Therefore the number
of ordinary `-1` numerators is

```
N=(3-3r)-A=23+2c-3r.
```

Ordinary valence-four edges have numerator zero; ordinary valence-five
edges have numerator minus one. The three special edge valences are six
or three, respectively. Direct incidence gives
`5N+4(E-3-N)+6r+3(3-r)=6(36+c)`, an independent consistency check.
The squared norm is

```
||P||^2=c^2+N+4r+(3-r)+(36+c)=c^2+3c+62.
```

Thus at constants 1 and 2 the norms are respectively 66 and 72, and the
complementary integer Fourier norms are 190 and 184. Each nonzero integer
coefficient costs at least one norm unit; each individual square is at
most the total. Consequently the support bounds are 190/184 and both
amplitude bounds are 13. These are necessary upper bounds, not claims of
attainment.

For the old `c=2,r=1` example there are 24 ordinary minus-one and 24
ordinary zero numerators, not 48 minus-one numerators. The latter count
violates the origin and quartet-edge incidence equations. This independently
accepts the cycle1513 correction of the unused cycle1504/1506 norm example.

The old notes explicitly produced no extension matrix or witness. The
cycle1501 native authority instead binds the earlier necessary CNF body
and its two geometric units. Its source audit contains neither corrected
source-only example, and the exact CNF and LRAT hashes remain unchanged.
This correction changes no native proof claim. No native checker was
invoked here; the existing accepted LRAT authority is inherited.

## Complete one-free allocation reduction

For a free coordinate `u`, the derivative has origin one, units zero,
range `{-1,0,1}`, and actual ordinary quadratic coefficients in `{0,1}`.
The three residual costs are `(k-1)(k-2)`, `k(k+1)`, and `k(k-1)`.
Their only positive values through six are two and six. There are five
coefficient types of each cost. Hence the complete scalar allocations are
at most three cost-two departures, or one cost-six departure.

At total cost at most four, a baseline constant has at most two incident
nonsingleton departures and is excluded by the inherited theorem. A
singleton departure at `u` gives constant zero or three and leaves at
most one incident nonsingleton, within the inherited one-departure guard.

At cost six consisting of three cost-two departures, a baseline constant
can survive only if all three departures are nonsingletons incident with
`u`. Otherwise at most two remain locally. With an exceptional singleton
at `u`, the other two must both be incident nonsingletons. No other
singleton may then depart from baseline.

A single cost-six departure missing `u` leaves the excluded baseline
derivative. If incident, a tripled quintic is excluded by the accepted
tripled-quartic lemma. A cubic `+2` has a simple even positive pair link
with `4m-2` edges: either a negative count or two, neither possible.
A cubic `-3` is retained. A singleton `-1` uses the baseline `c<=3`
guard. A singleton 4 is impossible directly: all other thirteen singleton
numerators are baseline and their sum with 4 is at least 17, exceeding 16.

Exactly the following conservative necessary types remain:

| Type | Constant | Full residual departure inventory |
|---|---|---|
| I | 1 or 2 | One cubic `-3` containing `u` |
| II | 1 or 2 | Three distinct nonsingleton cost-two departures, all containing `u` |
| III | 0 or 3 | The singleton at `u`, plus two incident nonsingleton cost-two departures |

This is a cover of possibilities, not a feasibility claim. The independent
control derives all 61 scalar allocations and checks 530 one-coordinate
incidence/constant cases. It rejects 37 incidence masks that assign two
different singleton departures to the same coordinate. Repeated abstract
nonsingleton types denote distinct physical coefficients; retaining all
such incidence patterns is a conservative cover, not a support catalog.

The old findings ledger has 30 historical open entries. Removing the
separately accepted cycle1388 magnitude exclusion gives 29; no ledger was
edited. Recomputed residual cost six selects exactly `(2,2,1^5)`,
`(2,1^8)`, and `(1^11)`. Larger-residual inventories are outside this result.

## Complement normalization and endpoint deduction

For a Boolean fiber `(f(0,x),f(1,x))`, put `p=f(1,x)-f(0,x)` and
`q=f(0,x)+f(1,x)-1`. All four fiber possibilities give
`pq=0`, `p^2+q^2=1`, and `h=z*p-q`. Selfduality reverses and complements
the fiber, making `p` complement-even and `q` complement-odd. Therefore
`Q=16q` has 1,586 possible odd Fourier indices. Without the proved
selfdual representative there would instead be 2,380 degree-at-most-five
indices, and restricting to the odd family would not be justified.

In every retained type all departures meet `u`. The exterior coefficients
are baseline, and the moments derived above and global level sums yield
the exterior `Q` sums `c-16,84-2c,c-68`. Its singleton entries are
`-1/-2`, with `3-c` copies of `-2`; its cubic entries are `0/1`, with
`84-2c` ones. If the fixed negative magnitudes sum to `M`, the other
quintic entries have `M+68-c` copies of `-1`. Negative cost 22 means
`sum m^2=22-M`. Consequently the exterior squared norms by level are
`22-3c,84-2c,90-c`, giving

```
||Q||^2=196-6c,       ||P||^2=60+6c,       c in {0,1,2,3}.
```

These formulas require the complete incident allocation and cost 22.
They are not formulas for arbitrary local polynomials. The fixed-`P`
annihilator is linear in `Q`; if both are unknown the same equations are
bilinear. No new linear rejection or target solve follows from this audit.

In Type I, the local cycle1395 argument depends only on this single
available free derivative. Pair inversion, parity and ordinary coefficients
exclude the exceptional `C3` and split `C3+C4` cases. Each exceptional
endpoint link is therefore an actual sphere with one degree-seven vertex
and all others degree four or five. No derivative at a second free
coordinate is needed to obtain either endpoint link of this one complex.

Removing the other endpoint's open star from either sphere leaves an
actual triangulated disk with boundary seven, boundary degrees three/four
and interior degrees four/five. The separately accepted cycle1401 written
disk lemma needs only these disk hypotheses and requires at least three
interior vertices. The endpoint order is thus `1+7+I`, with `I>=3` and
at most 12 vertices available, so it is 11 or 12.

The two endpoints and their common seven-cycle leave four physical
coordinates. Each disk uses at least three of those four as interiors,
so at least two occur in both. Such a coordinate is adjacent to both
endpoints but is absent from their edge link, giving a missing triangle
through the exceptional edge. The independent 25-pair subset control
has intersection counts `12,12,1` at sizes `2,3,4`. It checks this last
set calculation only; the reviewed planar disk proof supplies the
topological premise. The whole tetrahedral complex has not been proved
a manifold, and no whole-complex homology or Walkup inference is accepted.

## Acceptance boundary and reproducibility

The `c=0/3` two-nonsingleton extension is **pending future work**. It is
not used in the trichotomy: Type III is deliberately retained. In the
cited older authority chain, cycle1386 selects a baseline singleton,
cycle1393 avoids exceptional singleton owners when needed, and cycle1409
uses `c=0/3` only with zero or one nonsingleton departure. This review
finds no invalid constant widening in that chain and reopens no accepted
ledger exclusion. It does not purport to re-prove every historical result
in the repository.

The new checker imports no producer or earlier audit implementation. It
freshly verifies 38 source hashes, the scalar/incident allocation cover,
all eight signed-star `(c,r)` counts, twelve complete-allocation norm
cases, four Boolean fibers and 25 endpoint interior-set pairs. Normal,
optimized and instrumented results agree after omitting elapsed CPU time.
Eight unit controls pass in normal and optimized modes. They include
wrong-norm rejection, a real constant-guard countercontrol, missed-support
and repeated-singleton guards, exact source corruption, sign checks, and
an optimization-safe failure test. All 261 statements and 76 branches of
the new checker were covered; this is software control coverage, not
formal mathematical verification.

Each checker/test process enforces three CPU seconds and 512 MiB. The full
normal arithmetic/source pass used about 0.066 CPU seconds; the covered
pass used about 0.137. No target catalog, solver, native checker, or Boolean
construction search was run. The first coverage invocation failed because
the ordinary Python environment lacked the coverage module; that log is
preserved. The installed coverage CLI completed the independent run without
installing software or altering sources.

From the repository root, the core commands are:

```
/home/spinoza/venv/bin/python .research/attempts/008-sparse-spectrum-proof/one_free_independent_cycle1523.py --output /tmp/one-free-replay-cycle1523.json
/home/spinoza/venv/bin/python -O .research/attempts/008-sparse-spectrum-proof/one_free_independent_cycle1523.py --output /tmp/one-free-replay-O-cycle1523.json
/home/spinoza/venv/bin/python .research/attempts/008-sparse-spectrum-proof/test_one_free_independent_cycle1523.py -v
/home/spinoza/venv/bin/python -O .research/attempts/008-sparse-spectrum-proof/test_one_free_independent_cycle1523.py -v
```

This supplies a source-bound correction and conditional written contribution
for the next coherent archival version of the research packet, with its
historical premises retained. It is independent AI review and exact small
computation, not human peer review, proof-assistant formalization, a novelty
assessment, or a solution. No publication or new DOI was created.
