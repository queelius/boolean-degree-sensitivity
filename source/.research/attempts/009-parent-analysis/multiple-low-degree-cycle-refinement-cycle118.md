# Refinement of the draft multiple-low-vertex reduction

This is an unaudited mathematical draft. It adds to, and does not replace,
the frozen multiple-low-degree-cycle-reduction-draft-cycle118.md.

For the three unenumerated actual N=2 positions, let L be the forced degree3
ordinary vertices and H the remaining seven coordinates. Every high vertex
has final degree0,4,5,6,or7; degree3 is forbidden. Only the4-|L| high ordinary
vertices covered by negative triples can have degree6 or7. There are either
two lows/two such high vertices or three lows/one such high vertex.

Two adjacent degree3 vertices in a binary triangle cycle lie in a full
tetrahedron boundary. Indeed, if c has link triangle{v,a,b}, v already lies
in triangles cva and cvb. Its one remaining triangle must contain both va and
vb to make those pair incidences even, so it is vab. The four tetrahedron
faces exhaust all triangles at c and v. A third low vertex meeting either
therefore belongs to that same tetrahedron. Components of size at least2 in
the low-vertex adjacency graph are full tetrahedra.

Every high vertex of such a tetrahedron must have final degree at least6:
deleting the tetrahedron leaves a binary cycle, and final high degree4 or5
would leave degree1 or2, which is impossible; final degree3 is forbidden by
the singleton rules. Consequently, with two lows the only adjacent-low case
is the tetrahedron on both lows and both negative-covered high ordinary
vertices. With three lows, a two-low component would require two high vertices
of degree at least6 but only one exists; it is impossible. The only adjacent
case is a tetrahedron on all three lows and that one high vertex.

Thus there are only two construction types in each of the three positions:

1. Every low vertex is isolated from the others. Starting with a binary cycle
   Z on H, restore every low c by toggling a tetrahedron c union T with T a
   triple entirely in H. Both states of T are retained, including repeated
   link triples at distinct low vertices. Each restoration adds2 or4 faces.
   Therefore |Z|<=14-2|L|: at most10 faces for two lows, at most8 for three.
2. Add the single tetrahedron on the four ordinary vertices covered by the
   negative triples to a cycle Z on H. Its four faces contain lows, so none
   overlap Z, and |Z|<=10. In the two-low case its two high vertices gain3
   degrees each; in the three-low case its one high vertex gains3.

The seven-vertex binary-cycle weight distribution has only1,996 cycles of
weight at most8 and12,552 of weight at most10. These counts are already
independently known from the checkpoint111/112 full-space replay. The naive
isolated-link counts are therefore about85million (three lows) and15million
(two lows) before necessary intermediate high-degree and face-count filters.
This appears manageable with exact bitsets and avoids a2^35 or2^56 search.

For an independent implementation, enumerate base cycles in a different
ambient face indexing and compute degrees from the resulting face bitsets,
instead of trusting incremental degree updates. Compare with every binary
cycle on six vertices for low sets and high degree bounds satisfying the
stated assumptions. Include a triangular bipyramid with its two degree3
apices as an isolated-low positive control. Include an octahedral high cycle
plus a tetrahedron sharing one/two high vertices as explicit full-tetrahedron
controls. Ensure negative triples are forbidden as positive faces and derive
linear flags/counts from the actual singleton values at the end.
