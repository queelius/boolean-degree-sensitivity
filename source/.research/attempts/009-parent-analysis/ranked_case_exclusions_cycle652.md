# Verified geometry-34 exclusions from the case-596 inequality

GLOBAL STATUS: OPEN. These are 10 complete conditional first-case
exclusions, not a resolution of the full 14-variable question.

All cases belong to the accepted self-dual empty-pair branch, geometry 34,
and the complete cycle-278 marked-pair quotient. Row numbers are original
representative IDs. The geometric and Fourier conventions and necessary-model
soundness are the same as in `first116_exclusion_cycle639.md` and
`whole_first_case_spectrum_soundness_cycle585.md`.

Cycle 642 ranked all 292 representatives and found six positive unpropagated
bounds among the 94 then-open cases. Cycle 643 propagated those six and the
four next highest bounds. Cycle 644 independently replayed every deletion;
it did not verify the producer's fixed-point labels. All ten recomputed
bounds in cycle 645 were positive. Recorded initial bounds agree exactly
between the new precomputation and the existing direct per-case evaluator.

Each case then received its own complete input audit, full target matrix,
model-only audit, transferred integer certificate and independent literal
certificate check. No new numerical optimization was used. The independent
readers rebuild every target equation and gcd, compare the full primitive
matrix and cancel all variables exactly using signed-row and box inequalities.
Each model consequently implies 0 <= the negative integer shown below.

| First row | Variables | Equalities | Exact contradiction RHS |
| --- | ---: | ---: | ---: |
| 221 | 65470 | 7487 | -2611936416576 |
| 581 | 61726 | 7326 | -2074094571968 |
| 178 | 65078 | 7439 | -1517971125184 |
| 386 | 66656 | 7417 | -830761159296 |
| 597 | 66053 | 7515 | -945552411648 |
| 599 | 65247 | 7506 | -1174144938240 |
| 601 | 66344 | 7512 | -895648535744 |
| 191 | 65588 | 7492 | -485603439296 |
| 626 | 64151 | 7457 | -894422217152 |
| 656 | 64082 | 7457 | -1059797406400 |

The cycle-652 frontier compositions check scope and the complete quotient
before accepting each exclusion. Geometry 34 now has 208
of 292 cases excluded and 84 open. The full
geometry remains open. The detailed status snapshot records the equation
and box contributions, certificate sizes, parameters and source hashes.

The original transfer proposal's PENDING audit label is preserved as history.
The cycle-651 independent certificate manifests are the proof authorities.
The aggregation lemma is not used as an independent computational authority.

## Reproduce independent checks

The batch plan stores the exact argument lists for every stage. The following
replays input and certificate verification with fresh output paths:

```bash
cd /home/spinoza/github/math-theory/.research/attempts/009-parent-analysis
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ../../venv-exact/bin/python - <<'PY'
from pathlib import Path
import json, subprocess, tempfile
plan = json.loads(Path('ranked-certificate-batch-plan-cycle646.json').read_text())
out = Path(tempfile.mkdtemp(prefix='independent-ranked-cases-'))
for case in plan['plans']:
    for stage in case['steps']:
        if stage['cycle'] not in (647, 651):
            continue
        argv = list(stage['argv'])
        argv[argv.index('--output')+1] = str(out / ('first-%s-stage-%s.json' % (case['first_row'], stage['cycle'])))
        subprocess.run(argv, check=True)
print(out)
PY
```

The input readers reference the independently checked cycle-644 domain
authority. To replay those deletions too, run `verify_matched_whole_family.py`
on `matched-g34-ranked-family-propagation-cycle643.json` with a fresh output
path. Earlier branch reductions and quotient coverage remain dependencies.
No novelty claim is made for these partial exclusions.
