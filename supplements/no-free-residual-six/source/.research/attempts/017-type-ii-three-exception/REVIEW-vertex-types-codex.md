# Codex review of VERTEX-TYPES.md

OpenAI Codex (codex-cli 0.163.0, read-only sandbox), 2026-10-23, on the
version before the fixes it lists were applied. Verbatim final message.

**Verdict: sound as a necessary local reduction, with scope and wording fixes.** I found no bug that wrongly empties a supported vertex type. The saved root catalog is exact: 37 distinct sphere classes, with all requested control counts matching.

I formed my assessment before reading the previous review. All checks were read-only.

1. **Lemma 1: sound.**

   In [Lemma 1](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/VERTEX-TYPES.md:24), tetrahedra containing \(aby\) correspond exactly to edges incident to \(y\) in \(\operatorname{link}(ab)\). The same incidence is read at \(b\) in \(\operatorname{link}(ay)\) and at \(a\) in \(\operatorname{link}(by)\).

   Among the permitted pair links, degree four occurs only at a bowtie centre. Thus incidence four forces all three pairs to be \(-2\), with mutually centred bowties. With exactly three exceptional pairs, this forces the all-negative triangle shape.

   This is a necessary implication. An all-negative exceptional triangle does not itself force bowties. Outside that shape, every triangle contained in a tetrahedron has incidence exactly two.

2. **Lemma 2 setup and bounds: sound. Its scope and table wording need clarification.**

   The identities give
   \[
   A_x+P_x=8,\qquad 4d=A_x+3P_x,
   \]
   hence \(P_x=2d-4\). Every partner has a nonempty pair link, while nonpartners have empty links. Therefore the original vertex link has exactly \(d\le12\) vertices, \(F=P_x\), and \(E=3F/2\). Its Euler characteristic is two.

   Splitting a partner preserves edges and faces. The two faces incident to an edge through that partner belong to the same triangle of its \(2C_3\) link, so they consistently move to one copy. This remains valid when adjacent partners are also split. Consequently
   \[
   V=d+s,\qquad \chi=2+s.
   \]

   The stated degrees and copy constraints are necessary. Every component has at least four vertices and there are at most three degree-6 vertices globally. Thus each component has positive curvature:
   \[
   6\chi=\sum_v(6-\deg v)>0.
   \]
   It is therefore a sphere or projective plane.

   The sphere cutoff is correct, but the merge-budget argument is essential:
   \[
   n=12-2n_3-n_4+n_6,\qquad
   d\ge n-\lfloor n_3/2\rfloor.
   \]
   If \(n\ge13\), then \(n_6\le3\) forces \(n_3\le1\). No pair can merge within that component, so it already represents at least thirteen original partners, contradicting \(d\le12\). Copies paired with vertices in other components do not reduce this component's number of distinct originals.

   For a projective plane,
   \[
   n=6-2n_3-n_4+n_6\le9.
   \]
   Its minimum order is six, from \(E=3(n-1)\le\binom n2\).

   Two wording fixes are warranted:

   - “An unsplit vertex link is always a single sphere” must explicitly concern an **exceptional vertex**. The classification omits type \((0,0,0)\).
   - The split rows should list allowable order pairs. For \((0,2,0)\), these are \((5,5),(5,6),(5,8),(6,6),(6,8)\). For \((1,2,0)\), they are \((5,7),(5,8),(6,7),(6,8)\). In particular, \((8,8)\) violates the merged budget.

3. **Classification code: sound for the stated necessary-condition problem; no false-emptiness bug found.**

   In [vertex_types.py](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/vertex_types.py:49):

   - The degree filters and bounds \(n_6\le3,\ n_3\le6\) are necessary.
   - `max_internal_pairs` correctly computes a maximum matching. Every smaller matching size is obtainable by taking a subset.
   - After internal pairing, external copies can be paired across components exactly when no component supplies more than half the external copies.
   - The component-count bound follows from positive Euler characteristic.
   - `sum(n)-s <= 12` is the correct global budget.

   I compared `realizable` with an explicit matching oracle on 2,933 cases; all agreed.

   There is a missing condition if “consistent assignment” means a fully valid simultaneous quotient: disjoint neighbourhoods before merging need not remain disjoint after other copy pairs merge. This weakens the search and can admit false positives; it cannot cause false emptiness. I checked the stronger merged-neighbour and edge-preservation conditions on every surviving split candidate. Every listed order pair retained valid witnesses.

   Two output conventions should be documented:

   - `configurations` counts combinations of **component signatures**, not isomorphism classes. Thus \((2,0,0)\) reports five configurations, whereas its root catalog correctly contains nine sphere classes.
   - `only_single_sphere=True` for an empty row is vacuous. Existence must be read from `configurations` or `component_patterns`.

4. **Completeness of `surfaces.brute`: sound up to isomorphism.**

   The search in [surfaces.py](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/surfaces.py:103) has a complete target-following argument.

   Fix any connected closed triangulated surface and label one face \(012\). At every stage, the least open edge has a unique missing incident face in the target. Its third vertex is either already labelled or receives the next unused label, both of which the search tries.

   Neither pruning rule rejects this branch. Target edges have incidence at most two, and a partial vertex link is a subgraph of the target cycle, hence paths or the complete cycle. A proper subset of the target's faces cannot have no open edge, because the target's face-adjacency graph is connected.

   The coloured vertex-face incidence certificate distinguishes simplicial complexes up to isomorphism. The restricted labelling scheme need not generate every labelling; it generates every required isomorphism class.

   Fresh tests confirmed agreement between brute and split enumeration for projective planes through order nine, with counts \(1,3,16,134\), and between brute and sphere enumeration through order nine. The brute completeness argument does not depend on the projective-plane irreducibility theorem.

5. **Corollary: sound. The stronger statement in PLAN.md needs correction.**

   Splitness belongs to the pair itself, so it agrees at both endpoints. Every nonisolated vertex of the split-pair graph \(H\) has degree two. A nonempty simple graph with this property and at most three edges is a triangle. Its edges are all \(-2\), forcing precisely the excluded exceptional graph.

   There is also a direct mathematical check of the crucial restrictions, independent of the catalogs:

   - For \(s=1\), total characteristic three and the vertex budget force one sphere and one projective plane. With at most two degree-6 vertices, a projective-plane component cannot contain a degree-3 vertex. Both copies therefore lie in the sphere, requiring at least eight vertices because their neighbourhoods are disjoint. Adding the projective plane requires at least fourteen vertices, exceeding \(d+s\le13\).
   - For \(s=3\), there are six degree-3 copies and no degree-6 vertices. The budget and total characteristic five force two spheres and one projective plane. All copies lie on the spheres. A sphere with degrees in \(\{3,4,5\}\) has at most four degree-3 vertices, and cannot have exactly three: curvature leaves only the impossible sequences \((3,3,3,4,5)\) and \((3,3,3,5,5,5)\). The latter forces nine faces although \(F=8\). Thus the copies distribute as four and two; the four form a tetrahedron boundary and cannot pair internally, leaving too few external partners.

   Once \(s=0\), an exceptional link is a sphere without further enumeration: two projective planes would require all twelve available vertices and both would be six-vertex, degree-5 triangulations, leaving no exceptional link degree.

   However, [PLAN.md](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/PLAN.md:82) says “every vertex link a sphere.” Replace this with **“every exceptional vertex link a sphere.”** Two disjoint six-vertex projective planes satisfy the ordinary local degree, Euler, and budget conditions. This is a counterexample to that inference from the local conditions, not a construction of a globally admissible derivative.

6. **Root catalog: sound and complete for the specified degree filters.**

   I regenerated [roots.py](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/roots.py:19) in memory and obtained exact structural equality with [roots-catalog.json](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/roots-catalog.json). I additionally checked incidence, connectivity, cyclic vertex links, Euler characteristic, labels, degrees, and absence of duplicate isomorphism classes.

   Here the type is \((c6,p)\), with no split partners:

   | Type | Classes | Order: number of classes |
   |---|---:|---|
   | \((0,1)\) | 1 | 7: 1 |
   | \((0,2)\) | 3 | 5: 1, 6: 1, 8: 1 |
   | \((0,3)\) | 0 | None |
   | \((1,0)\) | 3 | 9: 1, 10: 1, 11: 1 |
   | \((1,1)\) | 2 | 8: 1, 9: 1 |
   | \((1,2)\) | 2 | 7: 1, 8: 1 |
   | \((2,0)\) | 9 | 8: 1, 9: 1, 10: 3, 11: 2, 12: 2 |
   | \((2,1)\) | 6 | 8: 1, 9: 1, 10: 3, 11: 1 |
   | \((3,0)\) | 11 | 9: 1, 10: 1, 11: 4, 12: 5 |

   All four requested accepted controls match exactly. These are complete **unmarked sphere candidates**. Assignments of exceptional partners, remaining exceptional pairs, and global extension constraints still require their own coverage.

My conclusions agree with the [previous review](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/REVIEW-vertex-types.md) on the core mathematics, enumeration, and copy-condition qualification. Its triangle-incidence and sphere-bound wording fixes are already incorporated. Its request to list the split order pairs explicitly remains applicable. I also reproduced the limited cross-degree calculation: nineteen bounds exceed eighteen, while the four all-positive cases equal eighteen. This excludes only the stated cross-degree subcase.

All seven existing tests passed normally and under `-O`. Coverage, measured entirely in memory with branch measurement enabled, was 97% for `surfaces.py`, 85% for `vertex_types.py`, and 93% for `spheres.py`. The existing suite does not test `roots.py` or saved-catalog equality; durable regression tests should include that equality, duplicate detection, and the nine-class two-negative control.

The empty rows support local exclusions. Nonempty rows establish candidates, not realizable derivatives. Ordinary disconnected links and the all-negative triangle remain outside the corollary's conclusion.