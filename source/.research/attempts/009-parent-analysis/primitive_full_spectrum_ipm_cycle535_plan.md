# Equivalent integer row normalization and IPM without crossover

GLOBAL STATUS: OPEN. The full outside model in cycle 530 reaches its
60-second numerical limit and supplies no vector or certificate. Its
coefficient range reaches 1,536 and its largest absolute right-hand side
is 66,560. The five exact norm equations contain large common factors.

Divide each integer row, including both bounds, by the positive gcd of
all its coefficients and bounds. Use divisor one for an all-zero row.
This preserves every feasible assignment exactly, including fractional
assignments. A certificate for the resulting integer rows is a valid
contradiction once an independent reader reconstructs each original row
and the gcd. It changes no word pool, pattern, coefficient domain, or
moment identity. Phase-I objective values before and after this scaling
are in different units and should not be compared directly.

Also turn off HiGHS crossover. The goal here is a useful primal vector or
an exact integer contradiction; a basic vertex solution is not required.
The installed SciPy 1.15.3 source `_highs_wrapper.py` deliberately returns
no LP solution unless HiGHS reports optimal status, explaining why prior
timeouts have no vector even after an internally optimal interior solve.
The installed HiGHS option is the string `run_crossover`, default `on`;
the explicit value `off` is accepted. A real IPM API probe with presolve
disabled reaches status zero, returns its vector and row duals, and has
zero crossover iterations. The probe and its forwarding warning are
retained in `cycle534-no-crossover-api-probe.log`.

The solver variant preserves every API warning in structured output and
uses the same integer reconstruction and verification requirements as
the frozen kernel. Nonoptimal statuses remain inconclusive. Test a true
interior solution on an optimal face, an exact contradiction, a forced
iteration limit, and rational assignments before the real run. Use the
same 60-second and 4-GiB initial budgets. Do not infer Booleanity from a
fractional solution; any integral core-word candidate still needs direct
verification on the full 16,384-point cube.

Primary option documentation, checked 2026-10-18:
https://ergo-code.github.io/HiGHS/dev/options/definitions/#run_crossover
The installed option type and behavior were checked locally, rather than
assuming the current documentation alone describes this bundled version.
