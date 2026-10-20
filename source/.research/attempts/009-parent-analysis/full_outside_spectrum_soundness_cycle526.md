# Full outside coupling with branch-specific spectral domains

GLOBAL STATUS: OPEN. This is a necessary model for the accepted self-dual,
empty-pair, four-negative-double/two-positive-double branch. It is not a
claim about arbitrary degree-five Boolean functions or a new exclusion.

## Coefficient domains follow from energy saturation

Write h=1-2f=(1/16) sum_S k_S chi_S. The already proved empty-pair profile
has odd layer sums A1=16, A3=-104, A5=104, and all other levels vanish in
the justified self-dual existence reduction. Granularity makes every k_S
integral, and Booleanity gives sum_S k_S^2=256. The current signed geometry
fixes four quintics to -2 and two different quintics to +2.

For any integer t, (t-1)(t-2), t(t+1), and t(t-1) are nonnegative. Hence
the singleton energy is at least 3*16-2*14=20; cubic energy is at least
104; and quintic energy is at least 104+4*6+2*2=132. Their sum is exactly
256, so every inequality is an equality. Thus all singleton coefficients
are 1 or 2, all cubic coefficients are -1 or 0, and all other quintics
are 0 or 1. Exactly two singleton coefficients equal 2. This also rules
out further exceptional coefficients in this branch. It does not rely on
a C4-only negative budget.

## One face captures all outside inputs

Order the four core coordinates as in the accepted component instance,
and retain the ten outside coordinates in its recorded order. Fix the last
outside bit to zero; all 512 assignments of the other nine bits remain.
For a core character C define B_C(y)=sum_z h(z,y) chi_C(z). Its complement
parity is (-1)^(|C|+1), and its degree is at most 5-|C|. The exact extension
in `parity_face_extension_cycle514.md` therefore loses no information.

A face character A on the first nine outside bits corresponds to the
unique full outside support obtained by adjoining the last outside
coordinate precisely when |A|+|C| is even. The global coefficient is k_S
for that outside support joined with C. The normalization cancels: B_C's
Fourier coefficients are these integer numerators k_S, with no extra
factor of sixteen. For C empty or a singleton, every |A|<=5-|C| is
represented, and all lifted global degrees are odd and at most five.

Use the exact one- or two-value domains proved above. A two-value domain
{lo,hi} is parameterized by k=lo+(hi-lo)u, with u a bit for a genuine
function and relaxed to [0,1] in an LP. Fixed coefficients need no flag.
The value equations link this full Fourier expansion to shared core-word
weights at every point of the nine-variable face. The fourteen singleton
flags sum to two. A numerical fractional solution is not a construction.

## Core words and the transferred zero rule

Two disjoint safe pairs force the four core triples to vanish and
B_15=4*delta, where delta=1-x_apex0-x_apex1. This is the already audited
matching-core lemma and holds at all outside inputs. The unrestricted
catalog has 152 words for delta=1, 222 for delta=0, and 152 for delta=-1.
Apply the actual weight guards, all six complete component domains, and
the projections of both complete binary relations. Do not transfer a
missing component into the safe-pair catalog.

Cycle 471 proves all three complementary quadratic products zero on apex
bits (0,1), with every other outside bit free. Each quadratic coefficient
function is complement-odd. Consequently its product with its
complementary quadratic coefficient is complement-even, and is also zero
on apex bits (1,0). Before using that transfer, check the exact odd identity
on every retained full component row; the underlying coefficient parity
also follows from self-duality. No zero-product condition is imposed on
the equal-apex slices. For a complete LP pool, none of the surviving words,
original component rows, or original binary pairs may be discarded.

## Exact second moments

For each modeled core coefficient B_C, Parseval on the nine-variable face
gives E B_C^2=sum_A k_A^2. A coefficient with its allowed two endpoints
has k_A^2=lo^2+(hi^2-lo^2)u_A. Therefore one additional linear equation per
core feature equates the average of squared word values to that affine
spectral sum. This remains necessary after relaxing the flags and word
choices. The squared word value must be averaged using the same shared
word weights; squaring their average would be a different constraint.

These identities extend the earlier `joint_core_coefficients.py` and
`generic_parseval_envelope.py` machinery. The old cycle-106 pilot used a
different fixed C4 setting, omitted the constant core coefficient, and
included C4-specific negative-count cuts. Those cuts are not transferred.
The new direction instead fixes the current geometry's exact exceptional
supports, retains its full component patterns, and includes B_0.

An independent reader must reconstruct all coordinate maps, full word and
pattern covers, coefficient domains, degree/value rows, singleton budget,
and second-moment equations. Only an exact independently checked integer
contradiction could exclude the current conditional group. An integral
global candidate would still require direct verification on all 16,384
inputs and exact degree/sensitivity checks.
