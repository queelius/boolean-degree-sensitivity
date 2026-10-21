# Independent audit of the ordinary disjoint-cubic contradictions

**PASS: all 47 disjoint (-2,-2) cases and 19 of the 47 mixed cases
are excluded under the stated local hypotheses. The other 28 mixed
cases remain unresolved by this bundle. The global Boolean problem
remains open.**

The exact source-bound replay is
`disjoint-cubic-ordinary-compact-independent-verification.json`, produced
by `verify_disjoint_cubic_compact.py`. It imports only previously frozen
independent audit primitives, no producer model, propagation search,
numerical solver, or SAT code. Its report SHA256 is
`705db31832b8118ea364b185f8b52cac701202a7929ace3f046d19667ffcaea6`.

This audit consumes the already independently checked complete cover in
`disjoint-cubic-root-link-cover-audit.md`: three root spheres
((9,22),(10,185),(11,762)), all 165 literal second-pair placements,
and 14/13/20 marked types. The authoritative key is
`(root_index, second_pair, second_value)`. The discovery-order orbit
label is not used as an array index or as a certificate key.

The scope is a thirteen-coordinate derivative with range
({-1,0,1}), origin one, unit values zero, even degree-four Fourier
representation at scale 16, constant (c\in\{1,2\}), binary quartic
numerators, and all ordinary quadratic coefficients zero or one.
Exactly two disjoint Fourier pairs are exceptional, with values
(-2,-2) or (-2,+1); all others are (-1/0).
Special ordinary coefficient-two cases require their separate proofs.

## Independent row and proof reconstruction

I reconstructed the ordered full model for every exported case and
checked its complete row count and SHA256 against the original saved
probe. I then reconstructed each compact row independently from its
literal support and mathematical reason. Every original-row index,
root face set, selected pair, sign, and original trace association agrees.

The selected rows have the following meanings:

- Downward closure and triangle incidence express a genuine simplicial
  complex with each present triangle in two tetrahedra.
- Root equalities fix the complete star of the marked negative endpoint,
  including its absent faces.
- For a baseline edge, its tetrahedron count minus four times its
  presence indicator is in ([0,1]). Exceptional pairs are present and
  have valence six or three as appropriate.
- For any coordinate subset (X), the induced Euler equation follows
  from (p(X)=1-\chi(K[X])\in\{-1,0,1\}). Its row is
  (-|X|\le-E(X)+T(X)-Q(X)\le2-|X|).
- The accepted sphere filter permits flag rows at ordinary vertices and
  negative endpoints. **No flag condition is imposed at either positive
  endpoint.** Negative endpoint link order lies in ([9,11]), positive
  endpoint order in the conservative interval ([7,10]), and ordinary
  order in ([6,12]).

The 66 proofs use exactly 4,731 rows and 4,721 deductions. The selected
row counts are 2,633 root equalities, 641 baseline-edge valence rows,
478 ordinary flag rows, 286 induced Euler rows, 275 negative-endpoint
flag rows, 215 downward rows, 162 triangle-incidence rows, 20 exceptional
edge-presence rows, 20 vertex-order rows, and one exceptional-valence
row.

Each deduction is checked by assigning the opposite Boolean value and
computing the exact attainable interval of its row over all remaining
unfixed bits. The opposite interval misses the permitted interval.
The final recorded row has an empty attainable intersection. No
propagation search or trust in a solver status is involved.

The independently reconstructed (c=2) model differs only in its three
global face-count rows. **None is selected in any compact proof.** All
selected rows and exact deductions therefore apply at both (c=1) and
(c=2). A full independently constructed second model also checks that
three-row change. This is not a claim about other constants, because
the structural cover has its own stated hypotheses.

## Coverage and controls

All 94 authoritative keys occur exactly once in the original report.
The compact report contains exactly its 66 contradictory keys. All
47 (-2,-2) keys are covered: 14, 13, and 20 by root type. The 19
mixed exclusions split as 8, 6, and 5; all other mixed keys are listed
explicitly as unresolved in the independent report.

Eight negative controls reject a copied proof under a wrong case key,
an altered coefficient, a wrong original index, omission of (c=2),
a flipped deduction, a missing case, a duplicate case, and a flag row
falsely assigned to a positive endpoint. The previously independent
(C_4*C_4) positive control satisfies the geometric and range rows;
(C_3*C_6) satisfies the geometric control while correctly failing the
range restriction.

The finite root quotient relabels arbitrary original derivatives. It
does not impose invariance on them. The source catalogs, complete cover,
producer files, original report, compact proofs, and independent helper
implementations are all hash-bound in the saved report. No new global
family or Boolean-existence conclusion is asserted here.
