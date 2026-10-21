# Exact linear top equations and Boolean interval propagation

This reusable engine checks necessary equations. It neither constructs a
Boolean function nor decides an arbitrary extension problem. Unknown
quintic Fourier numerators must be zero or one; any other numerator must
be supplied as fixed data.

For a Boolean degree-five function, the degree-ten part of the identity
g squared equals one gives, for each ten-set R,

    sum over unordered complementary five-sets S,T in R of k_S k_T = 0.

There are 126 terms. If the three second derivatives on a core triple C
are supplied, every quintic with at least two core vertices is fixed.
For R containing C, every complementary pair has at least one fixed
factor. Consequently these are exact linear equations, without any
relaxation of a product. There are binomial(11,7)=330 such ten-sets.
Zero-valued fixed coefficients must be supplied explicitly.

The pure-Python API in `three_one_linear_top.py` is:

- `top_rows(n, fixed, required)`: `fixed` maps five-set bitmasks to exact
  integer coefficients; `required` is the core bitmask. It returns
  `{ten_set, constant, terms}` rows. A product with two unknown factors
  raises `ValueError` instead of being silently dropped.
- `propagate(rows, initial)`: each row has target zero, and `initial`
  fixes additional variables to exact integers, including negative
  coefficients. It returns literal row-index deductions, an exact
  contradiction, or an inconclusive necessary fixed point.
- `replay(rows, initial, certificate)`: separately computes row bounds
  and validates every forced bit and final contradiction.

For general allowed row totals, `three_one_top_incidence.py` exposes
`propagate(rows, initial)` and `check(rows, initial, proof)`. Rows have
`constant`, `terms` pairs `(variable, integer coefficient)`, and a finite
integer `allowed` set. All unspecified variables are Boolean. For each
variable the producer tests the interval remaining after hypothetically
setting it to zero or one. If only one value can intersect `allowed`, that
value is forced. The checker independently recomputes each hypothetical
interval by a fresh pass through the literal row. These are interval
overapproximations, so an unrejected fixed point has no feasibility
meaning beyond passing these necessary tests.

`three_one_quartet_parity.py` additionally supplies exact GF(2) elimination
for even quartet coface sums. Every contradiction or forced bit includes
an explicit subset of original parity rows. `check_xor` replays that
subset using symmetric differences of sets, independently of the
producer's integer-bitset Gaussian elimination. A separate adapter may
reuse these mechanics with its own mathematical guard and row derivation.

Controls exhaust 576 small signed interval rows, 256 finite-allowed-set
rows, and 2,048 three-variable parity systems against every Boolean
assignment. They also test a single-character positive top control,
disjoint-character negative control, the two-unknown-factor rejection,
and deliberately corrupted interval/XOR witnesses. The application
scripts in these same modules are exploratory and have their own
explicit scope; importing the generic functions does not transfer that
application scope or assert a global exclusion.
