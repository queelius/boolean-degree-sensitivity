# Exact exclusion of geometry 34, first row 116

GLOBAL STATUS: OPEN. The result below excludes one complete conditional
case; it does not settle the 14-variable existence question.

The scope is the accepted self-dual empty-pair branch, signed geometry 34,
with marked pair {0,12}. Its four negative quintic supports are
[7216,9731,10764,12736], with Fourier numerator -2, and its positive double
supports are [7681,14849], with numerator +2, in h=1-2f at denominator 16.
Masks use zero-based coordinate bits. The core is [0,9,11,12].
First row 116 is an original representative ID in the complete cycle-278
quotient. The earlier reductions and quotient remain referenced dependencies.

The cycle-577 independent propagation authority supplies complete retained
component domains of sizes [8040,3896,1572,1,3704,10056]. The independent
cycle-633 input reader checks the complete four-core truth-table cover,
component values and parity, and projected coefficient domains. It verifies
36188 local words, 27269 complete component patterns and 1406 projected
coefficients, of which 1405 require free flags. No case-58 zero-product or
binary filter is imposed.

Every Boolean function in this case induces a feasible point of the
necessary box-bounded linear system. The system has 64862 variables,
7435 integer equalities and 4608788 nonzero entries. Its rows enforce
word and pattern normalization, categorical consistency, full spectral
value identities, five Parseval identities and the singleton total.
The soundness argument is in
`whole_first_case_spectrum_soundness_cycle585.md`.
Each equation is divided by its exact positive gcd before storage.

Cycle 631 transfers the independently verified case-596 functional and
finds a positive gap 1574103161088 on the propagated complete case-116
domains. This score alone is only a proposal. Cycle 637 converts it into
an ordinary certificate in the actual target matrix. No new numerical
optimization is used.

The translation matches equations by their structural identities. If a
categorical equality D_v is the omitted category in the target partition,
the target basis represents it by

    D_v = word_normalization - pattern_normalization - sum(D_u, u != v).

A category absent on both sides of the complete target partition has
identically zero coefficients. Target word, pattern and flag coefficients
are checked against the extended source functional. Subtracting each
simplex group's minimum coefficient times its normalization equation then
produces an exact contradiction after cancellation with box inequalities.
The general normalization argument is in
`simplex_reconstruction_soundness_cycle617.md`.

Crucially, the final proof does not require trusting these translation
steps. The independent cycle-638 reader reconstructs all target equations
and their gcds, compares the entire saved matrix, and checks the resulting
integer certificate directly. It imports neither the numerical solver
nor the producer row generators. It verifies 7404 signed-row terms and
64344 box terms, which cancel every variable and leave

    0 <= -1874336434240 + 300233273152 = -1574103161088.

This is impossible. Consequently this complete first case contains no
Boolean function. Cycle 639 checks the scope against the complete quotient
and previous frontier before accepting the exclusion: geometry 34 now has
198 of 292 first cases excluded and 94 remaining. No entire new geometry
has been excluded.

## Replay

Use fresh output paths; the saved inputs and certificates are immutable.

```bash
cd /home/spinoza/github/math-theory/.research/attempts/009-parent-analysis
RESEARCH_PY=/home/spinoza/github/math-theory/.research/venv-exact/bin/python
CHECK_DIR=$(mktemp -d)
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "$RESEARCH_PY" \
  verify_first_case_full_spectrum_inputs.py \
  --source matched-g34-first116-full-spectrum-inputs-cycle632.json \
  --output "$CHECK_DIR/inputs.json"
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "$RESEARCH_PY" \
  verify_first_case_spectrum_lp.py \
  --model matched-g34-first116-spectrum-model-cycle634.json \
  --run matched-g34-first116-transferred-spectrum-certificate-cycle637.json \
  --output "$CHECK_DIR/certificate.json" --memory-mib 4096
```

The necessary input audit references, rather than replays, the independent
domain-deletion proof at cycle 577. The final certificate is in
`matched-g34-first116-transferred-spectrum-certificate-cycle637.json.gz`;
the full target matrix is
`matched-g34-first116-spectrum-model-cycle634.matrix.json.gz`.
The production commands and resource statistics are in the completed
cycle-631 through cycle-639 logs.

The row-transfer helper has 100% statement coverage across 18 focused
tests, including feasible and infeasible integration controls. A subsequent
99-test regression suite and all 13 repository tests pass. These counts
overlap and do not represent full-pipeline coverage.

No novelty claim is made for this partial result. The bounded primary
literature check at cycle 604 records the broader Epoch challenge as open;
it does not establish priority for this case exclusion or resolve the
status of the full finite question.
