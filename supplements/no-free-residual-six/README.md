# Degree-five Boolean candidates: residual six with a negative-free coordinate excluded, two whole patterns excluded (v1.5.0)

Alexander Richard Towell, with substantial AI assistance (OpenAI Codex;
Claude Code with Claude Opus 5.5). Reserved DOI 10.5281/zenodo.23999933;
concept DOI 10.5281/zenodo.23496541.

**Global status: OPEN.** This is a packet of conditional local exclusions with
finite certificates, not a solution of the question.

For a Boolean function on 14 variables of degree at most 5 with full
sensitivity at the origin, in the existence-preserving self-dual empty-pair
normal form, this packet archives the accepted research checkpoints 1531 to
1534:

- residual Fourier defect <= 6 with at least two negative-free coordinates
  is excluded (1531), as is the case with exactly one (1532, 1533); hence every
  remaining residual <= 6 instance has negative-support union 14 (residual
  <= 6 is not closed: 20 of its patterns remain open in that case);
- lemma L1 and the exclusion of the whole negative quintic magnitude patterns
  (2,2,2,2) and (2,2,2,2,1) (1534). 27 of 73 patterns remain open.

`REPORT.md` states the exact claims, the premises they depend on, what the
replay checks and what is not claimed. `REPRODUCE.md` explains how to replay
every certificate. `CONTRIBUTION.json` and `CITATION.cff` carry the
structured metadata.

## Contents

| Path | What it is |
|---|---|
| `REPORT.md` | claims, premises, replay scope, limitations, AI disclosure |
| `REPRODUCE.md` | download, container build, replay command, expected receipt |
| `replay_packet.py`, `run_controls.py` | the replay driver and its controls |
| `runtime/` | Dockerfile and pinned Python requirements |
| `source/` | the research sources and evidence documents at their original paths under `.research/`: attempts 014 to 018 without their certificates, the acceptances, frontiers, ledgers and checkpoint manifests 1531 to 1534, everything they pin one level down, and lrat-trim with its source and license (580 files, 102 MB) |
| `SOURCE-MANIFEST.json` | original path, size and SHA-256 of every file in `source/` |
| `CERTIFICATE-MANIFEST.json` | every file of the separate certificates tar (41,304 files), with its stored and original SHA-256 |
| `CONTRIBUTION.json` | structured claim, verification and disclosure metadata |
| `verification/` | the receipt and logs of the staged replay |
| `build/` | the scripts that staged the packet |
| `review/` | the pre-publication AI review (Codex) and the changes made in response |
| `LICENSE.md`, `LICENSES/` | MIT for code, CC-BY-4.0 for notes, certificates and data |

The certificates themselves (CNF, label maps, LRAT proofs and certificate
JSON for attempts 014, 017 and 018: 17.8 GB stored, 100.8 GB uncompressed)
are archived beside this packet as the split tar
`certificates-v1.5.0.tar.part00` to `part08`.
