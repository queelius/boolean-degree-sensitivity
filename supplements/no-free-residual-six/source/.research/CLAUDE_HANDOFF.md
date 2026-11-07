# Claude Code handoff — 2026-10-21

Research is paused at the user's explicit request. The problem is **OPEN**.
All experiment processes from this session are terminal. Do not resume a
search merely by opening the directory. Start new research when the user
asks to continue. No external approval or publication step is pending.

## Objective and completion criteria

Decide whether a Boolean multilinear polynomial f on14 variables can have
real degree at most5, f(0)=0, and f(e_i)=1 for all14 coordinates.
The authoritative objective is [active-objective.md](active-objective.md).
Completion requires either an explicit construction independently checked on
all16,384 inputs, including exact degree and sensitivity, or a rigorous
nonexistence proof covering every remaining case with independently checkable
certificates. Pruning, a necessary profile, a ternary derivative, a prefix,
solver UNKNOWN, or a local obstruction does not complete the goal.

Read [current-checkpoint.json](current-checkpoint.json), which now points to
checkpoint1530, and [state.md](state.md). Follow pinned references rather than
recursively scanning the very large historical experiment directories.

In paths below, `H` means `attempts/009-parent-analysis`, `A` means
`attempts/008-sparse-spectrum-proof`, and `S` means `attempts/006-solver-resume`,
all relative to this `.research/` directory.

## Frontier: three different scopes

- Original magnitude ledger:73 total,44 excluded, **29 OPEN**. Canonical source:
  `findings/negative-quintic-pattern-cases-cycle1388.json`. Older similarly named
  ledgers can have stale counts; preserve them for historical hash bindings.
- Conditional two-negative-free-coordinate signed-star branch:26 genuine
  contexts,2 excluded and **24 OPEN**, comprising13 root geometries, with
  root(order7,index0) excluded and **12 roots OPEN**.
- Old raw12512-row relaxation:1 excluded, **25 OPEN**. The second root7
  exclusion uses additional proved topology constraints. Do not label that
  old raw row relaxation UNSAT, and do not add these counts together.

The complete typed local frontier is
`H/signed-star-genuine-frontier-cycle1510.json`;1530 preserves it unchanged.
Existence has a proved selfdual representative reduction. **Arbitrary
original Boolean functions are not assumed selfdual.**

## What was completed in the latest work

1. General theorem1507/1508, accepted before this handoff: in a combinatorial
   PL3-sphere, a valence3 edge whose opposite three edges have valence at most5
   can have its opposite triangle filled only if a vertex has graph degree4.
   Hence all positive signed-star opposite triangles are absent. The PL
   Alexander/Schoenflies premise is explicit, with Hatcher's author-hosted
   statement checked. This is written mathematics with independent AI review,
   not a formal proof or a novelty claim.
2. Elementary1514 theorem and independent1515 review: a simplicial S2 with
   exactly one degree3 vertex and all other degrees4/5 is an octahedron with
   one face subdivided. Every positive nonroot tip therefore has degree7;
   its three edges to its fixed opposite set A have valence5, other present
   nonroot incident edges have valence4. Preserve the correction: deletion
   alone leaves a punctured disk; **deletion plus capping** gives the octahedron.
3. Source-only1516 and independent1517 filter agree on all9146 sphere records
   of orders7..12. Necessary nonroot degrees: positive tips{7}, negative
   tips{9,10,11}, ordinary vertices{6,7,8,9,10,12}. The central root is outside
   these classes. The179583 inverse-cover transitions remain an explicitly
   inherited completeness premise, not a fresh replay.
4. Complete1518 inventory and independent1519 comparison derive3122 distinct
   added rows,3126 theorem occurrences and46688 terms across all26 contexts.
   There are4 genuine duplicate rows retaining both provenances. Ordinary
   degree11 is excluded without auxiliaries by D_v-2*x_vj<=10 for every j;
   all4096 twelve-bit edge vectors were independently checked. This does not
   impose degree>=6 by itself.
5. Accepted1513/1523 one-free residual<=6 reduction: negative-support union13
   allows three necessary allocation types, recorded in the source proof.
   The sole cubic-3 type has exceptional endpoint degrees11/12 and at least
   two missing triangles through that edge. No whole-complex manifold claim
   is made there. Unions14/no-free and larger residual budgets remain open.
6. New1526/1527 theorem extends the **adjacent pair of quadratic-2 exceptions**
   local obstruction to constants0/3, with all other coefficient hypotheses
   retained. Independently replayed945 literal rows,1111 opposite-value
   deductions and9 final contradictions. This removes only that subcase
   of TypeIII; it does not exclude every two-exception constant0/3 case.

Authority entry points:

- `H/link-math-parent-acceptance-cycle1520.json` (1515/1517 and source premises).
- `H/exact-tip-inventory-authority-cycle1519.json` and its manifest.
- `H/one-free-parent-acceptance-cycle1523.json`, and
  `A/one-free-independent-authority-cycle1523.json`.
- `A/adjacent-negative-extension-authority-cycle1527.json` and its manifest.
- `A/one-free-two-exception-source-receipt-cycle1523.json`: confirms the older
  **disjoint** negative/mixed two-exception cases at c1/2 have their own
  single-derivative authority; no second free coordinate is silently used.

## Last actual experiment — finished, independently checked, inconclusive

One order8,index3,constant1 propagation run used all12512 original rows plus
123 new rows:12635 rows,840913 terms,1079 native variables, no new auxiliaries.
It proposed344 fixed values (74 ones,270 zeros), leaving735 unassigned.
The producer reported a fixed point after13305 evaluations. The independent
reader verifies **every deduction and the full row-map bijection**, not
fixed-point completeness or satisfiability. There is no contradiction.

- Producer1521: exec session1486, terminal exit0, one query/no retry;
  2.92 external CPU seconds,2.94 wall,278319104-byte peak RSS.
- Reader1522: exec session66550, terminal exit0;
  4.31992 reader CPU seconds,6.09 external wall,271528KiB peak RSS.
- `H/tip-interval-handoff-cycle1521.json`, its manifest, and
  `H/extended-trace-authority-cycle1522.json` / manifest contain exact pins.
- Candidate `H/tip-interval-pilot-cycle1521.json` SHA256
  `6cdf1fb1262763a0b8857fbc92abd1c74e6b01b644e2c2e9fc247f8faa2ba6ed`.
- Independent authority SHA256
  `acd7c2dc14968ff88d830bbf08dc636d8bc095cc9412223e2e8eb73c5c3ad54b`.

Do not repeat this run without new evidence or changed constraints. The new
cuts yielded a valid prefix, not a new exclusion. Old root7 c1/c2 proofs are
separate accepted LRAT artifacts1476/1501; do not transfer their CNF indices.

## Corrections and failed approaches to retain

- Frozen1504/1506 erroneously counted all ordinary active edges as Fourier
  coefficients-1. Valence4 gives0; only valence5 gives-1. Correct signed-star
  squared norms are66/72, complement norms190/184, support bounds190/184,
  integer amplitude bound13. The old c2 numbers96/160 and amplitude12 are
  superseded. Fresh correction `H/fourier-extension-norm-correction-cycle1513.json`
  is independently accepted1523. No actual matrix, witness, CNF or LRAT used
  the bad estimate. Never edit the frozen old files to conceal the correction.
- `H/fixed-derivative-annihilator-dimension-cycle1528.md` explains why an
  actual even ternary p leaves homogeneous odd-degree<=5 kernel dimension at
  least530/434. A bare homogeneous full-rank test cannot settle extension;
  affine normalization, integer norm/sign/inventory and Boolean constraints
  remain essential. This is a written dimension observation, not a matrix run.
- Earlier MILP1493 hit a512MiB memory limit. Its1GiB successor1496 reached
  its15-second limit without a candidate. Earlier SAT UNKNOWN/partial proofs
  are inconclusive. Root7 is now genuinely closed; do not resume those searches.
- The3-to2 move can be admissible without preserving the ternary range or
  signed-star hypotheses. No unproved constant, flagness or symmetry transfer.

## Recommended continuation, once requested

Use the checked344-value prefix and1519 constraints to price one meaningful
proof-producing SAT experiment on the same order8 context, or pursue a new
analytic obstruction. Reuse the existing native encoder/independent1461
stream-reader architecture, but derive the new primary-variable allocation
and auxiliary bindings exactly. A new context needs its own CNF and proof;
root7 masks/DIMACS indices are not transferable. SAT candidates still need
full original-model checks; a ternary p alone needs a compatible Boolean
extension and all16384 original-input checks. UNSAT needs a complete accepted
LRAT ending at an actual verified empty clause.

Keep work beyond the two-free branch active in the research plan. TypeIII's
remaining constant0/3 two-exception cases are a focused analytic question;
1527 does not close disjoint or mixed cases there. An unverified lead at
session stop was to revisit the old two-positive proof at c3: a disconnected
ordinary link leaves at most10 cross edges, and the newly explicit positive
degree7 link structure may strengthen its old cross-edge argument. No proof,
certificate transfer or exclusion for this lead has been accepted.

Choose experiments using measured costs and information gained. Prefer one
properly bounded informative run to a succession of nearly identical short
UNKNOWN runs. Keep parameters, failures and certificates reproducible.

## Validation, publication and environment

From `/home/spinoza/github/math-theory`:

```sh
.research/venv-exact/bin/python -m pytest -q
.research/venv-exact/bin/python .research/attempts/009-parent-analysis/test_link_profiles_cycle1516.py
```

Root tests freshly passed13/13 at handoff. New producer/reader controls pass
normal/optimized modes with their per-packet coverage receipts. Certificate
replays and hashes have different scopes; a checkpoint pin check does not
replay mathematics or an old catalog cover.

This directory is not itself Git-controlled. Curated public source is
https://github.com/queelius/boolean-degree-sensitivity; local Git checkouts
include `.research/publication/boolean-degree-sensitivity` and the clean
`residual6-source-cycle1429` worktree. Do not initialize Git, move the active
evidence, or overwrite another worktree's changes as part of resuming.

Published version1.4 DOI **10.5281/zenodo.23544931** covers the earlier
conditional residual-six packet. It does **not** archive the later topology,
root7 certificates or this handoff's results. The central public catalog is
https://github.com/queelius/research-records, local `../research-records`.
The important accepted local contributions are candidates for a coherent,
portable successor in the same DOI family after packaging/replay and a cited
novelty assessment. No deposit or public source mutation occurred in this
session. Follow `AGENTS.md` and central `PUBLISHING.md`; never expose credentials.

Primary technique/novelty receipts include Frick2015, Theorem3.8 (printed43–44),
https://d-nb.info/1076082246/34, and Hatcher's PL discussion. They corroborate
prior classifications and topology premises; no new classification, global
solution, formal proof or human peer review is claimed. Exact access scope
is recorded in `H/primary-small-valence-literature-refresh-cycle1516.json`.

User: Alexander Richard Towell, lex@metafunctor.com,
ORCID0000-0001-6443-9897. Substantial OpenAI Codex assistance must be disclosed.
New general mathematics work belongs in `../math-research`; platform checkouts
remain separate; `research-records` is the shared public catalog. Existing
evidence stays here until a verified migration preserves it.
