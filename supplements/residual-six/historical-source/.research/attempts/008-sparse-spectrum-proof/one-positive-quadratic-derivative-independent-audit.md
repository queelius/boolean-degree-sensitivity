# One positive quadratic numerator is also impossible

This independently audits the parent's proposed extension of
`negative-free-derivative-catalog-audit.md`. The old frozen theorem and
manifest are unchanged. Assume the same thirteen-variable derivative p,
but permit exactly one quadratic Fourier numerator to be +1. All other
quadratic numerators are -1 or 0; quartic numerators remain 0 or 1;
the constant numerator c is at most 3; ordinary quadratic coefficients
remain 0 or 1. The conclusion is again nonexistence.

For a pair A with ordinary quadratic coefficient m_A, its positive
quartic link has 4m_A-a_A edges and even vertex degrees. At the exceptional
pair this is three edges, forming C3. All other nonempty edge links are
C4 or C5, exactly as before. Thus every triangle has two tetrahedra.

At a vertex w, let y count incident -1 quadratic numerators, let z be
the indicator that w is an endpoint of the exceptional pair, and let P_w
count incident tetrahedra. The origin and unit equations give

    -y+z+P_w=8,       4deg_K(w)=-y+z+3P_w.

Consequently P_w=2deg_K(w)-4 and y=2deg_K(w)-12+z. Since deg_K(w)
is an integer, y>=0 and z<=1 imply deg_K(w)>=6. Every vertex link
has Euler characteristic two. All its vertex degrees are 4 or 5,
except possibly one vertex of degree 3.

Each connected vertex-link component is a closed triangulated surface
with positive curvature and hence Euler characteristic one or two.
A component of characteristic one has at least six vertices: using
E=3(V-1) and E<=choose(V,2) gives V>=6. Its curvature
6=sum(6-degree) then forces exactly six vertices, all degree five.
In particular no characteristic-one component contains a degree-three
vertex. A disconnected link of characteristic two therefore consists
of two six-vertex projective-plane triangulations. Its center w is not
an endpoint of the exceptional edge.

Write these two components as A and B. Their skeleton forces 42 edges
of K. The global origin, unit, and quadratic equations still give
P=E-13 and E=49+c<=52, leaving at most ten A--B edges. Call the at most
two endpoints of the exceptional edge bad and all other vertices good.
Every good vertex has at least one cross neighbor. Otherwise its own
six-vertex link would be a characteristic-two surface with degrees
4/5, forcing all degrees four, whereas w has degree five there.
For a good vertex with exactly one cross neighbor, the old seven-vertex
link argument applies verbatim and forces that neighbor to be universal
to the opposite six-set.

There is a good cross-degree-one vertex. If both bad vertices lie on
one side, the six good vertices on the other side cannot all have
cross degree at least two. If the bad vertices are on opposite sides,
their exceptional edge is itself a cross edge; five good vertices of
cross degree at least two plus that edge would already need eleven
cross edges. A good degree-one vertex therefore supplies a universal
vertex in the other side, consuming six cross edges. Among the five
remaining vertices on that side at least three are good, and at most
four cross edges remain. Some good vertex has cross degree one and
supplies a second, opposite universal vertex. Their two stars need
eleven edges, a contradiction.

Thus every vertex link is a sphere and K is a connected closed
three-manifold with thirteen vertices, at most 52 edges, and exactly
one edge of valence three. The induced Euler identity
p(1_X)=1-chi(K[X]) is unchanged.

The producer-independent script `audit_one_positive_quadratic_catalog.py`
checks all 4,787 published records and all 622,592 induced subsets of
the 76 order-thirteen records with at most 52 edges. The exact target
with one valence-three edge consists of six records: 402, 405, 407,
439, 1836, and 1862. Each has an explicit independent triple, with
induced Euler characteristic three, contradicting p in {-1,0,1}.
The script also computes all Fourier numerators directly from every
target's induced Euler table and checks their valence interpretation.
This uses the same explicitly external completeness theorem, Frick
(2015), Theorem 3.10, and the same source hash as the frozen baseline
proof. The historical enumeration is not independently regenerated.

For the one-zero-pair problem, an exceptional global cubic numerator
+1 becomes this single positive quadratic numerator in each incident
negative-free derivative. Thus it does not prevent use of the derivative
obstruction: with all other required baseline conditions, every such
coordinate still forces a positive extension of the zero pair.

The original four-star transfer has four negative-free nonendpoints
and permits only two positive extensions. Therefore its entire residual
+1-cubic alternative is excluded, regardless of the exceptional support.
This does not yet address a -2 cubic exception.
