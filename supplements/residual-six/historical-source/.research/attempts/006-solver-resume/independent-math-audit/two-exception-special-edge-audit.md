# Independent audit: two exceptions with a doubled positive quartic

**PASS.** The local theorem in `009-parent-analysis/two-exception-positive-quartic-special-edge.md` is sound under its stated coefficient and range hypotheses. The exact source hashes, independent controls and predecessor bindings are recorded in `two-exception-special-edge-independent-verification.json`; the standalone checker is `verify_two_exception_special_edge.py`. No producer module or research solver is used.

This audit also accepts the stated conditional residual-four covering consequence. It does not by itself bind or exclude any support family, and does not resolve the original Boolean-function problem.

## Coverage and local arithmetic

The independent support enumeration checks all 255,255 unordered pairs of distinct four-sets on thirteen vertices, with a fixed special pair. Exactly 165 pairs have no private vertex outside the special pair; they are precisely two four-sets consisting of a common triple and the two separate special endpoints. For a doubled four-set and an exceptional quadratic pair, all 55,770 placements are checked. The 55 placements without a usable private vertex are precisely the disjoint exceptional/special pairs whose union is the doubled four-set.

In every other placement the previously audited private-vertex argument applies using only coefficients incident to that vertex. The exceptional ordinary coefficient and any other numerator exception lie away from it. Its unit link has exactly three degree-three vertices, all other degrees four or five, and Euler characteristic three on at most twelve vertices. The source and its earlier independent acceptance are hash-bound, rather than assuming that a global coefficient restriction survives differentiation.

For an ordinary baseline pair in one doubled four-set, the residual unit link has exactly three edges and is a triangle. In two doubled four-sets its residual unit link is empty. In no doubled four-set the link is empty, a four-cycle or a five-cycle. These statements follow from `4m=k+weighted incidence` and even vertex degrees; the checker also exhausts every six-vertex graph with at most five edges.

In the residual two-double placement the forced four unit tetrahedra either immediately coincide with a doubled tetrahedron, put a unit face through a pair contained in both doubled tetrahedra, or force a triangle in an ordinary no-double pair link. All 45 normalized choices for the two additional vertices are checked. This covers the remaining placement without an unstated disjointness assumption.

In the mixed placement, `k_xy=+1` is impossible by residual unit-link size. For `k_xy=-2`, **both** `m_xy=0` and `m_xy=1` must initially be retained. For each of the four triples inside the doubled four-set, a unit extension forces a triangle in an ordinary pair link outside that set. The checker verifies all 144 normalized forced patterns. Therefore there are no such unit extensions. Evaluation at the doubled four-set gives `p(D)=1+m_xy`, so the range restriction forces `m_xy=0`. Discarding that case by an earlier size assertion would not be valid; the source correctly treats it.

## Final mixed-case parity argument

The unit link at a special endpoint has Euler characteristic two. The other special endpoint has degree six or seven, the two exceptional-pair vertices have degree three, and every other vertex has degree four or five. The two degree-three vertices are nonadjacent to the special vertex and to each other. The curvature equation forces respectively nine or ten vertices, with every remaining vertex having degree five.

Deleting the special vertex leaves a four-vertex path as the link of each of its neighbors. Its two boundary neighbors are the ends; its two interior-edge neighbors are the middle vertices. Let `x` be either interior degree-three vertex. At each neighbor of `x`, exactly one face through `x` has no boundary edge. Consequently the number of incidences of such faces with neighbors of `x` is three. Each such face contributes two incidences, a contradiction.

Equivalently, these faces would select a perfect matching in the triangular link of `x`. The checker verifies the local path assertion in 2,400 labeled configurations and checks that the triangular link has no such matching; a four-cycle has two, providing a positive control. This reasoning uses neither connectedness of the deleted vertex's link nor a surface classification at that vertex. In particular it remains valid when its link is two disjoint triangles.

## Global transfer and limits

After all negative quintics are fixed, residual defect at most four allows singleton numerators only in `{0,1,2,3}` and at most two nonsingleton exceptions, each costing two. The accepted one-exception theorem applies locally even if singleton exceptions occur at several other coordinates: those exceptions disappear from the derivative, and the remaining constant is the differentiated coordinate's singleton numerator, at most three.

Thus every negative-free nonendpoint must lie in two nonsingleton exceptions. If there are two, they exhaust the residual budget and all singleton numerators are baseline. If either exception is a doubled positive quintic, the previously accepted ordinary-coefficient theorem excludes the special coefficient one and the present theorem excludes coefficient two. There can then be no negative-free nonendpoint. Otherwise both exceptions are distinct cubic supports, whose intersection has size at most two. This proves the stated covering bound and the stronger empty-free-set conclusion in the positive-quintic cases.

The new local proof requires no bound on the Fourier constant and uses no manifold census. The global transfer retains the explicit external dependencies of the already accepted one-exception theorem. All ten artifacts in that theorem's manifest are hash-checked. New support-family or orbit exclusions require a separate literal binding audit.
