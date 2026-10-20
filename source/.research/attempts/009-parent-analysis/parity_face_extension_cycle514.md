# Exact parity extension from one face

GLOBAL STATUS: OPEN. This lemma describes a possible stronger model; it
does not exclude a case, construct the target, or claim novelty.

Let s be r sign variables, t one further sign variable, and p in {0,1}.
Every function q(s) has a unique extension H satisfying H(s,1)=q(s) and

    H(-s,-t) = (-1)^p H(s,t).

Indeed the other face is forced to be H(s,-1)=(-1)^p q(-s). If
q(s)=sum_A a_A chi_A(s), its multilinear representation is exactly

    H(s,t) = sum_A a_A chi_A(s) t^b(A),
    b(A) = (p-|A|) mod 2, with b(A) in {0,1}.

The supports A with and without t are distinct, so no cancellation can
hide a term's degree. If d has parity p, H has degree at most d if and
only if q has degree at most d. The forward implication is restriction.
For the reverse implication, terms of degree d already have parity p;
only terms of degree at most d-1 gain the extra variable t.

The parity qualification is essential. When d has the other parity,
q(s)=chi_A(s) with |A|=d instead has extension of degree d+1. More
generally the required face-degree bound is the largest integer at most d
with parity p (only the zero polynomial is allowed if this bound is
negative). Booleanity, if imposed on q itself, is also
preserved by the forced second face. No such Booleanity is asserted for
individual core coefficient functions below.

For a self-dual Boolean f, put h=1-2f. Expand in four core sign variables z:

    h(z,y) = (1/16) sum_C B_C(y) chi_C(z).

Since h(-z,-y)=-h(z,y), coefficient uniqueness gives
B_C(-y)=(-1)^(|C|+1) B_C(y). Degree at most five gives
deg(B_C)<=5-|C|, whose parity is exactly |C|+1 modulo two.
Consequently a nine-variable face of the ten-variable outside cube,
together with this parity, captures the full degree condition for each
B_C without any extra degree cost. This can couple both apex orientations,
unlike fixing both apices in the current eight-variable slice model.

This applies only within the already proved existence reduction to
self-dual functions (`selfdualization.md` and its accepted reductions).
It does not assert that every original candidate is self-dual, nor that
the selected-slice zero-product rule holds on other apex orientations.
Any new full model must reconstruct those other core-word pools with
their actual quartic term, weight guards, and complete component domains.
The current exact 256-point model and its authorities remain unchanged.
