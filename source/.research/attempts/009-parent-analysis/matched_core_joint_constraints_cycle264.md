# Joint constraints for the remaining matched-core cases

GLOBAL STATUS: OPEN. These identities exclude no signed geometry by
themselves.

Let B_S be the unnormalized Fourier coefficients of a core truth word,
so B_S is the sum of g times the character on the sixteen core inputs.
A safe matching forces all four cubic core coefficients to be zero.
Its remaining fourth coefficient is B_1234=4 delta, with
delta=(z_a+z_b)/2. The accepted matching lemma gives exactly 526 possible
unrestricted core words.

At an ordinary outside singleton, the layer guards leave fifteen possible
vectors of the six pair coefficients. Each coordinate is -4 or +4.
The pairs carrying +4 form either a perfect matching (three possibilities)
or a path on all four core vertices (twelve possibilities). At an apex
singleton there are seven possible vectors: all zero, or exactly one
pair coefficient equal to 8. Cycle 264 checks these statements against
all 526 core words and separately enumerates the graph descriptions.

There is also a joint magnitude bound at every outside input. Write the
odd core part as L. By cycle 224 it is zero, one signed coordinate, or
half the sum of two signed coordinates. Its squared coefficient energy
is respectively 0,256,128. When delta is nonzero, the single-coordinate
case is impossible. The seven even coefficients other than B_1234 then
all have magnitude 4 or 12. Parseval says their squared sum is 240 or
112, respectively. Consequently at most one of them can have magnitude
12. (If L=0 there is exactly one; otherwise none.) When delta=0 these
seven coefficients are multiples of 8 and have squared sum 0,128,256.
These statements are also checked on all 526 words.

The independently checked cycle-263 scalar filter retains 57,906 of
76,144 canonical cubic spectra. Of these, only 3,546 have one negative
triple; the larger remainder has two. Both remaining geometry 19
(matching) and geometry 34 (P4) have only one-negative missing components,
all of which meet an apex. They therefore need no new negative-position
catalog before a joint experiment.

After transporting the canonical catalogs to the actual fixed negative
positions and all ordinary singleton partitions, geometry 19 has four
missing-component domains of 14,280 spectra each. Geometry 34 has domains
of 23,880,14,280,14,280 spectra. Safe components retain the existing 4,256
row choices. The candidate totals are domain sizes, not counts of Boolean
functions. Cycle 264 records every low-set map and source catalog index;
it has not yet independently audited this new actual-domain assembly.

The next experiment is a finite constraint problem with six variables,
one for each core-pair component. A variable selects a complete outside
cubic from its covered domain. At every outside point, their six values
must be the pair coefficients of an allowed core truth word, with the
actual delta and layer guards. This retains joint signs and magnitudes,
not just scalar intervals. Bitset domain propagation and a bounded exact
search can produce either a checked inconsistent search tree or a tuple
of necessary component functions.

A consistent six-component tuple still is not a Boolean construction.
The empty and singleton core Fourier components must also admit compatible
outside polynomials with the required degree, coefficient domains, and
the actual remaining negative supports. Such tuples must be passed to
that completion check. A bounded search returning UNKNOWN is inconclusive.
