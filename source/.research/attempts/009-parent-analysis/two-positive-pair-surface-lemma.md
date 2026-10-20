# Three necessary pair derivatives for adjacent positive doubles

Work only in the empty-zero-pair profile with four negative quintic
numerators -2 and two positive quintic numerators +2. These consume all 28
defect units. All other quintic numerators are 0/1, all cubics are -1/0,
and all singleton numerators are 1/2. Normalize g=1-2f=(sum k_S chi_S)/16.
The existing positive-double placement cover is a necessary, complete cover
in the fifteen remaining four-negative support geometries.

Its 333 literal positive pairs P,R all satisfy |P intersect R|=4, and each
has a pair B contained in their intersection but in no negative support.
These are literal finite checks against the accepted cover; no broader
unproved assertion about arbitrary supports is needed. Fix any such B.
The second difference q=-Delta_B f has scale-eight numerator consisting
of the incident linear/cubic terms on the other twelve coordinates. Its
two doubled cubic faces D1=P-B and D2=R-B meet in two vertices u,v.
Let a,b be their exclusive vertices.

Write H for the simple unit-face complex, L for the sum of the incident
cubic numerators, and W for the sum of the incident quintic numerators.
The ordinary pair truth f(B)=1 implies L+W=8. For every vertex x outside B,

    k_(B+x) + weighted_degree(x) = 4 f(B+x).

Quartic integrality gives even weighted edge incidences. Removing the
doubled faces leaves all simple edge incidences even. At u or v the
doubled faces contribute four units; the identity allows zero or one
remaining edges in their link, and the parity condition rules out one.
Thus u,v are absent from H. At a or b the doubled face contributes two;
the residual link must have two or three edges, and an even simple graph
of that size can only be a triangle. Thus a,b have degree three in H,
cubic numerator -1 and triple truth one. Every other active vertex has
link C4 or C5. Its cubic numerator is 0 or -1, respectively. All inactive
vertices have zero numerator and zero triple truth.

Consequently H is a disjoint union of closed triangulated surfaces with
exactly two degree-three vertices a,b, and all other vertex degrees four
or five. Let n be its order. The two shared vertices give n+2 active
triple truths, so summing the vertex identities yields

    L+3W=4(n+2),  W=2n,  |F(H)|=W-4=2n-4.

Hence chi(H)=2. Every connected component has positive Euler
characteristic, since all degrees are at most five. Each is a sphere or
a projective plane. A projective-plane component must have exactly six
vertices, all of degree five: its total curvature is six, each vertex
contributes at least one, and a simple triangulated projective plane has
at least six vertices. Two such components would require twelve vertices
of H, but n<=10 because u,v are outside H. Therefore H is a single sphere.

The sphere curvature equation is

    3*2 + 2*n4 + n5 = 12.

Thus n=2+n4+n5<=8, and n>=5. The independently accepted complete sphere
catalogs of orders 5 through 8 give exactly three qualifying surfaces:
order5/index0, order6/index0, and order8/index9. The source indices are
derived by the degree test and are not a manually maintained classification.
The two degree-three vertices determine a,b; adjoining two new shared
vertices u,v fixes the doubled faces. Padding with unused variables gives
three necessary spectra on twelve coordinates. Every coordinate
embedding remains allowed unless separately excluded by actual geometry.

All 4,096 inputs of each spectrum are checked exactly. Their numerator
ranges lie in {-16,-8,0,8,16}, the correct range for a Boolean second
difference. In particular the order-eight type attains +/-16; these
values are allowed and must not be discarded. Passing this local range
test does not construct a Boolean function on fourteen coordinates.

The producer saves all eligible pairs for all 333 placements, all source
surface references, full spectra, and exact value histograms. A separate
checker must accept catalog coverage and source integrity before a future
exclusion may rely on this lemma computationally. No support or magnitude
exclusion follows merely from obtaining this three-row necessary catalog.
