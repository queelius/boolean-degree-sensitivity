# Independent minus-three endpoint link reduction

Alexander Richard Towell; substantial OpenAI Codex assistance. 21 October 2026.

The three local conclusions requested from the separately proposed cycle1391
structure note are valid under the accepted cycle1393 classification. The
ordinary coefficient-zero case is impossible; the coefficient-one case cannot
have a disjoint triangle and four-cycle as its exceptional link; and every
remaining exceptional endpoint link is a sphere on nine through twelve
vertices. This is a necessary reduction, not construction or nonexistence of
the remaining derivatives or the original fourteen-variable function.

This review binds the structure note with SHA256
`4407c71f800f0abcd87c49199f5bbc806ebf3fdb816fc5f6435c24e96d859232`.
It corrects one local wording issue without changing that frozen note: in the
`C3+C4` argument, the endpoint triangle complex is **not yet a surface** at
the exceptional vertex. The splitting argument below proves that the result
is a disjoint union of surfaces. No assertion about all vertex links of the
four-uniform complex, its connectivity, or its being a three-manifold is
accepted here. There is no Walkup, flagness, disk-interaction, endpoint-catalog,
or shared-core-truth premise in this gate.

## Exact inherited setting

Use the accepted selfdual empty-pair existence representative: fourteen Boolean
variables, real degree at most five, origin value zero, all singleton and pair
values one. With `g=1-2f` and `k_S=16*g_hat(S)`, fix **every** negative quintic
before assigning the residual defect. Cycle1393 proves that residual defect
at most six and at least three coordinates avoiding the negative quintics
force exactly three such coordinates, a set `F`, and the sole residual
exception `k_F=-3`. All singleton numerators are one or two, other cubics
are minus one or zero, and all nonnegative quintics are zero or one.

That classification is an explicit inherited premise, including its historical
local theorem and finite/literature dependencies. Those catalogs are not
replayed here. Selfduality is an existence-preserving reduction; it is not
assumed of an arbitrary original solution.

For any `v in F`, let `p=Delta_v f` on the other thirteen coordinates and put
`A=F\{v}`. It satisfies

```
16p = c - 3 chi_A + sum_(J != A, |J|=2) a_J chi_J
                    + sum_(|D|=4) b_D chi_D,
c in {1,2}, a_J in {-1,0}, b_D in {0,1},
p in {-1,0,1}, p(0)=1, p(e_j)=0.
```

The ordinary quadratic coefficient `m_J` is the actual value `f(J+v)`, hence
zero or one. In particular `m_A=f(F)` is the same truth for all three
derivatives. No negative quintic meets `v`, so no negative quartic numerator
is hidden in this local form.

## Literal coefficient and incidence calculations

Let `K` consist of the tetrahedra `D` with `b_D=1` and all their faces. There
are no duplicate or weighted tetrahedra. Expanding
`chi_D=product_(j in D)(1-2x_j)` gives, for each pair `J`,

```
4 m_J = a_J + sum_(D contains J) b_D.                 (1)
```

For any triple, its ordinary cubic coefficient is minus one half of its
quartic incidence. It is an integer because `p` is integer-valued on the
cube, so that incidence is even. Equivalently, every vertex degree of a pair
link is even.

A baseline pair has link size in `{0,1,4,5}`. Its link is a simple even graph,
so it is empty, `C4`, or `C5`; a single edge is impossible. For such a pair,
being an edge of `K` is equivalent to `m_J=1`. Every triangle of `K` contains
a baseline pair, because there is only one exceptional pair. Its third vertex
has degree two in that pair's cycle link. Thus **every triangle of `K` belongs
to exactly two tetrahedra**.

The exceptional pair link has `4m_A+3` edges by (1), and every occurring
vertex of that link has degree two by the preceding triangle incidence.
Consequently it is `C3` if `m_A=0`; if `m_A=1`, it is either `C7` or the
vertex-disjoint union `C3+C4`. Even-degree parity alone would not suffice:
a triangle and square sharing a vertex have seven edges and even degrees,
but the shared vertex has degree four.

All three derivatives have the same **literal** exceptional graph on the
eleven coordinates outside `F`: its edge `xy` is present precisely when
`k_(F union {x,y})=1`. This is equality of actual coefficient supports, not a
permutation symmetry of the unknown function.

Fix an endpoint `w in A`. Write `A_w` for the sum of all quadratic Fourier
numerators through `w`, `P_w` for the number of quartics through it, and `d_m`
for the sum of its ordinary quadratic coefficients. Subtracting the origin
and unit values cancels the constant and every nonincident term, giving
`A_w+P_w=8`. Summing (1) over the pairs through `w` gives
`4d_m=A_w+3P_w`. Therefore

```
P_w = 2d_m-4.                                      (2)
```

Let `L_w=link_K(w)`, a triangle complex on `d<=12` vertices. It has `P_w`
faces, and each edge has two incident faces. Every vertex link is a cycle
`C4` or `C5`, except that at the other endpoint of `A` the link is the
exceptional graph. When that graph is a single cycle, this proves that
`L_w` is a disjoint union of closed triangulated surfaces. When it is
`C3+C4`, the exceptional vertex is singular and must first be split.

## Elementary surface facts used

For any closed connected triangulated surface, `3F=2E`, so

```
6 chi = sum_vertices (6-degree).                    (3)
```

Also `chi<=2`, and equality means a sphere. One elementary explanation is the
tree–cotree argument: contract a primal spanning tree, merge faces along a
dual spanning tree, and obtain a one-vertex, one-face cell decomposition
with `2-chi` remaining edges. This number is nonnegative; if it is zero,
the surface is the disk with its boundary collapsed, a sphere. The operations
preserve the homeomorphism type. Equivalently the inequality follows from
mod-two homology, with one-dimensional zeroth and second homology. No finite
surface or three-manifold catalog is being invoked.

If all degrees are three, four, or five, (3) makes each component's Euler
characteristic positive, hence one or two. A characteristic-one component
has exactly six vertices, all of degree five: positivity in (3) gives at
most six vertices, while `E=3(V-1)<=V(V-1)/2` gives at least six (a closed
simplicial surface has at least four). This numerical fact is sufficient;
identifying that component as a projective plane is unnecessary.

## Excluding `m_A=0`

Here the exceptional pair is an actual edge of `K`, since its link is `C3`,
despite its ordinary coefficient being zero. All other edges through `w`
have ordinary coefficient one. Thus `d_m=d-1`, and (2) gives `P_w=2d-6`.
Using edge incidence two,

```
chi(L_w)=d-P_w/2=3.
```

This surface union has exactly one degree-three vertex, the other endpoint,
and all other degrees four or five. On at most twelve vertices, its total
characteristic three cannot come from three characteristic-one components
(they need eighteen vertices). It must consist of one sphere and one
six-vertex characteristic-one component. The sphere contains the only
degree-three vertex and has at most six vertices.

Let the sphere have `n4` degree-four and `n5` degree-five vertices. Curvature
gives `3+2n4+n5=12`, and `1+n4+n5<=6`; a degree-five vertex requires six
vertices. These force `(n3,n4,n5)=(1,4,1)`, namely degrees
`(3,4,4,4,4,5)` on six vertices.

Its degree-five vertex is universal. Removing its open star leaves a disk
triangulating the pentagon formed by its link, with no interior vertices.
There are two diagonals. The required degrees say that four boundary vertices
meet exactly one diagonal and the fifth none: the diagonals would be disjoint.
Every pentagon triangulation has its two diagonals sharing a vertex (two
disjoint diagonals cross). Contradiction. This excludes `m_A=0`.

The marked Euler formula from the proposal is not needed here. In particular
the proof does not reuse an unmarked Euler bound or incorrectly identify the
exceptional edge with its zero ordinary coefficient.

## Excluding `m_A=1` with `C3+C4`

Now every edge through `w` has ordinary coefficient one, so `d_m=d` and
`chi(L_w)=2`. This is a statement about the triangle complex, not yet about
a surface. At its exceptional vertex `u`, the link consists of two
vertex-disjoint cycles, of lengths three and four.

Replace `u` by two distinct vertices `u3,u4`, assigning a face containing
`u` to the cycle containing its other two vertices. This is unambiguous:
those two vertices are adjacent in the link, and hence in one cycle. Each
neighbor of `u` belongs to exactly one cycle. The replacement preserves every
edge and face count, adds one vertex, and creates neither duplicate faces nor
an edge between the two copies. The copies have links `C3,C4`. At every old
neighbor, its previous circular link merely has `u` replaced by the unique
appropriate copy; other links are unchanged. The result is therefore a
disjoint union of closed surfaces, with Euler characteristic three, at most
thirteen vertices, copies of degrees three and four, and other degrees four
or five.

Again there must be one sphere and one six-vertex characteristic-one
component; three characteristic-one components need eighteen vertices.
The characteristic-one component is all degree five, so both copies belong
to the sphere. They are nonadjacent and their neighbor sets are disjoint,
of sizes three and four. The sphere therefore has at least
`2+3+4=9` vertices. Adding the other component requires at least fifteen,
contradicting the bound thirteen. This excludes `C3+C4`.

## The remaining endpoint links are spheres on 9–12 vertices

The common exceptional graph is consequently `C7` and `f(F)=1`. For each
derivative and either exceptional endpoint, `L_w` is now a genuine surface
union with characteristic two, one degree-seven vertex, and all other degrees
four or five. The component containing the degree-seven vertex has at least
eight vertices. Its curvature is at least `-1+7=6`, so its characteristic is
positive. Every other component also has positive curvature. If there were
another component, total characteristic two would force two
characteristic-one components. The extra component would need six vertices,
giving at least fourteen in total, beyond the available twelve. Hence `L_w`
is connected of characteristic two, a sphere.

If it had eight vertices, its degree-seven vertex would be universal.
Removing its open star gives a triangulated heptagon with no interior
vertices. Such a triangulation has at least two ears: the weak dual is a
tree on its five triangles, with four dual edges, so has at least two leaves.
Each leaf triangle supplies a boundary vertex of polygon degree two. Adding
back the universal vertex gives degree three in the sphere, contradicting
the required remaining degrees four or five. Thus each endpoint sphere has
order in `{9,10,11,12}`. This does not assert that any of those orders is
realizable with all the remaining polynomial conditions.

## Independent controls, scope and handoff

The new stdlib helper imports no cycle1391 producer, bitset engine, or
catalog generator. It checks literal edges, faces, links, Euler counts and
vertex splitting. The controls include a singular wedge of a tetrahedral
sphere and an octahedral sphere: splitting its `C3+C4` vertex preserves edges
and faces and raises characteristic by one. That control does not satisfy
all target degree guards. A genuine disjoint octahedral sphere plus a
six-vertex characteristic-one surface has characteristic three on twelve
vertices and shows that characteristic alone is not the obstruction. It has
no degree-three vertex. Duplicate labels, missing faces, Boolean/integer
aliases, a second singular vertex and a noninvolutive relabeling are tested.

The complete small enumerations are:

- 4,384 simple graphs on six labeled vertices with 0, 1, 4 or 5 edges. The
  even graphs are the empty graph, 45 four-cycles and 72 five-cycles. Even
  nonisolated graphs with at most five edges have at most five vertices,
  so these controls cover all the relevant baseline shapes up to labels.
- All twelve labeled pentagonal links and all 120 possible triples of
  complementary faces, 1,440 tests. Exactly sixty closed-surface completions
  survive, all with degrees `(3,3,4,4,5,5)`, none with the forbidden sequence.
- All 1,001 four-diagonal subsets of a heptagon. The 42 noncrossing
  triangulations are independently checked as literal sphere completions;
  28 have two ears and 14 have three, so all have forbidden degree-three
  boundary vertices after adding the universal vertex.

The written proof, rather than those finite examples alone, supplies the
unbounded-label link and surface deductions. Nine normal and nine optimized
unit controls pass, with explicit `-O` and `-OO` CLI rejection before output
creation; all thirteen project tests pass. Final coverage is 159/163
statements and 64/68 branches. The four uncovered branches are internal
invariant failures (a face crossing distinct link components, split
incidence mismatch, an unexpected even baseline link, and a malformed
noncrossing triangulation); no mathematical case is omitted to avoid them.
The first coverage attempt missed the dynamically imported helper; that
warning log is preserved, and a path-based coverage retry includes both
unit tests and the actual CLI.

Only the stated local reductions are accepted. No original support pattern,
remaining derivative, or global problem is excluded by this gate. No
whole-complex manifold claim, endpoint catalog, flagness, Walkup theorem,
later disk argument, shared-core truth table, target solver, new publication,
human peer review, formal proof or novelty claim is included. The exact
proof and controls are suitable for a future conditional publication packet
with the accepted cycle1393 premises; parent review and publication handling
remain separate. Frozen sources and canonical ledgers have not been edited.
