# Two positive cubic exceptions at a negative-free coordinate

Status: candidate local theorem, independent review pending.

Let p on13 Boolean variables take values in{-1,0,1}, with p(0)=1 and
p(e_v)=0. Write16p=c+sum k_A chi_A+sum l_D chi_D over pairs A and
quartets D. Assume c<=2, all l_D are0/1, and exactly two distinct pair
numerators k_J are+1 while every other k_A is-1/0. The ordinary quadratic
coefficients are0/1, apart from one specified pair e which may have
coefficient two. Then no such p exists.

Pair inversion and cubic integrality give empty/C4/C5 links at ordinary
baseline pairs and a C3 at an ordinary exceptional pair. Every triangle
has an ordinary pair, whose link is2-regular even if that pair is one
of the positive exceptions. Hence every occurring triangle belongs to
exactly two tetrahedra. This includes the case where e and the two
exceptional pairs themselves form a triangle; no baseline-pair assumption
is needed for that particular triangle.

## Ordinary quadratic coefficients all0/1

Here every triangle has a baseline pair, hence lies in zero or two
tetrahedra of K, the complex of positive l_D. The ordinary expansion is
p(1_X)=1-chi(K[X]). All13 vertices are active. At a vertex with z incident
positive exceptions, origin/unit and pair inversion give
P_v=2D_v-4 and y_v=2D_v-12+z, where y_v counts incident negative pair
numerators. All vertices therefore have D_v>=6, except that the unique
common vertex of two adjacent exceptions could have D_v=5. Each vertex
link has Euler characteristic two and every link vertex has degree3,4,5.
Its components have positive Euler characteristic. A characteristic-one
component is a six-vertex projective plane with all degrees five; thus a
disconnected vertex link consists of two such components on A,B of size6.

Suppose this occurs at w. Neither exceptional pair contains w. The two
cliques plus w already use42 skeleton edges. Since E=49+c<=51, there
are at most nine edges between A and B.

Call an endpoint of either exceptional pair bad, and other vertices good.
Every good vertex has a cross neighbor: otherwise its six-vertex link
would have one degree-five vertex w and all others at least degree four,
contradicting its characteristic-two degree sum24. A bad vertex incident
to exactly one exception also has a cross neighbor. If it did not, its
six-vertex link would have degrees(5,3,4,4,4,4). The degree-five vertex
is universal. Deleting it leaves a triangulated pentagon with two
diagonals whose endpoints would have to be disjoint. No such triangulation
exists; an explicit five-vertex check is supplied separately. Only the
common vertex of two adjacent exceptions can therefore lack a cross edge.

There is a good vertex of cross degree one. If the exceptions are disjoint
and every good vertex had cross degree at least two, the eight good plus
four bad vertices give total cross degree at least20. If they are adjacent,
the nine good and two singly bad vertices again give at least20. Either
would require at least ten cross edges. A good vertex of cross degree one
has the previously audited seven-vertex link and forces its cross neighbor
to be adjacent to the whole opposite six-set. This uses six cross edges.
If the good vertex is in A and its cross neighbor z is in B, the other
five vertices of B all require a cross neighbor, except possibly the
single doubly bad vertex, requiring at least four further
edges. This contradicts the bound nine.

Every vertex link is therefore a sphere. Each connected component of K
needs at least seven vertices (all but at most one vertex have degree at
least six), so K is connected. It is a closed13-vertex three-manifold
with E<=51 and all edge valences at most five. The accepted complete
published small-valence catalog and its independently checked76 induced
Euler obstructions cover the larger range E<=52. Thus some induced
Euler characteristic is outside{0,1,2}, contradicting p's range. This
step explicitly inherits the published catalog completeness dependency.

## A special ordinary quadratic coefficient two

If an ordinary +1 pair meets e, its endpoint link has at least one
degree-three vertex besides the opposite endpoint of degree s. When
triangle incidence is two, curvature gives n+n4+2t=s with t>=1 while
n>=s, a contradiction. If neither ordinary exception meets e, the
endpoint capped strips are unchanged. If e is itself exceptional,
s=7; otherwise s=8 or9. Both strips have a single interior cycle with
the same distance-two boundary.

A common strip face forces a C3 in the link of its boundary edge, so
that edge must be one of the at most two ordinary exceptions. Distinct
faces use distinct boundary edges. Exact cycle-root enumeration gives:
for s=7 or9 the root is unique, hence all s faces are common; for s=8,
among the eight roots every pair with at most two common faces has at
most four common interior edges. The odd cases are impossible. In the
even case the core contains at least1+5*8-4=37 edges.

There are three remaining vertices, nonadjacent to the endpoints. They
form a clique, since an independent triple with one endpoint would
violate the polynomial range. All have degree at least six except
possibly the common exceptional vertex, whose degree is at least five.
They contribute at least14 further edges. Thus E>=51, whereas the
special-edge mean identity gives E=48+c<=50.

All ordinary pair links, including exceptional C3s, are2-regular, so
the endpoint curvature and strip arguments retain the required face
incidences in every placement. Separate mathematical review and source
binding of the finite controls remain required before promotion.
