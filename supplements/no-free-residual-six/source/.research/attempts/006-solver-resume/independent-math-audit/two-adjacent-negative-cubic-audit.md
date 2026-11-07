# Independent audit: two adjacent negative quadratic numerators

**PASS for the stated ordinary-derivative hypotheses.** The nine compact contradictions, their complete root-link cover, and the structural transfer have been independently checked. This does not cover an ordinary quadratic coefficient two, disjoint exceptional pairs, another Fourier exception, or a constant outside {1,2}. It is a local derivative exclusion, not a complete Boolean-function decision.

The executable audit is `verify_two_adjacent_negative_cubic.py`; its report is `two-adjacent-negative-cubic-independent-verification.json`, SHA256 `12f650e0fcfc141de7195d46641342704cea93255093c20e43dbfaea4db6c090`. It uses only the standard library, imports no producer or solver code, and makes no new contradiction search.

## Hypotheses and normalization

Let p on thirteen coordinates have range {-1,0,1}, value one at the origin, value zero at every unit vector, and an even scale-sixteen Fourier representation

    16 p = c + sum_e k_e chi_e + sum_Q h_Q chi_Q.

Here c is one or two, all h_Q are zero or one, exactly two distinct adjacent k_e are -2, the others are -1 or zero, and all ordinary quadratic coefficients m_e are zero or one. These are assumptions on an individual derivative; no orbit invariance or averaging is used.

The coefficient identity is 4m_e = k_e + sum_(Q contains e) h_Q. The quartic link at a pair is an even simple graph. An ordinary pair therefore has empty, C4, or C5 link. An exceptional pair has m_e=1: m_e=0 would require a simple even graph with two edges. Its six-edge link has maximum degree two, because every triangle through it contains an ordinary pair. Hence the link is C6 or two disjoint triangles. Every present triangle belongs to exactly two tetrahedra. The coefficients are consequently the alternating face indicators of a simplicial complex K, and p(X)=1-chi(K[X]).

Writing P for the number of tetrahedra, the origin/unit identities give P=36+c and, at each vertex v, P_v=2 deg(v)-4. Thus

    f(K) = (13, 49+c, 72+2c, 36+c).

Every vertex link has characteristic two. If v meets z exceptional edges, summing the incident edge valences gives 4 deg(v)+2z <= 3P_v = 6 deg(v)-12, so deg(v)>=6+z. This yields the private-endpoint lower bound seven and the common-endpoint lower bound eight, including the two-cross-neighbor requirement used below.

## Structural coverage

At a private endpoint, splitting a disconnected exceptional edge link gives a closed surface complex of characteristic three with two degree-three vertices and all other degrees four or five. The degree-three vertices must belong to a sphere, whose disjoint three-vertex neighborhoods require at least eight vertices; the additional projective-plane component needs at least six. The split link has at most thirteen vertices. This is impossible. Both exceptional edge links are C6.

Every vertex link is now a union of closed surfaces. Each component has positive curvature, since there are at most two degree-six vertices and all others have degree four or five. A private endpoint cannot have a disconnected link: the component with its degree-six vertex would be the already excluded seven-vertex projective-plane configuration K7 minus a matching, whose octahedral-face deletion cannot have the required C6 boundary. At the common endpoint, separating the two degree-six vertices into different components invokes the same obstruction. Putting them together requires at least seven vertices there and six in the second projective plane, exceeding the twelve available. Thus these three links are spheres.

An ordinary vertex with disconnected link would give two complete six-vertex projective-plane skeletons A and B. Together with their center they use 42 edges, leaving at most nine cross edges since c<=2. Every good vertex has a cross neighbor: otherwise its order-six link would contain a vertex of degree five, contrary to the accepted order-six sphere classification. The two private endpoints also need a cross neighbor, and the common endpoint needs two, by deg(v)>=6+z. If all nine good vertices had at least two cross neighbors, the sum of cross degrees would be at least 22, whereas nine cross edges supply at most 18. A good vertex of cross degree one has the order-seven pentagonal-bipyramid link. Its cross neighbor is adjacent to all six vertices on the opposite side. The other five vertices on the neighbor's side each need another cross edge, requiring eleven. Therefore ordinary links are spheres as well. Minimum degree six forces connectivity on thirteen vertices.

The previously independent inverse-contraction sphere cover through order twelve is the finite completeness input. The new checker binds every catalog hash and independently recomputes degrees from literal faces. It obtains exactly these common-root links:

    (8,12), (9,32), (10,74), (10,75), (10,168),
    (11,499), (11,764), (12,2537), (12,5741).

Here each pair is (order, catalog index). The same fresh filter verifies all six ordinary-link sphere types are flag, and all three private-link types are flag with orders 9,10,11. These justify the local flag and private-order rows. No flagness of the common-root link or of the whole complex is imposed. Completeness comes from the accepted explicit sphere cover, not from a numerical class-count comparison.

## Literal rows and proof replay

The checker reconstructs each selected row from its mathematical support, separately from recreating the original row order. It checks 945 literal rows: 457 root-link values, 98 downward inclusions, 78 triangle-incidence equations, 97 ordinary-edge valence bounds, 102 ordinary-link flag inequalities, 63 private-link flag inequalities, two private-link order bounds, 47 induced Euler inequalities, and one no-independent-triple inequality. For example, the Euler row on X is exactly

    -|X| <= -sum_edges + sum_triangles - sum_tetrahedra <= 2-|X|,

and the local flag row uses the three link edges and their candidate face, with upper bound two. Each flag row's center is checked to be an ordinary or private vertex of the required type.

All saved original row indices match an independently assembled model. Its digest agrees with all eighteen original models, for both constants. The compact deductions are bound as subsequences of their original traces. The compact rows contain no global face-count equation and are identical for c=1 and c=2. Thus the nine proofs cover both constants; no trace for c=2 needs to be trusted separately.

Every one of the 1,111 forced binary assignments is checked by assigning the opposite value, computing the exact minimum and maximum over all still-free bits, and showing that interval misses the row's allowed interval. Each final row is then contradictory. The check neither assumes a unique propagation order nor trusts numerical tolerances.

The C4*C4 join satisfies all 1,185 independently reconstructed control rows and has induced Euler range [0,2]. The C4*C6 join satisfies the face/valence equations, but the exact range rows correctly reject it: its induced Euler range is [-1,3]. Seven corruption controls reject a wrong link ID, changed coefficient, wrong original index, incorrect forced value, noncontradictory terminal row, omitted case, and duplicated case.

The report binds the immutable pre-run note snapshot, the clarified current note, root's independent structural audit, and the accepted one-six-link and sphere-cover dependencies. The clarification that the common exceptional vertex needs two cross neighbors changes no model row. No source or producer file was modified.
