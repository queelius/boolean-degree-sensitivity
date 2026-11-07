# 018 notes (working; nothing here is accepted)

Claude Code (Anthropic), 2026-10-23. Global status: OPEN.

The final L1 cover design and its status are in `L1.md` and `README.md`;
the cover section at the end of this file is the earlier proposal.

## Done

- (a) `make_frontier.py` -> `no-free-frontier.json`: the 22 open
  inventories with remaining defect <= 6, each with the reason union 14 is
  forced (r <= 4: residual-four support constraints; r = 6: 1401 plus the
  1531 and 1533 exclusions) and pins to the partial reductions. Independent
  `frontier_reader.py` rederives the 39 / 17 / 22 split from the cost table
  alone; `test_frontier.py` (6 tests, normal and -O, with negative controls).
- (b) CONTROLS.md, `controls_n13.py`.
- Exact derivative model with negative quartics: `pilot_neg.py`. Integer
  cubic coefficients. Positive controls: the five real n = 13 derivatives
  with one negative quartic are FEASIBLE with all coefficients fixed (N = 12);
  one perturbed pair numerator makes it INFEASIBLE.

## Clean one-negative-quartic case (step (c)), observations

Setting: u in exactly one negative quintic, so p = Delta_u f has one
quartic Q with l_Q = -m, all other incident coefficients baseline.

- Unrooted CP-SAT: UNKNOWN at 600 s for m = 1, 2 (as unrooted 017 was).
- Identities still hold with the negative weight: sum l = 36 + c (so
  36 + c + m unit quartics), E = 49 + c, P_x = 2d - 4 (weighted).
- A vertex x outside Q has only unit pair links (no quartic through an
  outer pair is Q), so they are empty, C4 or C5, and its unit link is a
  union of closed surfaces with chi = 2 and degrees 4, 5: a deltahedron or
  two six-vertex projective planes. Nine such vertices.
- Inside Q the pair links change: for A in Q, the unit link of A has the two
  vertices of Q - A of degree congruent to m mod 2 and the others even, with
  m + 4 m_A - k_A edges; the edge joining Q - A is Q itself, not unit. For
  m = 1 and m_A = 0 it is a path of length 2 between them.
- Not yet done: the cross-edge argument for a disconnected outer link needs
  lower bounds on the cross degrees of Q's vertices, which the CROSS-EDGES
  count does not give (their degree bound from P_x = 2d - 4 is weak).

## Probes (exploration, CP-SAT verdicts only)

- Rooted at an outer vertex with a deltahedron link (orders 8, 9), Q in
  two placements, flag rows assumed at the other outer vertices: all 8
  (order, placement, m in {1,2}) cases INFEASIBLE in 4 to 10 s.
- Plan to avoid the missing cross-edge lemma: split by whether some outer
  vertex has a disconnected link (root there, link two six-vertex RP2 on
  the other 12 vertices, no flag rows) or none does (deltahedron root, flag
  rows at all other outer vertices). Both are honest finite covers.
- Consequence if it extends to the incident departures allowed by the
  residual: inventories with N <= 5 supports always have a coordinate in
  exactly one negative quintic (5N incidences over 14 coordinates leave at
  least 14 - (5N - 14) such coordinates: 8 for (2^4), 3 for (2^4,1)), so
  the lemma would exclude (2^4) and (2^4,1) as whole patterns.

## What (2^4) and (2^4,1) need (counting, to be reviewed)

Departures cost 2 (singleton k in {0,3}, cubic k in {-2,+1}, quintic k = 2)
or at least 6. (2^4) has r = 4, so at most two cost-2 departures in the
whole function; it has at least 8 coordinates in exactly one negative
quintic (Sum (delta - 1) = 5N - 14 = 6). Two distinct departure supports
share at most 4 coordinates, so at least 4 of those coordinates meet at
most one departure. (2^4,1) has r = 2: at most one departure at all, and at
least 3 delta = 1 coordinates. A derivative at u sees only departures whose
support contains u. Hence both inventories reduce to: no derivative at a
delta = 1 coordinate with negative quartic magnitude m (m = 2 for (2^4);
m in {1, 2} for (2^4,1)) and at most one incident cost-2 departure. Types:
none; constant 0 or 3; pair -2 or +1 with |pair meet Q| in {0,1,2}; quartic
+2 with |D meet Q| in {0,1,2,3}: 13 types per m.

- Budget model (departures chosen by the solver, any kind, total <= 4):
  UNKNOWN at 900 s on three of four samples; too loose.

## Cover design for the one-departure lemma (proposed)

Kind-restricted free placement solves (165 to 260 s on 8 workers per case);
explicit placements solve in about 5 s each. Explicit Case B counts with an
ordinary root (`cases018.py`, per m): about 38,500, 80% of them +2 quartic
departures. Reductions:

1. +2 quartic departure D (D != Q, so D has a vertex x outside Q, in no
   other departure): excluded by the accepted private-vertex argument
   (`006/two-exception-positive-extension.md`, audit
   `006/independent-math-audit/connected-six-unit-exclusion-audit.md`): it
   uses only data at x (baseline pairs through x, x in exactly one doubled
   quartic, p(0)=1, p(e_x)=0, cubic integrality), and no quartic through x
   is Q. Needs a written check that nothing else at x is assumed.
2. Pair departure with an endpoint x outside Q: x's pair links are unit
   cycles except the departure pair (C6 or split for -2, C3 for +1), so the
   local 017 vertex-type lemma applies at x: its link is one of the 3 type
   (1,0) spheres (-2) or the order-7 type (0,1) sphere (+1). Root at x and
   place only Q: about 100 cases per sphere.
3. Remaining with an ordinary root: pairs inside Q, no departure, constant
   0 or 3.
4. Case A (some ordinary vertex has a disconnected link) for every type:
   count interrupted (memory reap), not yet known; the root link
   automorphism group has order 7200, so it should be small.

Estimated total about 6,000 cases for m in {1, 2}.
