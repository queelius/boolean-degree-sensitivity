# Accepted residual-four negative-support covering theorem

The proposed transfer in attempt006 is sound. It is a necessary theorem
for a self-dual empty-pair representative; it does not prove nonexistence
for any complete magnitude pattern and does not claim every original
function is self-dual. The accepted existence-preserving reduction is the
reason this representative may be considered.

After subtracting every negative quintic's defect, the remaining defect
costs are (k-1)(k-2), k(k+1), and k(k-1) on levels one, three, and five.
For integer k, every nonzero cost is at least two; at cost at most four
the only departures are singleton 0 or 3, cubic -2 or 1, and nonnegative
quintic 2. Each costs exactly two. There are at most two departures.

If a vertex v avoids all negative quintics, p=Delta_v f is a ternary
thirteen-variable polynomial with p(0)=1 and p(e_i)=0. Its ordinary
quadratic coefficient at ij equals f(vij), because every pair truth is
one. Thus every such coefficient is zero or one. Its Fourier expansion
is even and its quartic Fourier numerators are nonnegative. Exceptions
not containing v disappear under differentiation; only its own singleton
numerator survives as the constant.

With zero or one incident nonsingleton exception, the accepted local
baseline and one-exception derivative theorems apply for constant at most
three. This statement was checked in the actual predecessor proofs; it
is not an application of their narrower global residual-two corollary.
If two nonsingleton exceptions occur, they consume the entire residual
budget, so the constant is one or two. If either is a doubled positive
quartic, the accepted ordinary private-vertex/Euler argument excludes it.
Otherwise they are two distinct quadratic pairs. Their supports are
adjacent or disjoint and their signs are ++, --, or mixed. The accepted
two-positive, adjacent-negative, adjacent-mixed, and disjoint-with-negative
theorems cover precisely this list. Their ordinary-coefficient hypotheses
hold; no special-edge transfer is needed. This exhausts every local case
and contradicts the existence of v. The negative supports therefore cover
all fourteen coordinates whenever residual defect is at most four.

The predecessor local proofs retain their explicitly recorded dependence
on published complete small-valence manifold and small-sphere catalogs.
Their historical enumerations were not regenerated here. The new transfer
does not introduce an additional external computational claim.

The accepted top-Fourier sign argument gives connectedness of the ordinary
intersection graph of negative supports. For m supports in c components
under intersection-four adjacency, the union has size at most m+3c+1.
Combining with the new cover gives c >= max(1,ceil((13-m)/3)). In particular
four magnitude-two supports require at least three such components. The
formula for component union size was independently audited previously and
does not require a residual-two hypothesis; only its old application did.

The independent scope checker imports no producer module. It generates
all 21 abstract exception allocations and 120 incident cases separately,
checks the exact case multiset and every component bound against the
frozen ledger, and verifies 76 immediate source hashes. It finds 19
currently open covered patterns, six newly covered at residual four.
Omitted-case and altered-component controls both fail as intended.
No whole pattern is marked excluded.

Reproduce with `python -m pytest -q test_audit_empty_residual_four.py`.
The full check is `audit_empty_residual_four.audit()`; the executable entry
point refuses to overwrite an existing report.
