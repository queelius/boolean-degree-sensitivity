You are being consulted by a Claude Code session that orchestrates this research. Read /home/spinoza/github/math-theory/.research/CODEX_BRIEFING.md for context and rules. Work read-only; do not start long solver runs unless the question asks for a bounded check. Say what you verified yourself, what you only read, and how confident you are. Disagree when you see a gap.

# Independent audit: does a passing read_all018.py establish lemma L1?

You are in `.research/attempts/018-no-free-residual-six` (read-only). The
certificate run for L1 has finished: 4442 (cover case, m) obligations,
3662 certificate JSONs in `certs/` (proofs are large; do not read `.lrat`
files, and do not run lrat-trim over the whole set). `read_all018.py
read-all-l1.json --jobs 6` is running now; do not run it yourself.

I want an adversarial audit of the *chain of reasoning*, not of the run:
if `read_all018.py` reports `ALL_L1_CASES_VERIFIED` with 0 rejected and 0
missing, what exactly is proved, and is there any gap between that and
"L1 holds, hence the patterns (2^4) and (2^4,1) are excluded"?

Read `L1.md`, `REVIEW-L1-codex.md`, `read_all018.py`, `reader018.py`,
`cover_reader018.py`, `model018.py` (only as far as needed), `certify018.py`
and the `seed_core` route in it, and `no-free-frontier.json`'s structure.

Questions, answer each explicitly:

1. **Reader independence.** Does `reader018.read` re-derive the rows from
   the stored case keys itself, rebuild the CNF from those rows, check the
   stored CNF against that rebuild (or against the label map), and *run*
   the pinned lrat-trim on the proof, rather than trusting a log or a
   status field written by the producer? Name the lines.
2. **Subset soundness.** Certificates from the seed-core route refute a
   subset of the case's rows. Confirm that a refutation of any subset of
   the rows of a case implies the case is infeasible, and that the reader
   checks every used row is a genuine row of *that* case (not of a
   sibling, a variant or another m).
3. **Variants.** One certificate covers several (type, m). How does the
   reader decide a variant is covered? Could a certificate for (type t,
   m=1) be credited for (type t', m=2) wrongly?
4. **Assembly.** `placement()` drops `type` and normalizes Q, pair and
   faces. Can two distinct cover cases collide under it so one
   certificate covers a case it was not built for? Is every cover case
   at m in {1,2} required? Is m in {1,2} the full range L1.md needs?
5. **Status logic.** `status` is `ALL_L1_CASES_VERIFIED` if there are no
   missing obligations and the cover reader passes; it does not require
   `rejected == []`. Is that a soundness issue or only hygiene? The
   docstring mentions `--skip-cover`, which is not implemented. Anything
   else stale?
6. **Cover to lemma to patterns.** Does `cover_reader018` establish that
   the 2221 cases exhaust every situation L1.md's statement quantifies
   over? Then does L1 plus the counting in L1.md really exclude (2^4) and
   (2^4,1) *as whole frontier patterns* in the normalization the frontier
   uses (selfdual empty-pair representative; existence only)? Flag any
   step that is argued only in prose and not checked by code.
7. **Anything else** you would want checked before this is frozen into a
   checkpoint (for instance: a negative control showing read_all fails on
   a deleted or tampered certificate; the `-O` behaviour of the readers).

For each finding give severity (blocking / should-fix / note), the file
and line, and what you verified yourself versus inferred. Disagree plainly
if you think the result does not establish what I said.
