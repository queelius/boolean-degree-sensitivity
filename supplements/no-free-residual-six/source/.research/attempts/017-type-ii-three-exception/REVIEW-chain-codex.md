# Codex review of the certification chain

OpenAI Codex (codex-cli 0.163.0, read-only sandbox), 2026-10-23. Verbatim
final message. Fixes applied after it: strict schema validation of row
keys, variable names and case data in reader017.py (its vertex-13 forgery
and others are regression tests in test_reader017.py); run_cover.py
schedules every missing (case, constant) obligation; read_all.py runs
cover_reader on all three covers and binds the covered shapes to the 24
OPEN rows of the frozen 1532 frontier.

**Verdict: the mathematical reduction and supplied cover are sound under the stated premises, but acceptance by the current reader is not sufficient.** I reproduced a certificate that invents vertex 13, obtains the false “necessary row” \(0=8\), and passes the actual pinned LRAT checker. This is a counterexample to verifier soundness, not a constructed ternary derivative.

The files changed during review. I rechecked the exploit against `reader017.py` SHA-256 `2704a4fa64387611459ffbb874dffddea8be09c18722b73585b7777860b63d4e`.

- **1. Model rows: sound.**

  Write \(x_S=\prod_{v\in S}x_v\), \(L_S=\sum_{D\supseteq S}l_D\), \(P_v=L_{\{v\}}\), \(K_v=\sum_{A\ni v}k_A\), \(K=\sum_Ak_A\), and \(L=\sum_Dl_D\). Expanding \(\chi_S(x)=\prod_{v\in S}(1-2x_v)\) gives
  \[
  p(x)=\frac{c+K+L}{16}
  -\frac18\sum_v(K_v+P_v)x_v
  +\frac14\sum_A(k_A+L_A)x_A
  -\frac12\sum_TL_Tx_T
  +\sum_Dl_Dx_D.
  \]

  Therefore the necessary equations are exactly
  \[
  K+L=16-c,\qquad K_v+P_v=8,\qquad
  4m_A=k_A+L_A,\qquad 2t_T=L_T.
  \]
  The vertex equation uses both \(p(0)=1\) and \(p(e_v)=0\). Binary \(t_T\) is justified by the triangle-incidence lemma outside triangle `---`.

  Consequently
  \[
  p(1_X)=1-|X|+\sum_{A\subseteq X}m_A
  -\sum_{T\subseteq X}t_T+\sum_{D\subseteq X}l_D,
  \]
  so ternarity gives precisely the implemented value bounds. The empty and singleton supports are already handled.

  For the implied rows, put \(D_v=\sum_{A\ni v}m_A\). Summing incident pair equations yields
  \[
  4D_v=K_v+3P_v.
  \]
  Together with \(K_v+P_v=8\), this gives
  \[
  P_v=2D_v-4,\qquad K_v=12-2D_v.
  \]
  The stated totals also follow: \(L=36+c\), \(E=49+c\), and \(T=72+2c\).

  The signs and exceptional constant shifts in [model.py](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/model.py:64) agree with these equations. These are necessary conditions sufficient for an exclusion argument; no converse assertion about integrating \(p\) into a globally admissible \(f\) is needed.

- **2. Near-flag rows and scope: sound, conditional on the stated enumeration premise.**

  The allowed types are exactly
  \[
  (0,0),(0,1),(0,2),(1,0),(1,1),(2,0).
  \]
  I regenerated the sphere enumeration through order 12 and reproduced the stored near-flag counts.

  If fewer than three of \(t_{vab},t_{vbd},t_{vad}\) equal one, the upper bound is automatic. Otherwise \(abd\) is a link 3-cycle. It is either a face, giving \(l_{vabd}=1\), or the neighbourhood of a degree-3 vertex \(y\), giving \(l_{vyab}=1\). Such a \(y\) is a +1 partner outside \(abd\). Hence
  \[
  t_{vab}+t_{vbd}+t_{vad}-l_{vabd}
  -\sum_{\substack{y\text{ a +1 partner}\\y\notin\{a,b,d\}}}l_{vyab}\le2.
  \]
  The +1 correction terms are essential. The implemented lower bound is weaker than the trivial Boolean lower bound and adds no restriction.

  All non-root vertices in this cover meet at most two exceptions. The types with three partners occur at star centres, which are chosen as roots. Excluding the root is sound: its link is fixed directly, and some possible star-centre links are not near-flag. Omitting root flag rows loses no necessary coverage.

- **3. Root fixing: sound for the actual cover cases.**

  Relabel the chosen abstract root as 0, identify its link with a catalog representative on \(1,\ldots,|L|\), and label its non-neighbours above \(|L|\). This is a coordinate permutation.

  The -2 partners must occupy exactly the degree-6 link vertices; the +1 partners occupy exactly the degree-3 vertices. All other exceptional vertices may occupy distinct degree-4/5 link vertices or non-neighbours.

  Thus
  \[
  m_{0v}=[v\in L],\qquad l_{\{0\}\cup F}=[F\text{ is a link face}]
  \]
  are justified fixings. I found no additional adjacency assumption in [root_fixings](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/model.py:127).

  This conclusion requires the certificate’s complete case data, including its faces, to match the covered case. Matching only exception pairs, root index, or displayed summary fields is insufficient.

- **4. Reader: wrong as an adversarial verifier, with a concrete counterexample.**

  [The vertex-row implementation](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/reader017.py:128) does not validate the vertex domain, and [parse_key](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/reader017.py:187) accepts `["vertex",13]`.

  Keep the fixture’s legitimate case, use `variables: []`, `constants: [1,2]`, and this sole row:
  ```json
  {"id":0,"key":["vertex",13],"terms":[],"lo":8,"hi":8}
  ```
  Supply labels `[]`, an empty LRAT proof, correct hashes, and:
  ```text
  p cnf 0 1
  0
  ```

  Since no actual pair or quartic contains 13, reconstruction produces \(0=8\). The clause checker accepts the empty clause because that reconstructed row is impossible. The pinned LRAT checker correctly verifies the already contradictory CNF.

  The actual result was:
  ```text
  constants: [1, 2]
  clause_soundness: PASS
  lrat_trim_exit: 20
  verdict: CASE_ROWS_INFEASIBLE_VERIFIED
  ```
  I redirected input bytes in memory; the mathematical checks, hashes, and actual proof checker were executed. `["implied_P",13]` and `["implied_k",13]` similarly manufacture \(0=-4\) and \(0=12\).

  **Required fix:** validate every row-key schema before reconstruction: integer vertices in `0..12`, correct cardinalities, distinct vertices, and appropriate key arity. Apply corresponding validation to semantic variable names and case data. Add adversarial regression tests, including optimized Python execution.

  For well-formed keys, the substantive checks are sound:
  
  - Row definitions are independently implemented and agree with the derivation.
  - Substitution correctly removes fixed terms and subtracts their contribution from both bounds.
  - The constants-list check reconstructs every row at every claimed constant. A constant-dependent row cannot support `[1,2]`.
  - Clause soundness has the correct implication direction. Given a satisfying base assignment, set each auxiliary label true exactly when its indicated prefix sum is attained. Every accepted root, transition, and dead-end clause holds. Missing clauses only weaken the CNF.

  Thus the demonstrated failure is in admitting a non-necessary row, rather than in the decision-diagram clause argument.

- **5. Cover completeness: sound for the supplied files, conditional on the catalog premise.**

  Independent enumeration of signed three-edge simple graphs gave 24 classes. The supplied 22 omit exactly star `+++`, already excluded before this cover, and triangle `---`.

  I verified:
  
  - Exact regeneration of `cover-cases.json`: 22 shapes and 2,775 cases.
  - Exact regeneration of `roots-catalog.json`.
  - Valid sphere structure and labels for all 37 catalog entries.
  - Agreement between both automorphism implementations on every entry.
  - A passing exhaustive placement check by `cover_reader.py`.
  - Rejection after deleting a required root case.

  Root choice is legitimate, partner assignments enumerate all required bijections, and remaining vertices receive all allowed injective placements. Both reductions apply genuine coordinate permutations. Every accepted link automorphism is checked on the full face set.

  There is a qualification to [cover_reader.py](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/cover_reader.py:84): it checks completeness relative to the supplied shape list and catalog. It does not itself establish that those inputs contain the required universe. For example, `{"shapes":[]}` passes vacuously. The current inputs passed the additional checks above; a final verification procedure should explicitly bind them to the reviewed universe and catalog.

- **6. End-to-end exclusion: sound after the reader fix and explicit coverage requirements.**

  The sufficient antecedent must be:

  For every covered case and every \(c\in\{1,2\}\), an exactly matching certificate passes the hardened reader and includes \(c\) in its verified constants list.

  “Each case has a verified certificate” alone permits certificates covering only one constant.

  There is also a concrete restart bug in [run_cover.py](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/run_cover.py:49). If c = 1 was completed with `constants:[1]`, but c = 2 was interrupted or failed, restarting schedules neither: initial jobs include only missing c = 1 cases, and c = 2 is scheduled only after a newly completed c = 1 job. Schedule missing case-constant obligations explicitly.

  Producer status strings and CP-SAT infeasibility reports do not replace independent row validation, LRAT verification, exact case binding, and complete constant coverage. Existing artifacts can be reused once those strengthened checks pass.

The supplied fixture verifies, and all 10 existing tests passed normally and under `-O`, with their temporary-file helper replaced by in-memory input. The latest measured reader coverage was 83%; the malformed-domain counterexample remains untested by that suite. Additional checks passed for the 16-cell positive control, ordinary-expansion identities, 89,776 row comparisons, and 5,824 small CNF encodings.

I did not establish completion of the certificate collection or any unconditional exclusion. No files were written, and neither `certs/` nor `../../log.md` was used as evidence.