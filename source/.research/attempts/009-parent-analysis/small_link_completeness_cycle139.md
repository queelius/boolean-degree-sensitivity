# Completeness of the small-link high-cycle enumeration

Let C be a simple family of triples on a set H, with every pair incident to
an even number of triples. Fix v in H with degree at most five. The link G
of v is an even simple graph on H minus v. An even graph with at most five
edges is empty or a simple cycle of length three, four, or five: any vertex
of degree at least four would force at least six edges, and two nontrivial
components would also require at least six. On seven vertices there are
1 + C(7,3) + 3 C(7,4) + 12 C(7,5) = 393 such graphs.

Fix a second vertex w in H minus v. For each link G, let K be the binary
triangle chain containing {w,a,b} for each edge {a,b} of G not incident to w.
Since every vertex of G has even degree, the pair boundary of K is G.
Consequently every C with this link has the unique representation

    C = cone(v,G) XOR K XOR Z,

where Z is a binary triangle cycle on H minus v. Conversely, every such Z
gives a cycle with link G. This is a bijection for each G, and different links
give disjoint classes. The cycle space on seven vertices has dimension 20:
choose freely all triangles avoiding one fixed vertex and force its triangles
by pair parity. Enumerating the links and that complete space is exhaustive.
This argument requires only even pair incidences, not a manifold assumption.

In the L=2 degree catalogs, there are six ordinary high coordinates. At most
four occur in the actual negative family, so at least one has final positive
degree four or five. This vertex is not among the forced-degree-three
vertices. Removing a forced triangle link reduces each affected high degree
by one or three. In the exceptional tetrahedron case, every high vertex of
that tetrahedron is critical (degree at least six), so the chosen vertex is
unaffected. Thus the residual cycle on at most eight high vertices always
has an eligible vertex of degree at most five.

The producer `small_link_high_cycles.py` constructs the seven-vertex cycle
space in integer face bits, updates exact weights/degrees as K is toggled,
and adds the link faces. Maximum degree and face-count tests only discard
families failing the requested bounds. The independent implementation
`independent_small_link_cycles.py` enumerates even edge subsets directly,
uses the opposite filling cone, unpacks every face bit, and independently
reconstructs weights/degrees. It returns full ambient face masks. The
existing forced-link reader restores low vertices in reverse order and
includes the full-tetrahedron exception.

Both high-cycle methods match complete six-vertex spaces under varied caps.
For the recorded eight-vertex benchmark, they use different eligible vertices
and agree on every one of 23,598 cycles, not just aggregate counts. The
independent manifest is
`small-link-high-cycle-benchmark-independent-manifest-cycle139.json`.
The benchmark itself is not a degree catalog and excludes no parent.
The full L=2 catalogs require their own complete reconstruction, now prepared
in `verify_singleton_stratified_catalogs_v2.py`.
