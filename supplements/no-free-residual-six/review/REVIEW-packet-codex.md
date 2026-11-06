# Review: v1.5.0 packet before publication (Codex, 2026-11-06)

Consultation `consultations/packet-review.*` (read-only, effort high). AI
review, not acceptance. Codex hashed the 570 staged sources, counted contexts,
covers and obligations, matched every receipt-referenced certificate input to
the manifest, ran four bundled fixture proofs through lrat-trim and exercised
the 018 assembly bookkeeping. It did not run the full replay.

## Findings and what was done

| # | Severity | Finding | Action |
|---|---|---|---|
| 1 | blocking | "Residual six closed" overstates: 20 residual <= 6 patterns remain open; 1531 to 1533 exclude only instances with a negative-free coordinate | Titles, abstracts, README, REPORT, CITATION, Zenodo metadata reworded; REPORT states explicitly that residual <= 6 is not closed |
| 2 | blocking | lrat-trim's license and source missing (only the binary was staged), although the license requires its notice | Added LICENSE, source, build files and upstream commit b30f400f to `source/` |
| 3 | blocking | `018-no-free-residual-six/README.md` differs from its 1534 pin | Confirmed (only mismatch of 1,942 pins). The pinned bytes were recovered by reversing the three post-acceptance navigation edits recorded in the session transcript (2026-10-24 08:33 and 22:47 UTC); the result matches the pin `00a0b9b8...`. The packet carries those bytes; `check_pins.py` now runs as part of the build and fails on any mismatch |
| 4 | gate | receipt not yet present | the final tarball is built only from a complete replay receipt (`make_release.py` refuses otherwise) |
| 5 | should-fix | premise summary not exhaustive; SCOPING.md is unreviewed | REPORT lists every `conditional_on` entry verbatim per checkpoint, and points to L1.md, not SCOPING.md |
| 6 | should-fix | x86-64 only; scratch scales with jobs; unquoted paths | REPRODUCE states x86-64, about 3.5 GB scratch per job, quoted paths |
| 7 | should-fix | `build/docker_replay.sh` resolved a non-existent path | fixed in the packet copy (packet-relative) |
| 8 | should-fix | controls: 014 accepted any failure; the 018 missing-certificate control is bookkeeping only | 014 controls now require the exact exit code and verdict or message; REPORT and `run_controls.py` describe the 018 control's actual scope |
| 9 | minor | CONTRIBUTION.json promised but absent; disclosure dates | written at release time with private-record and first-public-disclosure fields |
| 10 | minor | REPORT grouped the 017 and 018 assembly checks loosely | described separately (constants and the 24 frontier shapes; magnitudes, frontier reader, exact targets) |

The replay was restarted (`replay-full4`) after fixes 2, 3 and 8, because they
change `source/` or the controls.
