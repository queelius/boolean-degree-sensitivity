# Codex review of L1 and its certification chain

OpenAI Codex (codex-cli 0.163.0, read-only sandbox), 2026-10-23. Verbatim
final message. Applied after it: the scope wording (one incident cost-2
departure), Lemma 1 scope, explicit bowtie and lone-split arguments in
Lemma 5, the binding note (read_all018 compares the full case with the
cover; test added), and tests for the reader paths it listed.

**Verdict: the intended cost-2 reduction and cover are sound, conditional on the cited catalogs. L1 needs a scope correction, and the certification chain needs an explicit certificate-to-cover binding before it can support an exclusion.** I found no counterexample to the intended local mathematical arguments. The two verified fixtures do not establish all 4,442 obligations, so neither inventory should yet be marked excluded.

1. **Setting: sound.** In the stated existence-preserving selfdual representative,
   \[
   p(x)=f(x,u=1)-f(x,u=0),\qquad
   16p=k_u+\sum_A k_{uA}\chi_A+\sum_D k_{uD}\chi_D.
   \]
   Consequently \(p(0)=1\), \(p(e_v)=0\), and the ordinary quadratic coefficient is
   \[
   m_{ab}=p(e_a+e_b)-p(e_a)-p(e_b)+p(0)=f(1_{uab})\in\{0,1\}.
   \]
   Differentiation removes every Fourier term avoiding \(u\). Thus other negative quintics and residual departures avoiding \(u\) introduce no missing terms. The constant is \(k_u\), so a singleton departure at \(u\) must be counted.

   This normalization applies to the accepted representative, not automatically to every original function. [Normalization source](/home/spinoza/github/math-theory/.research/attempts/009-parent-analysis/one-free-residual-six-and-extension-audit-cycle1513.md:7)

2. **L1's stated scope: sound after narrowing it to cost-2 departures.** [L1.md:26](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/L1.md:26) says “at most one departure,” whereas the cover implements “at most one incident residual departure, of cost 2.”

   One departure could instead have cost 6: singleton numerator \(-1\) or \(4\), cubic numerator \(-3\) or \(2\), or positive quintic numerator \(3\). These are absent from the cover. The implementation therefore does not establish the broader wording. This is a proof-scope gap, not a demonstrated counterexample to the broader nonexistence statement.

   The appropriate correction is to specify **at most one incident residual departure, necessarily of cost 2 if present**. Negative quintics are charged to the negative inventory before the residual is defined.

3. **Counting reduction: sound, conditional on the inherited union-14 theorem.** For \(N\) negative supports covering all 14 coordinates,
   \[
   \#\{v:\delta(v)=1\}\ge 14-(5N-14).
   \]
   Hence there are at least eight such coordinates for \((2^4)\), and three for \((2^4,1)\).

   Their residuals are respectively \(28-4\cdot6=4\) and \(28-(4\cdot6+2)=2\). Every residual departure costs at least 2, and the next possible cost is 6. Thus the first inventory has at most two cost-2 departures; the second has at most one.

   Distinct departure supports have sizes 1, 3 or 5 and intersect in at most four coordinates. Therefore at least \(8-4=4\) of the first inventory's degree-one coordinates meet at most one departure. All three guaranteed degree-one coordinates in the second inventory do so. Singleton departures are included in this argument.

   I checked the two frontier entries and their shared union-14 authority hash. This establishes the reduction to the intended L1, not L1's computational conclusion.

4. **Lemma 1, triangle incidence: sound after making its scope explicit.** First exclude the \(+2\) quartic case using Lemma 4, or state that Lemma 1 concerns the remaining types.

   If \(T\not\subseteq Q\), at least two pairs of \(T\) are not contained in \(Q\). At most one is the exceptional pair. A remaining baseline pair sees only unit quartics and has an empty, \(C_4\), or \(C_5\) link. Its vertex degrees give incidence 0 or 2 for \(T\).

   For \(T\subset Q\),
   \[
   2t_T=-m+s,\qquad 0\le s\le9.
   \]
   Integrality gives the sharper bounds
   \[
   m=1:\quad t_T\in\{0,1,2,3,4\},\qquad
   m=2:\quad t_T\in\{-1,0,1,2,3\}.
   \]
   The stated interval \([-1,6]\) is a harmless larger domain. Its binary encoding is exact for that interval; the weighted triple equation imposes the stronger restrictions. [L1.md:40](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/L1.md:40)

5. **Lemma 2, ordinary links and weighted identities: sound.** At an ordinary vertex, no incident quartic is negative or exceptional. Every nonempty pair link is a single \(C_4\) or \(C_5\), so the unit link is a disjoint union of closed triangulated surfaces.

   The identities remain valid with signed quartic weights:
   \[
   K_v+P_v=8,\qquad 4D_v=K_v+3P_v,
   \]
   giving \(P_v=2D_v-4\). At an ordinary vertex, this is also the actual face count, so its link has Euler characteristic 2.

   Degrees 4 and 5 give positive curvature on every component. Thus the possibilities are one sphere or two projective planes. A characteristic-one component with these degrees has exactly six vertices, all of degree 5. Two such components occupy all twelve available link vertices.

   Globally, \(K+L=16-c\) and \(2K+4L=104\) give \(L=36+c\). Summing pair inversion then gives \(E=49+c\). No positivity assumption was improperly used in these global identities.

6. **Lemma 3, flag rows: sound, conditional on catalog completeness.** I independently checked the six supplied deltahedra: each is a closed surface of characteristic 2, has the required degrees, and has every graph triangle as a face.

   At an ordinary vertex outside part A, the row
   \[
   t_{vab}+t_{vbd}+t_{vad}-l_{vabd}\le2
   \]
   follows directly. The producer and reader restrict these rows appropriately. Completeness of the six-sphere list remains an inherited catalog premise. [NEAR-FLAG.md](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/NEAR-FLAG.md:30)

7. **Lemma 4, the private-vertex exclusion: sound despite the negative quartic elsewhere.** Choose \(x\in D\setminus Q\). All quadratic numerators through \(x\) are baseline, and its only non-unit incident quartic has weight \(+2\). Those are precisely the local hypotheses used by the audited argument.

   In particular, the unit link at \(x\) has exactly three degree-3 vertices, all other degrees 4 or 5, at most twelve vertices, and Euler characteristic 3. Characteristic 3 alone would not be a contradiction for a disconnected surface. The degree and size restrictions complete the obstruction: a sphere plus a six-vertex projective plane would force the sphere's degree sequence to be either \((3,3,3,4,5)\) or \((3,3,3,5,5,5)\), both impossible.

   The audit explicitly states that no restrictions on coefficients avoiding \(x\) are needed. The negative quartic \(Q\) therefore causes no gap. [Audited local argument](/home/spinoza/github/math-theory/.research/attempts/006-solver-resume/independent-math-audit/connected-six-unit-exclusion-audit.md:27)

8. **Lemma 5, exceptional endpoint classification: sound; the bowtie exclusion should be written explicitly.** For an exceptional pair \(xy\) with \(x\notin Q\), every quartic through \(x\) is unit.

   A bowtie link of \(xy\), centred at \(z\), would put four tetrahedra through \(xyz\). But \(xz\) is baseline, avoids the negative quartic, and has a cycle link, giving incidence at most two. Hence no bowtie occurs.

   A lone split partner is also impossible locally. Splitting it produces characteristic 3 on at most thirteen vertices. Both degree-3 copies must lie in the sphere component; their disjoint neighbourhoods require at least eight vertices there. Adding the six-vertex projective-plane component requires at least fourteen.

   The remaining links fall under the cited local classification: the three \((1,0)\) spheres of orders 9, 10 and 11, or the \((0,1)\) sphere of order 7. I checked the supplied entries' surface and degree properties. [VERTEX-TYPES Lemma 2](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/VERTEX-TYPES.md:33)

9. **Cover completeness: sound for the intended types.** There is always an ordinary vertex: \(Q\) and a departure pair occupy at most six of the thirteen coordinates.

   Part A covers any derivative with a disconnected ordinary link. Otherwise all ordinary links are deltahedra. B-ord chooses an ordinary vertex of maximum ordinary degree, making every listed `degcap` row necessary. B-exc chooses an exceptional endpoint outside \(Q\), with the partner at the unique special-degree link vertex. Both possible intersections with \(Q\) are included.

   I verified all **113,355 labelled placements** across 47 groups. The saved cover has 100 A cases, 1,769 B-ord cases and 352 B-exc cases. Regenerating `cases018.cover()` in memory reproduced it exactly.

   **The stronger claim of one representative per full orbit is wrong, with a concrete counterexample.** For B-ord root index 0, type `pm`, and \(Q=\{7,8,9,10\}\), all six two-element subsets of \(Q\) appear as departure pairs. Permuting these non-neighbour labels identifies them. There are 154 redundant representatives overall. This affects efficiency, not completeness. [Non-neighbour normalization](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/cases018.py:59)

10. **Model rows: sound.** The negative weight, shifted triple encoding, constant intervals, root fixings, flag rows, degree caps and implied rows have the correct signs and bounds.

    With
    \[
    p(X)=1-|X|+\sum_{A\subseteq X}m_A-\sum_{T\subseteq X}t_T+
    \sum_{D\subseteq X}l_D,
    \]
    the value rows express exactly \(-1\le p(X)\le1\). Integral coefficients make this the required ternary range. The constant interval correctly represents \(c\in\{1,2\}\), or exactly 0 or 3 for the singleton-departure types.

    The full algebraic model describes the specified local polynomial conditions. Its structural rows are justified within their cover branches. These remain **necessary conditions for a global Boolean function**; feasibility would not establish a compatible global extension.

    I compared 33,776 producer and reader rows across 24 representative part/type/magnitude combinations, including all structural rows and Q-containing value rows of each size from 4 through 13. Every comparison matched. [Model](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/model018.py:30)

11. **Producer, independent reader and variants: sound for the stored case's row-infeasibility claim.** Core extraction and deletion may retain a subset of necessary rows. Proving that subset infeasible suffices. Solver statuses alone do not suffice.

    The reader reconstructs rows by name, recomputes substitutions, checks the CNF clauses, and invokes the pinned LRAT checker. Clause checking has the needed direction: any assignment satisfying the rows extends to the accepted clauses by interpreting auxiliary labels as partial-sum states. Missing clauses weaken the encoding and cannot create a false exclusion.

    Variant reuse is sound because every stored substituted row must coincide for every claimed variant. Differences in omitted rows are irrelevant. The `cap-1` fixture legitimately supports all six combinations of constant-only type and magnitude; the A fixture rejects the other magnitude. I found no row or variant mutation that forged the checked infeasibility claim. [Variant verification](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:290)

12. **Certificate identity and final acceptance: sound after adding an explicit binding check.** A malicious certificate can pass with false catalog metadata. I changed `cap-1.json` in memory to
    ```python
    case["root"] = {"kind": "forged-catalog", "index": 999999}
    case["order"] = 1
    ```
    and the reader still returned `CASE_ROWS_INFEASIBLE_VERIFIED`. It derives the operative order from the unchanged faces and does not authenticate those metadata fields.

    This does **not** certify satisfiable rebuilt rows as infeasible. It demonstrates that the reader does not establish which advertised cover entry was proved.

    Final acceptance must compare each certificate's full case identity against the checked cover, validate its variants through the reader, and establish coverage of every required case/magnitude pair. `run018.py` trusts producer status records for scheduling and skipping work; it is not that acceptance checker. [Reader case construction](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/reader018.py:57), [scheduler](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/run018.py:49)

Verification performed:

- All 14 existing tests passed normally and under `-O`. Temporary certificate writes were replaced by in-memory input.
- Both fixture CNF/LRAT pairs verified.
- All five saved positive-control derivatives passed independent Fourier evaluation and coefficient-domain checks.
- The ten required sphere entries passed topology, degree and applicable flag checks.
- 5,824 small signed-row encodings passed clause checking; all 23,168 satisfying-assignment extensions satisfied their CNFs.
- The stock cover matcher was interrupted in part A after about fourteen minutes. The original reader then completed with an equivalent in-memory orbit-expansion matcher, returning `L1_COVER_READER_PASS`.
- Existing-test coverage was 96% for `model018.py` and 85% for `reader018.py`, including branch coverage. Permanent tests should cover the missing constant, vertex and `implied_P` reader paths, B-ord degree-cap construction, and certificate-to-cover identity checks.

No files were written. Neither `certs/` nor `../../log.md` was inspected. **The exclusion claim remains pending complete, independently bound certificate verification.**