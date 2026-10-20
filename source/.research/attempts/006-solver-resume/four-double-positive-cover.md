# Positive-double placements in the remaining four-double geometries

This is a complete necessary cover of positive doubled quintic placements
in the sixteen pairwise-intersecting support classes. It does not exclude
any entire support class. Its local theorem and literal coverage require
the independent acceptance recorded in a later wrapper; the saved producer
report deliberately retains its pending status.

Four negative quintic numerators of value -2 cost 24 of the empty-profile
defect budget 28. Every nonbaseline singleton, cubic or nonnegative quintic
costs at least two. With only four units left, exactly two cost-two
exceptions occur. Their possible values are singleton 0 or 3, cubic -2 or
1, and positive quintic 2. The accepted common-vertex lemma forces each
vertex in all four negative supports to have singleton numerator zero.
Those costs are charged first.

For a proposed positive double P, let U(P) be the union of all pairs of P
not contained in any negative support. The ordinary-pair single-positive-
double theorem says that every such pair must also lie in a different
positive double or in an exceptional cubic. Otherwise it sees exactly one
positive double, no negative quintic and only baseline cubics, which is
impossible. A singleton exception does not alter this local argument.

This leaves three exhaustive possibilities whenever a positive double is
present:

* One positive double with the other defect at a singleton: U(P) is empty.
* One positive double and one exceptional cubic J: U(P) is contained in J.
  Both cubic values -2 and 1 are retained.
* Two positive doubles P,R: U(P) is contained in R and U(R) is contained in P.

Each statement about the union is equivalent to the original individual
pair requirements. In the last case U(P)=P would force R=P, so the
implementation safely discards such P before enumerating distinct pairs.
All supports are literal subsets of the fourteen coordinates. No unknown
coefficient or truth value is assumed invariant under a symmetry.

The complete saved support cover gives nine common-vertex classes with
no possible positive double (eight have one common vertex, one has two).
Across the seven classes without a common vertex, it leaves one
single-double/singleton placement, 1,035 positive-double/cubic support
pairs, and 333 unordered pairs of positive doubles. The unique first case
is class40 with positive support 12568. The no-positive-double branch in
every one of the sixteen classes remains open.

The six tests compare the optimized union test against literal pair
quantifiers on a separate finite ground set, check residual-budget guards,
reject malformed supports and verify the complete source binding. A small
exact degree-ten propagation pilot tested one two-double placement in each
of the seven eligible classes. All seven reached a necessary fixed point;
none is a Boolean witness or an exclusion.
