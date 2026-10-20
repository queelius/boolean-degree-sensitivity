# Why the fresh spectrum model covers an entire first case

GLOBAL STATUS: OPEN. This note establishes necessity of the model;
it does not assert a contradiction or a Boolean construction.

The scope is geometry 34 of the accepted self-dual empty-pair branch,
with the marked quadratic component represented by original first row
163 in the complete quotient at cycle 278. The cycle-577 independent
reader proves that every function in this first case retains its six
component patterns in domains of sizes 6912, 3896, 298, 1, 3704 and
10008. These are complete necessary domains after sound deletions,
whether or not the producer's propagation reached a fixed point.

Write h=1-2f and h=(1/16) sum_S k_S chi_S. Within the accepted branch,
the integer coefficient layer sums are A1=16, A3=-104 and A5=104, and
Parseval gives sum_S k_S^2=256. The signed geometry fixes four quintics
to -2 and two to +2. For integer t, each of (t-1)(t-2), t(t+1) and
t(t-1) is nonnegative. Consequently the singleton, cubic and quintic
energies are at least 20, 104 and 132, respectively. Their sum is already
256, so equality holds term by term. Singletons therefore have values
1 or 2, cubics -1 or 0, and ordinary quintics 0 or 1. The six exceptional
quintics retain their specified values, and the singleton sum is 16.
This argument uses the proved branch profile, not a claim that arbitrary
Boolean functions are self-dual or have this spectrum.

Let C index a character on the four-coordinate core [0,9,11,12], and let
B_C(y)=sum_z h(z,y) chi_C(z). Its full outside Fourier coefficients are
the integers k_{C union S}; the factor sixteen cancels. The outside order
is [10,13,1,2,3,4,5,6,7,8]. Self-duality gives complement parity
(-1)^(|C|+1). Fixing the last outside coordinate to zero thus retains all
information, with the unique complementary-face lift described at cycle
514. The model includes every allowed coefficient of B_empty and the
four singleton-core B_C, totaling 1406 coefficients and 1405 free flags.

The accepted matching-core lemma supplies a complete necessary catalog
of four-variable Boolean core tables: all four cubic core coefficients
vanish, and B_15=4 delta, where delta=1-y_0-y_1. The independent reader
enumerates all 65536 core truth tables and applies the actual weight
guards. At each of the 512 face points, it then retains exactly the words
compatible with the six retained component unary domains. It checks
all 12707328 component entries against their original tables and their
odd complement identities. No first-58 product-zero rule, product group,
or first-58 binary relation is used. In particular the scope is the
entire first-163 case, not a subset defined by such restrictions.

Any Boolean function in this case determines a feasible integral point
of the following equations:

1. At each face point, select its one actual core word. In each component
   block, select its one actual complete pattern. These give the word
   and pattern normalization equations.
2. At each point and component value, the selected pattern and selected
   word have the same value. The categorical distribution equations
   express these identities; an omitted category follows by normalization.
3. Expand each B_C in its full projected spectrum. For a two-value
   coefficient {lo,hi}, set k=lo+(hi-lo)u with u in {0,1}. This gives
   all value equations and the singleton-total equation.
4. Parseval on the 512-point face gives sum_y B_C(y)^2 =
   512 sum_A k_A^2. On the two allowed endpoints,
   k_A^2=lo^2+(hi^2-lo^2)u_A. Hence the model's five second-moment
   equations are necessary. They average squared word values, not the
   square of an average.

Relaxing all selection variables and spectral flags to [0,1] preserves
every such integral assignment. Dividing each integer equation by its
positive gcd also preserves it. The frozen matrix has 7205 equations
and 4250162 nonzero entries. A separate scalar implementation reconstructs
the original equations and divisors and compares every saved primitive
row exactly. File hashes identify the audited artifacts; exact row
comparison supplies the mathematical check.

An integer nonnegative combination of signed row inequalities and box
inequalities that cancels every variable and leaves a strictly negative
right-hand side would exclude this entire first case. Any such certificate
must be checked independently against the reconstructed rows. Numerical
solver status, small residuals, or a fractional feasible point do not
establish a Boolean construction or an exclusion.
