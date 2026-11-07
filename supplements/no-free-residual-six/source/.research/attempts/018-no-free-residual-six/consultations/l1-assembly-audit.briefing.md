# Codex briefing (2026-10-23)

**Roles.** Claude Code (Opus 5.5) orchestrates this research. It plans the
work, runs the experiments, writes and maintains the evidence, and asks the
user before freezing or publishing. OpenAI Codex is consulted for
independent review, critique, counterexamples and new ideas. A different
model family gives an unanchored second view; Codex reviews found real bugs
in 017 and in L1. This was the user's choice on 2026-10-23.

If you are a Codex session consulted through `tools/consult_codex.py`:
- Work read-only.
- Answer the question asked, and say what you checked yourself and what
  you only read.
- Report disagreement plainly.
- Your answer is AI review, not acceptance. The orchestrator records what
  it used in a `REVIEW-*-codex.md` note.

If the user starts a Codex session directly, follow the user's
instructions; the rules below still apply.

This briefing supersedes `CLAUDE_HANDOFF.md` (2026-10-21, checkpoint 1530)
for current status. That file stays unchanged because checkpoints pin it.
The problem is **OPEN**.

## Objective and completion

Decide whether a Boolean multilinear f on 14 variables can have real
degree at most 5, f(0) = 0 and f(e_i) = 1 for all i
([active-objective.md](active-objective.md)). Done means either a
construction checked independently on all 16,384 inputs, including exact
degree, or a nonexistence proof covering every case with checkable
certificates. A pruning, necessary profile, ternary derivative, prefix,
local obstruction or solver UNKNOWN does not complete it.

## Where to start

1. [current-checkpoint.json](current-checkpoint.json) points to checkpoint
   **1533**; its summary is `attempts/009-parent-analysis/state-cycle1533.md`
   ([state.md](state.md) is a mutable copy).
2. [attempts/INDEX.md](attempts/INDEX.md): every attempt with status, entry
   documents and test environment. It is generated from
   `attempts/*/ATTEMPT.json` by `tools/attempts.py`.
3. `CLAUDE_HANDOFF.md`: the frontier, corrections and history up to 1530.
   The rules below and in the repository's `AGENTS.md`
   (`/home/spinoza/github/math-theory/AGENTS.md`) still apply.

Paths: `H` = `attempts/009-parent-analysis`, `S` = `attempts/006-solver-resume`.

Pinned notes keep the wording they had when they were drafted (for example,
017 `CERTIFICATES.md` still says "Proposed" and "Not frozen"). Current
acceptance status comes from the named acceptance JSON and the checkpoint,
not from a note's header.

## Normalization and glossary

Every spectral statement below concerns the accepted existence-preserving
**selfdual empty-pair representative**
(`H/one-free-residual-six-and-extension-audit-cycle1513.md`, lines 7 to
9): f(0) = 0, f = 1 on all inputs of weight 1 and 2, h = 1 - 2f. Arbitrary
original functions are not assumed selfdual.

- k_S = 16 h_hat(S), an integer, supported on levels 1, 3 and 5.
- **Cost.** The baseline values are singletons k in {1,2}, cubics in
  {-1,0} and quintics in {0,1}. The costs are (k-1)(k-2) for a singleton,
  k(k+1) for a cubic and k(k-1) for a quintic, with a total budget of 28.
- **Magnitude and residual.** A negative quintic of magnitude m (k = -m)
  costs m(m+1). A pattern is the multiset of magnitudes, and the residual
  (remaining defect) is r = 28 minus their total cost. Every other
  departure costs 2 or at least 6.
- **Free coordinate.** A coordinate in no negative-quintic support.
  "No-free" means the supports cover all 14 coordinates (union 14).
- These are necessary spectral inventories, not Boolean witnesses.

## What Claude Code did (2026-10-21 to 2026-10-23)

| Checkpoint | Result | Authority (in H) | Evidence |
|---|---|---|---|
| 1531 | Two-free residual-six signed-star branch excluded: 26/26 contexts, 13/13 roots, 24 raw-row LRAT certificates | `signed-star-two-free-acceptance-cycle1531.json` | 014 `NOTES.md`, 015 `REVIEW.md` |
| 1532 | One-free residual six: Types I and III excluded, Type II reduced to 24 shapes | `one-free-residual6-acceptance-cycle1532.json` | 016 notes |
| 1533 | One-free residual six excluded: the 24 Type II shapes fall to 3184 LRAT certificates; root-7 o7-i0-c2 also on raw rows | `one-free-residual6-acceptance-cycle1533.json` | 017 `CERTIFICATES.md`, 014 `ROOT7-C2-RAW.md` |

All of it is conditional on two things:
- the inherited premises named in each summary;
- AI review of the written lemmas: Codex reviewed 017 and L1, and fresh
  Claude subagents reviewed 016.

There is no human review and no end-to-end proof-assistant formalization.
The CNF UNSAT certificates are machine-checked: CaDiCaL produces LRAT
proofs that the pinned lrat-trim checks, so CaDiCaL itself is not a
trusted premise. The encoders and readers that tie the CNFs to the
mathematics are trusted code, reviewed by AI.

Exploratory and negative work:
- 011 established no new n = 14 exclusion. Full-SDP feasibility there is
  numerical only.
- 012 found n = 13 witnesses and proved the face-lift lemma.
- 013 was a dated literature search that found no resolution and no
  directly applicable SDP prior art. That is a negative search result, not
  a novelty claim.

## Frontier after 1533 (scopes are nested: never add them)

- Magnitude ledger, `empty_pair` section of `findings/negative-quintic-pattern-cases-cycle1388.json`
  (the same file's 21 one-edge patterns are all excluded): 73 patterns, 44 excluded, **29 OPEN**. No whole pattern has changed since
  the frontier was set.
- Residual defect <= 6: the two-free (1531) and one-free (1533) branches are
  excluded, so every residual <= 6 instance has negative-support union 14
  ("no-free"). This is conditional on the residual-four support constraints,
  1401/1404, 1531 and 1533.
  That is **22 of the 29 open patterns**: remaining defect 0, 2, 4 and 6
  for 7, 6, 6 and 3 patterns. Typed in `attempts/018-no-free-residual-six/no-free-frontier.json`,
  with an independent reader.
- The other **7 open patterns** have remaining defect 8 to 12 and are
  untouched by 014 to 018.

## In flight: attempt 018, lemma L1

Read `attempts/018-no-free-residual-six/README.md` first. In short:

- Proposed L1 (`L1.md`, reviewed by Codex) covers magnitude m in {1, 2}
  at a coordinate in exactly one negative quintic. It allows at most one
  incident residual departure, which must cost 2 if present. L1's claim is
  that no derivative exists there. If certification completes, the
  counting in `L1.md` would exclude (2^4) and (2^4,1). **Neither pattern
  is excluded yet.**
- Proof route: an exact cover of 2221 cases (`cases018.py`, checked by
  `cover_reader018.py`) times m in {1, 2}, so 4442 obligations. Each needs
  an LRAT certificate (`certify018.py`, read by `reader018.py`); assembly
  is `read_all018.py`.
- State on 2026-10-23 (about 23:35 local, UTC-5): `run018.py` is running
  with 8 jobs. Its bookkeeping (`status018.py`) reports about 1,025
  covered obligations of 4,442 and one failed certificate job. Assembly
  (`read_all018.py`) has not been run yet. The run is resumable from
  `certs/results.jsonl` and `certs/results-extra.jsonl`.
- **Case 754 (m = 1), resolved.** CaDiCaL timed out at 3600 s on the
  original core, because the core relied on a 253-term value row. A core
  taken inside the structural subset with value rows of size at most 3
  (`certify(..., seed_k=3, seed_core=True)`, the Codex consultation
  `consultations/case754-strategy`) has 1,437 rows. CaDiCaL refutes it in
  20 s, and reader018 verifies it in both modes. It covers the none, c0
  and c3 obligations at m = 1 (`certs/l1-00754s3-m1.json`). The failed
  partial proof is compressed and is not evidence.
- **Seed-core mode.** From about 23:45 the run uses `--seed-core 3`: a core
  inside the structural subset, with no deletion pass. It took about 8 s
  per pm case in a benchmark, against about 450 s with full-model cores
  (018 `README.md`).
- **Open issue: disk.** The disk is about 90% full. The proofs average
  44 MB, with some over 2 GB; about 65 GB more is expected and about 89 GB
  was free. A watchdog in the Claude session stops the run below 15 GB.
  Storing verified proofs compressed would need a reader change and review.
- When `read_all018.py` reports `ALL_L1_CASES_VERIFIED`, do three things:
  1. Write the acceptance, following 017 `make_acceptance_1533.py`.
  2. Get an independent audit.
  3. Ask the user before freezing checkpoint 1534.

## Planned next fronts (judgement, not established; critique welcome)

1. Finish L1 and freeze 1534 on approval.
2. The other 20 no-free inventories with residual <= 6. The L1 counting
   (enough delta = 1 coordinates and few departures) works for N <= 5
   supports. Unit-heavy inventories (9 or more supports) probably need a
   global argument rather than per-placement case trees (018 `PLAN.md` step
   (d) and `SCOPING.md`).
3. The 7 patterns with remaining defect 8 to 12.

What worked in 017 and 018:
- Root the derivative at a vertex whose link comes from a complete sphere
  catalog, place the remaining structure explicitly, then certify each case.
  Unrooted and budget-only CP-SAT models were UNKNOWN at 600 to 900 s.
- In 018, rooting at an ordinary vertex of maximum degree adds degree-cap
  rows. In pilots, cases certified in about 20 to 30 s with them, against
  a median of about 900 s without them. Those are session observations,
  not a controlled benchmark.
- "Variants": one certificate covers every (type, m) obligation whose
  substituted rows coincide, and the reader checks this.

## Conventions used in attempts 011 to 018

- One directory per attempt. Producers emit candidates; separately written
  readers re-derive them with negative controls. Notes are Markdown, and
  reviews are saved as `REVIEW-*.md`. Each attempt has an `ATTEMPT.json`;
  after editing one, run `tools/attempts.py index`.
- Readers validate keys strictly. In 017 a Codex review forged a
  certificate with an out-of-range vertex, and the reader accepted it. Keep
  readers rebuilding every row from its definition, never trusting stored
  coefficients.
- Tests run in both normal and `-O` mode. Under `-O`, pytest still
  enforces the rewritten asserts in collected test modules, but not the
  asserts in imported code. A verifier that checks with `assert` silently
  stops checking. Directly run scripts lose every assert; `tools/attempts.py
  test` counts these.
- 012 `verify.py` checks with `assert`, so under `-O` it accepts invalid
  functions. Its `-O` test run is declared `normal_only` in `ATTEMPT.json`.
  012 is closed and none of it is accepted, but do not run its verifier
  with `-O`.
- Frozen files are immutable. Successors and corrections go in new files.

## Freezing a checkpoint

Run `H/save_research_checkpoint_v3.py` from `H` in normal mode, with its
required arguments: `--cycle`, `--previous`, `--previous-sha256`,
`--authority`, `--summary`, `--artifacts` and `--next-cycle`. Since 1533,
`CLAUDE.md` and `AGENTS.md` have changed (`CLAUDE_HANDOFF.md` has not), so
also pass:

```sh
--superseded /home/spinoza/github/math-theory/CLAUDE.md /home/spinoza/github/math-theory/AGENTS.md
--snapshots checkpoint1533-navigation-snapshots.json checkpoint1533-agents-snapshot.json
```

Before editing any pinned entry document, take an immutable snapshot of it,
as in those two files. Then update `state.md`, `synthesis.md` and the
`CLAUDE.md` / `AGENTS.md` status lines.

## Validation and environment

From `.research/`:

```sh
venv-exact/bin/python -B tools/attempts.py validate     # navigation metadata vs checkpoint chain (not an integrity check)
venv-exact/bin/python -B tools/attempts.py index --check
venv-exact/bin/python -B tools/attempts.py test --jobs 2   # configured steps, normal and -O (about 30 min)
(cd tools && for m in test_attempts test_consult_codex; do ../venv-exact/bin/python -m unittest $m && ../venv-exact/bin/python -O -m unittest $m; done)
```

These run the configured tests, not every historical reader or certificate
replay. Attempts 001 to 008, 010 and 013 have no configured tests.

The interpreters are listed in [environments.json](environments.json):
- `venv-exact` (Python 3.10) runs the readers and most tests.
- the root `.venv` (`uv run --extra search`) has OR-Tools for the producers.
- 011 has its own `.venv` for cvxpy.

The `VIRTUAL_ENV ... does not match` warning from uv is harmless.

The machine is shared (12 cores, 62 GB, other users' jobs). Keep to 8
parallel jobs or fewer and watch the disk.

## Publication and attribution

The latest publication recorded in this workspace is v1.4 (DOI 10.5281/zenodo.23544931), which
covers only the earlier residual-six packet. Checkpoints 1531 to 1533, and
1534 if accepted, are candidates for a successor version in the same DOI
family. Publishing needs the user's approval and follows `AGENTS.md`.

Attribution:
- Author: Alexander Richard Towell.
- OpenAI Codex: most work up to 1530, and reviews since then.
- Claude Code (Opus 5.5): attempts 011 to 018 and checkpoints 1531 to 1533.
