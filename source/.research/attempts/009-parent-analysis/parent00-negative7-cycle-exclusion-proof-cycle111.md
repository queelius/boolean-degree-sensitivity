# Certified exclusion of negative triple7 under the actual0/0 parent

The necessary reduction in parent00-cubic-cycle-reduction-cycle111.md is now
completed by an independent finite enumeration. It excludes the missing-core-
diagonal cubic polynomial with sole negative triple7 for parent0/0, and every
position mapped to it by the already verified parent symmetry cover.

The singleton value sets force the positive triangle family P to avoid vertices
3,4, have degree3 at vertex2, degree4 or5 at each of5,...,9, and degree0,4,or5
at each apex0,1. Positive pair incidences are even, so vertex links are even
graphs; a nonempty link has at least three edges. The linear flags are uniquely
determined. Degree counting and B(0)=4 give Q=2+2a, where a is the number of
apices occurring positively. Thus Q=2,4,6 and |P|=8,10,12.

Removing vertex2 and replacing its triangle link by a face gives a binary
triangle cycle Z on W={0,1,5,6,7,8,9}, with6,8,or10 faces. The neighbor face
must be present in Z: otherwise removing a complete tetrahedron from P would
leave degree1 or2 at one of its neighbors, contradicting an even link. This
argument uses no manifold or symmetry assumption on P.

Coning at one vertex gives a bijection between all cycles on W and20 arbitrary
bits. The producer enumerates all1,048,576 cycles by Gray-code updates. A separate
reader enumerates them by successive independent basis expansions in a different
ambient triangle indexing. It reconstructs every possible stellar replacement
without the producer's degree prefilter. Both enumerations agree on the complete
weight histogram and on all resulting families.

Only240 families satisfy the required degrees, forbidden positive face7,
determined linear flags, and origin count. All have Q=4; none has Q=2 or6.
Each has an exact outside input where its cubic value is forbidden by a scalar
Boolean-core enumeration of the parent domains. The independent reader checks
all240 failures using integer arithmetic and finds no survivor. This proves
the stated negative-position exclusion.

The proof data are parent00-negative7-cycle-enumeration-cycle111.json.gz.
The accepted audit is parent00-negative7-cycle-independent-manifest-cycle111.json.
Run verify_parent00_cubic_cycles.py --output NEW_PATH to replay it; the checker
imports no optimizer or SAT solver. Small complete-cycle controls, a genuine
stellar cubic projection, and corrupted value-witness controls are tested.

This replaces the earlier uncertified integer-search inference for this scoped
case. The full Q=6 search had returned UNKNOWN; the enumeration supplies a
separate complete proof. The other parent0/0 negative-position representatives
and the global14-variable existence question remain open.
