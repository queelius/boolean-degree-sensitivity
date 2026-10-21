# A doubled positive quartic gives an elementary contradiction

This independently audits the parent's proposed lemma. Let p have the
same thirteen-variable origin/unit values, range {-1,0,1}, even Fourier
degrees zero/two/four, and ordinary quadratic coefficients in {0,1} as
in the preceding derivative obstruction. Suppose all quadratic Fourier
numerators are -1 or 0, and all quartic numerators are 0 or 1 except
for one four-set D of numerator 2. Then no such p exists. This proof
does not use the published three-manifold catalog, nor a bound on the
constant numerator.

For an edge A inside D, the positive-quartic link is a simple graph
with one edge doubled. Its total weighted edge count is 4m_A-a_A,
which is among 0,1,4,5. Integrality of ordinary cubic coefficients
forces all weighted degrees even. After removing the doubled edge,
the remaining simple even graph has at most three edges. Therefore
it is a triangle, with total weighted count five, m_A=1, and a_A=-1.
For edges not inside D, the nonempty links remain C4 or C5.

No unit quartic contains a triple T of D. To see this, suppose T+u
is a unit quartic, with u outside D. For a pair A inside T, the
residual triangle in its link forces T+v and A+u+v for some v outside
D. (The fourth vertex of D cannot be v, since that link edge is the
doubled one.) The other two pairs inside T now see the same two
edges from T+u and T+v, so they too force their quartics A'+u+v.
For any t in T, the link of the edge {t,u} consequently contains a
triangle on (T minus {t}) plus v. That edge is not inside D, so its
link must be empty, C4, or C5, a contradiction.

Delete the doubled quartic entirely and let K_0 consist of the unit
quartics and their faces. The skeleton is unchanged: the six edges
inside D have residual C3 links, and all other nonempty edge links
are C4 or C5. Every triangle belongs to exactly two tetrahedra.

For any vertex w in D, the weighted origin/unit equations give

    P_weighted(w)=2deg(w)-4.

Removing the doubled tetrahedron subtracts two from this incidence
count and preserves the skeleton. Thus the link of w in K_0 has

    chi=deg(w)-(P_weighted(w)-2)/2=3.

Its vertex degrees are 3,4,5, with exactly three degree-three vertices,
namely the other vertices of D. Each connected component is a closed
triangulated surface of positive Euler characteristic, at most two.
A characteristic-one component has six vertices, all degree five,
by the curvature/capacity argument from the preceding independent
audit. Three such components need eighteen vertices and cannot fit
inside the twelve available neighbors. Therefore the link consists
of one characteristic-two sphere component and one characteristic-one
component. All three degree-three vertices are in the sphere.

The sphere curvature identity is 9+2n_4+n_5=12. The possible degree
counts are (n_4,n_5)=(0,3) or (1,1). The second has only five vertices
but a degree-five vertex, impossible. The first has six vertices with
degrees (3,3,3,5,5,5). Its three degree-five vertices are universal;
the three degree-three vertices are pairwise nonadjacent and each has
three incident triangles. These nine triangles are distinct, whereas
a six-vertex characteristic-two closed surface has only eight. This
is the required contradiction.

The exact controls separately enumerate all weighted six-vertex pair
links, all 36 labelled instances of the forced link triangle, and all
900 possible eight-triangle selections for the twenty labelled graphs
of degree sequence (3,3,3,5,5,5). All controls agree with the proof.

In the four-star one-zero-pair branch, a doubled positive quintic gives
exactly this exceptional quartic in each incident negative-free
derivative. It therefore cannot evade the positive-extension conclusion.
Together with the baseline theorem, all four free nonendpoints would
be positive extensions, contradicting the accepted total two. Thus
the entire doubled-positive-quintic residual alternative is excluded.
