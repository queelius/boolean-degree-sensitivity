# A stronger restriction from the singleton core components

GLOBAL STATUS: OPEN. This necessary restriction does not by itself exclude
a signed geometry.

Work in the established self-dual four-negative/two-positive double
spectral branch, with a safe matching in the four-coordinate common core.
Use B_S for the unnormalized Fourier component on the core subset S.
The matching lemma implies that every B_i takes values in
{0,-8,8,-16,16}. The core truth words allowed by the layer guards give
B_i(0)=0 and B_i(e_j) in {0,-8} at each of the ten outside singleton inputs.

Fix a core coordinate i. Put a=k_{i}, so a is 1 or 2. Write M for the
number of its negative quadratic outside coefficients, P for the number
of its positive unit quartic coefficients, and N for its negative doubled
quartic coefficients. There are no positive doubled quartics in B_i:
the two positive double quintics contain all four core coordinates.
Thus

    B_i = a - sum_M chi_pair + sum_P chi_fourset - 2 sum_N chi_fourset.

Let ell count outside singleton inputs at which B_i=-8. Evaluation at
zero gives P=M-a+2N. Summing over the ten singleton inputs gives

    -8 ell = 10a - 6M + 2P - 4N = 8a - 4M,
    M = 2a+2ell,  P = a+2ell+2N.

Orthogonality therefore gives the exact squared norm

    E B_i^2 = a^2+M+P+4N = a^2+3a+4ell+6N.

Every multiple of 8 satisfies t^2 >= 8t. Consequently E B_i^2 >= 8a.
If N=0 and a=2, this already forces ell>=2. If N=0 and a=1, ell=0 is
impossible; ell=1 would give equality. Equality in the pointwise inequality
forces B_i to lie in {0,8} everywhere, contradicting the singleton value
-8 counted by ell=1. Hence

    N=0 implies ell>=2.

For N>0 we use only ell>=0. The distinction is necessary: if N is the
four-set {0,1,2,3} and z_4 is another outside coordinate, the polynomial

    B=(1-z_0 z_1 z_2 z_3)(2-z_4(z_0+z_1+z_2+z_3))

takes values in {0,8}, has a=2, one negative doubled quartic, four negative
quadratics and four positive unit quartics, and vanishes at zero and every
singleton input. Thus N=1 and ell=0 can occur for a necessary component.

For a core pair C, let Q_C count its negative linear outside coefficients.
The odd cubic B_C has B_C(0)=4, so the character sum over its ten singleton
inputs is 16-4Q_C. At an outside singleton both g(core=0) and every
g(core=e_i) equal -1. Taking their difference, and using vanishing core
triples, gives

    B_i(e_j) + sum_{C contains i} B_C(e_j) + B_1234(e_j) = 0.

The ten singleton values of B_1234=2(z_a+z_b) sum to 32. Summing this
identity therefore yields

    ell_i = 10 - (1/2) sum_{C contains i} Q_C.

The final necessary restriction is

    sum_{C contains i} Q_C <= 16  if N_i=0,
    sum_{C contains i} Q_C <= 20  otherwise.

Here N_i is read directly from the actual negative double supports whose
intersection with the core is exactly {i}. Geometry 19 has N_i=0 at all
four core coordinates. Geometry 34 has N_i=(0,0,0,1) in increasing global
coordinate order. The bounds can be represented by one additional finite
relation on the six component choices. They do not impose symmetry, and
they use self-duality only in the already proved spectral branch.

`matched_core_linear_count_checks_cycle283.py` checks the required core
word values exhaustively, checks the norm/equality arithmetic for both
allowed a values, and verifies the N=1, ell=0 positive control on every
input of its five relevant variables. Instance audits must additionally
check each candidate's Q value and the complete added relation before
using this restriction in a computational exclusion.
