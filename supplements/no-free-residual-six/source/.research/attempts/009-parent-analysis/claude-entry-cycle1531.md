# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status: research paused, problem OPEN

Research was paused at the user's request on 2026-10-21. **Do not start a
search, solver run or experiment just because this directory was opened.**
When the user asks to resume, read `.research/CLAUDE_HANDOFF.md` first. It
holds the frontier, the latest accepted results, the corrections and the
recommended continuation, and it is the source of truth over this file.

## Two projects share this tree

1. **Active: Boolean degree vs. sensitivity** (`.research/`, ~120 GB, ~55k
   files). Question: does a Boolean multilinear f on 14 variables exist with
   real degree ≤ 5, f(0)=0 and f(e_i)=1 for all i? This is the d=5 case of
   Epoch AI's "sensitivity vs. degree" challenge (`.research/goal.md`): beat
   sensitivity d^(log 6/log 3) ≈ 13.8 at d=5, so full sensitivity 14 at the
   origin. The authoritative statement is `.research/active-objective.md`.
   Done means one of two things: (a) a construction checked independently
   on all 16,384 inputs, including exact degree, or (b) a nonexistence proof
   covering every case, with checkable certificates. Pruning, a necessary
   profile, a ternary derivative, a prefix, a local obstruction or a solver
   UNKNOWN is not completion.
2. **Dormant: no-three-in-line** (`src/math_theory/`, `tests/`, `docs/`,
   `experiments/`). This is the only conventional Python package here and
   the project `README.md` describes. n=71 is open; every bounded run was
   UNKNOWN (`docs/experiment-log.md`, `docs/sat-attack.md`).

## Commands

```sh
# Root suite (13 tests, no-three-in-line). Either environment works:
.research/venv-exact/bin/python -m pytest -q
uv run --extra test python -m pytest -q
.research/venv-exact/bin/python -m pytest -q tests/test_no_three_sat.py::<name>   # single test

# Research packet tests are unittest files living next to their producers.
# Run them from inside the attempt directory (siblings import by bare module
# name), in both normal and optimized mode so assert-based checks can't silently vanish:
cd .research/attempts/009-parent-analysis
../../venv-exact/bin/python    -m unittest test_extended_trace_reader_cycle1522
../../venv-exact/bin/python -O -m unittest test_extended_trace_reader_cycle1522
cd -
.research/venv-exact/bin/python .research/attempts/009-parent-analysis/test_link_profiles_cycle1516.py

# no-three-in-line CLI
uv run python -m math_theory.no_three_in_line verify-known
uv run --extra search python -m math_theory.no_three_in_line search --n 19 --seconds 30 --workers 8
scripts/build_sat_solvers.sh    # builds build/solvers/{cadical-3.0.1,kissat-4.0.4}
```

`.research/venv-exact` (Python 3.10) is the research interpreter. It has
numpy, scipy, python-sat, pynauty and coverage. The LRAT checker used for
accepted UNSAT proofs is `.research/attempts/006-solver-resume/lrat-trim/lrat-trim`.
Per-packet coverage receipts are kept as `.coverage-*` files at the root.

## How the research evidence is organized

- **Cycles.** Work advances in numbered cycles (latest checkpoint: 1530).
  Files are named `<topic>-<role>-cycleNNNN.{py,json,md,log}`. The roles are
  `plan`, `preflight`, `launch`, `actual`, `result`, `validation`,
  `coverage`, `manifest`, `authority`, `acceptance`, `handoff`, `terminal`
  and `independent-review`.
- **Producer → independent reader.** A producer script emits a candidate
  artifact. A separately written reader, with its own negative controls,
  re-derives or checks it. A result counts as accepted only through an
  `*-authority-*` / `*-acceptance-*` JSON that pins SHA-256s of inputs,
  sources and outputs. Write down exactly what a reader verifies (for
  example, "every deduction" is not the same as "fixed-point completeness").
- **Checkpoint chain.** `.research/current-checkpoint.json` →
  `H/cycle<N>-parent-manifest.json`. Each manifest pins the `previous`
  manifest, the typed frontier, the summary and the newly accepted
  authorities. To freeze a new checkpoint, run
  `H/save_research_checkpoint_v2.py --cycle --previous --previous-sha256 --authority --summary --artifacts --next-cycle`
  from inside `H`. **A hash match proves file identity, not mathematical
  correctness.**
- **Abbreviations** used in the handoff and manifests, relative to
  `.research/`: `H` = `attempts/009-parent-analysis` (the current work),
  `A` = `attempts/008-sparse-spectrum-proof`,
  `S` = `attempts/006-solver-resume` (SAT and LRAT infrastructure).
- **Case scopes are nested and must never be added together or turned into
  a percentage.** From outer to inner: global decision cases → negative
  Fourier magnitude patterns → signed-star contexts and root geometries →
  raw row relaxations. Each scope has its own canonical file, named in the
  handoff.

## Traps

- Several older files have stale counts but are kept because hashes bind
  them. Examples: `findings/negative-quintic-pattern-cases.json` (no suffix;
  the canonical one is `-cycle1388`), `checkpoint-manifest.json` (Oct 13
  snapshot), `scores.jsonl` (ends at cycle 91) and `goal.md` (the broader
  challenge). `state.md` and `synthesis.md` are mutable views of the latest
  checkpoint.
- Don't read `.research/` recursively or `log.md` in full (~200 KB). Follow
  pinned paths from the handoff and manifests.
- The selfdual reduction holds for *existence* only. Never assume an
  arbitrary Boolean f is selfdual.
- CNF variable indices, masks and proofs belong to one context (for
  example, the root-7 LRAT proofs 1476/1501). They do not transfer. A new
  context needs its own CNF, an exact variable map and a complete proof.
  UNSAT means an accepted LRAT that ends in a verified empty clause.
- Keep these categories separate in prose and in JSON: necessary
  condition, actual ternary derivative, Boolean function, solver UNKNOWN or
  resource limit, and proved exclusion. A ternary p still needs a compatible
  Boolean extension that passes all 16,384 inputs.
- Do not revive old processes, and do not rerun a finished experiment
  because a stale state file suggests it. Rerun only with new evidence or
  changed constraints.

## Rules for files and workspace

- **Frozen artifacts are immutable.** Record corrections and successor
  experiments in *new* cycle files. Never edit a hash-bound proof,
  certificate, result or manifest, even to fix a known error (see the
  1504/1506 → 1513 Fourier-norm correction for the pattern).
- This directory is **not a Git checkout**. Do not `git init` it, and do
  not migrate the evidence tree. The curated public source is
  `.research/publication/boolean-degree-sensitivity` (Git), upstream
  `github.com/queelius/boolean-degree-sensitivity`.
- New general mathematics research belongs in `../math-research`. Evidence
  here stays until a portable successor reproduces it and maps old paths to
  new ones.
- For publication (Zenodo DOIs, the `../research-records` catalog), follow
  `AGENTS.md` § "Research publication and durable records" and the
  catalog's `PUBLISHING.md`. Published v1.4 is DOI 10.5281/zenodo.23544931,
  and it covers only the earlier residual-six packet. Disclose substantial
  AI assistance: OpenAI Codex did most of the work to date, and Claude now
  contributes too.
