# Fixed negative cubic interval certificates

Fix all four safe derivatives in an accepted actual four-cycle case, and choose
one missing core diagonal. Its Fourier numerator B on ten outside variables
has linear coefficients in{0,-1} and cubic coefficients in{0,1,-2}. The two
positive double quintics have four core variables and contribute no coefficient
to this block. If B has exactly one negative cubic at T, then

    B(z)=-sum_i u_i z_i+sum_{q != T} p_q z_q-2 z_T,

with Boolean flags u_i,p_q. Every outside point has an independently enumerable
set of allowed B values from its Boolean four-core restriction. Replacing those
values by their enclosing interval and all flags by[0,1] gives a necessary
linear relaxation, with129 variables and1024 interval rows. Therefore an
integer Farkas contradiction of this relaxation excludes that fixed position.

The reader reconstructs the allowed sets by scalar enumeration of all65536
Boolean four-cubes, evaluates every fixed derivative directly, and then checks
the certificate's used row bounds. It verifies that a nonnegative combination
of signed interval and box inequalities cancels all129 coefficients and leaves
a strictly negative right side. No numerical solver is imported by the reader.
Completeness for N=1 requires all120 distinct outside triples. A complete N=1
exclusion is only a necessary lower bound for this diagonal; cases with two or
three negatives and other fixed derivative choices remain separate.
