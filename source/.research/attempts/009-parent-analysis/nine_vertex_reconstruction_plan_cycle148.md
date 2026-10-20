# Exact residual enumeration for the remaining L=1 two-negative branch

GLOBAL STATUS: OPEN. This is an enumeration design, not an accepted exclusion.

The hard full degree profile is one forced degree-three vertex, six vertices
of degree five, and three critical vertices of degree seven. There are 18
positive faces. Remove the forced vertex by toggling the tetrahedron on its
three link vertices. The remaining nine-vertex cycle has one of these forms:

* 14 faces, all three critical degrees four, all other degrees five, and the
  critical triple absent. Restoring that absent face adds the tetrahedron
  boundary and raises those three degrees by three.
* 16 faces, exactly three vertices have degree one below their target
  (six for a critical vertex, four otherwise), all other degrees equal their
  target, and the triple of deficient vertices is present. Restoring raises
  their degrees by one and increases the number of faces by two.

These alternatives follow directly from whether the removed link triangle
was present before contraction. No other even-link degrees can occur.

Choose a fixed noncritical vertex v in this nine-vertex cycle. It has degree
four or five, so its link G is C4 or C5. Since there are only three critical
vertices, G has a noncritical vertex w. Fill G by its fan of triangles from
w. Toggle this filling together with the star from v to G, removing v.
The result is a binary cycle Z on eight vertices.

Every vertex of G loses two star faces. Every vertex other than w belongs
to at most two filling faces, so its degree cannot increase. Vertex w
belongs to |G|-2 filling faces; its degree increases by at most one. Thus
Z has three critical degree bounds seven, one noncritical bound six (w),
and four noncritical bounds five. Its face count is at most 14. Relabeling
these groups into the canonical eight-vertex frame gives exactly the finite
catalog measured in `eight-vertex-residual-pilot-cycle148.json` (169,339
cycles). That catalog has a separate complete reconstruction reader.

For each possible link G choose w deterministically among its noncritical
vertices. Transport every canonical Z to the actual eight coordinates;
toggle its fan and restore the star to obtain the candidate nine-cycle.
Keep only the two exact degree/face alternatives above. Each nine-cycle
is obtained once: its link at the fixed v is unique, the chosen w is fixed
by that link, and the operation is invertible. Restore the forced vertex
by its uniquely determined triangle. Check every final degree, pair parity,
face count, and forbidden negative face.

Independent verification should choose a different removed noncritical
vertex and a different fan apex, enumerate link edge subsets rather than
cycle permutations, transport faces literally, and compare the complete
final catalogs. Exhaustive small-vertex controls should precede production.
This reduces the search to about 882*169,339 candidate transports, with
vectorized exact face and degree tests, instead of scanning 2^35 cycles
for every nine-vertex link.
