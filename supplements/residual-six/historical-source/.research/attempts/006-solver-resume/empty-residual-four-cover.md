# Negative-support coverage with four residual defect units

Status: proposed transfer of independently accepted local theorems. The
global Boolean-function decision remains open. No magnitude pattern is
excluded by this note alone.

Let f be a self-dual fourteen-variable degree-at-most-five Boolean function
in the empty-zero-pair profile. Thus f(0)=0, all unit values and all pair
values are one. Put g=1-2f and k_S=16 g-hat(S). After fixing every negative
quintic numerator, suppose the remaining defect is at most four. Then
the union of their supports is all fourteen coordinates.

## Exact transfer

The nonnegative even defect costs on the remaining coefficients are

    singleton: (k-1)(k-2), cubic: k(k+1), quintic: k(k-1).

Cost zero means k belongs respectively to {1,2}, {-1,0}, and {0,1}.
The only nonzero costs at most four are cost two: singleton 0 or 3,
cubic -2 or +1, and nonnegative quintic 2. Every next departure costs
at least six. Thus there are at most two exceptional coefficients, and
every singleton numerator is at most three. Negative quintics are already
fixed and their full costs have been subtracted; they are not treated as
residual exceptions.

Suppose a coordinate v belongs to no negative quintic. The actual
derivative p=Delta_v f on the other thirteen coordinates is ternary,
has p(0)=1 and p(e_i)=0, and has the even Fourier expansion

    16p = k_v + sum_(|A|=2) k_(A+v) chi_A
                    + sum_(|D|=4) k_(D+v) chi_D.

Its ordinary quadratic monomial coefficient on {i,j} is exactly
f({v,i,j}), hence lies in {0,1}. Its quartic Fourier coefficients are
nonnegative because v is outside every negative support. This is an
ordinary derivative: there is no exceptional ordinary coefficient two.

If at most one nonsingleton exception is incident with v, the accepted
baseline, one-positive-quadratic, one-negative-quadratic, and one-doubled-
quartic derivative obstructions apply. Their local constant bound is
k_v<=3, independently of whether the remaining defect was spent on a
singleton or on an exception outside v. This uses the actual local
hypotheses of the four accepted results; it does not incorrectly apply
the older global residual-at-most-two corollary to a residual-four function.

If two nonsingleton exceptions are incident with v, they consume all
four residual units. Every singleton is then baseline, so k_v is one
or two. The complete list of ordinary local possibilities is:

| Incident exceptions | Accepted authority |
| --- | --- |
| At least one doubled quartic | Parent two-exception positive-quartic manifest; the ordinary Euler-characteristic-three argument |
| Two quadratic numerators +1 | Parent local-audits-cycle64 manifest and two-positive-cubic parent audit |
| Two adjacent quadratic numerators -2 | Researcher two-adjacent-negative-cubic accepted manifest |
| Adjacent -2 and +1 quadratic numerators | Researcher two-mixed-cubic accepted manifest |
| Disjoint quadratic numerators, at least one -2 | Researcher two-disjoint-cubic-ordinary accepted manifest |

Two distinct pair supports intersect in zero or one vertex, so these
possibilities exhaust all geometries. Each accepted theorem excludes
its local derivative. Hence v cannot exist, proving full negative-support
coverage. No symmetry of f, numerical infeasibility, or local-to-global
existence assumption is used.

The inherited local proofs retain their explicit external dependencies:
the published complete small-valence three-manifold enumeration and the
accepted complete small-sphere catalogs. The present bookkeeping does
not independently regenerate those historical enumerations.

## Component consequence

The accepted top-convolution lemma says that the ordinary intersection
graph of negative supports is connected. If m supports form c components
under intersection-four adjacency, each such component with m_i supports
uses at most m_i+4 coordinates. Joining these components along an ordinary
intersection spanning tree saves at least c-1 coordinates. Therefore

    14 <= |union of negative supports| <= m+3c+1,
    c >= max(1, ceiling((13-m)/3)).

The frozen magnitude ledger has six previously uncovered open patterns
with residual exactly four:

| Negative magnitudes | Number of supports | Necessary Johnson components |
| --- | ---: | ---: |
| 3,1,1,1,1,1,1 | 7 | 2 |
| 2,2,2,2 | 4 | 3 |
| 2,2,2,1,1,1 | 6 | 3 |
| 2,2,1,1,1,1,1,1 | 8 | 2 |
| 2,1,1,1,1,1,1,1,1,1 | 10 | 1 |
| Twelve unit magnitudes | 12 | 1 |

In particular, the four-double and three-double/three-unit cases each
need at least three Johnson components. These are necessary restrictions;
none of the six whole patterns is declared excluded.

## Reproducible scope checks

`empty_residual_four_cover.py` derives the allowed exceptional values
from the three quadratic costs, enumerates all 21 abstract global
allocations and all incident/hidden local cases, and binds each to an
accepted local authority. It checks every immediate source hash in those
authorities. Repeated types in an allocation represent distinct global
coordinates or supports; this conservative allocation cover does not
assert that every listed allocation is realizable.

`empty-residual-four-cover.json` records the complete case list and the
derived component bounds. Its ledger input is frozen separately so future
accepted exclusions do not invalidate the source snapshot. Controls reject
residual six, two exceptions with nonbaseline constant three, repeated
pair supports, and unrecognized exception values; a corrupted-source
control checks the manifest adapters. These checks verify bookkeeping,
not the mathematical local theorems or a full fourteen-variable witness.
