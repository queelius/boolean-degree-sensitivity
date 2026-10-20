# Conditional minima as one inequality certificate

Status: algebraic lemma established below. A general independent checker
for its application to the extended case-596 functional is NOT implemented.
This note does not accept any new first-case exclusion.

Let p[x,w] be nonnegative word weights with sum_w p[x,w]=1 at each face
point x, let lambda[j,r] be nonnegative complete-pattern weights with
sum_r lambda[j,r]=1 for each component j, and let 0<=z[l]<=1 be spectral
flags. Suppose valid linear equalities imply

    sum_x,w c[x,w] p[x,w] + sum_j,r d[j,r] lambda[j,r]
        + sum_l a[l] z[l] = b.

Fix a marked component k. Categorical consistency gives, for each point
x and possible marked value v,

    sum_{w: w[k]=v} p[x,w] = sum_{r: r[x]=v} lambda[k,r].

Use the appropriate feature coordinate of each word when components and
feature indices differ. The notation w[k] abbreviates that coordinate.
Let m[x,v] be the minimum c[x,w] over the complete eligible word pool
having marked value v. These pools may already satisfy independently
proved necessary unary restrictions.

For every word, c[x,w]-m[x,w[k]] is nonnegative. Multiply those differences
by p[x,w] and use categorical consistency. The word and marked-pattern
terms are at least

    sum_r (d[k,r] + sum_x m[x,r[x]]) lambda[k,r].

The remaining component groups contribute at least their complete-pattern
minima, and the flags contribute at least sum_l min(0,a[l]). Therefore
every feasible point satisfies

    b >= min_r (d[k,r] + sum_x m[x,r[x]])
         + sum_{j != k} min_r d[j,r] + sum_l min(0,a[l]).

This is an exact linear inequality, obtained from categorical and
normalization equalities and nonnegativity/box inequalities. A strict
violation is a contradiction. Complete pattern costs remain correlated
across face points: min_r sum_x is not replaced by sum_x min_r.

If a marked value v has no eligible word, categorical consistency and
nonnegativity force every pattern using that value at x to have weight
zero. Such patterns can be removed before taking the minimum. If every
marked pattern is removed, its normalization equation is contradictory.

The same proof applies after restricting the marked component to a subset
S of complete first-row representatives. In particular, if the conditional
bound for each r in S exceeds b, one certificate can exclude the union
of those cases. This offers a possible alternative to rebuilding a large
target matrix for each first row. It does not require a new optimization.

## Relation to the recorded experiments

Cycle 642 computes these conditional bounds for every one of the 292
representatives, with complete unpropagated component domains. Six of the
94 then-open cases have positive gaps. Cycle 645 recomputes bounds for a
ten-case pilot after independently verified domain deletions; all ten have
positive gaps. Their current acceptance path still uses the existing full
target matrix and independent integer-certificate reader.

For a future aggregated checker, the unresolved verification obligation is
the full extension of the source equality combination: source word and
pattern normalizations must be extended to complete target groups,
categorical rows to all matching target values, and spectral constants and
flag coefficients recomputed from the target coefficient domains. Checking
only the source columns cannot establish this extension. The checker must
also verify the complete target domain cover and every recorded minimum.

The present helper tests the bound arithmetic against direct per-case
evaluation, including feasible and infeasible scalar equations, correlated
patterns, reordered features, empty pools and large integers. These tests
support the implementation but do not replace the outstanding independent
extension audit. No priority claim is made for this standard linear
inequality argument.
