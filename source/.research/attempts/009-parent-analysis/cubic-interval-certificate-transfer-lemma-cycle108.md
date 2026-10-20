# Exact interval-certificate transfer

For a fixed negative triple set N, write the missing-diagonal polynomial
B(x) = -2 sum_{q in N} chi_q(x) + sum_j a_j chi_{q_j}(x) t_j,
where each t_j belongs to [0,1], and a_j is -1 for a linear support and +1
for a remaining cubic support. An exact certificate combines scalar interval
inequalities and coefficient box inequalities with nonnegative integers.
Its variable coefficients cancel exactly. A negative combined right side is
therefore a contradiction. The reader recalculates this cancellation.

Only the interval right sides depend on the fixed quartet. Thus the same
integer multipliers can be evaluated on another quartet, using its independently
enumerated scalar Boolean-core value sets. A newly negative right side proves
infeasibility there; a nonnegative side is inconclusive.

For an outside-coordinate permutation m, relabel supports by m. Then the
renamed polynomial at x equals the original polynomial at m^{-1}(x).
The renamed allowed set is consequently V(m^{-1}(x)). Relabeling a negative
pattern P to the certificate's pattern N and using these renamed intervals
gives the same valid inference. The target quartet need not be invariant under
m. No symmetry reduction of the target quartet is assumed.

The cycle108 transfer audit covers all420 actual-signature negative pairs
separately in each of the18 fixed quartets. Source cover maps only select a
certificate and a coordinate permutation. Every permutation and support map
is checked, every scalar value set is independently enumerated, and all new
right sides are calculated with Python integers. The original quartet is a
positive control: all420 transferred contradictions must reproduce their
original negative right sides. No whole Boolean function is asserted by a
feasible interval relaxation.
