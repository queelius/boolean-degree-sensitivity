# Shared Boolean core words for a safe matching

GLOBAL STATUS: OPEN. This lemma explains a possible extension of the
current C4 method. It excludes no signed geometry by itself.

Fix the ten outside variables and let g=1-2f be a Boolean sign function
of the four remaining core bits. Write its normalized core Fourier
coefficients as a_S, and set B_S=16 a_S. For a core pair ij with
complementary pair kl, the mixed difference of f is

    D_ij f(z_k,z_l) = -2(a_ij + a_ijk z_k + a_ijl z_l + a_1234 z_k z_l).

The safe-row pattern (t,t+delta,t+delta,t) therefore forces a_ijk=a_ijl=0
and B_1234=4 delta. Two disjoint safe pairs force all four core coefficients
of size three to vanish. Conversely, if those four coefficients vanish
and B_1234=4 delta, every core pair has that same derivative pattern for
its own t. Here delta is fixed by the two outside apices and lies in
{-1,0,1}. This equivalence uses neither symmetry of f nor a new
self-duality assumption.

Consequently a safe matching, a P4 containing that matching, and a C4
give the same unrestricted family of core truth words. The literal
mixed-difference enumerator and a separate full character transform agree
on all 65,536 four-bit truth tables, selecting exactly 526 words. Layers
and specified row values are additional restrictions, as in the existing
pipeline; equality of the unrestricted families does not identify their
row catalogs or global spectral geometries.

There is also a useful exact form for the odd part of g on the core.
With the three-coordinate coefficients zero,

    (g(z)-g(-z))/2 = sum_i a_i z_i.

This linear polynomial takes values only in {-1,0,1}. Flipping one sign
shows that 2a_i is integral. Its maximum absolute value is sum_i |a_i|,
which is at most one, and its values are integral. Hence it is zero,
one signed coordinate, or half the sum of two signed coordinates.
Equivalently the nonzero magnitudes among B_i are (), (16), or (8,8).
When delta is nonzero, the single-coordinate alternative is impossible:
its absolute value is one everywhere, forcing the even part to vanish,
contradicting B_1234 != 0. The exhaustive check verifies these cases too.

This also counts the words without enumeration. When the odd part is
zero, the even part is a free sign on each of eight antipodal pairs.
The fourth Fourier numerator is twice a sum of eight signs, so its
allowed values select C(8,3)+C(8,4)+C(8,5)=182 words. For a half-sum of
two signed coordinates there are 6*4 choices of the odd part. Its even
part vanishes where the odd part is nonzero, and is a free sign on the
four remaining antipodal pairs. The analogous count is
C(4,1)+C(4,2)+C(4,3)=14, giving 336 words. The eight signed-coordinate
words complete the total 182+336+8=526. There are 152 words for each
delta=1 and delta=-1, and 222 for delta=0.

The first transfer probe made an overstrong hypothesis: every missing
pair's negative triple pattern would belong to the existing C4 catalog.
The assertion correctly failed. That source and log are preserved as
`matching_core_word_lemma_cycle224.py` and `cycle224-lemma.log`.
For example, geometry 12 has a missing pair whose one negative outside
triple contains neither apex; geometry 81 has a missing pair with two
negative triples both avoiding the apices. Those patterns are outside
the existing catalog's proven scope.

The corrected v2 inventory finds that each of the six P4 geometries still
has at least two missing pairs within the catalog's negative-pattern
types: a single triple meeting an apex, or two disjoint triples meeting
opposite apices. A future P4 method can seek to fix two cataloged cubics
and leave the third to the unrestricted bounded-domain check. Establish
the actual position covers, singleton bounds, and all transport hypotheses
before transferring any catalog authority. The matching geometry has
four such missing pairs and would need an additional cataloged component.
These are next-step deductions, not accepted parent exclusions.
