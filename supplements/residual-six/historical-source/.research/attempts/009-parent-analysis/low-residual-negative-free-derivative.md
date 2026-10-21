# The negative-free derivative theorem with residual defect at most two

This is an accepted necessary-condition theorem for the two remaining
self-dual representatives. It does not resolve the original existence
problem. The reduction to a self-dual representative is existence-preserving;
no claim is made that every original function is self-dual.

Use g=1-2f and integer Fourier numerators k_S=16 g-hat(S). After fixing
all negative quintic numerators, suppose the remaining Fourier defect
budget is at most two. For the one-zero-pair representative the total
budget is 16; for the no-zero-pair representative it is 28. The defect
costs are

    singleton: (k-1)(k-2),   cubic: k(k+1),   quintic: k(k-1).

All these costs are nonnegative even integers. The baseline domains are
singleton {1,2}, cubic {-1,0}, positive quintic {0,1}. Thus the only
possible deviation after fixing the negatives is one singleton 0 or 3,
one cubic -2 or +1, or one positive quintic 2. Two deviations cannot
coexist within the stated residual budget.

Let v occur in no negative quintic and, if there is a zero pair e, assume
v is outside e. The derivative p=partial_v f takes values in {-1,0,1},
has p(0)=1 and p(e_w)=0 for all thirteen remaining coordinates, and
has the even Fourier expansion

    16p=k_v + sum_(|A|=2) k_(A+v) chi_A
             + sum_(|B|=4) k_(B+v) chi_B.

In the no-zero-pair case all its ordinary quadratic coefficients are
Boolean. In the one-zero-pair case this holds except possibly at e,
where the coefficient is 1+f(e+v). Consequently, if f(e+v)=0,
all ordinary quadratic coefficients again belong to {0,1}.

There are four exhaustive derivative cases:

1. Baseline quadratic and quartic Fourier domains, allowing constant
   k_v<=3. The original derivative obstruction excludes this.
2. One quadratic Fourier coefficient +1. The one-positive-quadratic
   extension excludes this.
3. One quadratic Fourier coefficient -2. The topology reduction gives
   three possible endpoint links. The compact certificates contain
   71,60,97 exact Boolean deductions, respectively, and prove all three
   impossible. Their independently reconstructed 230 literal rows contain
   no global face-count assumption, so the result holds for k_v<=3.
4. One doubled positive quartic Fourier coefficient. The elementary
   vertex-link Euler-characteristic-three argument excludes this.

These cases cover deviations either incident with v or elsewhere; a
deviation elsewhere leaves a baseline derivative. The independent audits
are in attempt008:

- `negative-free-derivative-catalog-audit.md`;
- `one-positive-quadratic-derivative-independent-audit.md`;
- `one-negative-quadratic-compact-exclusion-audit.md` and
  `one-six-edge-compact-independent-verification.json`;
- `doubled-positive-quartic-derivative-independent-audit.md`.

Therefore in the one-zero-pair case **every negative-free nonendpoint
v satisfies f(e+v)=1**, regardless of where the remaining two defect
units are spent. If S is the union of negative quintic supports and
d_H(e) is the number of zero extensions, this gives

    |[14] minus (S union e)| <= 12-d_H(e).

In the no-zero-pair case, the existence of any negative-free coordinate
is impossible: **the negative quintic supports must cover all fourteen
coordinates** under the stated residual-budget hypothesis.

The first two cases explicitly use the complete published enumeration
of 4,787 small-valence three-manifolds, Frick (2015), Theorem 3.10,
<https://d-nb.info/1076082246/34>, with data at
<https://www3.math.tu-berlin.de/IfM/Nachrufe/Frank_Lutz/stellar/3-manifolds.html>.
Its historical completeness computation is an external theorem and has
not been independently regenerated here. The third case uses the
separately covered small-sphere catalogs and exact interval certificates;
the fourth is elementary. All four are stronger than numerical or
uncertified solver infeasibility statements.
