# Direct rejection of L=7 and L=8 singleton branches

For a missing diagonal write B as P positive unit cubic coefficients, Q
negative unit linear coefficients, and N negative doubled cubic coefficients.
The condition B(0)=4 gives P=Q+4+2N. Summing B over the ten singleton inputs,
each cubic character contributes four and each linear character contributes
eight. Therefore

    sum_i B(e_i) = 4P - 8Q - 8N = 16 - 4Q.

If L ordinary singleton values are +4 and the other 8-L are -4, while b of
the two apex singleton values equal 8 and the rest are zero, the same sum is
8L-32+8b. It follows that Q=12-2L-2b, so Q<=12-2L. For L>=7 this is negative,
contradicting the nonnegative number Q of linear coefficients. The L=6 upper
bound is zero and is not an exclusion by this argument.

The supported-catalog producer records this scalar count contradiction for
each L=7 or L=8 branch, in place of a degree-catalog reference. The independent
reader recomputes the minimum singleton sum and the resulting upper bound,
checks that it is negative, and requires an empty candidate list for that
branch. All other branches must have complete degree-catalog authorities.
Missing L=0 or L=1 catalogs are not silently skipped. The small positive and
negative controls verify the boundary using the character-sum identity.
