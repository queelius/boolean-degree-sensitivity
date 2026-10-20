# Existence reduces to three self-dual cases

This reduction preserves existence. It does not assert that every original
candidate function is self-dual. In particular, the previously cataloged
nonzero even projections are valid necessary forms for the original f.

## Lemma for every odd degree

Let f be Boolean of real multilinear degree at most an odd integer d.
Assume f(0)=0, f(1)=1, f(e_j)=1 for every j, and at most one complementary
unit input `1-e_j` has value1. Choose i to be that exceptional coordinate
when it exists, and choose any i otherwise. Put

    h(x) = 1-f(x)-f(1-x),
    F_i(x) = f(x)+(1-x_i)*h(x).

Then F_i is Boolean, self-dual, has real degree at most d, and has the
same full sensitivity normalization at the origin.

Indeed, on the face x_i=1 it equals f(x); on x_i=0 it equals1-f(1-x).
It is therefore Boolean. Since h(1-x)=h(x),

    F_i(x)+F_i(1-x) = f(x)+f(1-x)+h(x) = 1.

The complement-even projection h has no odd Fourier levels. As d is odd,
its real degree is at most d-1. Thus `(1-x_i)*h` and F_i have degree at
most d, also after multilinear reduction.

Finally `F_i(0)=1-f(1)=0`, `F_i(e_i)=f(e_i)=1`, and, for j different
from i, `F_i(e_j)=1-f(1-e_j)=1` by the choice of i. This proves the lemma.

In Fourier language, if g=1-2f=p+h with p complement-odd and y_i=1-2x_i,
the transformed sign function is `g_new=p-y_i*h`, which is entirely odd
and still has degree at most d. This also gives a direct exact spectral
implementation of the transformation.

## Application to the fourteen-variable question

The saved complete necessary layer reduction leaves twelve profiles.
All twelve have B14=1. Exactly two have B13>1:
`(B2,B3,B4,B5)=(91,231,287,274)` and `(91,232,296,310)`.
Both were rigorously excluded by the spectral hypergraph repair bounds
in attempt008; every remaining profile has B13<=1. These are established necessary conditions
for any actual Boolean function, so the lemma applies to every remaining
candidate. If any solution exists, a self-dual solution exists.

A self-dual function must have `B_t+B_(14-t)=binom(14,t)` on every layer.
Applying this condition to the complete saved profile list leaves exactly

1. `(89,218,258,268)`, Fourier layer sums `(0,20,0,-112,0,108)`;
2. `(90,226,285,316)`, Fourier layer sums `(0,18,0,-108,0,106)`;
3. `(91,234,312,364)`, Fourier layer sums `(0,16,0,-104,0,104)`.

The first has two zero pairs. The adjacent configuration is already
excluded, leaving two disjoint pairs. The second has one zero pair; the
third has none. Coordinate relabeling gives one graph representative for
each. These three self-dual cases cover existence of all original
candidates. Proving all three impossible would settle nonexistence;
constructing any one of them and verifying it would settle existence.
Neither outcome has yet been achieved.

## Controls and qualifications

`selfdualization.py` exhausts all2048 normalized four-bit Boolean tables,
retains those of degree at most3 satisfying the lemma's hypotheses, and
checks the transformation with exact Mobius coefficients and every input.
The tests also demonstrate why each qualification matters: more than one
bad complementary unit can lose sensitivity, f(1)=0 changes the origin,
and even input degree can rise by one.

    python selfdualization.py
    python -m pytest -q test_selfdualization.py

The general argument above is independent of the finite controls. Primary
literature is being checked for prior use of this transformation; no
novelty claim is made here.
