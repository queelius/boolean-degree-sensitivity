# An Euler obstruction for the0/0 parent with sole negative triple13

Work with the accepted parent0/0 scalar sets and missing core mask3. For the
positive cubic family P let d_i be its vertex degrees, and let u_i in{0,1}
be the negative linear flags. With sole negative triple13={0,2,3},
B(e_i)=4-2(d_i-2*1_{i in{0,2,3}}-u_i). Every positive pair incidence is even,
by the already proved signed divisibility criterion.

Each vertex link is a simple even graph, so its edge count d_i is0 or at least3.
The exact singleton scalar sets give degree3 and u=1 at vertices1,2,3;
degree0 and u=0 at vertex4; degree4+u at vertices5,...,9; and either degree0,
u=0 or degree4+u at apex0. Let a=0 or1 indicate whether apex0 occurs positively.
Then V=8+a positive vertices and

    3F = sum_i d_i = 26+4a+Q,
    F = Q+6,

where Q=sum_i u_i and the second identity is B(0)=4. Hence Q=4+2a,
F=10+2a, and V-F/2=3. Every positive degree is at most5.

We now prove the needed combinatorial bound without classifying surfaces.
Consider any nonempty family of distinct triangles with even pair incidences
and all positive vertex degrees at most5. A nonempty simple even graph with
at most five edges is a single cycle: an even graph decomposes into edge-disjoint
cycles, each of length at least3. Thus every vertex link is a connected cycle,
and every used pair belongs to exactly two triangles.

In a connected component, the graph of adjacent triangles is connected. Indeed,
connected vertex links join all incident triangles by edge adjacency, so two
components of the triangle adjacency graph cannot meet at a vertex; connectivity
of the underlying vertex graph then rules out multiple adjacency components.
Over F2, a set of faces with zero boundary must therefore assign the same
coefficient to every face. The face-boundary matrix has rank F-1. The edge-to-
vertex boundary matrix has rank V-1, and their product is zero. Consequently

    F-1 <= E-(V-1),  so chi=V-E+F <=2.

Since3F=2E, also chi=V-F/2=sum_v(1-d_v/6)>0. Each connected component therefore
has integer Euler characteristic1 or2. No orientability assumption is used.

A chi2 component has V>=4 (each vertex has a triangle link), hence F=2V-4>=4.
A chi1 component has E=3V-3. Simplicity gives E<=V(V-1)/2, so
(V-1)(V-6)>=0. As V>=4, this forces V>=6 and F=2V-2>=10.

For total Euler characteristic3, the components must have characteristics
2+1 or1+1+1. They need at least14 or30 faces respectively. Our candidate has
only10 or12 faces. This contradiction excludes sole negative triple13.

The computational audit only checks the scoped scalar sets, the exhaustive
degree/count consequences, and the cover map; the combinatorial bound above
is a complete mathematical proof. Positive controls are one and two disjoint
tetrahedral boundaries. Two boundaries sharing a vertex give a useful excluded-
scope control: their degree6 vertex invalidates the degree<=5 premise, so the
bound must not be applied to them.

This proves one parent0/0 negative-position class, not the whole parent or the
global14-variable problem. Apply no part of the low-degree component argument
to degree6/7 links without a separate justification.
