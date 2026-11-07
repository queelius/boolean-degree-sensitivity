# Residual six with a negative-free coordinate excluded; two whole patterns excluded (checkpoints 1531 to 1534)

Alexander Richard Towell, with substantial AI assistance (see "Authorship and
AI assistance"). Version 1.5.0, reserved DOI 10.5281/zenodo.23999933, concept
DOI 10.5281/zenodo.23496541.

**Global status: OPEN.** This packet contains no Boolean construction and no
nonexistence proof for the original question. It archives four conditional
local results and the finite certificates behind them.

## The question

Does a Boolean function f on 14 variables exist whose real multilinear degree
is at most 5, with f(0) = 0 and f(e_i) = 1 for every i (full sensitivity 14 at
the origin)? This is the d = 5 case of Epoch AI's open problem on sensitivity
versus degree (https://epoch.ai/frontiermath/open-problems/degree-sensitivity-boolean):
such an f would beat the sensitivity bound d^(log 6 / log 3), about 13.8 at
d = 5.

## Normalization (existence only)

All statements concern the existence-preserving self-dual empty-pair
representative used throughout the program: if any f with the properties
exists, then one in this normal form exists. The reduction holds for
existence only. Arbitrary Boolean functions with the properties are not
assumed to be self-dual. In the normal form the negative quintic Fourier
coefficients form one of 73 "empty-pair magnitude patterns"; the residual
Fourier defect measures how far the remaining spectrum departs from the
pattern's baseline; a coordinate is negative-free when it lies in no
negative quintic support. The accepted definitions used here are in
`source/.research/attempts/018-no-free-residual-six/L1.md` and the earlier
archived versions of this record family. (`SCOPING.md` in the same directory
is an unreviewed planning note, not an authority.)

## Results

Each result is conditional on the premises listed in its acceptance JSON
(`source/.research/attempts/009-parent-analysis/*-acceptance-cycle153N.json`)
and summarized below. Scopes are nested; the counts below are not additive and
give no completion fraction.

| Checkpoint | Statement | Finite evidence |
|---|---|---|
| 1531 | Residual defect <= 6 with at least two negative-free coordinates: no Boolean function. The 26 native signed-star contexts are exhaustive for this case, their raw rows are necessary, and every context is excluded. | 24 raw-row LRAT certificates (attempt 014); 2 contexts from earlier root-7 proofs (cycles 1476, 1497, 1501) |
| 1532 | One-free residual six (exactly one negative-free coordinate u): Types III and I have no realization; Type II is reduced from 136 departure-shape classes to 24. Statements about one derivative p = Delta_u f. | written arguments (016) with small exact checks |
| 1533 | One-free residual six: no Boolean function. The 24 Type II classes are excluded. Also, the root-7 context o7-i0-c2 has infeasible raw rows without the 1497 unit clauses, so all 26 signed-star contexts are excluded on raw rows. | 3,184 case certificates over an independently checked cover, each valid at c = 1 and c = 2 (017); 1 raw-row certificate (014 raw-1) |
| 1534 | Lemma L1, and the whole magnitude patterns (2,2,2,2) and (2,2,2,2,1) admit no Boolean function. L1: if a coordinate u lies in exactly one negative quintic, of magnitude m in {1,2}, and in at most one residual departure, of cost 2, then no derivative p = Delta_u f with the required properties exists. With negative-support union 14, counting gives an L1 coordinate in both patterns. | 3,662 case certificates covering all 4,442 obligations of an independently checked 2,221-case cover at m = 1 and m = 2 (018) |

Combined: 1531 to 1533 exclude every residual <= 6 instance that has a
negative-free coordinate, so every remaining residual <= 6 instance has
negative-support union 14. Residual <= 6 is **not** closed: 20 of its
patterns remain open in the no-free (union 14) case. 1534 then excludes two
whole patterns. 27 of the 73 original
magnitude patterns remain open: 20 with residual <= 6 and union 14, and 7 with
residual 8 to 12. The ledger is
`source/.research/findings/negative-quintic-pattern-cases-cycle1534.json`.

## Premises the results depend on

The replay does not re-prove these. They are written arguments, earlier
accepted results or external facts. Listed verbatim from each acceptance's
`conditional_on` (H = `attempts/009-parent-analysis`; "selfdual" means the
self-dual normal form above, existence only):

### 1531 (`signed-star-two-free-acceptance-cycle1531.json`)

- H/two-free-independent-review-cycle1409.md and every premise it inherits (selfdual representative, defect accounting, old local exclusions in its guard table, its two-free minus-three and doubled-quintic arguments); not re-reviewed in 015
- pynauty certificate correctness; Steinitz-Rademacher contractible-edge lemma; Whitney embedding uniqueness
- Replaced inherited premise: 006 inverse-contraction cover (179,583 transitions) replaced for this branch by the 015 independent vertex-split enumeration

Review kind: AI review by a different model family plus fresh finite computation and an independent adversarial subagent; not human peer review or formal verification.

### 1532 (`one-free-residual6-acceptance-cycle1532.json`)

- the 1513/1523 one-free trichotomy and every premise it inherits (selfdual representative, defect accounting)
- Type III: the accepted local premises of each two-exception source theorem (one-six-edge and one-three-edge arguments, six-vertex and pentagon lemmas, endpoint sphere catalogs and their inherited inverse-cover completeness), the 1526/1527 acceptance, the 76-record scan and the completeness of the Frick 2015 Theorem 3.10 catalog for (+1,+1), the 015 enumeration for L7/L8
- Type I: the 1395 local argument from its displayed form onward; the endpoint lemma is a hand proof at all orders
- Type II: the 006 private-vertex argument (two-exception-positive-extension.md and its accepted audit), the parity and weight identities of TYPE-II-RIGID-SHAPES.md, small-sphere facts S3, S4, S6 (exhaustive to 12 vertices and by curvature), pynauty for the producer shape list (the reader does not use it)

Review kind: written arguments, each reviewed by a fresh AI subagent (Claude) that re-derived it and replayed or rebuilt its finite checks in scratch files; small exact checks with tests in normal and -O mode; not human peer review or formal verification.

### 1533 (`one-free-residual6-acceptance-cycle1533.json`)

- everything checkpoint 1532 accepts for Types I and III, and the 1513/1523 trichotomy with its premises
- the written lemmas VERTEX-TYPES.md, CROSS-EDGES.md, NEAR-FLAG.md, SPECIAL-SHAPES.md (AI-reviewed)
- the 015 sphere enumeration (Steinitz-Rademacher contractible edges, pynauty certificates, Whitney uniqueness); CaDiCaL 3.0.1 and the pinned lrat-trim
- for o7-i0-c2: the 009 native raw rows and the 1409 premises, as for the other signed-star contexts

Review kind: written lemmas and code reviewed by OpenAI Codex (four reviews plus an end-to-end audit with a sampled certificate re-check) and a Claude subagent; exact checks and 44 tests in normal and -O mode; certificates checked by an independent reader and lrat-trim; not human peer review or formal verification.

### 1534 (`no-free-residual6-acceptance-cycle1534.json`)

- everything checkpoint 1533 accepts, including union 14 for both patterns (the no-free frontier authorities pinned in no-free-frontier.json) and the selfdual empty-pair reduction (existence only)
- the written reductions in L1.md (triangle incidence, ordinary-link classification, flagness, exceptional-endpoint classification, the doubled-quartic exclusion via 006 connected-six-unit-exclusion-audit.md, the A/B split and maximum-degree root choice), AI-reviewed
- completeness of the 017 sphere catalogs (roots-catalog.json, deltahedra.json) and surfaces.py, as accepted in 1533; CaDiCaL 3.0.1 and the pinned lrat-trim

Review kind: lemma, cover and code reviewed by OpenAI Codex (L1 review, case-754 strategy, end-to-end assembly audit); exact checks and tests in normal and -O mode; every certificate checked by an independent reader and lrat-trim; not human peer review or formal verification.

In addition: for the two root-7 contexts in 1531, the earlier 009 proofs
(cycles 1476, 1497, 1501), whose documents and proofs are in `source/` but
are not replayed here (the packet does replay a separate raw-row control,
raw-0, for o7-i0-c1, and 1533's raw-row certificate for o7-i0-c2). CaDiCaL
3.0.1 produced the proofs but is not trusted: every proof is checked by the
bundled lrat-trim 0.2.0 (`source/.research/attempts/006-solver-resume/lrat-trim/`,
upstream github.com/arminbiere/lrat-trim commit b30f400f, built in that
checkout; source, build files and license are included, and a rebuild gives
an equivalent but not necessarily byte-identical checker).

## What the replay checks

`replay_packet.py` (see `REPRODUCE.md`) runs, in a network-less container in
which the historical research path is the packet's read-only `source/` tree:

1. every source file's SHA-256 against `SOURCE-MANIFEST.json` (580 files).
   When the packet was built, every one of the 1,942 SHA-256 pins in the four
   acceptances, the four checkpoint manifests and the 1520 authorization that
   names a file in `source/` was checked against the staged bytes. One pinned
   navigation file, `attempts/018-no-free-residual-six/README.md`, had been
   edited after checkpoint 1534; the packet carries its pinned bytes, recovered
   by reversing the recorded later edits and checked against the pin (noted in
   `SOURCE-MANIFEST.json`);
2. every stored certificate file against `CERTIFICATE-MANIFEST.json` (41,304
   files, 17.8 GB stored, 100.8 GB uncompressed);
3. 014: `verify_core.py --require-raw` on the 24 certificates of 1531, the
   o7-i0-c2 certificate of 1533 and the o7-i0-c1 control, each output compared
   with the archived verify record. The reader rebuilds the context's rows from
   the pinned 009 sources, checks that every CNF clause is sound for those rows,
   and runs lrat-trim;
4. 017: the frozen assembly driver `read_all.py`, unchanged. Every
   certificate is read by the independent reader `reader017.py` (rows rebuilt
   from their keys, clause soundness, lrat-trim); the driver runs the cover
   reader on the three covers, requires every cover case at both constants
   c = 1 and c = 2, and binds the covered shapes to exactly the 24 open Type II
   classes of the 1532 frontier;
5. 018: the frozen driver `read_all018.py`, unchanged. Every certificate is read
   by `reader018.py`; the driver requires every case of the 2,221-case cover at
   both magnitudes m = 1 and m = 2 (4,442 obligations), runs the cover reader
   and the frontier reader, and requires the target rows to be exactly
   (2,2,2,2) and (2,2,2,2,1). For 017 and 018 the replayed results (certificate
   hashes, cases, constants or variants, input pins, verdicts) must equal the
   archived read-all receipts;
6. positive and negative controls in normal and optimized mode: an untouched
   certificate passes each reader; a proof without its empty-clause step (pin
   updated) is rejected by lrat-trim; an altered proof under its old pin and a
   changed row bound are rejected by the readers' own checks. For 018 the
   assembly bookkeeping (`missing` and `status`) is exercised on the archived
   result records with one certificate removed; this does not rerun discovery
   after deleting a real certificate, which the full stage 5 covers;
7. the unit tests of attempts 014 to 018 in normal and optimized mode.

`verification/REPLAY-RECEIPT.json` is the receipt of the staged replay.
A passing replay shows that the finite certificates are complete for their
covers and verify. It does not check the written reductions that turn those
finite facts into the statements above, and a hash match proves identity of
files, not correctness of mathematics.

## Disclosure

The results of checkpoints 1531 to 1534 were recorded privately in the
research tree on 2026-10-23 and 2026-10-24. This archive is their first public
disclosure; its publication date is the Zenodo publication date.

## Not claimed

No Boolean construction; no nonexistence proof; no human peer review; no
proof-assistant formalization; no novelty assessment. The global question
remains open. Work after checkpoint 1534 (attempt 019 and later) is not
accepted and is not included.

## Authorship and AI assistance

Alexander Richard Towell directed the program. OpenAI Codex did most of the
work up to cycle 1530 (mathematics, code, drafting, exact checks and reviews)
and acted as reviewer and auditor for attempts 017 and 018. Claude Code (Anthropic,
Claude Opus 5.5) did attempts 011 to 018, including the 1531 to 1534 results,
and prepared this packet. AI review is not human peer review.

## Licenses

Original code: MIT (`LICENSES/Original-code-MIT.txt`). Original proofs, notes,
certificates and data: CC-BY-4.0 (`LICENSES/CC-BY-4.0.txt`). lrat-trim is by
Armin Biere (University of Freiburg) under its own MIT license
(`source/.research/attempts/006-solver-resume/lrat-trim/LICENSE`).
