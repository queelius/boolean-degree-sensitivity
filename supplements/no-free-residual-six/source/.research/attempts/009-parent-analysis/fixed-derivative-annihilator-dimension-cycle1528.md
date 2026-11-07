# A dimension limit on a future fixed-derivative Fourier test

Alexander Richard Towell, with substantial OpenAI Codex assistance.
Written linear-algebra observation. No actual derivative, matrix, solver or
new exclusion; not a claim of independent or formal verification.

Assume an ACTUAL even ternary derivative p on the13-variable cube, in the
accepted signed-three-star domain. Write P=16p. The independently corrected
Fourier squared norms of P are66 at constant1 and72 at constant2.
Parseval and p(x) in {-1,0,1} imply exactly

    |{x:p(x)!=0}| = 2^13 * ||P_hat||^2 / 16^2
                   = 32 * ||P_hat||^2,

namely2112 or2304 inputs. The evenness pairs these inputs into1056 or1152
antipodal pairs, with no fixed input under complementation.

The real vector space of odd polynomials of degree at most5 on13 variables
has dimension

    binom(13,1)+binom(13,3)+binom(13,5) = 1586.

For odd q, the homogeneous annihilator p*q=0 is equivalent to one equation
q(x)=0 per nonzero-p antipodal pair; its companion equation is redundant by
oddness. Thus rank-nullity gives the following LOWER bounds:

| constant | truth support of p | independent equations, at most | odd kernel dimension, at least |
| --- | --- | --- | --- |
| 1 | 2112 | 1056 | 530 |
| 2 | 2304 | 1152 | 434 |

Without a justified odd restriction, the degree-at-most5 space has dimension
2380. Using all support points gives kernel dimension at least268 or76.
These are bounds, not measured ranks or exact dimensions.

Since P has rational Fourier coefficients, this annihilator is a rational
linear system. Its nonzero real kernel therefore contains nonzero rational
vectors and, after clearing denominators, nonzero integer vectors. That
says nothing about the required scale16 normalization, squared norm190/184,
small integer amplitudes, support size, unit values, coefficient inventories,
or pointwise q^2=1-p^2. Most integer kernel vectors need not meet any of those.

Consequently a bare homogeneous rank/nullspace test cannot reject every
nonzero complement in this branch. A future fixed-p extension test should
retain the affine sensitivity constraints, exact norm, sign/inventory and
Boolean conditions. An inconsistent AFFINE system can still have a valid
modular left-annihilator certificate as described in1506; this observation
does not invalidate that method. It prevents expecting the homogeneous
annihilator alone to have full column rank.

The earlier incorrect norm96 would have suggested only a50-dimensional odd
kernel lower bound. Correcting it to72 raises that lower bound to434, which
materially changes the search price. No matrix or witness used the old
estimate. This is a strategy consequence of the accepted1523 correction,
not an original Boolean-function construction or nonexistence proof.

Sources: corrected source receipt fourier-extension-norm-correction-cycle1513.json;
independent authority attempts/008-sparse-spectrum-proof/
one-free-independent-authority-cycle1523.json; parent acceptance
one-free-parent-acceptance-cycle1523.json. The global14-variable problem and
all29 remaining original magnitude patterns stay OPEN.
