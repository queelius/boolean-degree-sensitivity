# A doubled positive quartic cannot occur in the negative-free derivative

Let p on thirteen Boolean variables have p(0)=1, p(e_i)=0, integer
ordinary coefficients, and ordinary quadratic coefficients in {0,1}.
Suppose

    16p=c + sum_(|A|=2) a_A chi_A + sum_(|B|=4) b_B chi_B,

where every a_A is -1 or 0, and every b_B is 0 or 1 except one
b_D=2. These hypotheses are inconsistent. This lemma needs neither
the published three-manifold catalog nor a solver certificate.

At a pair A, quartic inversion gives total weighted link size
4m_A-a_A, where m_A is the ordinary quadratic coefficient. Cubic
integrality makes every weighted vertex degree of this link even.
When A is not contained in D, the link is empty, C4 or C5. When
A is contained in D it has one doubled edge. Removing that doubled
edge leaves a simple even graph with at most three edges. The empty
remainder would give total size two, incompatible with 4m_A-a_A.
Therefore the remainder is C3, m_A=1 and a_A=-1.

No unit-weight tetrahedron can contain a triple T in D. For suppose
T+u occurs, with u outside D. Even incidence at T forces another
T+v. In each of the three pair links A contained in T, the residual
triangle contains T minus A and its two neighbors u,v. Thus all
three A+u+v are unit tetrahedra. For any t in T, the pair link of
{t,u} now contains a triangle on the other two vertices of T and v.
But {t,u} is not contained in D, so its link must be empty, C4 or
C5, none of which contains a triangle. Contradiction.

Delete the doubled tetrahedron and let K be the ordinary simplicial
complex formed by the unit tetrahedra. All six pairs in D remain
edges, with links C3; all other nonempty edge links are C4 or C5.
Every triangle belongs to exactly two unit tetrahedra. For triangles
outside D this follows from an edge not contained in D; triangles
in D have just been shown absent. In particular all vertex links
are disjoint unions of closed triangulated surfaces with vertex
degrees three, four or five.

The same origin/unit and quadratic summations as in the baseline
derivative argument give weighted tetrahedron incidence
P_w=2deg_K(w)-4. For w in D, deleting weight two leaves
P'_w=2deg_K(w)-6. The vertex link L therefore has

    chi(L)=deg_K(w)-P'_w/2=3.

Exactly three vertices of L have degree three: the other vertices
of D. All other degrees are four or five. Curvature makes each
surface component have positive Euler characteristic. A component
of Euler characteristic one has at most six vertices; the elementary
simple-graph bound gives at least six, so it has exactly six and
all degrees five. Thus it contains none of the degree-three vertices.
Since L has at most twelve vertices, Euler characteristic three can
only be realized by a sphere and one six-vertex projective plane.
All three degree-three vertices belong to that sphere.

Its curvature equation is 9+2n_4+n_5=12. Either it has five vertices
including a degree-five vertex, impossible, or it has six vertices
with degrees (3,3,3,5,5,5). In the latter case the three degree-five
vertices are universal. Each of the other three vertices is adjacent
only to them and belongs to three triangles. These are nine distinct
triangles, whereas a six-vertex sphere has eight. Contradiction.

An independent proof and literal small controls are recorded in
`008-sparse-spectrum-proof/doubled-positive-quartic-derivative-independent-audit.md`
and `doubled-quartic-derivative-controls.json`.

Consequently, in the outside-pair four-star case, a unique positive
quintic numerator two cannot be its residual defect. Every negative-free
nonendpoint coordinate, whether or not it occurs in that quintic,
would be forced to give a positive extension of the zero pair.
There are four such coordinates and only two positive extensions.
Together with the positive-cubic extension, this leaves only a cubic
numerator minus two. This is a subcase reduction, not a full decision.
