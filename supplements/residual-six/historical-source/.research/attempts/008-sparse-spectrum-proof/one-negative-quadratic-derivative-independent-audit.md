# Independent audit of the single negative quadratic exception

The parent's `009-parent-analysis/one-negative-quadratic-derivative.md`
passes mathematical audit. Its conclusion is structural only: the
required derivative would yield a connected closed thirteen-vertex
three-manifold with exactly one edge of valence six, all other edge
valences four or five, and at most 52 edges. No contradiction for this
class is claimed here, and the valence-at-most-five manifold catalog
cannot be applied to it.

The exceptional pair link has six edges and even degrees. Any triangle
through that pair also contains an ordinary pair whose link has vertex
degrees two, so the six-edge exceptional link itself has every vertex
degree two. It is C6 or two disjoint triangles, with no figure-eight
possibility. In the latter case, splitting its singular vertex in an
endpoint link increases Euler characteristic from two to three. The
result is a union of closed surfaces with exactly two degree-three
vertices. A characteristic-one component is a six-vertex all-degree-five
projective-plane triangulation. Thus the two split vertices must be in
one sphere component, and a projective-plane component also occurs.
Their disjoint three-neighbor sets force the sphere to have at least
eight vertices; together this needs fourteen, exceeding the split link's
at most thirteen vertices.

For the C6 case, a disconnected endpoint link would be two projective
planes. Its degree-six vertex must lie in a seven-vertex component with
the other degrees all five, hence skeleton K7 minus a matching on the
other six vertices. Deleting the universal vertex leaves six of the
eight octahedral triangles. Their mod-two boundary equals that of the
two omitted triangles and cannot be C6. This exhausts all 28 choices,
independently replayed with the selected-six-face convention.

Every ordinary vertex link is handled by the same good/bad cross-edge
argument in the independent +1-quadratic audit: at most two bad vertices,
at most ten cross edges, and two opposite universal stars requiring
eleven. The exceptional edge is present, so the split-bad-endpoint case
also has the needed cross-edge lower bound. Connectivity follows from
minimum skeleton degree six; the exceptional endpoints have degree at
least seven by their incident negative Fourier weight two.

The independent literal filter `audit_one_six_edge_vertex_links.py`
checks all 9,148 previously covered sphere records of orders six through
twelve. It independently reconstructs every skeleton, edge incidence,
vertex link cycle and Euler characteristic. Exactly three records have
one vertex of degree six and all remaining degrees four or five:
(order,index)=(9,22),(10,185),(11,762). Each is also flag, checked by
the absence of missing triangles and four-cliques. The parent's target
rows agree exactly, and all 28 local projective-plane boundary controls
pass. Thus local flag inequalities may be used at these endpoint links
as well as at ordinary links. This does not establish global flagness.

Catalog completeness is inherited only from the already independently
checked inverse-contraction coverage in006; this script is an independent
filter and literal validity check, not a new completeness generator.
