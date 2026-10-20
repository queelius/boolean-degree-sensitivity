# Exact low-degree-link route for the remaining L=2 catalogs

This is an unimplemented strategy, not an accepted exclusion.

For L=2, the existing forced-degree-three reduction leaves at most eight
high vertices. Direct coning-basis enumeration on eight vertices has 35 bits.
However, at least one high ordinary vertex is outside all negative triples:
there are six ordinary highs, while the allowed negative family covers at
most four ordinary coordinates. Its final positive degree is four or five.
Deleting the forced degree-three links never increases high degrees.
Thus this vertex's degree in the residual high cycle is at most five.

The link of a vertex in a simple binary triangle cycle is an even simple
graph. With at most five edges it is empty or a single cycle of length three,
four, or five. On the other seven vertices there are exactly

    1 + C(7,3) + 3 C(7,4) + 12 C(7,5) = 393

such labeled links. Fix one link G. Fill G by its canonical cone K from any
fixed vertex among the seven; edges incident to that vertex contribute no
triangle. Then boundary(K)=G. Every high triangle cycle with this link has
the unique form

    cone(v,G) XOR K XOR Z,

where Z ranges over the complete cycle space on the other seven vertices.
This space has only 20 bits. Enumerating all 393 links and all 2^20 seven-
vertex cycles is exhaustive and avoids a 2^35 search. The links are mutually
disjoint classes. Weight and degree bounds can be applied in exact vectorized
integer arrays before converting survivors to ordinary triangle families.

For an efficient implementation, precompute the seven-vertex cycles in the
56-face bit coordinates of the eight-vertex simplex, along with their weights
and degrees. A cone filling has at most five faces. Toggling its faces updates
weights/degrees using membership indicators; then add the anchor-link faces.
Apply the existing maximum degree and face-count bounds. Restore forced
degree-three vertices, including the exceptional tetrahedron case, exactly
as in the already verified classification. Keep the negative-face rejection
after all restorations.

Before using this method, compare it exhaustively with the existing coning
enumeration on at most seven vertices for varied caps and anchor choices.
The independent implementation should use a different anchor/filling choice
and independently rebuild the whole face set. Record a full L=2 degree
catalog before applying any parent-specific scalar filters. This strategy
may be expensive despite reducing the dimension; measure candidate counts
and runtime before expanding all negative-position representatives.
