# Conditions for transferring a cubic catalog beyond C4

GLOBAL STATUS: OPEN. This records a route to a future transfer; no new
parent or geometry exclusion is asserted.

Assume the established four-negative-double/two-positive-double spectral
family, with g=1-2f=(1/16) sum k_S chi_S, and let K be the four common
coordinates of the positive quintics. Suppose two disjoint pairs in K
are safe and have the previously proved row pattern. The matching lemma
in cycle 224 forces every core Fourier component of size three to vanish
at every outside input. Orthogonality then forces every global k_S with
|S intersect K|=3 to be zero.

For a pair C in K, the component B_C is an odd cubic on ten outside
coordinates. Its singleton coefficients are in {-1,0}; its cubic
coefficients are in {-2,0,1}. Write P for the positive triple family, N
for its negative triples, and Q for the number of singleton coefficients
equal to -1. The degree-five positive doubles have four core coordinates,
so they do not occur in B_C.

The layer guards and matched core-word identity imply B_C(0)=4. At an
ordinary outside singleton the possible values are {-4,4}; at either
apex singleton they are {0,8}. Cycle 229 checks all six core pairs and
all 65,536 literal core words independently, without importing the
row producer or the earlier literal-word enumerator. Thus

    |P| = Q + 4 + 2|N|,
    B_C(e_i) = 4 - 2(d_i - 2 n_i - u_i),

where d_i and n_i are positive and negative triple incidences and
u_i indicates a negative singleton coefficient.

The even-pair-incidence condition also transfers. The integer polynomial
H=sum k_S chi_S is pointwise either 16 or -16, so H-16 is divisible by 32
on the Boolean cube. Every integer multilinear coefficient of H-16 is
therefore divisible by 32, by finite differences. For a four-set U,
its coefficient is 16 sum_{S superset U} k_S; hence the displayed sum
is even. Take U=C union {i,j} for two outside coordinates. Terms with
three core coordinates vanish by the matching lemma, and the positive
double quintics contain only one outside coordinate. Thus the sum is
the signed incidence of the outside pair ij in B_C's triples. Negative
coefficients -2 are even, so every pair incidence in P is even.

Each nonempty vertex link of P is consequently a simple even-degree graph,
and has at least three edges. This gives d_i=0 or d_i>=3, the degree
condition used by the existing catalogs. Summing pair incidences also
shows |P| is even, and therefore Q is even. These arguments supply the
same scalar and triangle-cycle conditions without a fourth safe pair.

To use an existing catalog as an actual cover, still bind its complete
numerical scope, the negative-position type, the actual coordinate maps,
and the split of ordinary singleton values. The cycle-224 v2 inventory
shows that all six P4 cases have two missing components with compatible
negative-position types. Some third components have negative triples
avoiding both apices and are outside the existing catalog. Leave those
components to a general bounded-domain search or construct a new complete
catalog; do not silently discard them.

A prospective P4 pipeline fixes three safe rows and two cataloged missing
pair cubics, then uses literal core words to constrain the remaining
cubic. The current modular-dual and bounded-domain method applies to that
last cubic once these first choices have a complete independent cover.
The extra cubic join and the full cover remain unimplemented and unproved
as an end-to-end exclusion method.
