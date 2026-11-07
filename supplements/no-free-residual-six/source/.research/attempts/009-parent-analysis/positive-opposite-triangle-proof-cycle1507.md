# Every positive edge has a missing opposite triangle

Alexander Richard Towell, with substantial OpenAI Codex assistance. The parent researcher proposed this connected-sum generalization; the present producer proof was written after a separate mathematical audit, and cycle1508 supplies another independent review. This is a written conditional theorem. No target model, CNF, solver query, original-pattern exclusion or Boolean construction is produced.

## A general local theorem

Let K be a finite combinatorial PL3-sphere, and let ab be an edge of tetrahedral valence3. Its link is the triangular cycle boundary A, where |A|=3 and a,b are outside A. Assume the three edges inside A all have tetrahedral valence at most5.

**Theorem.** If the triangle A is a face of K, then K has a vertex of graph degree4. Consequently, if K has minimum graph degree at least5, A is missing.

The actual signed-star application has minimum degree at least6, so it satisfies this slightly weaker sufficient guard. No flagness, alpha bound, vertex count, degree of the root, Fourier symmetry or Boolean self-duality is used in the local theorem.

## 1. Filled endpoint caps immediately give degree four

Suppose A is present. If aA is a tetrahedron, then the vertex link of a contains the four triangles of the tetrahedral boundary on {b} union A: the three bxy from abxy in the edge star, and A from the cap aA. This boundary is a nonzero2-cycle over F2. The only nonzero2-cycle of a triangulated S2 is the sum of all its faces. Hence the entire link of a is that boundary and d_K(a)=4. The same applies to bA.

It remains to treat the case where both tetrahedra aA and bA are absent. Their absence must be established before using them as new caps; adding a duplicate tetrahedron would be invalid.

## 2. The precise ball and capping construction

The closed edge star N=ab*boundary A consists of the three tetrahedra abxy, one for each edge xy of boundary A. It is an embedded PL3-ball with boundary the union of the two cone disks a*boundary A and b*boundary A. By the PL Alexander/Schoenflies theorem, the closure B of its complement in S3 is also a3-ball.

The filled triangle A lies in B and is a properly embedded PL2-disk: its interior is not a face of N, its boundary is exactly boundary A in the boundary of B, and no other part of it lies in that boundary. Cutting a3-ball along such a disk gives two3-balls. Call them B_a and B_b, according to which cone disk their boundary contains. Their boundaries are respectively

    boundary B_a = (a*boundary A) union A = boundary(aA),
    boundary B_b = (b*boundary A) union A = boundary(bA).

This standard disk consequence follows by gluing the disk to either boundary cone disk, forming an embedded PL2-sphere, and applying Alexander/Schoenflies. It is used only in the tame finite PL category, not for arbitrary wild embeddings. The source sphere has genuine S2 vertex links, so all the needed local manifold/collar conditions hold.

The two original balls meet exactly in A. Their vertices outside A are disjoint; a belongs only to B_a and b only to B_b. There is no edge between these two outside vertex sets inside B. In the original K the **only** edge between the sets is ab, restored from N. No graph-alpha hypothesis is needed for this assertion.

Cap B_a by the absent tetrahedron aA, obtaining a combinatorial3-sphere C_a. Cap B_b by bA, obtaining C_b. These are literal triangulated balls plus one tetrahedron on their existing boundary vertices; no new vertex or identification of unrelated vertices is made. Equivalently, K is the connected sum of C_a, the boundary4-simplex on {a,b} union A, and C_b, along the two endpoint caps. The explicit ball description resolves the fact that those central caps share the face A; no disjoint-cap shortcut is assumed.

Classical external input: Allen Hatcher, *Notes on Basic 3-Manifold Topology*, Theorem1.1, author-hosted https://pi.math.cornell.edu/~hatcher/3M/3Mfds2014.pdf . Its accompanying discussion states the PL version of Alexander's theorem; only the ordinary embedded-sphere/ball and proper-disk consequences are applied. Original bibliographic source: J.W.Alexander, *On the Subdivision of3-Space by a Polyhedron*, PNAS10(1)(1924),6–8, DOI https://doi.org/10.1073/pnas.10.1.6 . The parent located its primary abstract/introduction, but fresh full-PDF access was blocked; no complete reading of that original proof is asserted. The source note1509 will separately record access evidence. No PDF is redistributed and no new proof of that classical theorem is claimed.

## 3. Exact edge-valence accounting

Fix an edge e inside A. Its incident tetrahedra in K come from three disjoint lists: those in B_a, those in B_b, and the unique central tetrahedron ab*e. Capping B_a adds one tetrahedron aA through e, and capping B_b adds one bA. Therefore

    val_K(e) = val_C_a(e) + val_C_b(e) - 1.       (1)

Each cap complex is a genuine3-sphere; each edge link is a simple circle with at least three vertices. Thus both cap valences are at least3. By the assumed upper bound5 on val_K(e), equality is forced:

    val_K(e)=5, val_C_a(e)=val_C_b(e)=3           (2)

for all three edges of A. The subtraction in(1) is exactly one, not two: the two cap removals subtract2 and the central edge-star tetrahedron adds1.

There is an independent local check on the first equality. In link_K(e), the edge ab is present, and the third vertex of A is present but adjacent to neither a nor b, because aA,bA are absent. A simple circle of length at most5 with this configuration must be the5-cycle a-b-c-z-d-a. This corroborates, rather than replaces, the full cap accounting.

## 4. The capped spheres collapse to five vertices

We show C_a is exactly a boundary4-simplex. Let v be a vertex of A and y,z the other two. In the S2 link of v in C_a, y and z are adjacent because A is a face. Their degrees in this link are the valences of vy and vz in C_a, both3 by(2).

An S2 containing two adjacent degree3 vertices is the tetrahedral boundary. Indeed, the first vertex's three neighbors are the second vertex and two others. The two triangles through their common edge force exactly the same other two neighbors for the second vertex. The four resulting triangles form a full tetrahedral boundary2-cycle, which must be the entire S2. Therefore d_C_a(v)=4.

The face A has exactly two tetrahedral cofaces in C_a. One is its new cap aA; denote the other cA. The vertex c is outside {a} union A, lies in B_a, and is an original vertex, not the other endpoint b. This same c is supplied by the single face A for all three choices of v.

Each v in A has exactly the four neighbors {a,c} union (A minus{v}). Its tetrahedral-boundary link therefore supplies acxy for every two-set xy in A. Together with aA and cA these are all five boundary tetrahedra of the4-simplex on {a,c} union A. Their mod2 sum is a nonzero3-cycle. A connected triangulated3-sphere has no4-simplices and a one-dimensional top-cycle space generated by the sum of all tetrahedra. Consequently C_a is exactly this five-vertex boundary.

The private vertex c does not lie on boundary B_a=boundary(aA). Its entire original K-star is therefore contained in B_a and unchanged by adding/removing the cap aA. Neither the central edge star nor B_b contains c. Hence

    d_K(c)=d_C_a(c)=4.

This proves the theorem. No lower bound on the sizes of the two outside vertex sets is needed: the private vertex and its unchanged star give the contradiction directly whenever the original minimum degree is at least5.

## 5. Optional exact exceptional shape

The same argument applies to C_b, giving a distinct private vertex d on its other side. When the endpoint caps were both absent, the whole original K is therefore exactly the seven-vertex stacked sphere built from three boundary4-simplices along the two caps. Its degree multiset is

    (4,4,5,5,6,6,6).

It has11 tetrahedra. Thus a filled opposite triangle can occur if degree4 vertices are allowed; the minimum-degree guard is real. Cycle1508's independent seven-vertex control addresses this boundary case. This optional classification is not required for the signed-star application and is not a new catalog-completeness claim.

## 6. Signed-star consequence and exact research scope

In a genuine signed-star sphere every positive edge is a root edge of valence3. Its three opposite link vertices exclude the root, so all three edges inside A are ordinary and have valence4/5. This is automatic from the common-root exceptional-star hypothesis. It does not require proving that another positive tip lies outside A. Accepted minimum degree6 and the theorem imply:

    the opposite triangle of EVERY positive root edge is missing.

The conclusion covers all root orders; the earlier root7 and root>=10 arguments are special cases. It is vacuous at roots with no positive edge. It does not settle negative-edge6-cycle fillings, rule out a root, or close a whole original coefficient pattern.

The application inherits accepted1413/1453 geometry and1489 minimum degree. It uses no c1 LRAT proof and applies equally to either allowed constant when those geometric premises hold. The literal root7 consequences remain masks176=0 and200=0; no new physical or SAT indices are asserted for other roots. Deriving any further native unit must use its accepted structured root source and receive a separate exact encoding gate before a query.

This producer adds no unit, row, CNF, propagation run, feasibility search, new local witness or global exclusion. The theorem is written mathematics with substantial AI assistance, pending its separate1508 independent gate and parent composition; it is neither formal verification nor human peer review, and novelty is not established. The original Boolean14 question and29 whole patterns remain OPEN.
