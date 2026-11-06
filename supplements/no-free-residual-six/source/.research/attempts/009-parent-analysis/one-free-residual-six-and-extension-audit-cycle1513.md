# Beyond the two-free branch: one-free types and the exact extension signature

Alexander Richard Towell, with substantial OpenAI Codex assistance. Source audit and written deductions only. No target solver, local-family/catalog enumeration, new native row or canonical ledger edit. New conclusions below are proposed for independent review; inherited authorities remain explicit.

## Current scope, not an assumed global normalization

Checkpoint1510 leaves29 original empty-pair magnitude inventories OPEN. The underlying historical findings JSON still labels30 rows open; the separately accepted1388 exclusion of(3,1,1,1,1,1) supplies the effective29-row view. The1513 receipt derives this view without editing the ledger. Negative cost is C=sum m(m+1), residual defect r=28-C.

All subsequent statements concern the accepted **existence-preserving selfdual empty-pair representative**, with f(0)=0, every singleton/pair truth1, h=1-2f and integer k_S=16*h_hat(S) at odd degrees1/3/5. An arbitrary original function is not assumed selfdual. The exact level sums are16,-104,104 and total square norm256. Costs are(k-1)(k-2), k(k+1), k(k-1) at levels1/3/nonnegative5. A free coordinate belongs to no negative quintic.

The accepted1401/1404 theorem forces negative-support union>=12 at residual<=6. At union12, accepted1409 gives the two-free signed-three-star types; those are the current26 local contexts. This note instead treats union13, where exactly one coordinate u is free. No positive-quartic complex or old local exclusion is transferred to union14, because differentiating a coordinate in a negative quintic gives a negative quartic.

## 1. Necessary one-free residual-six allocation types

At u, p=Delta_u f has range{-1,0,1}, p(0)=1, units0, integer scale16 even Fourier degrees0/2/4, and actual ordinary quadratic coefficients in{0,1}. Its constant is c=k_u. The old accepted local guards, explicitly audited1405/1409, exclude: no nonsingleton departures or one quadratic+1/-2 at c<=3; one doubled quartic at its stated unbounded-constant guard; and two nonsingleton cost2 departures at c1/2 only. The last guard is NOT enlarged to0/3 here.

The only cost2 departures are singleton0/3, cubic-2/+1, or positive quintic2. The only cost6 ones are singleton-1/4, cubic-3/+2, or positive quintic3. There is no cost4 coefficient departure.

For residual at most4, the derivative is excluded directly: baseline c1/2 sees at most two nonsingleton departures; an exceptional singleton0/3 leaves at most one, within the old c<=3 guards. Thus a one-free survivor must spend exactly6.

For three cost2 departures, every departure must meet u. If c is baseline1/2, fewer than three incident nonsingletons would hit the old two-exception guard. A singleton departure elsewhere likewise leaves at most two. If u owns a singleton departure c0/3, exactly two incident nonsingletons must remain: missing one would reduce to an accepted one-exception local case. All other singleton coefficients are baseline.

For a single cost6 departure: a missed u gives a baseline derivative. A tripled positive quintic through u is excluded by the accepted tripled-quartic lemma. A cubic+2 through u gives a simple even pair-link graph of size4m-2, either negative or2, impossible. A cubic-3 through u is not excluded by the two-free proof: only one derivative is available. Singleton-1 at u is baseline local c<=3 and excluded. Singleton4 is impossible already from the GLOBAL singleton level sum: all other13 singleton numerators are at least1, so their sum with4 is at least17>16. The apparent c4 catalog gap therefore requires no new catalog extension for this residual-six case.

The resulting conservative necessary types are exactly:

| Type | c | All residual departures |
|---|---|---|
| I |1/2|One cubic-3 containing u|
| II|1/2|Three distinct nonsingleton cost2 departures, all containing u|
| III|0/3|The singleton at u and two distinct nonsingleton cost2 departures, both containing u|

Nonsingleton cost2 means cubic-2/+1 or positive quintic2. These rows are not actual functions and impose no unproved common-pair/star geometry on the residual supports. The genuine one-free cases of the still-open residual6 inventories are(2,2,1^5),(2,1^8),(1^11). Inventories with larger residual budget are outside this classification.

## 2. Exact odd complement signature, valid only in the normalized branch

Write f(t,x)=g(x)+t*p(x), z=1-2t, and q=2g+p-1. Then

    h(t,x)=z*p(x)-q(x),  p*q=0,  p²+q²=1.

Selfduality of this REPRESENTATIVE makes p even and q odd. Thus with P=16p and Q=16q,

    k_(u union S)=P_S for even S,   k_S=-d_S for odd S not containing u,
    Q=sum_(|S|=1,3,5) d_S*chi_S.

Here all d are integers and there are1586 possible odd indices. This is a necessary odd-family restriction within the proved normalized existence branch; it is not an unproved assumption on arbitrary extensions. The unrestricted2380-variable version of1506 remains appropriate when selfduality is not established.

For all three types above, every residual departure meets u. Therefore all outside singleton/cubic/nonnegative-quintic coefficients are baseline. The exact level sums give

    sum d_(1)=c-16, sum d_(3)=84-2c, sum d_(5)=c-68.

In particular the13 singleton entries are-1/-2 with exactly3-c entries equal to-2. The cubic entries are0/1 with exactly84-2c ones. The positive quintic d entries are exactly the prescribed global negative-quintic magnitudes; every other quintic entry is0/-1. At residual6 their negative cost is22. If M is the sum of those magnitudes, exactlyM+68-c other quintic entries are-1.

The exact norms are

    ||P||²=60+6c,      ||Q||²=196-6c, c in{0,1,2,3}.       (1)

For example, ||Q_(1)||²=22-3c, ||Q_(3)||²=84-2c and ||Q_(5)||²=90-c, summing to(1). This uses C=22 and the complete incident allocation; it is not a norm claim for arbitrary local polynomials. These scalar equations exhaust the same defect accounting rather than giving a new contradiction by themselves.

Once an actual p is fixed, the sparse annihilator equations P*Q=0 are linear in d and may be supplemented by these exact signs, level sums and inventory constraints. Before p is fixed, both P and d are unknown and the multiplication equations are bilinear. Treating them as a globally known linear system would be invalid. With union14 there is additionally no guaranteed nonnegative quartic derivative complex. These are explicit failed shortcuts, not a proposal to launch a larger solver.

## 3. A concrete one-free C7 strengthening

In TypeI, the sole incident quadratic exception in p is-3. The accepted1395 local proof gives its edge ab link C7 and spherical endpoint links with one degree7 vertex and all others4/5. This local conclusion does not need a second free derivative. Remove the degree7 vertex from either endpoint sphere. The antistar is a disk with boundary7, boundary degrees3/4 and interior degrees4/5.

The accepted1399/1401 elementary disk lemma requires at least three interiors. Thus EACH exceptional endpoint has graph degree11 or12, strengthening the earlier9..12 interval. All possible interiors lie in the same four physical off-cycle coordinates. Each endpoint sees at least three of those four, so at least two off-cycle vertices are adjacent to both endpoints. They are not in link(ab)=C7 and therefore give at least two missing triangles through ab.

This deduction uses the endpoint spheres, not an unproved whole-complex manifold. Complement homology/Walkup/meridian arguments cannot yet be applied to that whole complex without an additional manifold proof. A promising subsequent source-only question is whether the ordinary4/5 plus one7-edge incidence identities force a whole sphere; no such classification or target filter is claimed here. A future endpoint price can start from only orders11/12, not repeat the excluded9/10 range.

## 4. Correction to the frozen1504/1506 norm example

The old1506 note and my frozen1504 sanity review mistakenly counted every ordinary ACTIVE edge as a Fourier coefficient-1. That is false: ordinary valence4 edges have numerator0; valence5 edges have numerator-1. The error was in a source-only extension price, not in any native CNF/LRAT or actual witness.

For a signed three-star let r be its number of negative exceptional pairs, c the constant, E=49+c, and P_count=36+c. The special quadratic sum is3-3r. If N counts ordinary Fourier numerators-1, evaluation at0 gives

    c-N+(3-3r)+(36+c)=16, so N=23+2c-3r.

Equivalently,6P_count=4(E-3)+N+3(3-r)+6r. The squared Fourier norm is therefore

    c²+N+(3-r)+4r+P_count = c²+3c+62.

For c1 this is66, leaving qnorm190; for c2 it is72, leaving qnorm184. The maximum integer coefficient magnitude is13 in either case, and support bounds are190/184 respectively. The previously stated c2 norm96/qnorm160/magnitude12 are superseded. The old algebra, coefficient counts2380/1586, normalization and exact modular-dual certificate argument remain valid.

The frozen1504/1506 files are not edited. A fresh correction receipt binds their exact hashes, and the1513 handoff reports that no matrix or witness used the bad norm and the native proof1501 is unaffected. Separately,1514 Section4 is read with its explicit fresh correction: deleting the degree3 vertex gives the octahedron-minus-cap disk; DELETE-AND-CAP gives the closed octahedron. Its degree7/valence consequences are unchanged.

## Priority chosen from the evidence

The best broad next source audit is the TypeIII guard gap: can the accepted two-nonsingleton local exclusion be proved at c0/3 using its actual ordinary-coefficient constraints and retained certificates? This potentially removes a one-free class across three still-open inventories, rather than another native two-free root. No constant widening or proof transfer is assumed.

This is an incomplete FUTURE one-free classification, not a gap identified in an accepted exclusion. The1409 guard table and allocation proof explicitly restrict two-nonsingleton uses to c1/2; its c0/3 uses have at most one nonsingleton. The earlier1382/1386 and1393 free-coordinate selections likewise avoid exceptional singleton owners when necessary, or reach the baseline/no-nonsingleton c0/3 case. Thus no previously excluded inventory is reopened by this observation, and the29-row status is unchanged. These cited authorities, rather than an imagined general constant-free local theorem, are the premises retained here.

TypeI's two near-universal endpoints give a second, sharply scoped analytic target. The global fixed-p annihilator is a useful extension test only AFTER an actual p exists; without one it supplies no justified global linear rejection. No target experiment is requested by this handoff, and no whole-pattern or global status changes.
