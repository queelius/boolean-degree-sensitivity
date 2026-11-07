# Two exceptional coefficients and a negative-free derivative

This note concerns a negative-free nonendpoint u of the unique zero pair e
in the self-dual one-edge profile. Assume singleton numerators are 1 or 2
and the nonsingleton defect consists of exactly two cost-two exceptions.
We prove that a positive doubled quintic among those exceptions cannot
prevent f(e+u)=1. The case of two exceptional cubics is treated separately.

Suppose f(e+u)=0 and write p=Delta_u f on the other thirteen coordinates.
Then p(0)=1, p(singletons)=0, every ordinary quadratic coefficient m_A is
0 or 1, and

    16p = c + sum a_A chi_A + sum b_D chi_D,

where the sums have orders two and four. Every a_A is -1 or 0 apart from
incident exceptional cubics, and every b_D is 0 or 1 apart from incident
positive doubled quintics. No b_D is negative. The coefficient of the
special pair e is m_e=1 precisely because f(e+u)=0. The range of p is
{-1,0,1}. Exceptions not incident to u disappear upon differentiation.

If u sees at most one exception, the already independently audited
low-residual derivative theorem gives a contradiction. It remains to
handle two doubled quartics, or one exceptional quadratic J and one
doubled quartic D. The proof below is elementary and reuses the accepted
small surface argument from the one-doubled-quartic theorem.

## The local link calculation

For a pair A with baseline a_A, quartic inversion gives weighted top-link
size 4m_A-a_A in {0,1,4,5}. Cubic integrality forces every weighted vertex
degree of the link to be even. A link with no doubled edge is therefore
empty, a four-cycle, or a five-cycle. A link with one doubled edge has a
residual unit triangle: subtracting weight two leaves size two or three,
and only the latter supports a nonempty simple even graph. A link with
two doubled edges has no unit edges, since subtracting weight four leaves
at most one unit edge, whose degree parity would fail.

First suppose there are exactly two distinct doubled quartics D1,D2,
with every quadratic numerator baseline. Choose x in D1 minus D2.
All pairs through x are baseline and see at most the doubled quartic D1.
Second, suppose there is just one doubled quartic D and one exceptional
quadratic J. Choose x in D minus J; this is possible since |D|=4 and |J|=2.
Again every pair through x is baseline and sees only D. In either case
write D for the doubled quartic containing x.

No unit tetrahedron can contain a triple T subset D with x in T. Suppose
T+r is a unit tetrahedron, where r is outside D. Use the two pairs A in T
that contain x. Each has a residual unit triangle in its top link. Since
T+r occurs, cubic parity gives a second unit tetrahedron T+s, and the
residual triangles force both A+r+s. These statements use only the two
baseline pairs through x; the third pair in T is irrelevant. The link of
{x,r} consequently contains a triangle on (T minus {x}) union {s}.
But {x,r} is baseline and contained in no doubled tetrahedron. Its link
is empty or a four-/five-cycle, which cannot contain that triangle.
This contradiction proves the assertion.

Now take the simplicial link at x formed only by unit tetrahedra. Exactly
three vertices have degree three: D minus {x}. Every other occurring
vertex has degree four or five. Every link edge belongs to exactly two
triangles. Indeed, triangles of the original complex through x inside D
are absent by the preceding paragraph; every other such triangle uses a
pair through x outside D, and that pair has a cycle link. Thus this is a
disjoint union of closed triangulated surfaces, on at most twelve vertices.

Let d be the number of its vertices. Every nonempty pair link through x
has m_{xv}=1, so the ordinary quadratic degree is d. The equations p(0)=1
and p(e_x)=0 give A_x+P_x=8 for quadratic and weighted quartic incidences.
Summing the ordinary quadratic inversion gives 4d=A_x+3P_x, whence
P_x=2d-4. Removing the doubled tetrahedron leaves 2d-6 unit tetrahedra.
The link therefore has Euler characteristic d-(2d-6)/2=3.

The accepted elementary surface obstruction now applies verbatim: vertex
degrees are 3,4,5, with exactly three degree-three vertices. Each component
has positive Euler characteristic. A characteristic-one component must
have exactly six vertices, all of degree five. With at most twelve
vertices, total characteristic three requires a sphere and such a
six-vertex component. The sphere contains all three degree-three vertices;
its curvature equation leaves either an impossible degree-five vertex on
five vertices, or degree sequence (3,3,3,5,5,5) on six vertices. In the
latter case the three universal vertices force nine distinct triangles,
whereas the sphere has eight. This is impossible.

Hence both local two-exception alternatives contradict f(e+u)=0.
The argument does not claim a special-edge coefficient-two theorem;
that stronger extension is separately investigated by the parent.

## Consequence for six negative units

If the two global nonsingleton exceptions include a doubled positive
quintic, every negative-free nonendpoint is a positive extension of e.
If they are both exceptional cubics, a negative-free nonendpoint can fail
to be positive only if it belongs to both cubic supports. Two distinct
three-sets intersect in at most two vertices. Therefore at most two free
nonendpoints can be nonpositive in this remaining alternative.

In particular, when d_H(e)=11 and there are at least four negative-free
nonendpoints, every alternative is impossible: there is only one positive
extension in total. With three free nonendpoints, the same conclusion
holds if a hitting equality fixes that unique positive extension inside
the negative-support union.

The predecessor local theorem and one-double surface proof are bound by
`009-parent-analysis/low-residual-derivative-complete-manifest.json` and
`008-sparse-spectrum-proof/doubled-positive-quartic-derivative-independent-audit.md`.
Independent review of this extension is maintained separately.
