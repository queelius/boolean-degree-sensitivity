# One-free Type II: shapes, a free reduction, and what remains

Alexander Richard Towell, with Claude Code (Anthropic) assistance. Source
audit and exact shape enumeration only; no solver run, no exclusion of a
whole pattern.

## The case

Type II (1513/1523): c in {1,2} and three distinct nonsingleton cost-two
departures, all containing the free coordinate u. In p = Delta_u f these
are three distinct departures among: a pair numerator -2, a pair numerator
+1 (on distinct pairs), and a doubled quartic l_D = 2. Everything else is
baseline, p(0)=1, p(e_v)=0, and ordinary quadratic coefficients are 0/1.

## Shapes and the private-vertex reduction

`type2_shapes.py` enumerates the departure shapes up to relabelling
(pynauty canonical forms of the coloured incidence graph; the 24 pair-only
classes are confirmed by an independent brute force over all relabellings
in `test_type2_shapes.py`). There are 136 classes.

A doubled quartic D with a vertex x that lies in no other departure is
excluded at any constant: the argument of
`006-solver-resume/two-exception-positive-extension.md` (accepted in
`006-solver-resume/independent-math-audit/connected-six-unit-exclusion-audit.md`,
reviewed again in REVIEW-closure.md) uses only data incident to x, namely
baseline pairs through x, x in exactly one doubled quartic, p(0)=1,
p(e_x)=0 and cubic integrality. It gives a unit link at x with Euler
characteristic 3, which the surface lemma rules out. This removes 105 of
the 136 classes.

| Departures | classes | private-vertex excluded | open |
|---|---|---|---|
| three -2 pairs | 5 | 0 | 5 |
| two -2, one +1 | 7 | 0 | 7 |
| one -2, two +1 | 7 | 0 | 7 |
| three +1 pairs | 5 | 0 | 5 |
| with doubled quartics | 112 | 105 | 7 |

The seven covered doubled-quartic shapes (every vertex of every doubled
quartic lies in another departure):

1. -2 on {0,1}, -2 on {2,3}, Q2 on {0,1,2,3}
2. -2 on {0,1}, +1 on {2,3}, Q2 on {0,1,2,3}
3. +1 on {0,1}, +1 on {2,3}, Q2 on {0,1,2,3}
4. -2 on {0,1}, Q2 on {0,2,3,4}, Q2 on {1,2,3,4}
5. +1 on {0,1}, Q2 on {0,2,3,4}, Q2 on {1,2,3,4}
6. Q2 on {0,1,2,3}, {0,1,2,4}, {0,1,3,4}
7. Q2 on {0,1,2,3}, {0,1,4,5}, {2,3,4,5}

A first look at shape 4 or 5 at a vertex x of the shared triple: the two
pairs from x to the rest of the triple see two doubled edges, so they carry
no unit faces. The unit link at x then has Euler characteristic 2, with the
two private vertices of degree 3 and all others of degree 4 or 5. That is
not immediately contradictory (such spheres exist), so these shapes need
more than the one-vertex count.

## What the open shapes need

The 24 pair-only shapes are three-exception analogues of the accepted
two-exception theorems (adjacent and disjoint -2/-2, -2/+1, +1/+1). Those
were proved by: a structural step making every vertex link a sphere; a
root at a -2 endpoint whose link is one of the catalog spheres (9,22),
(10,185), (11,762) (or the unique (7,2) sphere at a +1 endpoint); an
exhaustive placement of the other exceptions around the root; and compact
finite certificates over constant-free rows (downward closure, two
tetrahedra per triangle, edge valences, flag and induced-Euler rows).

The same plan applies to three exceptions, with c in {1,2} only, so the
cross-edge bound M <= E - 42 = 7 + c <= 9 used by the two-exception
proofs is available unchanged. The new work would be: (i) the structural
step for three exceptions (a disconnected ordinary link now has up to six
bad vertices, so the counting must be redone); (ii) a root-link and
placement cover for each of the 24 shapes; (iii) a model producer and an
independent row reader for the new rows; and (iv) certificates. The 014
pipeline (CP-SAT core, decision-diagram CNF, CaDiCaL LRAT, pinned
lrat-trim, independent clause-soundness reader) can produce and check (iv)
once (iii) exists; its row reader is tied to the 009 signed-star row
sources and would need a successor for the new row families.

The seven covered doubled-quartic shapes are few and rigid enough that a
written local argument may settle them before any model is built.

Global status: OPEN. No whole magnitude pattern changes.
