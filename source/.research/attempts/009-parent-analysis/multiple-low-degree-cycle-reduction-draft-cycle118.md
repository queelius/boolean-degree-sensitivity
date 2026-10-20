# Draft reduction for the three remaining larger N=2 cubic positions

This is a proposed next complete enumeration, not an accepted exclusion.
Audit the argument, test on complete small controls, and independently replay
the resulting catalogs before changing a frontier.

For parent0/0, the unenumerated positions are [13,50], [13,98], [37,74].
Both apices have negative incidence1. Let L be the negative-covered ordinary
coordinates among{2,3,4}; these have forced positive degree3 and linear flag1.
The other coordinates in{2,3,4} are absent. The common remaining coordinate
set is H={0,1,5,6,7,8,9}. There are3 low vertices for [13,50] and2 for each
of the other two positions. These facts should be regenerated from singleton
scalar sets and the negative incidences, not hardcoded as separate models.

Every positive-triangle family is a binary2-cycle. A degree3 vertex c has a
triangle link T. Toggling the tetrahedron boundary on c union T removes all
faces containing c and leaves a binary2-cycle. For another degree3 vertex v
in T, the reduced degree is either2 (if T was absent in the original family)
or0 (if the full tetrahedron was present). Degree2 is impossible in a nonempty
simple even vertex link. Hence another forced-low vertex is either unaffected
at degree3 or becomes absent. A low vertex that is absent cannot lie in a
later removal link. Removing L in a fixed order therefore encounters only
degrees0 and3, and ends with a cycle Z supported on the seven coordinates H.

Conversely, reverse the fixed removal order. Start from any binary2-cycle Z
on H. At each low coordinate c, either leave c absent or toggle a tetrahedron
on c and a triple T of H plus already processed low coordinates. T must avoid
low coordinates currently at degree3: the toggle increases a neighbor degree
by1 if T is currently a face, and by3 otherwise. An inactive processed low
coordinate may be included; then T is necessarily absent and it becomes
degree3. At the end require every low coordinate to have degree3. This retains
the cases where two or three low vertices belong to the same tetrahedron;
simply applying only stellar subdivisions would miss them.

This reverse process is complete because deterministic forward peeling
recovers its choices from every final family. Distinct reconstruction paths
should be checked for duplicate final families rather than assumed distinct.
Positive degrees of high vertices only increase under restoration, so pruning
when a current high degree exceeds every allowed final degree is sound.
Face counts likewise only increase, by2 or4 per restored center.

If a is the number of active apices, degree counting for every N=2 position
gives Q=2+2a, hence Q in{2,4,6} and P=Q+8 in{10,12,14}. To verify: the
low vertices contribute3r; the five high ordinary vertices contribute
20+2(4-r) plus their linear flags; active apices contribute4a plus their
linear flags; Q includes r low linear flags. The total is28+4a+Q=3P.
This provides a cheap face-count filter independent of r=|L|.

Enumerate the seven-vertex base space with its20-bit coning basis, then
recursively restore at most three low vertices using both face states and
the skip option. This avoids enumeration of all2^35 cycles on nine vertices
or2^56 on ten. The cost depends on the intermediate degree filters and
should be measured with a small deterministic pilot before an exhaustive run.

Suggested controls: compare the reverse procedure with exhaustive binary
cycle spaces on five/six vertices for all selected low sets; include a
tetrahedron with two and three low vertices, a stellar subdivision, disjoint
tetrahedra, and a positive cubic control. The independent replay should use
full ambient face bitmasks and directly recomputed degrees, rather than the
producer's incremental neighbor-degree updates.
