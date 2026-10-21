# Residual-six negative quintic supports cover at least twelve coordinates

Alexander Richard Towell; substantial OpenAI Codex assistance.21 October2026.
Written proof composition, submitted for separate independent review1401.
No human peer review, formal verification or novelty is claimed.

## Exact claim

Let f be the accepted selfdual-empty existence representative on fourteen
variables, of real degree at most five, with f(0)=0 and every singleton and
pair value one. Set g=1-2f and k_S=16*g_hat(S), using characters
chi_S(x)=(-1)^(sum_(i in S)x_i). Fix ALL negative quintics. If their cost
removed from the exact defect budget leaves at most six, their supports
cover at least twelve coordinates.

The existence-preserving representative reduction, exact integral Fourier
scale and older local derivative exclusions are inherited premises. This
claim concerns that representative; it does not assume an arbitrary original
solution is selfdual. It does not exclude every remaining magnitude pattern.

## Proof

Let F avoid all negative quintic supports. If |F|>=3, the accepted1393
classification gives |F|=3, k_F=-3 as the sole residual exception, singleton
numerators1/2, other cubic numerators-1/0, and nonnegative quintics0/1.
Its three-singleton fallback uses only the older baseline c<=3 theorem;
the two-nonsingleton arguments use actual c=1/2. The main classification's
written proof and explicit older premises are bound below.

For v in F, the actual derivative p=Delta_v f on thirteen coordinates has
one exceptional quadratic Fourier numerator-3 on F minus{v}; all other
quadratic numerators are-1/0 and all quartic numerators0/1. Its ordinary
quadratic coefficients are Boolean, p(0)=1 and p(e_i)=0. Accepted1395
therefore gives f(F)=1, a common physical cycle C7 on seven of the eleven
outside coordinates, and spherical exceptional endpoint links with that
degree-seven vertex and all other degrees four or five. These conclusions
do not assert that the whole quartic complex is a three-manifold. The cycle's
edge ij means exactly k_(F union{i,j})=1; no independent normalization or
function symmetry is used.

For each pair A in F let D_A have the outside triples T with k_(A union T)=1
as its triangles. These are three ACTUAL triangle families of the same
polynomial. Take v in A and the endpoint link at A minus{v} in its derivative.
That sphere consists of D_A together with the cone from F minus A on the
same C7. Removing the open star of this degree-seven vertex leaves the
triangulated disk D_A with boundary C7. Its boundary degrees are3/4 and its
interior degrees4/5. The possible interiors lie in the same four-set R of
outside coordinates not on C7. The elementary disk lemma1399, reproduced
independently in1401, requires at least three interior vertices in EACH disk.
Thus the three disks require at least nine interior-vertex incidences.

The exact-core-F Fourier block is

    B_F(z)=-3+sum_(ij edge of C7) chi_{ij}(z)
          =-4 sum_(X subset F) (-1)^|X| f(1_X+z).

The second equality is ordinary eight-point Fourier inversion with the
outside assignment z held fixed. For r in R, the first expression at z=e_r
equals4. All four truth values at X empty or singleton equal1, by the
singleton/pair layers. Hence

    sum_(A subset F, |A|=2) f(A+r)-f(F+r)=1.          (1)

Booleanity implies that exactly one or two of the three pair truths are one,
never zero or three. The top truth is respectively zero or one.

For each such A,r, ordinary pair inversion in Delta_v f for v in A gives

    k_(A+r)+sum_(Q quintic containing A+r) k_Q = 4 f(A+r).   (2)

Every quintic here meets a free coordinate and is nonnegative0/1. Because r
is off-cycle, no core-three quintic occurs through it. The sum is exactly
the number of triangles of D_A containing r. Its simple link graph has even
degrees by integral ordinary cubic coefficients. If f(A+r)=0, the baseline
cubic k_(A+r) in{-1,0} makes that graph have zero or one edge; parity excludes
one. Thus r is absent from D_A. If f(A+r)=1, it has four or five edges and r
occurs. Since r is not a boundary vertex, it is interior. Consequently the
pair truth in(1) is exactly the indicator that r is interior to D_A.

Each of the four r in R is therefore interior to exactly one or two disks.
This allows at most eight total interior incidences, contradicting nine.
The assumption |F|>=3 is impossible, so |F|<=2 and the negative support union
has size at least twelve. QED.

## Elementary disk premise and evidence

The disk lemma has no catalog premise. A boundary chord cannot cut off an
interior-free side, because a rooted polygon-dual-tree ear away from that
chord's endpoints would have boundary degree two. This excludes zero or one
interior vertex. With two interiors there are ten nonboundary edges. If the
interiors are adjacent there can be no boundary chord, forcing their degree
sum eleven>ten. Otherwise their degree lower bounds leave at most two
boundary chords: zero gives only seven triangles instead of nine; one gives
two fans and a boundary vertex of degree five; two give two fans separated
by an empty triangle, whose common chord endpoint has degree six. All violate
the boundary upper bound four. The full planar proof is source-bound1399.

The1398 proof independently derives (1),(2), the incidence equivalence and
the exact sign/factor in the core block. Its tests reconstruct all256 Boolean
core words, check all1296 possible four-off-unit choices, and preserve genuine
counterexamples to promoting a scalar coefficient into a Boolean extension.
The1395 controls distinguish parity from a cycle, repair a singular vertex
by splitting, and check the tiny pentagon/heptagon mechanisms. The1399 controls
check414 distinguished-base polygon ears and valid disks violating individual
degree guards. None claims an all-guards disk or a Boolean construction.
Parent normal/optimized tests and all three actual control scripts passed;
the parent replay source hashes were unchanged before and after execution.
The mathematical proof, not a target catalog or numerical solver, supplies
completeness. No new endpoint filter was needed.

## Exact source pins and limits

* Main classification1393 authority:25038a992790c16673a96709f8f7a3da0f650b5b8089f9cac6f74df7b74c981c.
* Endpoint1395 authority:02706b0f91065e9bdec12a3f74e103f53603f8597d01e826154371f24e714c08.
* Core1398 handoff:46cb42ed0a7f9d5b0fdf32d97e55d581d4a3884fb83406b8a6c55e9a033fa720.
* Disk1399 manifest:cee89dfcc7640b51f481d233ff41f98abd50c66fbf02f7e33c5b2855b7a8d3b4.

These are SHA256 pins to the named cycle files in this directory; final parent
authority binds absolute paths, the written proofs and all replay receipts.
Historical classification/certificate premises of1393 remain explicit and are
not freshly regenerated. The full14-variable problem and29 original magnitude
patterns remain OPEN. In particular a connected seven-support family has union
at most11 by a spanning tree and is excluded at residual<=6, but disconnected
families are not thereby excluded. No whole-pattern ledger is changed here.
