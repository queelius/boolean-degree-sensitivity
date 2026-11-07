**Verdict: a clean pass completes the finite refutation step. Together with the stated mathematical reductions and inherited catalog/normalization premises, it establishes the current, narrowed L1 and excludes both whole frontier patterns. I found no blocking gap in that conditional implication.**

I disagree with the stronger reading that `ALL_L1_CASES_VERIFIED` alone is an end-to-end verification of those mathematical premises or the frontier reduction. Several essential steps remain written arguments or inherited results.

1. **Reader independence — note: sound, but it checks clause soundness rather than rebuilding an identical CNF.**

   `reader018.read` independently constructs the case, including its magnitude, coefficient domains and root fixings. It imports neither the producer nor its encoder. Row definitions are implemented in [reader018.py:110](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:110), with substitution at [line 185](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:185).

   For every stored row, it parses the key and reconstructs the expected row at [line 309](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:309), then requires exact coefficient and bound agreement at [line 319](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:319). Key validation begins at [line 205](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:205).

   It reads the stored CNF, maps label row IDs to the checked rows, and invokes `check_clauses` at [line 327](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:327). That checker, beginning at [line 256](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:256), establishes the direction needed here: **every satisfying assignment of the rows extends to a satisfying assignment of the accepted clauses**, interpreting auxiliary variables as partial-sum states. Missing encoding clauses only weaken the CNF.

   Finally, it checks the binary’s pinned hash at [line 328](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:328), **runs** `lrat-trim --forward --no-trim` at line 329, and requires both exit code 20 and an exact `s VERIFIED` output line at line 331. Producer statuses and saved checker logs are not evidence.

   **Verified myself:** source inspection, the checker binary’s hash, and bounded clause-extension controls. I did not run any LRAT verification.

2. **Subset soundness — note: sound.**

   If a genuine case satisfied its full necessary row system, it would satisfy every subset. Therefore an unsatisfiable subset excludes that case; neither core minimality nor the correctness of CP-SAT’s core extraction is a trusted premise.

   The seed route selects structural rows and small value rows, optionally extracts a core within them, and disables the deletion pass at [certify018.py:104](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/certify018.py:104). Those selected rows are subsequently encoded at [line 129](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/certify018.py:129).

   The reader does not trust their provenance. Each used key is reconstructed under **that certificate’s** `Q`, pair, type, magnitude, faces and branch. Flag and degree-cap rows additionally enforce their branch restrictions at [reader018.py:153](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:153) and [line 162](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:162).

   A row copied from a sibling is usable only if it is also exactly a valid substituted row of the advertised case. That is sufficient. The reader alone does not authenticate catalog metadata; assembly supplies that binding.

   **Verified myself:** all 1,437 stored rows of seed-core certificate `l1-00754s3-m1.json` matched their reconstructed definitions for all three advertised variants. This checked rows, not its proof.

3. **Variants — note: sound.**

   The primary variant must be included and duplicates are rejected. Different types may be combined only within `none/c0/c3`; `pm` and `pp` cannot substitute for one another. Each alternative magnitude/type constructs another `Case`, and **every retained substituted row must coincide**, at [reader018.py:293](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:293) and [line 311](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:311).

   Thus `(t,1)` can legitimately cover `(t′,2)` when the retained rows are insensitive to both changes. Differences in omitted rows do not matter. An unchecked variant declaration cannot earn coverage.

   Assembly uses the reader-returned variant list, including magnitude, at [read_all018.py:55](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/read_all018.py:55).

   **Verified myself:** source inspection and reconstruction of the two fixture row sets and the seed-core example. I found no incorrect cross-magnitude or cross-type transfer in this logic.

4. **Assembly — note: normalization creates harmless type collisions; no unintended current collision found.**

   `placement()` retains every field except `type`, including `part`, `root`, `order` and faces. Sorting changes representation, not vertex labels or geometry. Assembly then separately keys by verified type and magnitude. See [read_all018.py:41](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/read_all018.py:41).

   **My structural check of the actual cover found:**

   - 2,221 cases: 1,769 B-ord, 352 B-exc, 100 A.
   - 1,211 placement keys.
   - No duplicate `(placement, type)` keys.
   - Shared placement keys include constant-only types and `pm/pp`; the latter cannot share coverage because the reader forbids that variant substitution.

   Consequently, distinct cover cases do collide under `placement()` alone, but **not in a way that incorrectly transfers coverage**.

   Every cover row is required at both magnitudes by [read_all018.py:61](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/read_all018.py:61). These are exactly the magnitudes quantified over by the current [L1.md:27](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/L1.md:27). This does not establish a version allowing magnitude 3 or an incident cost-6 departure.

5. **Status logic — note for rejected certificates; should-fix for CLI behavior and stale documentation.**

   Ignoring rejected certificates in the success condition is **not a soundness defect**. Only verified results enter `ok`. If every obligation has a verified provider, an additional rejected, redundant certificate does not invalidate those proofs. Requiring zero rejected is a useful acceptance policy, and your stated hypothetical already satisfies it. See [read_all018.py:55](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/read_all018.py:55) and [line 65](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/read_all018.py:65).

   There are two operational issues:

   - `--skip-cover` is stale documentation at [line 7](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/read_all018.py:7). Cover verification is unconditional. The ad hoc argument handling at line 81 also fails to reject unsupported arguments reliably.
   - An ordinary `INCOMPLETE` result still exits successfully: `main()` returns the document, and [line 81](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/read_all018.py:81) does not translate its status into an exit code. Automation must inspect the JSON/status rather than treating exit zero as acceptance.

   Additional stale text: [certify018.py:12](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/certify018.py:12) names `reader017.py` and gives an obsolete `certify017.py --c` invocation. The exact-orbit claims in [cases018.py:19](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/cases018.py:19) remain stronger than the documented redundant cover.

   **Verified myself:** source inspection; I did not invoke the assembly CLI.

6. **Cover → L1 → whole patterns — note: mathematically sound conditional chain; should-fix: frontier “binding” is weaker than advertised.**

   `cover_reader018` verifies labelled-placement coverage relative to the supplied root catalogs: B-ord at [line 135](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/cover_reader018.py:135), B-exc at [line 147](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/cover_reader018.py:147), and A at [line 163](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/cover_reader018.py:163). Its matcher permits root-link automorphisms and permutations of non-neighbour labels.

   **It does not itself establish that every mathematical situation in L1 reaches those catalogs.** That requires the written arguments in [L1.md:44](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/L1.md:44): triangle incidence, ordinary-link classification, flagness, exceptional-endpoint classification, and the private-vertex exclusion of a doubled quartic. The A/B split and maximum-degree root choice at [L1.md:84](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/L1.md:84) also remain written reductions. Catalog completeness is inherited.

   I checked the reasoning and found no new gap. In particular, the doubled-quartic exclusion needs the degree/size argument in its cited audit: **Euler characteristic 3 alone is insufficient for a disconnected surface**. The fuller argument is present at [connected-six-unit-exclusion-audit.md:57](/home/spinoza/github/math-theory/.research/attempts/006-solver-resume/independent-math-audit/connected-six-unit-exclusion-audit.md:57).

   The counting at [L1.md:34](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/L1.md:34) is valid. With union 14 and \(N\) negative supports,
   \[
   \#\{\delta=1\}\ge 28-5N.
   \]
   For \((2^4)\), this gives at least eight such coordinates and residual 4, hence at most two cost-2 departures. Their distinct supports intersect in at most four coordinates, leaving at least four eligible for L1. For \((2^4,1)\), there are at least three degree-one coordinates and at most one departure, so each is eligible. No common-pair or other restricted support geometry is assumed.

   **The assembly’s frontier handling is only recording, not verification.** At [read_all018.py:63](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/read_all018.py:63), it selects target rows and hashes the frontier file. It neither calls `frontier_reader` nor requires exactly those two targets nor checks their union-14 authorities. It could report success with an empty `target_inventories`.

   I independently checked that the actual two entries have the correct costs/residuals, that their authority hash matches, and that the authority explicitly gives union 14 for both. Also, `frontier_reader` checks pins and basis kinds, but does not itself verify that semantic conclusion inside the authority; see [frontier_reader.py:52](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/frontier_reader.py:52).

   Therefore these are **whole-pattern exclusions in the frontier’s selfdual empty-pair representative**, conditional on the inherited results. They do not assert that selfdual normalization preserves the Fourier inventory of an arbitrary original function.

7. **Before freezing — should-fix controls and evidence binding; note: no `-O` bypass found.**

   Add assembly failure controls that remove **all verified providers of one obligation**, change a case’s root metadata, and advertise an invalid variant. Deleting an arbitrary redundant certificate need not cause failure. Existing [test_reader018.py:108](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/test_reader018.py:108) tests placement identity, not the full assembly path. These controls should use isolated inputs, leaving the running verification untouched.

   Bind the acceptance to `read_all018.py`, `cover_reader018.py`, L1, the catalog/surface dependencies, and the named normalization and union-14 authorities. The assembly receipt currently hashes `reader018.py` but omits several of those dependencies. I verified that the current catalog files and relevant lemma/surface files match their checkpoint-1533 acceptance pins.

   There is also a **file-change race**: [read_all018.py:32](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/read_all018.py:32) verifies a certificate, then rereads it at line 35 and binds that second copy’s case. If the file changes between those reads, verified evidence and credited identity can diverge. Returning the checked identity/hash from the reader, and verifying an immutable input set, would close this. This is not evidence that the present run encountered a race.

   The readers’ substantive checks use explicit exceptions, not removable assertions: [reader018.py:42](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:42), [cover_reader018.py:29](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/cover_reader018.py:29). I found no optimization-dependent bypass.

**Verification scope:** I ran 11 proof-free existing tests in both normal and `-O` modes; all passed. I additionally checked 2,380 small signed-row encodings and 7,364 satisfying-assignment extensions per mode, with 13 rejection controls; reconstructed the two fixture row sets and the seed-core example; and independently checked the ten supplied sphere entries’ topology, degrees and applicable flagness. Coverage confirmed that these tests did **not** exercise the full assembly or LRAT path.

I read the prior review and inherited arguments; I did not rerun catalog enumeration, the full cover check, `read_all018.py`, or any proof checker, and did not open `.lrat` files or write files. **Confidence is high in the audited conditional implication; inherited completeness and normalization were not independently reproved here. This is AI review, not checkpoint acceptance.**