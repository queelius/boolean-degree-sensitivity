# Review: Codex audit of the L1 assembly (2026-10-24)

Consultation `consultations/l1-assembly-audit` (Codex session
01a16c7e-ff2a-7c30-a9f9-de89c8080028, effort max, read-only). AI review,
not acceptance. Curated by Claude Code (Opus 5.5).

## Verdict

No blocking gap. If `read_all018.py` passes cleanly, the finite refutation
step of L1 is complete. Together with the written reductions in `L1.md` and
the inherited catalog and normalization results, that establishes the
current (narrowed) L1 and excludes (2^4) and (2^4,1) as whole frontier
patterns, in the frontier's selfdual empty-pair representative, for
existence only. Codex disagrees with reading `ALL_L1_CASES_VERIFIED` alone
as an end-to-end check of those written premises, and so do I.

## What Codex confirmed (by source reading and its own bounded checks)

- `reader018` rebuilds every row from its key under the certificate's own
  case. It checks clause soundness (every row solution extends to a CNF
  solution) and *runs* the pinned lrat-trim, requiring exit 20 and
  `s VERIFIED`. Producer logs are not trusted.
- Refuting a subset of rows refutes the case, so seed-core certificates are
  sound. Codex reconstructed all 1,437 rows of `l1-00754s3-m1.json` for its
  three variants.
- Variants: pm and pp never substitute for each other; every retained row
  must coincide across claimed variants.
- Assembly: no duplicate (placement, type) in the 2221-case cover;
  placements shared across types cannot transfer coverage wrongly.
- Counting in `L1.md` (`#{delta=1} >= 28 - 5N`) checked; it needs no
  support geometry beyond union 14.
- No assert-based check in the readers; no `-O` bypass.

## Findings and what I did

| Finding | Severity | Action |
|---|---|---|
| `status` did not require 0 rejected | note (policy) | `read_all018.status()` now requires it |
| Exit code 0 even when `INCOMPLETE`; ad hoc argv | should-fix | argparse; exit 0 only on `ALL_L1_CASES_VERIFIED` |
| `--skip-cover` in docstring, not implemented | should-fix | docstring rewritten |
| Frontier only hashed, not read; targets could be empty | should-fix | `targets()` runs `frontier_reader` and requires exactly (2^4) and (2^4,1), once each |
| Receipt pins only `reader018.py` | should-fix | `DEPENDENCIES` pins `read_all018`, `reader018`, `cover_reader018`, `frontier_reader`, `L1.md`, the cover, the frontier, the 017 catalogs and `surfaces.py`, and the lrat-trim binary |
| Verify-then-reread race in `one()` | should-fix | `reader018.read` hashes the certificate, CNF and labels from the bytes it parses and returns `case` and `cert_sha256`; assembly binds those. lrat-trim still reads CNF and proof by path, so the acceptance run reads a write-protected `certs/` |
| Assembly negative controls missing | should-fix | `test_read_all018.py` (13 tests): no provider, one m only, rejected certificate, forged root, tampered proof hash, each status condition, dropped and duplicated target |
| `certify018.py` docstring named 017 tools | should-fix | rewritten |
| `cases018.py` claims exact orbits | note | docstring now says soundness rests only on the cover reader's matching |
| Written steps not code-checked: triangle incidence, link classification, flagness, exceptional endpoints, the doubled-quartic exclusion, the A/B split, catalog completeness (inherited) | note | to be listed as premises in the acceptance |
| `frontier_reader` checks pins and basis kinds, not the union-14 conclusion inside the authority | note | inherited from checkpoint 1533's acceptance; listed as a premise |

The preliminary `read-all-l1.json` from the run started before these fixes
records the edited reader's hash while running the old one, so it is not
evidence. Acceptance needs a fresh run of the fixed `read_all018.py`.
