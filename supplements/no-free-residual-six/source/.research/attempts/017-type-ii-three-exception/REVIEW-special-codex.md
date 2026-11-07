# Codex review of NEAR-FLAG.md and SPECIAL-SHAPES.md

OpenAI Codex (codex-cli 0.163.0, read-only sandbox), 2026-10-23. Verbatim
final message. Applied after it: the scope and wording fixes in both notes;
the reader validation (already added after REVIEW-chain-codex.md) rejects
its ["pair",[0,0]] input and non-four-element doubled supports;
cover_reader.py checks the root index range (regression test added).

The structural arguments and the models produced by `certify017.substituted` are **sound, conditional on the earlier lemmas and the 015 sphere enumeration**. The notes need a few scope and wording fixes. I also found a substantive reader-validation defect: malformed row keys can generate unjustified contradictions.

These conclusions establish necessary conditions and exhaustive placement covers. They do not exclude either shape.

The claims in [NEAR-FLAG.md](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/NEAR-FLAG.md:9) have the following status.

- **Scope: sound after a stated fix.** Begin the lemma with “In the pair-only setting of VERTEX-TYPES.md, outside triangle ---”. Excluding triangle --- alone does not explicitly exclude doubled-quartic shape 1. Its exceptional vertices have type `(1,0)`, but the cited sphere premise does not apply to them. The implementation correctly excludes those vertices.
- **Catalog coverage: sound conditionally.** The cited lemmas give a sphere with at most twelve vertices, exactly the specified degree-6 and degree-3 vertices, and all remaining degrees 4 or 5. The enumeration filter therefore includes every possible link. This does not assert that every catalog sphere is globally realizable.
- **Computed classification: sound.** An independent adjacency and missing-triangle calculation, without calling `near_flag.classify`, reproduced every field of `near-flag-result.json`:

| Type | Spheres | Flag | Near-flag | Orders |
|---|---:|---:|---:|---|
| `(0,0)` | 6 | 6 | 6 | 6, 7, 8, 9, 10, 12 |
| `(0,1)` | 1 | 0 | 1 | 7 |
| `(0,2)` | 3 | 0 | 3 | 5, 6, 8 |
| `(1,0)` | 3 | 3 | 3 | 9, 10, 11 |
| `(1,1)` | 2 | 0 | 2 | 8, 9 |
| `(2,0)` | 9 | 9 | 9 | 8 through 12 |

- **The inequality: sound.** If fewer than three positive terms equal one, the nonnegative subtractions suffice. Otherwise `abd` is a link cycle. If it is a face, `l_vabd=1`. Otherwise it is the neighborhood of a degree-3 vertex `y`, whose vertex link is a triangle, so `yab` is a face and `l_vyab=1`. This also justifies using the particular edge `ab` in the subtraction. Independent checks found zero violations in 31,680 ordered instances across the 24 allowed sphere classes, including absent ambient vertices.
- **Excluded types and root handling: sound.** Each of `(1,2)`, `(2,1)`, `(3,0)` has exactly one non-near-flag catalog sphere, at orders 7, 8, 9 respectively. Each admits an ordering with row value 3. Three incident exceptional edges exhaust the exceptional graph, making that vertex the unique star center; `root_of` selects it. The producer and reader reject flag rows at the root and at these types. The empty `(0,3)` catalog is correctly omitted from the usable list.

For triangle --- in [SPECIAL-SHAPES.md](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/SPECIAL-SHAPES.md:12):

- **Triangle incidence: sound.** Incidence four requires all three pair links to be bowties centered at the remaining vertex. Only `abc` can satisfy that requirement. Every other present triangle has incidence two.
- **Degree bound: sound.** Pair inversion gives
  \[
  6d-12=3P_x\ge 4d+2n(-2)-n(+1),
  \]
  hence \(d\ge6+n(-2)-n(+1)/2\). Each exceptional vertex has \(d\ge8\). This argument does not use the exceptional-link sphere classification.
- **CROSS-EDGES applicability: sound.** F1 uses that degree bound for triangle ---. F2 and F3 apply to ordinary vertices with cross degree zero or one, whose small links are spheres. There is no circular use of the excluded exceptional-link classification.
- **Ordinary root and cover: sound.** An exceptional vertex has at least six ordinary neighbors. Rooting at one gives a deltahedron link. Independent orbit enumeration reproduced **81 cases covering 1,285 distinct labelled exception sets**.
- **Encoding: sound.** The exceptional triple has
  \[
  \sum_{D\supset abc}l_D=2(t_{abc}+t2_{abc}),
  \]
  and both variables have coefficient \(+1\) in every applicable value row. No flag rows are generated or accepted at `a,b,c`.

For shape 1:

- **Pair links: sound.** A baseline pair inside \(D_0\) already carries weight two. Its remaining unit part must be an even simple graph with two or three edges, forcing a triangle, \(m=1\), and \(k=-1\). Each exceptional pair has unit weight \(4m\), hence an empty unit part or a \(C_4\).
- **Triangle incidence: sound after a wording fix.** In item 2, baseline pair links outside \(D_0\) should be described as **empty, \(C_4\), or \(C_5\)**. For a present triangle the relevant links are nonempty. The conclusion remains correct: weighted incidence is 2 or 4 inside \(D_0\), and 0 or 2 elsewhere.
- **Degree bound at \(D_0\): sound.** The two baseline pairs contribute 10. If the exceptional pair has \(m=1\), the lower bound is \(10+6+4(d-3)\). If it has \(m=0\), it is \(10+2+4(d-2)\). Both equal \(4d+4\), giving \(6d-12\ge4d+4\), hence \(d\ge8\).
- **Weighted edge count: sound.** Put \(K=\sum_Ak_A\) and \(L=\sum_Dl_D\), including the doubled weight. Then
  \[
  K+L=16-c,\qquad K+2L=52,\qquad 4E=K+6L.
  \]
  Consequently \(L=36+c\) and **\(E=49+c\)**.
- **Disconnected ordinary-link exclusion: sound.** Every \(D_0\) vertex has cross degree at least two. Ordinary vertices have cross degree at least one; cross degree one forces a cross-degree-six vertex opposite. Thus either the total cross-degree sum is at least 24, exceeding \(2M\le18\), or one side sums to at least 11, exceeding \(M\le9\). Clarify item 4’s pronoun: the ordinary vertex with cross degree one is the vertex whose link has seven vertices.
- **Root and cover: sound.** A \(D_0\) vertex has at least five ordinary neighbors. Independent enumeration reproduced **328 cases covering 8,847 distinct labelled exception sets**. Every supplied doubled quartet is exactly the union of two disjoint -2 pairs.
- **Doubled and wide-triple encoding: sound.** The doubled variable is fixed to one and carries coefficient two wherever the quartic weight occurs. Exactly the four triples inside \(D_0\) receive `t2`. Flag rows exclude every \(D_0\) vertex.

The necessary-relaxation claim for [model.py](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/model.py:34) through [certify017.substituted](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/certify017.py:39) is **sound**. Expanding the Walsh characters gives
\[
p(X)=1-|X|+\sum_{A\subseteq X}m_A
-\sum_{T\subseteq X}\tau_T+\sum_{D\subseteq X}l_D,
\]
where \(\tau_T=t_T+t2_T\) on wide triples. Thus the value rows express the required range exactly. No ordering constraint between `t` and `t2` is needed: the permitted wide values are represented by their sum, and flag rows never use those wide triples.

Fresh checks passed for one representative of each root order, in each special shape, at both constants: **24 models, 250,848 full-row comparisons and 250,536 substituted-row comparisons**. Direct Walsh evaluation agreed with the implemented row algebra in 49,152 checks. The 16-cell positive control passed all 601 rows and all 256 input values. All six existing cross-edge unit tests passed.

The reader guarantees require separate qualifications.

- **Necessary-row validation: wrong, with a reproduced malformed-input counterexample.** [reader017.py](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/reader017.py:187) accepts `["pair",[0,0]]`. For the supplied order-six root, substitution produces
  \[
  4m_{(0,0)}+\kappa_{(0,0)}=8.
  \]
  Its binary left side is at most five. These are not legitimate pair variables, yet the clause checker also accepts the corresponding empty clause. The reader therefore fails to establish its claimed necessary-row guarantee for arbitrary certificate input. Validate distinctness, cardinality, integer labels, and label range for every row-key support.
- **Shape-1 input recognition: sound after validation repair.** `Case` accepts exceptions `{1,2}`, `{2,3}` and `doubled=[[1,2,3]]`. Require a four-element doubled support and disjoint exceptional pairs. The supplied cases satisfy those conditions.
- **“Every listed case is valid”: wrong for arbitrary cover input.** [cover_reader.py](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/cover_reader.py:110) accepts a negative `root_index` during Python catalog lookup, then never checks that entry in its enumeration of nonnegative indices. Appending an invalid such case to a reduced valid cover still returned PASS. Validate the index range and catalog order. The supplied covers contain neither defect.

The mathematical notes are ready after the stated wording fixes, subject to their inherited enumeration premises. Independent certificate-based exclusions should wait for the reader validation repairs. No files were modified; the research log and active certificates were not inspected.