# Codex review of CROSS-EDGES.md

OpenAI Codex (codex-cli 0.163.0, read-only sandbox), 2026-10-23, on the
version before the fixes below were applied. Verbatim final message.

**Verdict: sound after the stated fixes.** The conditional conclusion survives independent checking: none of the 46 shape-constant cases admits the stated necessary cross-degree conditions. I found one real implementation bug, masked by the supplied JSON, and two proof details that should be explicit.

| Claim | Verdict |
|---|---|
| Disconnected ordinary link, 42 forced edges, degree and cross-sum identities | Sound |
| F1, including triangle --- | Sound |
| F2 | Sound after explicitly establishing its sphere premise |
| F3 | Sound after explicitly establishing its sphere premise and choosing an ear away from the chord endpoints |
| Enumeration of 23 open signed shapes | Sound |
| Search constraints with the supplied JSON | Sound |
| Triangle --- branch implements a catalog-independent bound | Wrong with a counterexample; currently masked |
| Reported controls | Sound |
| Exclusion of disconnected ordinary links | Sound after the stated fixes, conditional on the upstream classification |

**The implementation bug.** In [step4_count.py:60](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/step4_count.py:60), the triangle exception tests:

```python
signs == ('-', '-', '-')
```

But `main()` and the test helper pass `sg`, the string `"---"`, rather than `sn`, the tuple. Consequently, their triangle --- searches take the catalog branch instead of the intended topology-independent branch.

I reproduced the distinction:

| Input `orders` | String `"---"` gives | Tuple `('-', '-', '-')` gives |
|---|---|---|
| Supplied JSON | `[2, 3, 4, 5, 6]` | `[2, 3, 4, 5, 6]` |
| `{(2, 0): [9]}` | `[3]` | `[2, 3, 4, 5, 6]` |
| `{}` | `[]` | `[2, 3, 4, 5, 6]` |

Thus the claim that this branch independently implements only \(D_v\geq8\) is false as implemented. The current result remains valid because the supplied `(2,0)` row happens to contain every order from 8 through 12.

Fix: use tuple signs consistently, keeping `sg` only for display, and add a regression verifying that triangle --- options remain `2..6` with an empty catalog. No files were changed during this review.

**The setting is sound.** An ordinary link is a union of closed triangulated surfaces, with total Euler characteristic 2 and degrees 4 or 5. Every component has positive curvature, so it is a sphere or projective plane. Disconnectedness therefore means two projective planes. Each requires at least six vertices; the twelve-vertex budget forces two six-vertex triangulations, each with skeleton \(K_6\).

Consequently:

- The forced skeleton edges number \(15+15+12=42\).
- Every remaining edge joins \(A\) to \(B\), giving \(M=(49+c)-42=7+c\).
- Every \(v\in A\) has exactly its five side-mates, \(w\), and its cross neighbours, so \(D_v=6+\operatorname{cross}(v)\).
- Each cross edge contributes once to each side sum.
- The link of \(vw\) is a \(C_5\) on \(A\setminus\{v\}\). Thus \(w\) has degree 5 in \(L_v\), adjacent precisely to those five vertices. This is a statement about adjacency in \(L_v\), not merely the ambient skeleton.

**F1 is sound without assuming spherical exceptional links in triangle ---.** Pair inversion and the tetrahedron count give

\[
6d-12=3P_v
      =4d+n_{-1}+2n_{-2}-n_{+1}.
\]

Hence

\[
d\geq6+n_{-2}-n_{+1}/2.
\]

At a triangle --- vertex, \(n_{-2}=2\) and \(n_{+1}=0\), so \(d\geq8\), independently of splits or bowties.

**The sphere premise for F2 and F3 is available, but should be stated.** Insert the following justification before [F2](/home/spinoza/github/math-theory/.research/attempts/017-type-ii-three-exception/CROSS-EDGES.md:38):

- An ordinary vertex with cross degree 0 or 1 has a link on 6 or 7 vertices. Its disconnected alternative requires twelve vertices, so its link is a sphere.
- An exceptional vertex outside triangle --- has a sphere link by VERTEX-TYPES.md.
- An exceptional vertex in triangle --- has cross degree at least 2 by F1.

This removes the apparent circularity. Neither argument needs a sphere assumption at a triangle --- exceptional vertex.

For **F2**, the complementary disk is a pentagon without interior vertices. Every triangulation has boundary degrees \(2,2,3,3,4\). Restoring \(w\) gives the full link degree sequence

\[
3,3,4,4,5,5.
\]

Exactly two partners are therefore \(+1\), both on \(v\)'s side, and there is no \(-2\) partner. In particular, an ordinary vertex cannot have cross degree 0.

For **F3**, the chord argument works, with one necessary explanatory sentence:

> Choose an ear whose tip is not an endpoint of the separating chord.

Such an ear exists. For a triangular region, take its third vertex. For a larger triangulated polygon, two ears can be chosen nonadjacent, whereas the chord endpoints are adjacent. The chosen tip has degree 2 in the whole complementary disk: it cannot have edges crossing the separating chord. Restoring \(w\) makes its degree 3 in \(L_v\), giving a same-side \(+1\) partner.

If there is no chord, every boundary edge must have its incident disk triangle through \(z\), so \(z\) meets all five boundary vertices. Together with \(vz\), these give \(\operatorname{cross}(z)=6\).

I independently enumerated the relevant disks with fixed pentagonal boundary:

- No interior vertex: 5 triangulations, all with the asserted F2 degrees.
- One interior vertex: 21 triangulations. Exactly one has all five spokes; every other triangulation has a boundary degree-3 vertex after restoring \(w\). All 35 applicable chord-side ear checks passed.

**The remaining search logic is sound.**

- Side capacities and ordinary-vertex counts are correct. Since there are at most six exceptional vertices, the `>6` rejection is actually unreachable for these inputs.
- The F2 partner test is correct: after checking type `(0,2)`, all incident exceptional partners are precisely the two \(+1\) partners.
- `plus_same` selects the other endpoint correctly. An independent adjacency-set calculation agreed in all 3,168 vertex-side cases.
- Ordinary multisets lose no relevant information because the imposed conditions are invariant under permutations of ordinary vertices within a side. I checked equivalence with sorted labelled assignments for sizes 0 through 6, including the empty multiset.
- The universal requirement is only an existence condition on the opposite side. Multiple forcing vertices may share one universal neighbour, so combining their requirements with Boolean OR is valid.
- The supplied unsplit catalog patterns are all single spheres, making the current `cf[0][1]` extraction valid. An explicit schema assertion would protect this assumption.

The search intentionally omits additional necessary conditions, including full bipartite graphicality and some forced exceptional adjacencies. Those omissions weaken the model and therefore cannot create a false exclusion.

**Independent reproduction and controls.** I implemented a separate stdin-only search using per-side dynamic programming over the degree sum, presence of degree 6, and requirement for an opposite degree-6 vertex. It did not reuse the production feasibility routine or option extraction.

Separately enumerating all 496 labelled signed three-edge graphs without isolated vertices produced 24 isomorphism classes. Removing the previously excluded star +++ leaves:

| Triangle | Star | P4 | P3+K2 | 3K2 |
|---|---|---|---|---|
| 4 | 3 | 6 | 6 | 4 |

The independent outcomes agree with production:

| Conditions | Surviving shape-constant pairs |
|---|---|
| All stated conditions | 0 |
| Remove F3 | 32 |
| Remove the F2 side rule | Only P4 +++, \(c=2\) |
| Larger-budget control, 3K2 +++, \(c=5\) | Survives |

The F2 control has both side multisets `[0,1,2,2,2,2]`. Its two zero-degree internal path vertices lie on opposite sides despite their exceptional edge. It is a witness for the relaxed numerical model, not a realizable configuration. Likewise, the other controls demonstrate search sensitivity, not existence of underlying functions.

All five supplied tests passed normally and under `-O`. In-memory statement/branch coverage reported 85%, notably missing the intended triangle branch. A separate entry-point check verified valid JSON containing 23 shapes, 46 distinct rows, and no survivors.

The resulting exclusion concerns **disconnected ordinary links only**. It excludes no entire shape or original magnitude pattern. Exceptional links in triangle --- remain outside the sphere conclusion, and the doubled-quartic shape remains outside this argument. The upstream surface catalogs were treated as premises, not regenerated.