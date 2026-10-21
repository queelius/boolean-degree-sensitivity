# Proposed residual-six bound: at most three negative-free coordinates

Alexander Richard Towell; substantial OpenAI Codex assistance.21 October2026.
Final proposed proof for independent review. Existing0/1/2-exception theorems are inherited;
the weight-three lemma and the coupled transfer below require fresh review.
No canonical status, whole-pattern exclusion or global completion is promoted.

## Exact normalization and old local guards

Work with the accepted selfdual empty-pair existence representative, not an
assumption that an original unknown solution is selfdual. Let every singleton
and pair truth be1 and f(0)=0. Use k_S=16*g_hat(S),g=1-2f. After fixing ALL
negative quintics, suppose residual Fourier defect is<=6. The remaining costs
are (k_i-1)(k_i-2), k_T(k_T+1), and k_Q(k_Q-1) for nonnegative quintics.
They are nonnegative even integers. Their cost-zero domains are {1,2},
{-1,0}, {0,1}. Cost2 values are respectively {0,3},{-2,1},{2}; cost6 values
are {-1,4},{-3,2},{3}. There is no single-coefficient cost4. Thus every
allocation is either at most three cost2 coefficients, or a single cost6
coefficient. Repeated abstract types refer to DISTINCT actual coefficients.
Negative quintics are not residual exceptions.

Let F be coordinates in no negative quintic. For v in F, p=Delta_v f on13
coordinates is ternary, p(0)=1,p(e_i)=0, and has

    16p=c+sum_A2 a_A chi_A+sum_D4 b_D chi_D,
    c=k_v, a_A=k_(A+v), b_D=k_(D+v)>=0.

Its ordinary quadratic coefficient m_ij is exactly f(vij), hence0 or1.
Its ordinary cubic coefficients are integers. In particular

    4m_A=a_A+sum_(D contains A)b_D,
    sum_(D contains T3)b_D is even.

The last identity says each weighted pair-link graph has even weighted
vertex degrees. All constants and coefficient domains here are derived from
the actual derivative, rather than chosen independently.

The accepted old local exclusions, in this ordinary0/1 setting, are:

* No nonsingleton exception: c<=3, baseline a in{-1,0},b in{0,1}.
* One quadratic+1 or-2: c<=3, other quadratics and all quartics baseline.
  For-2, use the later compact constant-independent certificate acceptance,
  not the old certificates explicitly restricted to c=1,2. Its preceding
  structural reduction STILL requires c<=3; no constant-unrestricted full
  negative-quadratic theorem is asserted. Every new use below chooses c=1or2.
* One doubled quartic: no constant bound, other incident domains baseline.
* Two quadratic cost2 exceptions, all adjacent/disjoint and sign choices:
  use c in{1,2}. The++ theorem's bound c<=2 is sufficient; do not transfer
  the other two-quadratic theorems to c=0 or3 here.
* Two nonsingleton cost2 exceptions including a doubled quartic: the accepted
  ordinary private-vertex/Euler argument applies. Only c in{1,2} is needed
  in this transfer. Its local private-vertex calculation does not use c.

These old results retain their published manifold/sphere and finite-certificate
premises. Structural reductions that were once labeled proposed are not
accepted solely from that label: the accompanying accepted manifests and later
independent audits must be bound. The historical findings summary describes
one-edge progress and is not a current residual-six theorem.

## New local lemma: a single tripled quartic is impossible

Assume p has the preceding ternary/origin/unit/ordinary-quadratic/integrality
conditions. Let all a_A be-1 or0 and all b_D be0 or1 except b_D0=3. There
is no bound on c. We claim no such p exists.

For a pair A inside D0, its weighted top-link size is4m_A-a_A, among0,1,4,5,
and it contains the edge D0 minus A with weight3. Thus m_A=1 and the size is
4 or5. All remaining edges are simple unit edges, distinct from that heavy
edge, with even total weighted vertex degrees. Size4 would leave just one
unit edge, which would have to join the heavy endpoints to repair parity;
that is the same edge and is unavailable. Therefore size5 holds, a_A=-1,
and the two residual unit edges form a length-two path joining the heavy
endpoints, through a vertex z outside D0.

Write D0={a,b,c,d}. Start with A={a,b}; the residual path produces unit
quartics abcz and abdz. The link at ac has heavy edge bd and contains unit
edge bz. Its residual length-two path therefore uses the SAME z and forces
acdz. The link at bc, containing unit edge az and heavy edge ad, similarly
forces bcdz. Hence all four other facets of D0+z occur with weight1.

The pair az lies in no tripled quartic. Its simple unit link contains the
triangle bc,bd,cd. But its allowed total size is0,1,4 or5 and all degrees are
even. A triangle already uses three edges; adding only one or two distinct
simple edges cannot leave all degrees even. Equivalently the symmetric
difference with that triangle would be a nonempty simple even graph with at
most two edges. Contradiction. This proves the new lemma, using only pair
inversion and parity, not a manifold catalog or an unproved local flag claim.

## Local extraction of the existing doubled-quartic private-vertex proof

The accepted proof in006/two-exception-positive-extension.md establishes the
following local fact. If a coordinate w of p belongs to exactly one doubled
quartic D, all other quartic numerators through w are0/1, and every quadratic
numerator through w is baseline, its unit-tetrahedron link has Euler
characteristic3 and exactly three degree-three vertices, all other degrees4/5,
on at most12 vertices. The accepted elementary surface argument excludes it.
The proof uses only coefficients incident with w: its pair links see one
weight2 edge/residual C3 or ordinary C4/C5, no unit tetrahedron contains a
triple of D through w, and removing D's weight2 changes incidence2d-4 to2d-6.
Thus other doubled quartics or exceptional quadratic pairs AVOIDING w do not
invalidate this local fact. This extraction needs explicit independent review
before using it beyond the original two-exception statement.

## Coupled transfer for four distinct coordinates of F

Assume |F|>=4 and select four distinct such coordinates F0. No independent
per-vertex defect charges are made; a global exception may affect several.

For actual residual cost<=4 there are at most two cost2 departures. Choose v
from F0 outside all exceptional singleton coordinates (at most two). Then its
constant is1 or2 and it sees at most two nonsingleton exceptions, so precisely
the accepted old local guards give a contradiction. The stronger accepted
global residual-four full-support theorem is a useful comparison but is NOT a
logical premise of this new11-coordinate bound. All new transfer uses select
baseline constants1 or2. For a single cost6 coefficient, the possibilities are:

1. Singleton-1 or4: choose v in F0 different from its one coordinate. The
   derivative is completely baseline with c in{1,2}, old contradiction.
2. Cubic-3 or2: its support has only three coordinates; choose v in F0 outside
   it. Again all incident coefficients are baseline and c in{1,2}.
3. Positive quintic3: if some v in F0 avoids its support, use baseline. Otherwise
   choose any v in F0; its derivative has exactly the single tripled quartic
   excluded by the new lemma.

It remains to consider exactly three cost2 departures.
If any is a singleton, there are at most two nonsingleton departures. Choose
v in F0 distinct from every exceptional singleton coordinate (there are at
most three). Its c is1 or2, and it sees at most two nonsingleton exceptions.
Every such case is covered by the exact old0/1/2-exception guards above.

Otherwise all three are nonsingleton. All singleton constants are baseline.
For every v in F0, if it avoids even one exception support it sees at most
two, again impossible. Therefore ALL THREE support sets contain F0. A cubic
support of size3 cannot contain the four distinct F0 coordinates. Hence all
three departures are doubled positive quintics S1,S2,S3. They are distinct,
so necessarily Si=F0+{t_i}, with three distinct tips outside F0.

Choose v in F0. Its three doubled quartics are
Di=(F0 minus{v})+{t_i}. In this13-variable derivative each tip t_i lies in
exactly one doubled quartic, and all incident quadratic numerators are
baseline. The extracted private-vertex obstruction applies at t_i. Other
Di avoid it and cannot affect any pair/triangle/unit equation used there.
Contradiction. This exhausts the exact residual-six allocations.

Proposed conclusion: |F|<=3, equivalently the negative quintics cover at least
11 coordinates, when residual defect<=6. It does NOT strengthen to full14
coverage or assert an independent two-cost charge per free coordinate.
Three cubic supports on four vertices can each give all vertices at least
two incident exceptions; their shared cost is6, not8. The proof instead
uses the already complete two-exception exclusion at baseline constants to
force membership in every one of the three support sets.

## Conditional application and status

A connected Johnson-four family of six quintics has union size<=10 by adding
at most one coordinate along each spanning-tree edge. The current magnitude
(3,1,1,1,1,1) has residual6 and six supports, so its connected branch would
contradict the proposed union>=11 theorem. Its other branches have separate
accepted proofs. This consequence is NOT promoted here: new lemma, private-
vertex extraction, complete allocation/guard cover and inherited branch
composition require parent/independent acceptance. All30 original whole
patterns remain OPEN in the unchanged canonical ledger.

## Bound source and control record

The exact61 abstract allocations are1/5/15/40 at costs0/2/4/6. The executable
source separately lists584 actual local incident/hidden templates and explicitly
marks unsupported c0/3 two-quadratic cases, heavy cubic cases, and three-exception
local geometries. The coupled proof does not assume those unsupported local
theorems: it chooses a different baseline-constant coordinate or uses the two
new structural arguments. Abstract repeated types always mean distinct physical
coefficients, and repeated positive cofaces are rejected in the private-tip
control. The signed level/value/cost types are generated from the actual three
quadratic defect polynomials. No negative quintic is permitted as a residual
exception.

Small controls inspect weighted links with one weight3 edge, all residual paths,
the forbidden outside triangle, all203 partitions of six possible path-middle
labels, the private-tip maps, the two private-sphere degree cases and the shared
three-cubic incidence counterexample. An ordinary-coefficient-two weighted-link
control shows that the weighted-link path step cannot be transferred without
the Boolean ordinary-quadratic guard; it is not a counterexample to the entire
lemma with that hypothesis dropped. These are structural controls, NOT a
ternary-polynomial feasibility search. No new solver
run, historical catalog regeneration, ledger update or publication is performed.
The source audit rehashes direct accepted authority entries and records their
statuses; it does not independently replay all predecessor certificates.

The exact source paths, pins, controls, timings and coverage are bound in the
new1382 manifest. This remains proposed until separate1386 and parent review;
no human peer review, proof-assistant formalization, mathematical novelty or
solution of the original14-variable goal is claimed.
