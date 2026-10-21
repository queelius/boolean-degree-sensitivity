# Mathematical audit of the two-adjacent-minus-two ordinary derivative

**Structural reduction PASS. Finite interval proofs and complete row coverage require their separate independent audit.**

I reviewed `../006-solver-resume/two-negative-cubic-ordinary-derivative.md`
with c in {1,2}, thirteen active coordinates, ordinary quadratic
coefficients zero/one, and two adjacent exceptional Fourier pair
numerators -2. The quartic Fourier coefficients must remain zero/one.
These hypotheses exclude the special ordinary coefficient-two case;
this audit does not silently transfer to that case.

Every triangle has a baseline pair, so its tetrahedron incidence is two.
The exceptional pair links are C6 or two C3s. The earlier splitting
argument depends only on the valences incident with a private endpoint,
so it applies separately to each edge here. Splitting two C3s would
require at least eight sphere vertices plus six projective-plane
vertices, exceeding thirteen. The private endpoint link cannot contain
the characteristic-one (6,5,5,5,5,5,5) component, by the accepted
octahedron-boundary argument. Thus both exceptional pair links are C6
and both private endpoint links are spheres.

The common endpoint link has two degree-six vertices and all others
degree four/five. Curvature is positive on each component. A
disconnected link would consist of two characteristic-one components.
If the exceptional vertices are separated, the preceding one-six
component obstruction applies. If together, that component needs at
least seven vertices and the other at least six, exceeding twelve.
The common endpoint link is therefore a sphere.

For an ordinary vertex, a disconnected link is two six-vertex
projective planes. Their cliques and center require42 skeleton edges,
leaving at most nine cross edges because E=49+c<=51. The singleton and
pair identities give skeleton degree at least6+z at a vertex incident
with z exceptional edges. Thus each private endpoint needs a cross
edge and the common endpoint needs at least two. If all nine good
vertices had cross degree at least two, the cross-degree sum would be
at least22. A good vertex of cross degree one therefore exists, and
the accepted seven-vertex all-degree-four/five link is a pentagonal
bipyramid. Its cross neighbor is joined to all six vertices of the
opposite side; the other five vertices on that neighbor's own side
each need another cross edge. Eleven exceeds nine. All ordinary
vertex links are spheres too, and the minimum degree gives connectedness.

The common-root link has exactly two degree-six vertices; curvature
forces its order between eight and twelve. Its complete source cover
is therefore the previously independently audited inverse-contraction
sphere catalogs through order twelve. The independent filter recorded
alongside this audit reconstructs degree from literal triangles and
obtains nine link types. Private endpoint links use the existing
complete one-six-vertex classification, of orders9,10,11; those three
links are flag. Ordinary links use the existing all-degree-four/five
flag classification. No global flagness and no flagness at the common
exceptional endpoint is asserted.

The model adapter's added private-endpoint order and local flag rows
are necessary under these classifications. The induced-Euler range
is0<=chi<=2 because p=1-chi. The basic f-vector is
(13,49+c,72+2c,36+c). Reconstructing the actually used rows and checking
each interval certificate is a separate obligation. Raw eighteen-model
contradictions alone do not supply that independent verification.
