# 018 scoping: the no-free (union 14) residual <= 6 case

Claude Code (Anthropic), 2026-10-23, for Alexander Richard Towell. The
source theorems cited here are OpenAI Codex-assisted work. This file is a
reading-only scoping note: no solver, search, enumeration or experiment
was run, no existing file was edited, and nothing here is accepted. Global
status: OPEN.

Path abbreviations as in the handoff: `H` = `attempts/009-parent-analysis`,
`A` = `attempts/008-sparse-spectrum-proof`, `S` = `attempts/006-solver-resume`,
all relative to `.research/`. "Accepted" means bound by an authority or
acceptance file. "Derivation (018)" marks my own short arguments in this
note. They are unreviewed, though each one restates an accepted instance.

## 0. Headline findings

1. **The no-free residual <= 6 case is not a small leftover.** It is
   exactly the 22 still-open empty-pair magnitude inventories with
   remaining defect <= 6, with negative-support union 14 now forced in
   every one of them. For the 19 inventories with residual <= 4 this
   was already an accepted theorem (residual-four cover, Section 2.1). For
   the 3 with residual 6, it follows from 1404 + 1531 + 1533. So union 14
   at residual <= 6 is 22 of the 29 open original patterns. The other 7
   open patterns have residual 8 to 12.
2. **Two of the 22 were attacked pattern by pattern, under exactly this
   union-14 condition, and stalled.** These are (2,2,2,2) (67 support
   classes, 52 excluded, 15 open) and (3,2,1,1,1,1,1) (hundreds of
   conditional local patterns still open). See Section 4. Enumerating
   support configurations does not scale to the unit-heavy inventories,
   which have 8 to 14 supports.
3. **What breaks** is every whole-derivative theorem. They all need a
   derivative with no negative quartic (THEOREM.md line 207). **What
   survives** is every global Fourier/Boolean identity. Also surviving
   are the H130 zero-triple Turan framework, connectivity and Johnson
   component bounds, the top (degree-ten) convolution, and the
   incidence-local derivative lemmas at vertices that avoid the negative
   quartics. The last group includes the Lemma 2 private tip, the
   origin/unit identities and the vertex-link deltahedra.
4. Recommended first steps are in Section 5. In short: (a) write a typed
   frontier for the 22 rows; (b) analyze the existing n=13 witnesses as
   controls (analysis of saved data, not a search); (c) prove by hand a
   **one-negative-quartic derivative lemma** at a coordinate in exactly one
   negative quintic; (d) only then count union-14 support classes for the
   small-N inventories.

## 1. Residual defect: statement, hypotheses, cost table

### 1.1 Hypotheses (normalization)

- **Representative.** The accepted existence-preserving *selfdual empty-pair
  representative*. It is Boolean, has real degree <= 5, f(0)=0, and every
  singleton and every pair truth equal to 1. See H/one-free-residual-six-and-extension-audit-cycle1513.md
  line 9, H/three-disks-union12-proof-cycle1404.md lines 9-19,
  publication/residual6-cycle1408/THEOREM.md lines 175-187. The reduction
  itself is `findings/n14d5-current-case-reductions.md` lines 19-42 and
  `H/selfdualization.md`. It is a reduction of existence only: an arbitrary
  original solution is **not** assumed selfdual (1513 line 9, CLAUDE.md "Traps").
- **Scale.** g = 1-2f, k_S = 16*g_hat(S), chi_S(x) = (-1)^(sum_{i in S} x_i).
  Selfduality makes g odd, so only levels 1, 3 and 5 occur, with integer
  k (1404 lines 11-12; 1513 line 9).
- **Exact level sums and norm.** sum_{|S|=1} k = 16, sum_{|S|=3} k = -104,
  sum_{|S|=5} k = 104, sum k^2 = 256 (1513 line 9).
  Derivation (018), for the record: evaluating g = sum g_hat chi at 0, summed
  over units and summed over pairs gives K1+K3+K5 = 16,
  12K1+8K3+4K5 = -224 and 65K1+25K3+K5 = -1456. Hence K1=16, K3=-104, K5=104.
  Parseval for a +-1 function gives 256.
- **Free coordinate.** A coordinate in no negative quintic support (1409
  lines 37-40; 1513 line 9).

### 1.2 Budget 28 and the cost table

Cost functions (H/residual6-negative-union-theorem-cycle1382.md lines 13-19;
H/residual-six-independent-review-cycle1386.md lines 19-31):

| level | cost | zero-cost values | cost 2 | cost 6 | cost 12 | cost 20 |
|---|---|---|---|---|---|---|
| singleton | (k-1)(k-2) | 1, 2 | 0, 3 | -1, 4 | -2, 5 | |
| cubic | k(k+1) | -1, 0 | -2, 1 | -3, 2 | | |
| quintic | k(k-1) | 0, 1 | 2 (or -1) | 3 (or -2) | -3 | -4 |

The exact identity is that the total cost is 28 (1386 line 23). Derivation
(018): sum (k^2-3k+2) over singletons + sum (k^2+k) over cubics + sum (k^2-k)
over quintics = 256 - 3*16 + 2*14 - 104 - 104 = 28. A negative quintic k=-m
costs m(m+1) = 2, 6, 12, 20 for m = 1..4. Every cost is a nonnegative even
integer, and there is no single-coefficient cost 4 (1382 lines 15-19).

**Residual defect** r = 28 - C, where C = sum m(m+1) over *all* negative
quintics, fixed first (1513 line 7). Negative quintics are never residual
exceptions (1382 line 20). At r <= 6 the residual allocations are: zero to
three distinct cost-2 departures (singleton 0/3, cubic -2/+1, quintic 2),
or one cost-6 departure (singleton -1/4, cubic -3/+2, quintic 3). The
abstract allocation counts at r = 0/2/4/6 are 1/5/15/40, 61 in total
(1382 line 166; THEOREM.md lines 192-198).

The free-derivative setting is p = Delta_u f with
16p = k_u + sum_{|A|=2} k_{A+u} chi_A + sum_{|D|=4} k_{D+u} chi_D, p in {-1,0,1},
p(0)=1, p(e_i)=0, ordinary quadratic coefficient m_ij = f(uij) in {0,1}. Its
inversion identities are 4m_A = a_A + sum_{D contains A} b_D, and
sum_{D contains T} b_D is even for each triple T
(THEOREM.md lines 17-42 and 200-209; 1382 lines 22-36).

## 2. Union 14 within residual <= 6: what is forced, what is listed

### 2.1 Scope of the case (accepted chain plus ledger)

- r <= 4 implies union 14. This is an accepted necessary theorem:
  `findings/empty-residual-four-support-constraints.json` (status
  ACCEPTED_NECESSARY_SUPPORT_CONSTRAINTS, 19 covered open patterns). The
  authority is H/empty-residual-four-accepted-manifest.json, the proof
  S/empty-residual-four-cover.md lines 7-11 and 27-63, and the review
  H/empty-residual-four-parent-audit.md lines 9-36. It uses the old local
  guards at c <= 3 or c in {1,2} and inherits the Frick 2015 and small-sphere
  catalog premises (cover lines 65-68). The 1382 proof cites it only as a
  comparison (1382 lines 112-114).
- At r <= 6, union >= 12: theorem 1401/1404
  (H/three-disks-independent-authority-cycle1401.json,
  INDEPENDENTLY_ACCEPTED_RESIDUAL6_NEGATIVE_UNION_AT_LEAST12; proof
  1404 lines 21-83).
- Union 12 is excluded (checkpoint 1531, H/state-cycle1531.md lines 3-5),
  conditional on the 1409 classification (two-free review 1409 lines 14-25).
- Union 13 is excluded (checkpoints 1532/1533, H/state-cycle1533.md lines 3-9),
  conditional on the 1513/1523 trichotomy and the 016/017 lemma notes.
- Hence, conditional on all of the above, **every** residual <= 6 instance is
  a union-14 instance. This matches 1513 line 11, 1513 line 60 and the handoff
  lines 70-74 ("Unions14/no-free ... remain open").

From the canonical ledger `findings/negative-quintic-pattern-cases-cycle1388.json`
(empty_pair, budget 28), the r <= 6 inventories are the multisets over
{1,2,3,4} with C in {22, 24, 26, 28}. There are 39: 17 excluded and **22 open**.
The open ones are below. N = number of negative supports, M = sum m,
E = 5N-14 = the incidence excess sum_x (delta(x)-1) forced by union 14,
c_min = the accepted Johnson-four component bound (Section 2.2, C2),
delta_min = the largest guaranteed minimum negative degree, floor(5N/14).
"pos5" is the forced number of quintics with k=1 at r=0, namely 104+M (C5).

| r | open inventory | N | M | E | c_min | delta_min <= | prior partial work |
|---|---|---|---|---|---|---|---|
| 0 | (3,2,1^5) | 7 | 10 | 21 | 2 | 2 | large conditional tree, Section 4 |
| 0 | (3,1^8) | 9 | 11 | 31 | 2 | 3 | none |
| 0 | (2^4,1,1) | 6 | 10 | 16 | 3 | 2 | none |
| 0 | (2^3,1^5) | 8 | 11 | 26 | 2 | 2 | none |
| 0 | (2,2,1^8) | 10 | 12 | 36 | 1 | 3 | none |
| 0 | (2,1^11) | 12 | 13 | 46 | 1 | 4 | none |
| 0 | (1^14) | 14 | 14 | 56 | 1 | 5 | none |
| 2 | (3,1^7) | 8 | 10 | 26 | 2 | 2 | none |
| 2 | (2^4,1) | 5 | 9 | 11 | 3 | 1 | common intersection >= 2 excluded; size 1 gives common singleton 0 (ledger partial_reductions) |
| 2 | (2^3,1^4) | 7 | 10 | 21 | 2 | 2 | none |
| 2 | (2,2,1^7) | 9 | 11 | 31 | 2 | 3 | none |
| 2 | (2,1^10) | 11 | 12 | 41 | 1 | 3 | none |
| 2 | (1^13) | 13 | 13 | 51 | 1 | 4 | none |
| 4 | (3,1^6) | 7 | 9 | 21 | 2 | 2 | none |
| 4 | (2^4) | 4 | 8 | 6 | 3 | 1 | 67 classes, 15 open (Section 4) |
| 4 | (2^3,1^3) | 6 | 9 | 16 | 3 | 2 | none |
| 4 | (2,2,1^6) | 8 | 10 | 26 | 2 | 2 | none |
| 4 | (2,1^9) | 10 | 11 | 36 | 1 | 3 | none |
| 4 | (1^12) | 12 | 12 | 46 | 1 | 4 | none |
| 6 | (2,2,1^5) | 7 | 9 | 21 | 2 | 2 | none (union 14 newly forced) |
| 6 | (2,1^8) | 9 | 10 | 31 | 2 | 3 | none (union 14 newly forced) |
| 6 | (1^11) | 11 | 11 | 41 | 1 | 3 | none (union 14 newly forced) |

The N, M, c_min and r columns agree with the residual-four JSON for the 19
rows it covers. The magnitude list is derived from the cost table alone, so
it is already a **finite, exact list at the inventory level**. At the level
of support placements there is a complete list only for (2^4). For
(3,2,1^5) there are only unplaced component-shape tuples (57). See Section 4.

### 2.2 Constraints on configurations that are derivable now

Each item says whether it is accepted and where. All are necessary
conditions, not exclusions.

- **C1, connectivity (accepted, fully general).** The ordinary intersection
  graph of negative supports is connected for any Boolean f of degree <= 5
  (H/negative-support-components-parent-audit.md lines 3-16). Proof: on
  Q union R for supports in different components, the top coefficient of g^2
  has only nonnegative products plus the positive k_Q k_R.
- **C2, Johnson-four components (accepted).** If the N supports form c
  components under intersection-four adjacency, then
  14 <= |union| <= N + 3c + 1, so c >= max(1, ceil((13-N)/3))
  (same audit lines 18-24; S/empty-residual-four-cover.md lines 70-79).
- **C3, H130 capacity (accepted lemma; general applicability is my
  reading).** Let H be the zero-triple 3-graph. It has 364-234 = 130 edges in
  this profile (A/empty-seven-units.md line 7). For a quartet U,
  Z_H(U)-2 <= c(U) = min(2, floor(m(U)/2)), where m(U) is the sum of the
  negative magnitudes of quintics containing U (A/empty-seven-units.md
  lines 7-14). Any 130-edge 3-graph on 14 vertices has
  W(H) = sum max(0, Z(U)-2) >= 8 (A/weighted-bad-quartets.md lines 1-8, 39-40,
  premise Markstrom-Talbot catalogs, line 89). So **W_cap = sum_U c(U) >= 8**.
  This was used to exclude 6991 of 7539 seven-unit classes
  (A/empty-seven-units.md lines 26-29).
  Derivation (018) of why it holds at every residual: the ordinary quartic
  coefficient is a_U = f(U)+Z_H(U)-2 (A/empty-3211111-connected-odd.md
  line 47), and by selfduality a_U = -(1/2) sum_{Q contains U} k_Q (line 48).
  Positive quintic departures only lower Z_H(U), and cubic and singleton
  departures do not enter. For unit-only inventories, c(U) >= 1 requires U to
  lie in two supports, so there are **at least four Johnson-four adjacent
  pairs**.
- **C4, vertex deletion (accepted ingredients).** deg_H(i) = 29-k_i
  (A/empty-3211111-connected-odd.md line 12). Derivation (018) from the
  singleton, pair and triple inversion identities:
  sum_{Q contains i} k_Q = 36+k_i and sum_{T contains i} k_T = -20-2k_i, so
  4(78-deg_H(i)) = 196+4k_i. Then |H-i| = 101+k_i. If k_i >= 1, this
  exceeds ex(13, K4^-) = 101 (A/empty-asymmetric-r2-final-reduction.md line 57).
  So for every such i there is a permission quartet U, not containing i,
  with m(U) >= 2 and Z_H(U) >= 3. At r=0 this holds for all 14 coordinates.
  The per-vertex identity sum_{Q contains i} k_Q = 36+k_i means the
  positive quintics through i number exactly 36+k_i+w(i), where w(i) is the
  negative magnitude through i (r=0).
- **C5, exact baseline counts at r=0 (derivation (018) from the level sums).**
  Exactly two singletons equal 2 and twelve equal 1. Exactly 104 cubics
  equal -1. Exactly 104+M quintics equal +1, with all others 0 off the
  negatives. Parseval check: 8+12+104+(104+M)+sum m^2 = 256 if and only if
  M + sum m^2 = 28 = C. For r > 0 each departure shifts these counts by a
  known amount.
- **C6, top convolution on disjoint negatives (accepted identity; the general
  form is derivation (018)).** For every ten-set R,
  sum over unordered complementary 5+5 splits of k_S k_{R\S} = 0
  (A/notes.md lines 304-313; A/exact-linear-top-propagation-engine.md
  lines 8-11). If negatives Q, R are disjoint, then
  m_Q m_R <= sum m_S k_{(Q union R)\S}, summed over negatives S contained in
  Q union R other than Q and R. Here the complement is nonnegative, with
  k <= 1 at baseline, <= 2 or <= 3 with a quintic departure. Each such S
  meets both Q and R. At r=0: **two disjoint negatives need further negative
  mass >= m_Q m_R inside their union.** Accepted instances: Q meets P in
  (3,2,1^5) (A/empty-3211111-connected-odd.md lines 16-21); in (2^4), 50 of
  67 classes fall to this alone and one needs two forced positive doubles
  (S/empty-four-double-geometry.md lines 36-61). The same identity also
  forces a negative inside the union of any two disjoint +1 quintics.
- **C7, minimum negative degree.** Since sum_x delta(x) = 5N, some
  coordinate has delta <= floor(5N/14) (table column). For N <= 5 there are
  at least 14-E coordinates with delta = 1 (E = 5N-14). That gives >= 8 for
  (2^4) and >= 3 for (2^4,1).

**Can a finite configuration list be derived quickly?** At the inventory
level, yes, and it is the table above. At the placement level, the method
of S/empty-four-double-geometry.md lines 7-27 generalizes: Venn-cell
compositions of the excess E over the 2^N - N - 1 multi-membership cells,
then C1, C2, C3, C6 as filters. That is cheap for N = 4 (67 classes, done)
and plausible for N = 5, 6, 7. It is hopeless for N >= 9: even the
*unconstrained-union* connected 7-unit catalog already has 7539 classes
(A/empty-seven-units.md lines 18-22), and the open inventories go up to
N = 14. I have **not** run this count. It is recommended as step (d) only.

## 3. Which tools apply at union 14

### 3.1 Break (need a free coordinate or a nonnegative quartic complex)

- Every whole-derivative local theorem: BASELINE_LE3 (whole-complex manifold
  classification with the Frick 2015 premise), OLD_LOCAL_012, the 1395
  endpoint theorem in its stated form, the 1409 two-derivative common-C7
  argument, and the 1513/016/017 Type I-III machinery. Their setting
  explicitly says "No negative quartic occurs here" (THEOREM.md line 207;
  publication/residual6-cycle1408/CLAIMS.json, assumptions OLD_LOCAL_012 and
  BASELINE_LE3; 1513 lines 11 and 60).
- The 1404 three-disk argument and the 1409 shared-disk argument. They need
  |F| >= 3 or |F| = 2 free coordinates to see the same actual triangle
  families in several derivatives (1404 lines 41-83; 1409 lines 82-140).
- The 1513 one-free signature formulas with C = 22 and baseline outside u.
  The formulas sum d_(1) = c-16 and so on, and the norm (1), assume every
  residual departure meets u (1513 lines 48-58).
- Bilinear annihilator shortcuts before p is fixed (1513 line 60; handoff
  lines 125-129, 1528).

### 3.2 Survive (global; no free coordinate used)

- Level sums, the budget 28 and the cost table (Section 1).
- Inversion identities for f itself (derivation (018), same algebra as 1404
  eq. (2)): 4f(T) = k_T + sum_{Q contains T} k_Q; a_U = -(1/2) sum_{Q contains U} k_Q
  (so that sum is even); sum_{S contains A} k_S = 8 for pairs;
  sum_{S contains i} k_S = 16. So mod 2 the support of the odd quintics is a
  4-cycle in the 13-simplex, every triangle has signed valence in
  {0,1,4,5} (baseline cubic), and every vertex link (= the quartic part of
  Delta_u f) is a signed 3-complex. This is a reformulation, not a result.
- All degree 2..10 parts of g^2 = 1, in particular the top identity (C6),
  with the exact linear propagation engine once enough coefficients are fixed
  (A/exact-linear-top-propagation-engine.md lines 8-19).
- The H130/Turan framework: |H| = 130 > 126 = ex(14, K4^-), W >= 8, the
  repair and restoration lemmas (A/low-weight-repairs.md lines 1-21), and the
  G124/G123 catalogs. This was the historical engine for every excluded
  small-N inventory. It is free-coordinate independent, but its power per
  configuration falls as N grows. The static demand-two cover was a
  documented **negative** strategy diagnostic (H/static-two-cover-review-cycle1381.md
  lines 30, 40).
- C1, C2, C4, C6, C7.
- The odd/even decomposition at **any** coordinate: f = g0 + t p, h = z p - q,
  pq = 0, p^2+q^2 = 1, p even, q odd (1513 lines 37-46). The level-sum
  specializations do not carry over (3.1).
- Face-lift equivalence: n=14 existence holds if and only if an n=13 witness
  with g(1,...,1)=0 exists (attempts/012-n13-probe/FACE-LIFT.md lines 1-25).
  This is global and not union-specific.

### 3.3 Survive locally (incidence-local lemmas in a non-free derivative)

Take p = Delta_u f with delta(u) >= 1 negative quartics D = Q\{u}. Call a
vertex x of p **clean** if no negative quintic contains both u and x. At
least 13-4*delta(u) vertices are clean.

- At a clean x, every quartic through x is nonnegative. So the identities
  A_x+P_x = 8, 4d = A_x+3P_x, P_x = 2d-4 hold, because they use only
  coefficients incident with x (THEOREM.md lines 104-118). Under baseline
  incident quadratics, the vertex link at x is then a 2-sphere with degrees
  4/5, which means a deltahedron (the 017 conclusion for ordinary links,
  H/state-cycle1533.md line 5). Incident exceptions fall under the 017
  VERTEX-TYPES catalog.
- Lemma 2 (private doubled quartic) is stated to allow arbitrary
  exceptions avoiding the tip (THEOREM.md lines 71-74). It therefore applies
  at a clean tip.
- Pair-derivative (second derivative) tools with incident hypotheses only:
  the one-negative-double pair structure (S/one-negative-double-pair-necessary-structure.md
  lines 6-45; H/one-negative-double-pair-necessary-accepted-manifest.json)
  and the complete small one-negative pair catalog
  (S/single-negative-small-complete-accepted-manifest.json, 18 rows). They
  were built for (2^4) and do not assume a free coordinate.
- **Near a negative facet (derivation (018), unreviewed).** Let b_{D0} = -m,
  with incident quadratics baseline, a pair A in D0, and e = D0\A. The
  weighted link total 4m_A - a_A lies in {0,1,4,5}, so the positive edge
  count is that total + m. Parity (THEOREM.md lines 29-42) then gives:
  - m=1: the positive part is an e-endpoint path system of size 2, 5 or 6
    (size 1 would duplicate e). Mod 2, A has valence 3, 6 or 7. Valence 3
    forces f(u+A) = 0 and a_A = -1.
  - m=2: the positive part is an even graph of size 3, 6 or 7, matching one
    dimension higher the accepted pair-level list C3, C6, 2C3, theta, C7,
    C3+C4 (S/one-negative-double-pair-necessary-structure.md lines 19-41).
  - m=3: path systems of size 3, 4, 7 or 8.

  So a non-free derivative is a mod-2 3-cycle that is "deltahedral" away
  from its negative facets and has valence-3/6/7 edges on them. Valence-3
  edges are exactly where the accepted PL-sphere theorem 1507/1508 and the
  1514 sphere theorem operate (handoff lines 46-58).

## 4. Prior attempts on union 14 and what they concluded

grep over all `.md` files at depth <= 3 under `.research/` (log.md excluded
from the bulk grep, then grepped for specific lines) for union14,
"union 14", no-free, zero-free and "no free". Findings:

- **No union-14-specific general attack exists.** Every "no-free" mention
  after 1513 only records the case as open: H/state-cycle1531.md line 9;
  H/state-cycle1532.md line 9; H/state-cycle1533.md line 11;
  attempts/017-type-ii-three-exception/CERTIFICATES.md lines 13-15;
  attempts/016-one-free-type-iii/TYPE-I-CLOSURE.md line 110 and
  TYPE-III-CLOSURE.md line 103; attempts/014-context-pricing/NOTES.md
  lines 13 and 111; attempts/015-sphere-catalog-audit/REVIEW.md line 132.
- **(2^4) four-double frontier, residual 4, union 14 forced (accepted
  necessary).** The complete Venn enumeration gives 1277 weighted
  allocations, 1028 connected, 67 S4-classes. 50 fall to the direct top
  product, 16 are pairwise intersecting, and 1 forces two positive doubles
  (S/empty-four-double-geometry.md lines 7-27, 36-61; log.md line 739).
  After many local catalogs the latest frontier is
  S/four-double-frontier-cycle91.json: **52 excluded, 15 open** (classes
  24, 41, 45, 57, 60, 61, 63, 65 "common_one" and 40, 55, 56, 58, 59, 62, 64
  "no_common"), with `whole_magnitude_patterns_excluded_by_this_update: 0`.
  Class 40's 505 singleton subcases were all excluded, but class 40 itself
  stays open (log.md line 867). Conclusion: exact, certified, enormous
  effort for one N=4 inventory, and **not closed**.
- **(3,2,1^5), residual 0, union 14 (accepted conditional branches).** The
  connected-odd branch is excluded (1920 placements;
  H/empty-3211111-connected-odd-accepted-manifest.json). Q meets P in
  general (A/empty-3211111-connected-odd.md lines 16-21). The component
  reduction leaves 57 unplaced shape tuples
  (A/checkpoint-empty-3211111-components.md lines 32-54). Many role
  branches are excluded (unit-partner, isolated-unit, no-full-core
  two-safe, one clean shared-tail core pattern; H/one-clean-shared-tail-core-pattern-accepted-manifest.json,
  scope lines 50-55). The last status line reports **108 zero-safe / 642
  one-safe necessary patterns per role** still open (log.md line 860).
  Conclusion: the whole pattern is open, and the case tree branches faster
  than it closes.
- **(2^4,1), residual 2 (accepted partial).** A common intersection >= 2 of
  the four doubles is excluded. Common intersection 1 forces the common
  singleton to be 0 (ledger `partial_reductions`, citing
  H/empty-22221-common-pair-parent-audit.md and
  H/empty-2222-pair-singletons-parent-audit.md).
- **Earlier union-14 theorems at lower residual (accepted).** Union 14 at
  r <= 2 (H/negative-support-components-parent-audit.md lines 26-28) and at
  r <= 4 (Section 2.1).
- **Failed or limited approaches to keep in mind.** The static demand-two
  H-repair covers lose against adaptive repair: limit 7 fails everywhere,
  the minimum static cover is 8, and the result was "pivot"
  (H/static-two-cover-review-cycle1381.md lines 21-40). Twelve one-row
  cycle/top diagnostics reached necessary fixed points only, a limited
  negative experiment (log.md line 851). No solver UNKNOWN on a union-14
  model appears in the files read. The MILP 1493/1496 and SAT UNKNOWN runs
  concern two-free contexts (handoff lines 130-132).

## 5. Recommendation

Guiding observation: the inventory list is finite and small (22), but the
placement lists are not, for N >= 8. A plan has to cut across inventories
with a structural lemma before any enumeration.

**Step (a): typed frontier (low difficulty, about 1 cycle).** Write a new
`no-free-residual6-frontier` JSON for the 22 rows of Section 2.1. Bind the
residual-four authority, 1401, 1531 and 1533 as the reasons union 14 is
forced, and carry over the existing partial reductions ((2^4) cycle-91
frontier, (2^4,1), (3,2,1^5) branches) by pin. Keep the scopes nested and
do not sum them. Write an independent reader that rederives the 39/17/22
split from the cost table and the ledger.

**Step (b): controls from the existing n=13 witnesses (low difficulty,
cheap analysis of saved files, high information).** The 104 selfdual n=13
witness classes (attempts/012-n13-probe/REPORT.md lines 156-160) are real
degree-5 functions. For each one, compute the n=13 analogs of the k_S
spectrum, the negative-quintic union, the residual, and the derivatives at
coordinates with delta = 1. This shows which local derivative shapes with
negative quartics are *realizable*. Any proposed union-14 local lemma that
does not use a 13-coordinate count must not exclude them. A positive
control of this kind (the 16-cell at n=8) was decisive in 017
(H/state-cycle1533.md line 5).

**Step (c): one-negative-quartic derivative lemma (high difficulty, the key
lever).** Statement to aim for: at a coordinate u in exactly one negative
quintic Q, with magnitude m in {1,2,3}, constant k_u in {1,2}, and all other
incident coefficients baseline, no ternary p = Delta_u f exists. Then extend
to one or two incident cost-2 departures, mirroring how OLD_LOCAL_012 grew
from the baseline theorem. Available ingredients: deltahedral links at the
>= 9 clean vertices (3.3), the facet-pair structure (3.3, m=1/2/3), the
1507/1508 and 1514 sphere theorems for valence-3 edges, the 015
vertex-split sphere enumeration, and the 014/017 row-model plus LRAT
pipeline if a finite cover is needed. Expected reach: every configuration
that has a delta = 1 coordinate with little incident residual. That covers
all of (2^4) (>= 8 such coordinates, local incident cost 6-8) and (2^4,1),
and plausibly many small-N placements. Risk: the free baseline theorem
needed a whole-complex manifold catalog (Frick 2015,
BASELINE_LE3 external_premise). The signed analog may likewise need a
catalog of 3-cycles with one negative facet on <= 13 vertices.

**Step (d): support counts for N <= 7 (low-medium difficulty, enumeration,
not a solver).** Only after (c) is at least proposed: enumerate union-14
Venn placements for N = 5, 6, 7 with C1, C2, C3, C6 and C7, and route each
class to (c) or to H130. The counts decide whether these inventories are
finished per placement or need further structure.

**Unit-heavy inventories (N >= 9; for example (1^14), (2,1^11), (1^11)):
very high difficulty, open-ended.** Here delta_min can be 3 to 5, so
single-derivative lemmas need up to five negative quartics. A local-cost
double count frames what would suffice. Write L(u) = sum of the costs of
coefficients containing u. Then sum_u L(u) = sum_S |S| cost(S) <= 5*28 = 140,
so some u has L(u) <= 10. In the free case the accepted local theorems
reach only L <= 6, so this frames the gap and is not a proof route by
itself. A global argument (H130/Turan, or the mod-2 4-cycle view of 3.2)
is the more plausible attack, but no concrete lemma is in hand.

**What not to do:** do not start per-placement case trees for N >= 8. Do not
reuse two-free or one-free CNF indices or contexts. Do not treat the 1513
C=22 signature as valid here.

## 6. Category ledger for this note

- *Accepted exclusions used:* union 12 (1531), union 13 (1533), and the 17
  excluded r <= 6 inventories (ledger 1388). None is new here.
- *Accepted necessary conditions used:* union >= 12 (1401/1404), union 14 at
  r <= 4 (residual-four manifest), C1, C2, the H130 capacity rule and
  W >= 8, deg_H(i) = 29-k_i, the top identity.
- *Necessary conditions derived here (018, unreviewed):* the general form
  of C3 (all residuals), C4, C5, C6, C7, the facet-pair valence lists, and the
  local-cost double count.
- *Solver UNKNOWN or resource limits:* none in the union-14 scope that I
  found.
- *New exclusions:* none. Global status OPEN. The 29 open patterns are
  unchanged.
