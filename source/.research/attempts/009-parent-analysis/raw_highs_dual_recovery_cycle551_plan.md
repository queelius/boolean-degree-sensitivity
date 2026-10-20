# Recover dual candidates without equating solver status with proof

GLOBAL STATUS: OPEN. This is the next planned experiment, not an accepted
certificate or case exclusion.

Cycle 541 restarts the same full-spectrum model with a 600-second limit.
It ends after 80 IPM iterations, before the limit, with an imprecise
interior solution and no crossover. HiGHS reports model status Unknown;
SciPy reports status 4 and returns no vector. The printed phase objective
is approximately 0.0677076331. The numerical trace is not a certificate.
The frozen producer and independent model audit must retain that result.

Inspection of the installed SciPy 1.15.3 wrapper confirms that its LP path
returns early for every model status except Optimal, before retrieving
row duals. The bundled `_highspy._core._Highs` object exposes passModel,
setOptionValue, run, getInfo, getModelStatus, and getSolution. Its HiGHS
version is 1.8.0. Use the installed API; no package upgrade is needed.

The next kernel should preserve the same exact phase-I matrix and bounds,
but call that pinned underlying API and save its model/run status,
solution validity flags, iterations, objective diagnostics, and any
finite row-dual candidate of the correct length. A nonoptimal solution
must not be labeled feasible or optimal. The wrapper describes such
results as unsafe to use as solutions: here they are only candidate
weights for independent exact reconstruction.

For each candidate dual, round its nonnegative inequality multipliers to
integers at a recorded scale, sum the original integer rows, and cancel
the residual columns using exact box inequalities. This procedure can
start with arbitrary candidate weights; the proof is solely the final
integer cancellation and negative right-hand side. Save unsuccessful
reconstruction attempts too. An invalid, absent, nonfinite, wrongly sized,
or noncontradictory vector remains inconclusive. Never accept the printed
objective or a solver infeasibility flag as proof.

First test positive and negative small integer LPs, deliberately perturbed
dual weights, absent and invalid candidates, and a deterministic iteration
limit. Verify matrix construction against the frozen kernel and the
independent scalar rows. Retain the exact parameters and installed module
identity. Then run one bounded full-model pilot, at most 600 solver seconds
and 4096 MiB, recording every returned candidate before later analysis.
Avoid additional identical runs with linprog, which discard the needed
state by design.

If an exact contradiction is recovered, run
`verify_primitive_full_spectrum_lp.py` against a compatible frozen result
envelope, or add a separately tested reader for the new envelope. Compose
the remaining product group with the prior complete 497-group cover using
`compose_spectrum_partition_closure.py`; its tests already reject UNKNOWN
and mismatched scopes. Only then update first row 58's status. If no
certificate can be reconstructed, inspect the exact residual/box loss
before deciding whether a new method or another case is more informative.

After a certificate exists, `dual_partition_extension_cycle551_plan.md`
describes how to test whether its exact linear functional extends to
larger complete domains. That transfer is contingent, and it may fail.
