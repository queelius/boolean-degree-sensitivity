# Ordinary derivatives with two disjoint cubic exceptions

Status: independently accepted local exclusion. All 94 marked ordinary cases
are excluded for both allowed constants. The complete fourteen-variable
Boolean decision remains open.

The hypotheses are exactly those in `disjoint-cubic-local-reduction.md`:
a thirteen-variable ternary derivative p, p(0)=1, every unit value zero,
ordinary quadratic monomial coefficients in {0,1}, Fourier constant numerator
c in {1,2}, quartic numerators in {0,1}, and two disjoint exceptional pair
numerators. At least one is -2; the other is -2 or +1. These are local
derivative hypotheses, not an assertion of a fourteen-variable Boolean
extension or a restriction to symmetric functions.

The independent structural audit proves that every vertex link is a sphere.
A negative endpoint has a flag link with one vertex of degree six and all
others of degree four or five. The independently complete sphere catalogs
leave exactly the three root types (9,22), (10,185), and (11,762). Every one
of the 55 placements of the second exceptional pair is explicitly mapped
to a representative. There are 47 marked types and two signs, giving 94
necessary cases. The authoritative key is `(root_index, second_pair,
second_value)`; a discovery-order label is not an index into a sorted list.

`disjoint-cubic-ordinary-compact-proofs.json` excludes all 47 negative-pair
cases and 19 mixed cases. Its independent checker reconstructs all 4,731
selected rows and replays 4,721 exact Boolean deductions. Each row is
unchanged when c=1 is replaced by c=2; no global face-count row occurs.

For a mixed case, the positive endpoints have spherical links with one
degree-three vertex and all other degrees four or five. Filtering the same
complete catalogs gives only the seven-vertex sphere of index 2. Therefore
both positive endpoints have exactly seven neighbors. These two additional
necessary rows are the only strengthened geometric assumptions in
`disjoint_mixed_degree_seven.py`.

The final models remove every global face-count row. Each exact proof in
`disjoint-mixed-constant-independent-branch-proofs.json` consists of a
binary tree of explicit Boolean case splits. At a leaf, the saved rows
are literal necessary model rows or unit rows recording precisely that
root-to-leaf path. Every forced value is justified because its alternative
violates an integer interval bound; the final interval is disjoint from
the required range. Both branches are present at every internal node.
The original model and all leaf rows are thus independent of c, so a
complete tree covers both allowed constants.

The initial bounded interval pass, its integer-gap assertion, and an
exploratory SAT refutation are retained separately. None is needed to
trust a final leaf: the independent verifier reconstructs its rows and
checks every inference and complete branch cover. The old assertion was
an omitted case where both Boolean values violate a row, such as 2x=1.
The new generator records one valid forced value and then the resulting
literal contradiction. It does not weaken the checker or infer a result
from an exception, timeout, or unverified solver status.

The independent checker `independent-math-audit/verify_disjoint_mixed_branches.py`
verifies all 28 remaining mixed keys: 110 tree nodes, 69 leaves, 4,648
literal rows and 4,800 deductions. It re-filters the sphere catalogs,
reconstructs all model digests and selected rows, and checks every explicit
branch path. The keys are exactly the complement of the previously accepted
19 mixed cases. Thus the two artifacts jointly exclude all 94 ordinary
local cases. Special ordinary
coefficient-two cases use separate accepted patch proofs. The full
fourteen-variable Boolean decision still requires the separate remaining
negative-support families.
