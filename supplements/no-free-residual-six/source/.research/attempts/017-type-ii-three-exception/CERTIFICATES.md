# 017 result: the 24 open Type II shapes

Alexander Richard Towell, with Claude Code (Anthropic) assistance; the
source theorems are OpenAI Codex-assisted work. Proposed result, reviewed by
Codex and Claude subagents (not human review). Not frozen. Global status:
OPEN.

## Claim (proposed)

None of the 24 open Type II shapes of `H/one-free-residual6-frontier-
cycle1532.json` has a ternary derivative p = Delta_u f at c = 1 or c = 2.
With checkpoint 1532 this would exclude the one-free residual-six case
(residual Fourier defect <= 6 with exactly one negative-free coordinate).
It would change no whole magnitude pattern: the no-free residual case and
residual defect above six stay open.

## Chain

1. Structure (written, reviewed): VERTEX-TYPES.md, CROSS-EDGES.md,
   NEAR-FLAG.md, SPECIAL-SHAPES.md. Outcome: every vertex link of known
   type is a sphere from a complete catalog; near-flag rows are valid at
   the stated vertices; only the stated triples may have incidence 4.
2. Cover (exact, independently checked): `cases.py` produces
   `cover-cases.json` (22 shapes, 2775 cases, rooted at an exceptional
   vertex), `triangle-cover.json` (81 cases) and `shape1-cover.json` (328
   cases), both rooted at an ordinary vertex. `cover_reader.py` (no shared
   code, its own automorphism routine) checks that every labelled placement
   is covered.
3. Model (exact rows plus proved rows): `model.py`. Pair, triple, vertex,
   constant and value rows are equivalent to the hypotheses on p; flag and
   implied rows are proved consequences. Positive control: the 16-cell at
   n = 8, c = 0 is feasible and passes an independent Fourier evaluation.
4. Certificates (untrusted producer): `certify017.py` substitutes the root
   fixings, extracts a CP-SAT core, encodes it with the 014 decision-diagram
   encoder, proves UNSAT with CaDiCaL 3.0.1 (LRAT) and checks with the
   pinned lrat-trim. A core without the constant row covers c = 1 and 2.
5. Reader (independent): `reader017.py` rebuilds every stored row from its
   key and the case alone, applies the fixings, checks every clause and
   runs lrat-trim. `read_all.py` requires a verified certificate for every
   case of the three covers at both constants.

## Numbers

`read_all.py` (result `read-all-result.json`): status ALL_CASES_VERIFIED.

| cover | shapes | cases | certificates |
|---|---|---|---|
| `cover-cases.json` (exceptional root) | 22 | 2775 | 2775 |
| `triangle-cover.json` (ordinary root) | 1 | 81 | 81 |
| `shape1-cover.json` (ordinary root) | 1 | 328 | 328 |

- 3184 certificates, all LRAT-verified by the pinned lrat-trim and by
  `reader017.py`; 0 rejected, 0 missing (case, constant) obligations.
- Every core avoids the constant row, so each certificate holds at both
  c = 1 and c = 2 (the reader rebuilds every row at both constants).
- 471,742 core rows in all (largest core 2,622), 43,863,984 clauses;
  certificate files about 13 GB in `certs/`.
- `cover_reader.py` passes on all three covers (14,643 + 1,285 + 8,847
  labelled placements), and the covered shapes equal the 24 OPEN rows of
  the frozen frontier `H/one-free-residual6-frontier-cycle1532.json`.
- Tests (normal and -O): `test_surfaces_vertex_types` 7,
  `test_step4_count` 6, `test_reader017` 17, `test_cover` 11,
  `test_assembly` 3.

## Premises

The written lemmas VERTEX-TYPES.md, CROSS-EDGES.md, NEAR-FLAG.md and
SPECIAL-SHAPES.md (each reviewed); the 015 sphere enumeration
(Steinitz-Rademacher, pynauty certificates, Whitney); CaDiCaL plus the pinned
lrat-trim; and, upstream, the 1513/1523 one-free trichotomy and its
premises, as frozen in checkpoint 1532. The certificates prove that the
case rows are infeasible; that the rows are necessary is the written
argument plus `reader017.py`.

## Reviews

Codex (OpenAI) reviews: VERTEX-TYPES (REVIEW-vertex-types-codex.md),
CROSS-EDGES (REVIEW-cross-edges-codex.md), certification chain
(REVIEW-chain-codex.md: model rows, near-flag rows, root fixing and cover
sound; the reader accepted out-of-domain keys, a real verifier hole, now
fixed with adversarial tests), NEAR-FLAG and SPECIAL-SHAPES
(REVIEW-special-codex.md: sound after wording fixes). Claude review:
VERTEX-TYPES (REVIEW-vertex-types.md). Final end-to-end audit by Codex
(REVIEW-final-codex.md): the evidence supports the conditional exclusion;
its fixes (full-case matching in read_all.py, the placement count, restart
scheduling) are applied, with regression tests.
