# A unique degree-three vertex forces the seven-vertex link

Alexander Richard Towell, with substantial OpenAI Codex assistance. The parent researcher identified the stronger classification consequence in Frick's primary source and proposed the elementary proof below. This producer independently audits and writes it. No target enumeration, solver, native row, ledger edit or original-pattern exclusion occurs.

## Exact elementary theorem

Let L be a finite simplicial2-sphere with exactly one vertex of degree3 and every other vertex of degree4 or5. Then L is the octahedral sphere with one face stellarly subdivided. In particular L has seven vertices; the unique degree3 vertex has three degree5 neighbors, and the remaining three vertices have degree4.

No flagness or symmetry hypothesis is imposed. The theorem follows from the elementary induction and patch lemma below; the complete small-surface catalog is not a premise of this proof.

## 1. Two local facts, with their small-order guards

In a simplicial2-sphere, two adjacent degree3 vertices force the whole sphere to be the tetrahedral boundary. If their names are u,v, the two triangles through uv have other vertices x,y. The degree3 link circles of u and v then supply the other two triangles uxy and vxy. The four triangles form a nonzero mod2 top-cycle, so they are all faces of the connected2-sphere. In particular, on more than four vertices adjacent degree3 vertices are impossible.

Likewise, a degree3 vertex v has a triangular link A which is not already a face unless the whole sphere is the four-vertex tetrahedral boundary. The cone from v and that face would form the same top-cycle. Removing v and its three incident faces and inserting the absent face A therefore gives a genuine sphere on one fewer vertex; degrees decrease by1 exactly at the three A vertices. This is the ordinary inverse face subdivision, with no duplicate face.

## 2. The all-degree-four face patch

**Patch lemma.** A2-sphere all of whose vertex degrees are4/5 and which contains a face abc of three degree4 vertices is the octahedron.

Let abx,bcy,caz be the other faces through the three edges of abc. The outside vertices x,y,z are distinct and avoid a,b,c. For example, if x=y, the vertex link of b would contain the full triangular circle on a,c,x and would have order3, contradicting d(b)=4. The other possible coincidences are excluded in the same way.

The four-neighbor link circle at a supplies axz, the corresponding circle at b supplies bxy, and the one at c supplies cyz. These seven faces form the octahedral sphere with the face xyz deleted: a disk with boundary xyz. Its six vertices and12 edges can be read directly. Every outer vertex x,y,z already has four distinct neighbors in this patch. Its degree in the whole sphere is at most5, so it has at most one neighbor in the complementary disk's interior.

The complementary disk has boundary xyz. Write m for its number of interior vertices, E_bi for boundary-to-interior edges, and E_ii for edges between interior vertices. Then

    E_bi <= 3,       E_ii + E_bi = 3m.          (1)

The equality is the Euler/triangle-incidence count for a triangulated disk with three boundary vertices: it has3m+3 edges, including its three boundary edges. Every interior vertex retains its whole-sphere degree at least4.

If m=1, (1) forces its degree3, contradiction. If m=2, the simple interior graph has at most one edge, so E_bi>=5, contradiction. If m>=3, planarity of that simple graph gives E_ii<=3m-6 and hence E_bi>=6, again contradictory. Therefore m=0, the complementary disk is the face xyz, and L is exactly the octahedral sphere. This proof covers all m, not just a finite observed cutoff.

## 3. Induction for the unique degree-three vertex

Induct on the number n of vertices of L. A four-vertex sphere has four degree3 vertices, so is outside the hypothesis. Let v be the unique degree3 vertex and cap its link triangle A as in Section1, obtaining L'. All vertices outside A keep their degrees4/5; vertices of A have degrees3/4. Thus every degree3 vertex of L' lies in the single face A.

If L' has four vertices, it is the tetrahedral boundary, whose fourth vertex outside A also has degree3. This contradicts the unchanged degree4/5 of that vertex. Thus L' has more than four vertices. Since all vertices of A are adjacent, Section1 shows L' has at most one degree3 vertex.

Suppose it has exactly one, w. The induction hypothesis identifies L' as an octahedron with one face subdivided. Its unique degree3 vertex w has all three neighbors of degree5. But w belongs to face A, and the other two A vertices, which are neighbors of w, have degrees at most4 in L'. Contradiction.

Hence L' has no degree3 vertex. All three vertices of its cap face A must then have degree4, and all other degrees are4/5. The patch lemma makes L' the octahedron. Restoring v subdivides one of its faces and yields exactly the stated seven-vertex sphere. Conversely that explicit face subdivision has the required degrees. This completes the induction without appealing to the11-sphere catalog.

## 4. Consequences in a genuine signed-star sphere

Let ab be a positive exceptional edge, with a the common root and b its tip, in the already accepted genuine signed-star3-sphere. Its link has valence3. Since b is a nonroot tip, every other edge incident with b is ordinary, of valence4/5. The vertex link L_b is therefore exactly in the theorem's domain: the link vertex a has degree3 and every other vertex degree4/5.

It follows that

    d_K(b) = 7                                      (2)

at **every** root order, for both constants. This sharpens the earlier lower bound7. It is not a statement about the root's own graph degree, and does not apply to a tip of a negative valence6 edge or a vertex incident with multiple exceptional edges.

Let A be the fixed three-vertex edge-link of ab. The three edges from b to A have tetrahedral valence5. The remaining three neighbors of b have valence4 edges to b. Removing a from L_b leaves an octahedron on A and an opposite three-set B; A and B are its two opposite faces. Consequently the local link has exactly10 triangles. The degree/incident identities also give exactly10 tetrahedra and15 triangles through b. A future literal model can express (2) or the equivalent ten-quartic count; no such row is added here.

This link statement is carefully distinguished from original graph adjacency. Root a has no L_b-edge to B, so triangles abx are absent for x in B; it does **not** follow that original graph edges ax are absent. The octahedral antipodal matching is a local combinatorial description, not a proved function automorphism or a license to relabel separate links independently.

## 5. Primary source and novelty limits

Florian Frick, *Combinatorial restrictions on cell complexes* (2015), Theorem3.8, printed pp43–44, primary thesis https://d-nb.info/1076082246/34 (zero-based PDF pages48–49), explicitly lists eleven degree-at-most-five sphere triangulations and the projective-plane example, attributing the enumeration to Brinkmann and McKay. The primary thesis text was freshly opened for this note. The octahedron with one face subdivided is among those examples. The unique-degree3 conclusion is consistent with that published classification; no novelty is claimed.

The proof above does not import that catalog or re-enumerate it. Its only topological inputs are ordinary simplicial2-sphere links, planar graph bounds and top-dimensional mod2 cycle connectedness. No external PDF body is redistributed. Tiny explicit sphere/patch controls corroborate the reasoning; they are not a classification algorithm.

The signed-star application retains the accepted1413/1453 geometric hypotheses. It assumes neither an arbitrary original Boolean function is selfdual nor that every raw selected-row assignment is a sphere. Necessary rows from this result would be theorem-based additions, not asserted entailments of the old5413-row CNF. Independent review and a source-to-encoding gate are required before a future query. All29 original whole patterns and the full Boolean14-variable goal remain OPEN.
