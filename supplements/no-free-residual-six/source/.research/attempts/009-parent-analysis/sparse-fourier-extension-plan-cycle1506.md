# Exact sparse Fourier gate for a future local witness

Alexander Richard Towell, with substantial OpenAI Codex assistance.
21 October 2026. Elementary proposed extension strategy; no local witness,
new target computation, case exclusion, or novelty claim.

The active Boolean14 problem is still open. This builds on the exact fiber
criterion in `boolean-extension-next-step-cycle1492.md`. It is useful only
after an actual local ternary polynomial has been independently verified.

Let p=P/16, where P has the source-bound even Walsh coefficients on sets of
sizes0,2,4. A Boolean extension f(u,x)=g(x)+u*p(x) supplies

    q=2*g+p-1,       p*q=0,       q^2=1-p^2.

The polynomial q has degree at most5. Its Walsh coefficients are integer
multiples of1/16: the Boolean g has integer multilinear Mobius coefficients,
so its degree<=5 Walsh coefficients have denominator dividing32; twice these
coefficients, plus those of p-1, have denominator dividing16. Write
q=sum_{|S|<=5} d_S*chi_S/16, with every d_S an integer. There are2380 possible
sets S on13 coordinates. No self-duality is used here.

Multiplication by fixed p gives a sparse homogeneous integer linear system:

    sum_{U symmetric_difference S=W} P_U*d_S=0

for every W of size at most9. The normalization conditions are also linear:

    sum_S d_S=0,       sum_{S containing j} d_S=-8   (each j).

Indeed q(0)=0 and q(e_j)=1. These equations are necessary, not sufficient:
q must still have exactly the required zero and +/-1 fiber values. If the
linear system has no integer solution, this particular p cannot extend.

An inexpensive exact rejection certificate may be a vector y over an odd
prime field for the augmented linear system A*d=b, with y*A=0 but y*b!=0.
Its verifier can reconstruct A and b from exact pinned coefficients and check
the dot products modulo that prime. This excludes integer d even if rational
solutions with prime-divisible denominators exist. A numerical rank, a solver
status, or failure to find such y is not a certificate. No matrix or certificate
has been produced here.

Parseval supplies an additional small lattice budget:

    sum_S d_S^2 = 256 - sum_U P_U^2.

For the current root7,c2 native context, the prospective P has constant2,
48 ordinary coefficients-1, two exceptional+1, one exceptional-2, and38
quartic coefficients+1. Thus sum P_U^2=4+48+2+4+38=96 and sum d_S^2=160.
Consequently at most160 coefficients can be nonzero and each has magnitude
at most12. These statements are conditional on an actual p with precisely
that source profile; they do not assert its existence. A future verifier
should recompute this budget from the actual spectrum, not trust a lookup.

Only in a proved selfdual branch, or as an optional positive construction
family, may q be restricted to odd degrees1,3,5 (1586 coefficients). Rejecting
that smaller system alone does not reject arbitrary extensions. An accepted
candidate must finally verify f on all16384 inputs, with exact degree and
all14 origin sensitivities, as required by the original objective.

Next action if a local witness appears: compute its sparse multiplication
matrix, price exact modular elimination, then test linear feasibility before
encoding thousands of free Boolean fibers. Keep modular controls and any
certificate independently checkable. Until then this is a strategy note,
not authorization for another target encoding or experiment.
