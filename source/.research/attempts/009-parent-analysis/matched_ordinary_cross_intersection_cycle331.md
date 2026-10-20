# Complementary ordinary cubic families must cross-intersect

GLOBAL STATUS: OPEN. This is a necessary restriction for the matched-core
instances whose negative cubic terms all contain an apex, including signed
geometries 19 and 34. It is not an exclusion of either geometry.

Write the scaled sign function as

    16g = sum_{S subset K} chi_S B_S,

where K is the four-coordinate core. The proved matched-core lemma gives
B_T=0 for every core triple T and B_K=2(z_a+z_b), with a,b the two outside
apices. The coefficient of chi_K in (16g)^2=256 is therefore

    B_empty B_K + B_12 B_34 + B_13 B_24 + B_14 B_23 = 0.

(Both sides of the coefficient equation have a common factor two.) Each
pair component B_C has degree at most three. On z_a=-z_b, B_K vanishes,
so the sum of the three complementary products is identically zero as a
function of the other eight outside coordinates.

Let U be any six of those eight coordinates. The Fourier coefficient of
chi_U in a product B_C B_D, for complementary core pairs C,D, comes only
from disjoint cubic supports A,B with A union B=U. A term involving an apex
has ordinary degree at most two, and a linear term has degree one, so neither
can contribute to ordinary degree six. Thus this coefficient is

    sum_{A disjoint B, A union B=U} k_C(A) k_D(B).

All ordinary cubic coefficients in the indicated instances are 0 or +1:
the only possible negative cubic coefficients have an apex. Consequently
every summand across all three complementary products is nonnegative.
Since their sum must be zero, no positive ordinary triple of one component
can be disjoint from a positive ordinary triple of its complementary
component. The two positive families must cross-intersect.

This is also a consequence of the existing exact pointwise core relations,
not a stronger assumption about the unknown function. It can improve
propagation because it excludes complete candidate combinations using a
Fourier coefficient, rather than considering each input separately.

For a finite encoding, for each unordered complementary pair (C,D) and each
ordinary triple A, append a binary relation forbidding the simultaneous
events 'A is positive in C' and 'some positive triple in D is disjoint from
A'. Both columns are deterministic functions of the existing candidate
row. Other component columns are zero. The allowed six-tuples are the zero
tuple and each of the two single-one tuples. Considering all 56 ordinary
triples in one orientation covers every forbidden pair; a second orientation
is unnecessary. There are 3*56=168 appended relations. Old candidate indices
and point columns are unchanged.

The checker must verify the nonnegative ordinary cubic coefficients and
the complementary-product identity on the existing delta=0 relation rows.
It must reconstruct the appended columns independently. This statement does
not apply without modification when a negative cubic support avoids both
apices: cancellation can then occur.
