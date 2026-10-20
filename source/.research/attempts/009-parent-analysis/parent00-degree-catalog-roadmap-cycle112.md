# Next deductions for the remaining0/0 cubic representatives

These are proposed next reductions; only negative7 is currently accepted as
excluded. Confirm each argument and bind its scope before updating a frontier.

For any negative family N, write n_i for its vertex incidence. At the0/0
parent, the singleton scalar sets give d_i-2n_i-u_i in{2,-2} for apices0,1,
0 for ordinary2,3,4, and4 for ordinary5,...,9. Positive pair incidences are
even, so every positive vertex link is a simple even graph. Thus a nonempty
positive degree is at least3. For the actual N=1/2 signatures, n_i is0 or1.

It follows structurally that:

- a negative-free vertex among2,3,4 has d=u=0;
- a negative-covered vertex among2,3,4 has d=3,u=1;
- an ordinary vertex among5,...,9 has d=4+2n_i+u_i;
- an apex with n_i=0 has d=3,u=1;
- an apex with n_i=1 has either d=u=0 or d=4+u.

All linear flags are determined by the positive degrees. The origin imposes
P=Q+4+2|N|. These rules should be generated from the scalar values and incidences,
not maintained as a per-pattern coefficient lookup table.

The audited parent cover has the following representatives:

|index|negative family|positive/linear support bound|possible cheap route|
|---|---|---|---|
|0|[7]|eight coordinates, degree3 at2|Already excluded by seven-vertex base cycles|
|1|[13]|nine coordinates, degree3 at1,2,3|Proposed Euler obstruction below|
|2|[13,50]|ten coordinates, three degree3 vertices, one degree6/7 vertex|Multiple link peeling or other coupling|
|3|[13,98]|nine coordinates, two degree3 and two degree6/7 vertices|Multiple link peeling|
|4|[35]|seven coordinates|Direct complete2^20 binary-cycle enumeration|
|5|[37]|eight coordinates, degree3 at1,2|One degree3 link reduction to seven vertices|
|6|[37,74]|nine coordinates, two degree3 and two degree6/7 vertices|Same degree pattern as index3, different forbidden faces|
|7|[37,194]|eight coordinates, one degree3 and three degree6/7 vertices|One link reduction, retaining both stellar and tetrahedron cases|
|8|[97]|seven coordinates|Direct complete2^20 binary-cycle enumeration|
|9|[97,386]|seven coordinates|Direct complete2^20 binary-cycle enumeration|

For a degree3 center c, its link is a triangle T. Toggling the tetrahedron cT
always removes c and gives a cycle on the other vertices. If T belongs to the
base cycle, restoring c increases the face count by2; otherwise it increases
the count by4. The latter case may only be discarded after checking that
removing the tetrahedron would force a base vertex degree1 or2. This was valid
for negative7. It also appears valid for index5: only one other degree3 vertex
and one degree6/7 vertex are available, so a three-vertex T must include a
degree4/5 vertex. It is NOT valid without further work for index7, which has
three degree6/7 vertices. Use both cases there.

## Proposed elementary Euler proof for index1, negative13

The degree rules give three required degree3 vertices1,2,3, five required
degree4/5 vertices5,...,9, and optional apex0 of degree0,4,5. Vertex4 is absent.
Let a be0 or1 according as apex0 is absent or present. Then positive support
size V=8+a. Summing triangle incidences gives3P=26+4a+Q, while P=Q+6.
Thus Q=4+2a, P=10+2a, and Euler characteristic V-P/2=3.

Every positive degree is at most5. A nonempty simple even graph with at most
five edges is one cycle. Hence all vertex links are cycles and every edge
lies in exactly two faces: the positive family is a disjoint union of closed
triangulated connected surfaces. No classification of surfaces is needed.
For each component, the mod2 face-boundary kernel has dimension1 (equal face
weights propagate along the connected dual graph), so Euler-Poincare gives
chi=2-b1<=2. Also chi=sum_v(1-d_v/6)>0. Therefore each component has chi1 or2.

A chi2 component has at least four faces. For chi1, E=3V-3 and simplicity gives
3V-3<=V(V-1)/2. Since V>=4, this forces V>=6 and F=2V-2>=10. Total chi3 would
require at least a chi2 and a chi1 component, hence at least14 faces (or three
chi1 components, hence at least30). But P is10 or12. This would be a rigorous
contradiction for index1 after checking the degree derivation and source binding.

The finite-cycle enumerator can serve as a separate check on small controls
for this lemma, but an exhaustive enumeration on nine vertices is unnecessary.
Do not apply the surface argument to a degree6/7 vertex: its link may be
disconnected or have degree4, so the manifold conclusion would fail.
