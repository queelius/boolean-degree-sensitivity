# Restore the already saved presolved candidate before another optimization

The cycle-552 raw run returns status Unknown with validity flags true, but
its original-coordinate residual is about 2863 and its reported final
phase column is zero. Exact box reconstruction correctly fails, with
positive integer right-hand side 59954587972475 at scale 10^12.

Presolve removed one column and five rows. The saved primal array has the
reported phase objective, 0.0677076330972816, in its last retained entry;
the five trailing row duals are zero. This supports the hypothesis that
HiGHS left a compacted presolved solution in the original-sized buffers
after the imprecise IPM status, without reversing presolve. It is a
hypothesis about the numerical interface, not a mathematical result.

Rebuild the identical original phase-I matrix and rerun deterministic
presolve only. Use the documented installed postsolve overload accepting
a HighsSolution. Check dimensions, zero padding, finite entries and the
presolved primal residual before providing the compacted arrays. Compute
the candidate reduced costs from the reduced matrix and row duals. Call
postsolve, save all resulting numerical vectors and validity flags, and
check their original-coordinate residuals. Do not change the original
cycle-552 artifacts or reclassify its failed reconstruction.

The restored dual is only a candidate. The final acceptance remains exact
integer row combination, exact box cancellation and a negative right-hand
side, followed by the independent scalar-row verifier. The restoration
need not be trusted to establish the mathematics. If it fails, retain the
failure and use a bounded run with presolve disabled; do not repeatedly
reuse an unmapped buffer. Positive and negative small LP controls must
first survive an explicit presolve/solve/postsolve round trip, and invalid
padding must be rejected.
