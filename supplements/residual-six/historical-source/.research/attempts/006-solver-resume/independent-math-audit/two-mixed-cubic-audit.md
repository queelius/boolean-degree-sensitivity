# Independent audit: adjacent mixed cubic exceptions

**PASS for both stated local cases.** The ordinary case has a complete two-link cover and exact compact contradictions. The separate ordinary-coefficient-two case follows from the checked curvature identity. This is not a statement about arbitrary placements of that special edge, other Fourier defects, or the full fourteen-variable problem.

The independent implementation is `verify_two_mixed_cubic.py`. Its report `two-mixed-cubic-independent-verification.json` has SHA256 `15ec69b56db1cacc90a5cbae8e369f0a9c5fee6f20b97d3ea4cd40bdd05a19a4`. It imports only frozen primitives from the previous independent audit, not producer or solver code. No model search was run.

## Ordinary quadratic coefficients zero or one

The assumptions are exactly those of the source note: thirteen coordinates; ternary p with p(0)=1 and every unit value zero; even scale-sixteen Fourier expansion with c in {1,2}; binary quartic numerators; pair numerator +1 at ax and -2 at bx for distinct a,b,x; all other pair numerators -1 or zero; and every ordinary quadratic coefficient in {0,1}.

Pair inversion gives 4m_e=k_e+P_e. At ax, m=0 would give P=-1, so its link has three edges and is C3. At bx, m=0 would give an impossible two-edge even simple graph, so its link has six edges. Every triangle has a baseline pair whose link has maximum degree two. Hence every present triangle has two incident tetrahedra, and the bx-link is C6 or two disjoint triangles. At its private endpoint b the accepted splitting argument applies without change and excludes the latter. All vertex links are therefore unions of closed surfaces of characteristic two.

The link of a has one degree-three vertex, the link of x has one degree-three and one degree-six vertex, and all remaining degrees are four or five. Every component has positive curvature. A projective-plane component containing the degree-three vertex would have N+N4=4 at a, or at most five at x, but a triangulated projective plane needs at least six vertices. Thus the component containing that vertex is already a sphere of characteristic two and there can be no additional positive-characteristic component. Both links are spheres. The accepted one-six-edge argument likewise makes link(b) a sphere.

The fresh sphere filter checks all relevant small orders, including the tetrahedron boundary. It verifies the necessary bounds deg(a)>=7, deg(b) in {9,10,11}. The general identity P_v=2deg(v)-4 and the incident valences 3 and6 give deg(x)>=7. The ordinary links, if disconnected, would be two complete six-vertex projective-plane components A,B. Their skeleton plus its center uses42 edges, leaving at most nine cross edges because E=49+c<=51. Every good vertex needs at least one cross edge by the order-six link obstruction. The cross degrees of a,b,x are at least1,3,1. If all nine good vertices had cross degree at least two, the sum would be at least23, exceeding18. A good cross-degree-one vertex has the accepted pentagonal-bipyramid link, so its cross neighbor meets all six opposite vertices. The other five vertices on that neighbor's side each require another cross edge. Eleven exceeds nine. Hence all vertex links are spheres.

Rooting at x gives exactly one degree-three vertex, one degree-six vertex, and other degrees four or five. Curvature gives N+N4=11, so order at most eleven. The previously independently complete sphere catalogs, re-filtered from their literal faces and bound by their accepted hashes, give exactly order8/index6 and order9/index10. Their unique degree-three and degree-six vertices fix the sign marking. Relabeling to a representative does not assume invariance of the derivative.

The independent filter also rechecks flagness of every ordinary-link type and all three private-minus link types. No flag condition is imposed at a or x. Although the complete plus-link filter here gives the single order-seven class2, the producer uses only the weaker necessary order bound7..10; no extra restriction was inserted into the replay.

## Compact rows and exact contradictions

All four original model digests are independently reconstructed. The two compact proofs contain132 rows and131 deductions. The rows consist of71 fixed root-link values,20 ordinary-edge valence bounds,20 ordinary-link flag inequalities, five private-minus flag inequalities, eleven induced Euler inequalities, and five downward inclusions. Each row is recognized from its literal mathematical support and separately bound to its recorded original index. Each compact trace is a subsequence of its bound original trace.

The compact rows use no global face-count equations and are identical for c=1 and c=2. The order-eight case uses46 rows and45 deductions; the order-nine case uses86 rows and86 deductions. For every deduction the checker tries the opposite binary value and computes the exact extremal interval over the remaining bits. The final intervals miss their allowed bounds. No numerical tolerance, symmetry assumption, or search result is used.

The C4*C4 join passes all reconstructed control rows. The C3*C6 join passes the face/valence rows and correctly fails the induced-range rows. Eight corruption controls reject a wrong sign marking, coefficient, original index, forced value, terminal row, missing case, duplicate case, and a flag constraint placed at the positive endpoint.

## Special ordinary coefficient m_ab=2

This argument is separate from the ordinary models. Assume the only ordinary coefficient two is ab, across the two exceptional edges ax and bx. The ax link is still C3. Even the triangle abx therefore has tetrahedron incidence zero or two; all other triangles have a baseline pair. Consequently every present triangle still has incidence two.

In link(a), vertex b has degree s=8 or9, vertex x has degree3, and every other vertex has degree4 or5. The origin/unit identity uses the weighted ordinary degree M_a=deg_K(a)+1 and gives P_a=2M_a-4=2deg_K(a)-2. Since every link edge belongs to two triangles, the link has characteristic one. These identities require neither a connected link nor a surface classification.

Let n count the link vertices other than b and let n4 count its degree-four vertices. Summing degrees and using characteristic one gives

    s + 3 + 4n4 + 5(n-1-n4) = 6n,
    n+n4 = s-2.

But the simple link graph gives b exactly s distinct neighbors, so n>=s. This is impossible. The independent control checks all132 relevant integer degree profiles and finds no survivor; changing the characteristic to two admits arithmetic profiles, so the characteristic-one guard is material. This proves the claimed special-edge placement without assuming ordinary-case sphere coverage.

The report preserves all producer hashes and records the accepted sphere-cover and one-six-edge dependencies. No producer, frozen source, or prior audit artifact was modified.
