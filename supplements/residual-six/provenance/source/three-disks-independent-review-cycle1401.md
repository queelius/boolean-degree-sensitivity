# Independent review of the three-disk support-cover theorem

Alexander Richard Towell; substantial OpenAI Codex assistance. 21 October 2026.

The final composition in `three-disks-union12-proof-cycle1404.md`, SHA256
`622ee562e447fe9d2ca9f4a49de9931575e2b058972ec7717b0a0b64a94e83f9`,
is sound under its explicitly inherited representative, integrality, defect
and local-classification premises. The independently accepted conclusion is:

> In the selfdual empty-pair existence representative on fourteen variables,
> if subtracting the entire cost of all negative quintics leaves residual
> defect at most six, the negative quintic supports cover at least twelve
> coordinates.

This review freshly checks the three-disk composition, the needed core Fourier
identities and the elementary disk lemma. The earlier cycle1393 classification
and cycle1395 endpoint reduction are inherited accepted premises, with their
exact validation receipts. It does not freshly replay the older catalogs or
computational exclusions underlying cycle1393. No whole-pattern status or
canonical ledger is changed. The original existence problem remains open.

## The actual common disks and their degree guards

Suppose the negative-free set `F` has at least three coordinates. Cycle1393
forces `|F|=3`, a single cubic numerator `k_F=-3`, singleton numerators one
or two, other cubics minus one or zero, and all nonnegative quintics zero or
one. No negative quintic meets `F`. Cycle1395 then forces `f(F)=1` and the
same literal seven-cycle `C` in all three derivative exceptional links.
An edge `xy` of `C` means `k_(F+x+y)=1`; these are actual shared coefficients,
not independently chosen links or an assumed function symmetry.

For a core pair `A={a,b}`, let `c` be the remaining member of `F`. Define
`D_A` by its triangles `T` outside `F` with `k_(A+T)=1`. In the derivative
at `a`, take the link of `b`. Its triangles containing `c` are precisely
`c+xy` for edges `xy` of `C`. Every other triangle is a triangle of `D_A`.
The accepted endpoint link is a sphere. Thus it is exactly

```
cone_c(C) union D_A,
```

with intersection `C`. The closed complement of the open star of `c` is
`D_A`, a triangulated disk with boundary `C`. This is the antistar of an
actual vertex in an actual endpoint sphere; arbitrary local link selections
are not being glued together.

Every cycle vertex loses just its neighbor `c`, so its degree **in the disk**
is three or four. Vertices not on `C` were not adjacent to `c`; their degrees
remain four or five. All possible interior vertices belong to the same
four-set `R` outside `F union C`. It is irrelevant whether the full quartic
complex is connected or a three-manifold. Its unreviewed ordinary-vertex
topology, flagness and Walkup-type properties are not used.

## Independent proof of the seven-boundary disk lemma

Let `D` be a simplicially triangulated closed disk whose boundary is a
seven-cycle, with boundary degrees three or four and interior degrees four
or five. A chord joins two nonconsecutive original boundary vertices. The
disk embedding makes it separating; different edges cannot cross.

An interior-free side of a chord is a triangulated polygon. Root its triangle
dual tree at the triangle incident with that chord. If there is just one
triangle, its third vertex is an ear away from both chord endpoints.
Otherwise a leaf different from the root supplies such an ear. Its two
boundary edges lie on the original boundary arc, and an edge from its common
vertex to the other side would cross the chord. It therefore has degree two
in the **whole disk**, contradicting the boundary lower bound. Hence every
chord has an original interior vertex on both sides. This uses neither
disjoint coordinate supports nor any extra positivity assumption.

If there are no interior vertices, the polygon ear theorem already gives
degree two. If there is one interior vertex, no chord is allowed. Every
boundary edge must have that interior vertex as its triangular third vertex;
a triangle with three original boundary vertices would require a chord.
Thus the one interior vertex has degree seven, contradicting its upper bound.

Suppose there are two interior vertices `u,v`. Euler's equation and triangular
edge incidence give

```
E = 3I+2B-3,     F = 2I+B-2.
```

For `B=7,I=2`, there are ten nonboundary edges and nine triangles. Let `d`
be the number of boundary chords, `r` the number of edges from interior to
boundary, and `t` the number of edges between interiors. Then

```
d+r+t=10,    t in {0,1},    degree(u)+degree(v)=r+2t.
```

If `t=1`, any chord would have to separate `u,v` by the empty-side result,
which would force their edge to cross it. Thus `d=0,r=9`; their degree sum
is eleven, not twelve, and exceeds the permitted ten.

If `t=0`, both interior degrees are at least four, so `r>=8` and `d<=2`.
Every chord separates `u` from `v`.

- For `d=0`, no triangle has two interior vertices, while a triangle with
  three boundary vertices would require a chord. Every triangle therefore
  has one interior vertex and one original boundary edge. There are only
  seven such boundary edges, each incident with one triangle; this contradicts
  the required nine triangles.
- For `d=1`, the two regions contain one interior vertex each and no further
  boundary diagonal. Each is a fan: every edge of its polygonal boundary
  has that interior vertex as the third vertex of its incident triangle.
  Each chord endpoint has the two original boundary neighbors, the chord
  neighbor, and both interior neighbors. These five vertices are distinct,
  contradicting the boundary upper bound four.
- For `d=2`, the noncrossing chords cut the disk into three regions. The
  region dual is a three-vertex tree. Both dual edges must lie on the path
  between the regions containing `u,v`, since both chords separate them.
  The interiors are consequently in the end regions, and the middle region
  is empty. There are no unused chords within any region. An empty region
  with more than three vertices would need an additional boundary diagonal,
  so the middle region is one triangle. Its two chord edges share a vertex
  `x`. The end regions are fans, so `x` neighbors both interiors. The two
  distinct chord neighbors and two original boundary neighbors are distinct
  from those interiors and from each other, since chords are not original
  boundary edges. Thus `degree_D(x)>=6`, another contradiction.

These cases exhaust `I<=2`. Every disk has at least three interior vertices.
The argument is a complete planar proof. The finite polygon/fan controls do
not stand in for enumerating all possible disks, and no all-guards positive
example is asserted. Applying the lemma to the three physical disks requires
at least nine interior incidences.

## Independent sign, scale and incidence derivation

Let `g=1-2f` and `k_S=16*g_hat(S)`. For a fixed outside assignment `z`, the
coefficient of the full three-core character is obtained by averaging only
the eight core inputs:

```
B_F(z) = 2 sum_(X subset F) g(1_X,z) (-1)^|X|
       = -4 sum_(X subset F) f(1_X,z) (-1)^|X|.
```

The constant term in `g` cancels. There is no second outside averaging factor.
Since the only full-core Fourier terms are the cubic and seven positive
quintics,

```
B_F(z) = -3 + sum_(xy edge of C) chi_{xy}(z).
```

At an off-cycle unit `z=e_r`, this equals four. The four truths for `X` empty
or singleton are all one, by the original singleton and pair layers. Put
`s_A=f(A+r)` for the three core pairs and `h=f(F+r)`. The exact equation is

```
4 = -4*(-2 + sum_A s_A - h),
sum_A s_A - h = 1.                                  (1)
```

Booleanity gives exactly one pair truth when `h=0` or two when `h=1`.
In particular an off-cycle coordinate cannot activate all three pair rows.
This restriction would be false at an on-cycle unit, where `B_F=0`; the
off-cycle hypothesis is essential.

For `A={a,b}` and `r in R`, pair inversion in `Delta_a f` gives

```
4 f(A+r) = k_(A+r) + sum_(Q quintic, Q contains A+r) k_Q.   (2)
```

The cubic is baseline because `r` is outside `F`. Every quintic in this sum
contains the negative-free coordinate `a`, so is binary and nonnegative.
Any quintic containing the third core coordinate would be `F+r+x`, but that
would be a cycle edge through `r`, impossible off-cycle. Consequently the
sum is exactly the number of triangles of `D_A` incident with `r`.

The pair link in that derivative is the link of `r` in `D_A`, a simple graph
with even degrees by cubic integrality. If `f(A+r)=0`, (2) permits only zero
or one edge; a single simple edge is not even. The link is empty and `r`
does not occur in `D_A`. If `f(A+r)=1`, the incidence is four or five and
`r` does occur. Since it is off the boundary, it is an interior vertex.
Thus `s_A` is exactly, not merely an upper bound on, the interior incidence
indicator of `r` in the corresponding physical disk.

There are four possible off-cycle coordinates. Equation (1) gives at most
two incidences per coordinate, for a total at most eight. The three disk
lemmas require at least nine. This contradiction eliminates `|F|>=3`;
therefore `|F|<=2`, and the negative support union has at least twelve
coordinates. The classification of `|F|>=3` was already exhaustive in1393,
so there is no additional residual type or singleton-constant case omitted
by this composition.

## Independent controls and precise scope

The new helper imports only the standard library, and none of the1398/1399
producer helpers, catalog enumerators or solver kernels. It computes the
scaled Walsh transform directly from `g`, and reconstructs all eight inputs
for all 256 Boolean core words. Among the sixteen completions of the four
known low-layer truths, exactly six have full-core block four. Their fourfold
product has 1,296 assignments, with total incidences four through eight in
counts `81,324,486,324,81`; none has three rows of size at least three.
These independently chosen words form a conservative superset of possible
actual shared Boolean restrictions, not a construction.

Independent polygon cuts and literal disk checks cover all fourteen
one-chord fan disks and all 91 pairs of heptagon chords. There are 56
noncrossing pairs; 21 have the required empty middle triangle, and their
literal fan completions have a degree-six boundary vertex. Seven one-chord
and seven two-chord examples satisfy the interior degree bounds, so the
boundary upper-bound failures are not a vacuous use of already-invalid
interiors. A valid disk with adjacent centers has center degrees five and
six and valid boundary degrees, verifying the sum-eleven obstruction. A
heptagonal cone is a valid disk with interior degree seven, refuting omission
of the interior upper bound. A boundary-only polygon triangulation refutes
omission of the boundary lower bound. None is mislabeled an all-guards
positive disk.

Missing faces, duplicate/Boolean-label aliases, crossing or duplicate chords,
an on-cycle/all-one truth block, and a noninvolutive coordinate relabeling are
tested. Ten normal and ten optimized unit controls pass, including explicit
`-O`/`-OO` CLI rejection before output creation; thirteen project tests pass.
The actual independent controls finish in 0.0863 CPU seconds under coverage.
The new helper has 149/149 statements and 42/42 branches covered; coverage
is a control metric, not a formal proof or exhaustive path guarantee.

Only the portion of1398 needed for (1), (2) and their exact physical incidence
meaning is accepted here; unused sector formulas or proposed two-free
extensions are not silently promoted. The full pure disk lemma1399 is
accepted by the independent written proof above. The later two-free
classification, whole-complex topology, endpoint flagness, sphere catalogs,
Walkup bound, and any target solver remain outside this gate.

A family of at most seven distinct negative five-supports that is connected
under four-coordinate overlap has union at most `5+(7-1)=11`, by a spanning
tree. It therefore cannot occur under the stated residual-six hypotheses.
That conditional corollary does not exclude an entire disconnected magnitude
pattern; no pattern ledger is changed here. In particular neither this
theorem nor a DOI would settle the original fourteen-variable problem.

The exact proof and independent controls are ready to be included in a
conditional publication packet together with the inherited1393/1395 premises.
No publication, novelty assessment, human peer review or formal verification
has been performed by this review. The frozen source versions and all final
receipts are bound by the separate1401 authority and manifest.
