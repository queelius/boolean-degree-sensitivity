# Tripled quartics, private tips, and a coupled residual-six bound

This successor retains the complete earlier union-eleven proof below and adds
the stronger conditional union-twelve deduction in[UNION12.md](UNION12.md).
Its complete chapters are[THREE-FREE.md](THREE-FREE.md),[ENDPOINT.md](ENDPOINT.md),
[CORE-DISKS.md](CORE-DISKS.md) and[DISK-LEMMA.md](DISK-LEMMA.md).
BASELINE_LE3 is now an explicit additional inherited assumption in CLAIMS.json;
OLD_LOCAL_012 remains restricted to constants1/2. Mathematical claims and
archival lifecycle metadata are separate. This preparation remains unpublished.

Alexander Richard Towell. Prepared21 October2026 with substantial OpenAI Codex
assistance. This local packet has not yet been publicly disclosed or archived.
The new local arguments below are written proofs. Their finite controls are
separate checks of small combinatorial mechanisms, not formal verification.
The coupled conclusion explicitly assumes the older local theorem stated below.

## 1. Derivative setting and identities

Write `chi_S(x)=(-1)^(sum_{i in S} x_i)`. Let p be a real multilinear polynomial
on thirteen Boolean coordinates, with values in{-1,0,1}, p(0)=1, and p(e_i)=0.
Suppose

    16 p = c + sum_{|A|=2} a_A chi_A + sum_{|D|=4} b_D chi_D.

Assume every ordinary multilinear quadratic coefficient m_A of p is0 or1,
and every ordinary cubic coefficient is an integer. Expanding each character
as a product of(1-2x_i) gives

    4 m_A = a_A + sum_{D contains A} b_D,                 (1)
    sum_{D contains T} b_D is even for every triple T.   (2)

Indeed the ordinary cubic coefficient at T is minus one half of the sum in(2).
For a fixed pair A, make a weighted simple link graph: a quartic D containing A
gives the edge D minus A with weight b_D. When its weights are nonnegative
integers, equation(2) says every weighted vertex degree is even. When a_A is-1
or0, equation(1) limits the link's total weight to{0,1,4,5}.

A nonempty simple graph with all degrees even has at least three edges. With
four or five edges it must be a four-cycle or a five-cycle: every nonisolated
degree is at least two; a degree at least four would require at least six
edges, and two nonempty components would also require at least six. These
elementary facts, not a catalog or a flag-complex assumption, will be used.

## 2. A single tripled quartic

**Lemma1.** In the setting above, suppose every a_A is-1 or0 and every b_D is0
or1 except one b_D0=3. No such p exists. The constant c is unrestricted.

For a pair A contained in D0, the link contains one edge of weight three and
has total weight four or five. Weight four leaves one unit edge. To restore
even degrees at the heavy edge's two endpoints, that unit edge would have
to duplicate the heavy edge, which is unavailable: different quartics give
different simple edges. Thus the total is five. Its two unit edges must form
a length-two path between the heavy endpoints through a new vertex z.

Write D0={a,b,c,d}. The path in the ab link forces unit quartics abcz and
abdz. The ac link has heavy edge bd and already has unit edge bz. Its unique
second residual edge must be dz, forcing acdz with the same z. The bc link
similarly forces bcdz. Consequently all four remaining facets of D0+{z} have
weight one.

The az link has no heavy edge and contains the triangle bc,bd,cd. Its total
size must be four or five, so it would add one or two distinct unit edges to
an already even triangle. Those added edges would themselves have to form
a nonempty simple even graph, which cannot have one or two edges. This is
a contradiction. No constant bound, manifold classification, or global
Boolean-function symmetry entered the proof.

## 3. Private-tip extraction for a doubled quartic

**Lemma2.** In the derivative setting, let w be a coordinate and D a quartet
containing w. Suppose b_D=2, every other quartic through w has weight0 or1,
and every a_{wx} is-1 or0. Then no such p exists. Coefficients whose supports
avoid w may be exceptional; no bound on their number or on c is required.

Only equations incident with w will be used. A pair wx contained in D has
one weight-two edge. Its unit residual graph must be even by(2). Its allowed
total weight is four or five by(1), so the residual has two or three unit
edges. Two cannot form a nonempty simple even graph; hence it is a triangle.
A pair wx outside D has a simple empty, four-cycle or five-cycle link.

First, no unit quartet can contain a triple of D that contains w. For suppose
D=wabc and wabr has unit weight, with r outside D. The residual triangle
at wa contains edge br, hence has another vertex s and contains bs,rs.
The residual triangle at wb contains ar, hence has another vertex t and
contains at,rt. The unit cofaces of the triple wab are the same whether
viewed in the wa or wb link. They are exactly r,s in the first and r,t in
the second, so s=t. This vertex is outside D: s=c would duplicate D as a
unit quartet. The two triangles therefore force unit quartets wars and
wbrs. The ordinary wr link now contains the triangle ab,as,bs, impossible
in an empty, four-cycle or five-cycle link. Every pair used contains w;
exceptions avoiding w cannot affect this contradiction.

Take the link L of w in the **unit-weight** quartets only: each unit quartet
wxyz contributes triangle xyz. The preceding argument shows that, for each
of the three vertices of D minus w, its vertex link in L is exactly a triangle
disjoint from the other vertices of D. Every other occurring vertex link is
a four-cycle or five-cycle. Thus L is a disjoint union of genuine closed
triangulated surfaces. Exactly three vertices of L have degree three; all
others have degree four or five. At most twelve vertices occur. This is a
statement about L, not about any complex away from w. In particular pinched
surfaces with disconnected vertex links are not allowed.

Let A_w=sum_x a_{wx} and P_w=sum_{D' contains w} b_{D'}. Subtracting p(e_w)
from p(0) cancels all coefficients avoiding w and gives

    A_w + P_w = 8.                                    (3)

Let d be the number of vertices of L. A pair through w has m=1 exactly when
its unit link is nonempty. In the opposite case, m=0 gives link weight zero
or one by(1), and weight one is excluded by parity; both its link and a are
then zero. Summing(1) over pairs through w therefore gives

    4d = A_w + 3P_w.                                  (4)

Hence P_w=2d-4. Removing the doubled quartet's weight two leaves2d-6 unit
triangles of L. Every edge lies in two triangles, so the Euler characteristic
of L is d-(2d-6)/2=3.

Here is a complete elementary surface contradiction. For a connected closed
triangulated surface, Euler characteristic is at most two. One may see this
without classification: over the field with two elements, the zeroth Betti
number is one and the second is one. A two-cycle must have equal coefficients
on adjacent triangles, and the face-adjacency graph is connected for a genuine
connected surface. Thus chi=2-beta_1<=2. On the other hand,

    6 chi = sum_vertices (6-degree)

is positive when all degrees are at most five. Each component consequently has
chi one or two. For a chi-one component, E=3(V-1)<=V(V-1)/2 forces V>=6;
the curvature sum6 forces V<=6. It therefore has six degree-five vertices.

Total chi three on at most twelve vertices must consist of one chi-one and
one chi-two component. Three chi-one components would require eighteen
vertices. All three degree-three vertices belong to the chi-two component,
which has at most six vertices. Write n4,n5 for its other vertex counts.
Curvature gives9+2n4+n5=12. The only possibilities within six vertices are
(n4,n5)=(1,1) or(0,3). The first requires degree five on only five vertices.
In the second the degree sequence is(3,3,3,5,5,5). Its three degree-five
vertices are universal. Each degree-three vertex is adjacent exactly to those
three, whose cyclic vertex link forces three distinct faces through it.
There are consequently at least nine faces. A chi-two surface on six vertices
has2(V-2)=8 faces. Both possibilities are impossible. This proves Lemma2.

The local doubled-quartic surface argument predates this packet. What is made
explicit here is its incident-only extraction: arbitrary exceptions avoiding
w disappear from every equation used. Predecessor source pins and AI reviews
are retained in PROVENANCE.json and historical-source/.

## 4. Explicit inherited local theorem

The following is **assumed**, with its exact accepted source pins in CLAIMS.json.
It is not re-proved by running this packet's small controls.

**Assumption OLD_LOCAL_012.** No derivative in the setting of section1 has
c in{1,2}, all a_A in{-1,0} and all b_D in{0,1}, except for at most two
distinct nonsingleton cost-two departures in total. A quadratic departure has
value-2 or+1; a quartic departure has value2. All adjacent/disjoint pair-support
geometries and all sign combinations are included. Ordinary quadratic
coefficients must remain0/1. A coefficient cannot take two exceptional values
or count twice on one physical support.

This summarizes the inherited baseline, one-exception and two-exception
theorems **only at constants one and two**. The baseline and one-quadratic
results have an older c<=3 guard, the two-positive result c<=2, and other
two-quadratic results constants1/2. We use none at c=0 or3. The compact
one-negative-quadratic rows are constant-independent, but their preceding
structural reduction still requires c<=3. Recorded published manifold/sphere
classifications and exact finite certificates remain premises. Source bytes
are supplied as historical evidence where author-owned, not as a claimed
complete replay closure. Third-party classification bodies are not bundled.

## 5. Coupled residual-six theorem

Use the inherited selfdual-empty existence representative on fourteen variables:
f is Boolean, degree at most five, f(0)=0, all singleton and pair truths are one,
and only odd Fourier levels of g=1-2f occur. Use the accepted integral scale
k_S=16*g_hat(S). After fixing **all** negative quintics, suppose the sum of
the remaining nonnegative defect costs is at most six:

    singleton: (k-1)(k-2),
    cubic: k(k+1),
    nonnegative quintic: k(k-1).

The original existence-preserving representative reduction and empty-profile
full budget28 are explicitly inherited in CLAIMS.json. No original unknown
function is assumed selfdual merely from its origin sensitivity.

**Theorem3, conditional on OLD_LOCAL_012 and this normalization.** The negative
quintic supports cover at least eleven coordinates.

All costs are nonnegative even integers. Their zero-cost domains are respectively
{1,2},{-1,0},{0,1}. The five cost-two departures are singleton0 or3, cubic-2 or1,
and quintic2. The five cost-six departures are singleton-1 or4, cubic-3 or2,
and quintic3. There is no single cost-four departure. Thus the only allocations
are zero to three cost-two departures, or one cost-six departure. The abstract
multiset counts at total costs0,2,4,6 are1,5,15,40, totaling61. Repeated
abstract types represent distinct actual coefficients.

Let F avoid the union of all negative quintic supports. For v in F, define
p=Delta_v f=f(x with v=1)-f(x with v=0). Then p is ternary, p(0)=1 and each
unit value is zero. Differentiating the characters gives exactly

    16p=k_v + sum_{|A|=2} k_{A+v} chi_A
             + sum_{|D|=4} k_{D+v} chi_D.

No negative quartic occurs here. Its ordinary quadratic coefficient at ij is
p(ij)-p(i)-p(j)+p(0)=f(vij), hence0 or1. Ordinary cubic coefficients are
integers. Thus section1 applies with the actual shared coefficients.

Suppose four distinct coordinates F0 lie in F. For at most two cost-two
departures, choose v in F0 outside every exceptional singleton owner. Then
c=k_v is one or two and at most two nonsingleton departures are incident.
Assumption OLD_LOCAL_012 gives a contradiction. The same choice works for
three cost-two departures if at least one is a singleton: at most three
singleton owners cannot cover F0, and at most two nonsingleton departures
remain. This does not use a separate global residual-four theorem.

For a single cost-six singleton or cubic, its support has size one or three,
so some v in F0 avoids it and has a baseline derivative, again impossible.
For a cost-six positive quintic, either some v avoids it and the same argument
works, or every v in F0 lies in it and Lemma1 excludes its tripled quartic.

Only exactly three nonsingleton cost-two departures remain. Every singleton
is baseline. If any v in F0 misses any one departure support, its derivative
has at most two departures and OLD_LOCAL_012 excludes it. Therefore all three
supports contain F0. No cubic support contains four distinct coordinates, so
all three are doubled quintics S_i=F0+{t_i}. Distinct physical supports give
three distinct tips t_i outside F0.

Differentiate at any v in F0. Its doubled quartics are(F0 minus{v})+{t_i}.
Each t_i belongs to exactly one of them; all quadratic numerators through
t_i are baseline. Other doubled quartics avoid that tip, so Lemma2 applies.
This last contradiction proves |F|<=3, or negative support union at least11.

The argument couples shared supports. It does not assign an independent
two-unit cost to every negative-free coordinate. Three cubic supports on four
coordinates can each give every coordinate at least two incident exceptions
at total cost six; that invalidates the tempting independent-charge shortcut.

## 6. Finite checks and limits

The portable standard-library controls independently cover all61 allocations
and54,411 conservative intersections with four selected coordinates, after
discarding1,784 impossible complete-support aliases. Of these cases,54,409
route to an old theorem at constant one/two, one to Lemma1, and one to Lemma2.
They do not assert realizability by an actual Boolean function, and they do
not re-prove OLD_LOCAL_012.

Other controls check exact character normalization and inversion;1,590 weighted
links, including60 admissible heavy paths;171 forbidden triangle completions;
2,520 labeled forced-quartic configurations; and all20 graphs and900 candidate
face sets for degree sequence(3,3,3,5,5,5). Genuine closed spheres and a projective
plane pass the surface checker. A characteristic-three surface with four
degree-three vertices and a pinched pair of spheres are essential countercontrols.

The written proofs are not replaced by these finite mechanisms. The original
fourteen-variable existence problem remains open. No novelty, human peer review
or proof-assistant formalization is established. See APPLICATION.md for the
separate inherited whole-pattern application and its unbundled graph premises.
