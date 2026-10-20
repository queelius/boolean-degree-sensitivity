# Complete multiple-low-vertex cubic catalogs

The setting is the exact parent0/0 missing-core-mask3 cubic, with negative
families[13,50], [13,98], and[37,74]. Every positive-triangle family P is a
binary2-cycle: every pair has even incidence. The singleton restrictions
give a set L of two or three forced-degree3 ordinary vertices and a common
seven-coordinate set H. Every high degree is in{0,4,5,6,7}; only the4-|L|
negative-covered high ordinary vertices can have degree6 or7. These options
are independently derived from B(e_i)=4-2(d_i-2n_i-u_i).

If two degree3 lows c,v are adjacent, the link of c is a triangle{v,a,b}.
The triangles cva and cvb already use two of v's three incidences. Evenness
of pairs va and vb forces the third triangle to be vab. Thus a full
tetrahedron boundary is present, exhausting every face at c and v. Any
additional low adjacent to either belongs to this same tetrahedron.

Deleting this tetrahedron leaves a binary cycle. A high vertex in it cannot
have final degree4 or5, since deletion would leave degree1 or2, impossible
for a nonempty simple even vertex link. Degree3 is forbidden by the singleton
options. Hence such a high vertex must have final degree6 or7.

For two lows, the only adjacent-low case is the tetrahedron on the two lows
and both negative-covered highs. For three lows, a two-low component would
need two degree-at-least6 highs but only one exists. The only adjacent case
is the tetrahedron on all three lows and that single high. In either case
it is precisely the tetrahedron on the four negative-covered ordinary
vertices. Its four faces contain lows and are disjoint from a cycle on H.

Otherwise all low vertices are mutually nonadjacent. Each has a triangle
link entirely in H. Toggling its tetrahedron removes it. Repeating gives a
cycle Z on H. Conversely, starting with Z, toggle every low's tetrahedron
in a fixed order, retaining both states of its high link triangle. Restoring
a low increases the face count by2 or4 and every affected high degree by1
or3. Repeated link triangles are permitted. This reconstructs every isolated-
low family; the non-isolated families are exactly the single exceptional
tetrahedron case above.

Degree counting gives Q=2+2a and P=Q+8, where a counts active apices, so the
maximum face count is14. Isolated-low bases have at most14-2|L| faces; the
exceptional-tetrahedron bases have at most10. All high base cycles are covered
by the complete20-bit coning basis. Monotonic high degrees justify upper-bound
pruning during restoration. Forbidden negative faces are tested only on the
final family, since a high base face may be toggled away.

The producer enumerates high faces and updates degrees incrementally. The
independent reader instead expands the cycle basis in the full120-face
ambient coordinates, reverses the restoration order, toggles full tetrahedron
bitmasks, and recomputes degrees by bit counts. It does not use the producer's
remaining-degree reachability prefilter. It matches complete candidate sets
and checks every rejecting input or every1024-input survivor. Both methods
are checked against exhaustive six-vertex cycle spaces; explicit controls
include a triangular bipyramid and octahedral cycles with full tetrahedron
components on two and three low vertices.

| Negative family | Degree-bounded families | Degree/count/forbidden-face candidates | Scalar survivors |
|---|---:|---:|---:|
| [13,50] | 1290 | 1122 | 220 |
| [13,98] | 3197 | 2523 | 1035 |
| [37,74] | 3197 | 2330 | 751 |

These nonempty catalogs provide necessary cubic projections only. They do not
construct a Boolean function on14 variables or exclude the three positions.
Acceptance requires the independent manifest
parent00-multiple-low-cycle-catalogs-independent-manifest-cycle119.json.
Reproduce its complete enumeration with a fresh output path:

    python verify_multiple_low_cycles.py --output /tmp/multiple-low-audit.json

Use the exact research environment. The elementary cycle argument is not
claimed as a new general theorem; the global existence question remains open.
