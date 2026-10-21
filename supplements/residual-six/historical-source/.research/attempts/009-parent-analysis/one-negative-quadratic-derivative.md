# Structure with one quadratic Fourier numerator minus two

This is a proposed structural reduction for the last residual cubic
alternative. It is not itself a contradiction. Assume the preceding
derivative hypotheses (thirteen variables, p(0)=1, p(e_i)=0, ordinary
quadratic coefficients 0 or 1), with all positive quartic numerators
0 or 1 and all quadratic Fourier numerators -1 or 0 except a_J=-2.
Assume c<=3 in the constant Fourier numerator.

Pair inversion and evenness give an empty/C4/C5 link at ordinary
pairs and a six-edge even graph at J; m_J=1 is forced because
m_J=0 would leave a two-edge simple even graph. A triangle containing
J also contains an ordinary pair, whose link vertex degree is at
most two. Therefore the J-link has all vertex degrees two. It is
either C6 or two disjoint C3s. All triangles of the tetrahedron
complex K consequently belong to exactly two tetrahedra.

The origin/unit identities still give

    P_w=2deg_K(w)-4,  f(K)=(13,49+c,72+2c,36+c).

Every vertex link has Euler characteristic two. Ordinary edge
valences are four or five, so only the two endpoints of J can have
a nonstandard vertex link. At those endpoints the vertex corresponding
to the other endpoint has six incident triangles.

## The exceptional edge link is connected

If its link were two disjoint triangles, split the corresponding
vertex in an endpoint link into two vertices, one for each triangle.
The resulting complex is a disjoint union of closed surfaces, has
Euler characteristic three, and has exactly two degree-three vertices;
every other vertex degree is four or five. Each component has positive
Euler characteristic. A component of characteristic one must be the
six-vertex complete-skeleton projective plane and cannot contain a
degree-three vertex. Thus there is one sphere containing both split
vertices and one projective plane. The split vertices have disjoint
three-vertex neighborhoods, so the sphere needs at least eight vertices.
The projective plane needs six. But the split link has at most thirteen
vertices. This contradiction excludes the disconnected J-link.

## An endpoint link is a sphere

An endpoint link now has one vertex of degree six and all others of
degree four or five. It is a union of closed surfaces and has total
Euler characteristic two. Every component has positive characteristic:
at most one vertex has degree six and all the others have positive
curvature. If disconnected, there would be two projective planes.
The component containing the degree-six vertex has at most seven
vertices by curvature and at least seven by that degree. All its
other six vertices therefore have degree five. Its skeleton would be
K7 minus a matching on those six vertices.

Remove the universal vertex and its six incident triangles. On the
other six vertices the available triangles are exactly the eight faces
of an octahedron, of which six must occur. Their boundary must be a
six-cycle, the link of the removed vertex. But the boundary equals
that of the two omitted octahedron faces: they are disjoint, meet at
a vertex, or share an edge. Those boundaries are respectively two
disjoint triangles, two triangles meeting at one vertex, or a four-cycle.
None is a six-cycle. Thus both endpoint links are spheres.

## The ordinary links are also spheres

An ordinary link, if disconnected, is two six-vertex projective planes.
As in the independently audited one-positive-quadratic proof, its
center and the two complete six-vertex skeletons force 42 edges,
leaving at most ten cross edges. Mark the endpoints of J bad. Every
good vertex has positive cross degree; a good vertex of cross degree
one forces its neighbor to be universal to the other side by the
seven-vertex lemma. There must be a good degree-one vertex: if both
bad vertices are on one side, six good vertices on the other side
cannot all have degree at least two; if the bad vertices are on
opposite sides, their present edge plus degree at least two at the
five good vertices would already give eleven cross edges. A universal
neighbor leaves at most four edges at the other five opposite vertices,
including at least three good vertices, so another good degree-one
vertex exists. The resulting two universal stars require eleven edges,
a contradiction.

Thus K is a connected closed three-manifold with exactly one edge
of valence six and all other edges of valence four or five. Connectivity
follows from minimum skeleton degree six (the exceptional endpoints
have degree at least seven). The published valence-at-most-five
catalog does not cover K and must not be used to exclude it.

The complete small-sphere catalogs already independently enumerated
in attempt006 contain only three possible endpoint links: order9
class22, order10 class185, and order11 class762. This last finite
filter is recorded in `one_six_edge_vertex_links.py` and
`one-six-edge-vertex-links.json`. Their catalog completeness is
separately certified by the inverse-contraction coverage files.
All three endpoint-link spheres are flag, as checked independently by
attempt008; the ordinary endpoint-free link spheres have the same
property. Local flag constraints are therefore valid at every vertex.
Global flagness is not asserted.
