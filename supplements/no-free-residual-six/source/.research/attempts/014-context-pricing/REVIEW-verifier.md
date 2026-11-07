# Independent adversarial review of verify_core.py (2026-10-23)

Reviewer: a fresh Claude subagent with no access to the producing session's
context, asked to find any way the verifier could accept rows that are
feasible. AI review, not human review. Its report, condensed; file:line
refer to verify_core.py before the hardening below.

## Findings

Soundness of accepted clause shapes (76-117): no hole found. Root units need
label (r,0,0); step clauses tie the literal to term k of row r (104-106) and
use the true-literal polarity (107), so both branches and negative
coefficients are right; missing clauses only weaken the CNF; dead-end ranges
(114) are correct even with repeated variables; the empty clause needs a
row infeasible alone (93); labels need distinct aux ids in (1079, nvars],
a core row, and 0 <= k <= row length. lrat-trim's parser
(006/lrat-trim/lrat-trim.c:1060-1240) is stricter than read_cnf and only
diverges in the safe direction; it prints `s VERIFIED` only after an empty
clause is checked (2564-2572). The binary is hash pinned and run on the
clause-checked path. Ran raw-2, raw-19, raw-25 (verified) and the tests.

Binding holes, each reproduced on tampered copies outside 014:

1. The printed label came from the certificate, not the model; a relabelled
   raw-18 certificate verified under the raw-19 label.
2. Raw-only scope was not enforced; a core using an added row (id 12600)
   verified.
3. Row ids were not range checked; id -1 silently selected the last added
   row.

Lesser: the authorization file was not hash pinned; verify records omitted
model id, row ids and hashes; context_rows/read_cnf/CLI were untested.

Verdict: acceptance soundly implies infeasibility of the listed rows of the
named context. For the 24 real certificates the reviewer separately checked
index-to-context agreement and raw-only ids, so the stated raw claims hold.

## Response

All addressed in verify_core.py: authorization SHA pinned; row ids must be
distinct non-bool integers in range, and `--require-raw` rejects ids at or
above common + context rows; the record's label is derived from model_id and
it carries model_id, row_ids, row_scope and every input hash. New tests
(test_verify_core.py) cover bad ids, scope, derived labels, and CLI runs
against tampered copies of raw-19 for the three demonstrated attacks; 99
tests pass. All 24 certificates were re-verified with `--require-raw` into
`certs/raw-<i>.verify2.json`; `make_summary.py` builds the summary from those
records and cross-checks model and row ids against each core.
