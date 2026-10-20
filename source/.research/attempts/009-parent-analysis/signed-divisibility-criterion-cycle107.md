# An exact signed divisibility criterion

Let C(z)=sum_q c_q product_{i in q} z_i have integer coefficients, including
possibly q=empty. With z_i=1-2x_i, its Boolean multilinear coefficient on T is

    (-2)^|T| sum_{q containing T} c_q.

An integer multilinear polynomial is everywhere divisible by8 on the cube
if and only if each of its Boolean monomial coefficients is divisible by8.
One direction is evaluation; the other is the integral inclusion-exclusion
formula recovering coefficients from values at subsets. Consequently C is
everywhere divisible by8 exactly when:

1. C(0 in x-coordinates)=sum_q c_q is divisible by8;
2. every vertex incidence sum is divisible by4;
3. every pair incidence sum is even.

Higher-order coefficients already contain the factor8. Signs and repeated
integer weights require no unsigned-code assumption. This proves the criterion
directly; it is consistent with the polarization viewpoint in Ward's criterion.
The independent control test exhausts17496 signed three-variable polynomials
and compares these incidence conditions with every cube evaluation.

For a missing-diagonal projection B in the actual four-cycle branch, apply
this to C=B-2(z_a+z_b). The allowed Boolean core words give C divisible by8
and B(0)=4. Thus the positive cubic supports have even pair incidences;
at vertex i, deg_P(i)-2deg_N(i)-u_i-2*1_{i in {a,b}} is divisible by4.
Summing the even pair incidences shows3P is even, hence P is even.
The origin equation P-2N-Q=4 then makes Q even. These statements justify
the parity and vertex equations of integral_missing_diagonal.py.

The exact control in missing-diagonal-one-negative-control-cycle107.json shows
that N=1 is possible for a necessary cubic projection. The criterion is not
a nonexistence proof and does not construct a Boolean function on14 variables.
