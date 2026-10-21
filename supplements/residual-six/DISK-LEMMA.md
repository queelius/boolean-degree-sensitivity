# A seven-boundary disk needs at least three interior vertices

Alexander Richard Towell; substantial OpenAI Codex assistance.21 October2026.
Written elementary proof and small exact controls; the pure lemma was
independently accepted in final1401. Original1399 source bytes are retained
separately in provenance/source/. No sphere catalog, solver or feasibility model is used.
This is a pure triangulated-disk statement, not a Boolean construction or
whole-pattern exclusion. The original14-variable goal remains OPEN.

## Statement and conventions

Let D be a finite simplicial triangulation of a topological closed disk.
Its boundary is one simple cycle on exactly seven distinct vertices.
Every boundary vertex has disk-skeleton degree3 or4, and every interior
vertex has disk-skeleton degree4 or5. Then D has at least three interior
vertices. Degrees here count distinct neighboring vertices IN THE DISK;
boundary degrees do not include a hypothetical removed sphere apex.

A boundary chord is an edge joining two boundary vertices that are not
consecutive on the original seven-cycle. Edges do not cross in the disk
embedding. A chord separates D into two triangulated disks; their boundaries
consist of that chord and the two original boundary arcs. Interior vertices
of either side are actual original interior vertices on that side.

## Empty-side ear lemma

If one side of a boundary chord has no interior vertex, then D has a
boundary vertex of degree two, contradicting the hypotheses.

Indeed that side is a triangulated polygon, with the chord as its base
edge. Its triangle dual is a tree: it is connected, and a p-vertex polygon
has p-2 triangles and p-3 internal diagonals. Root the tree at the unique
triangle incident with the base edge. If there is only one triangle, its
third vertex is an ear away from the base endpoints. Otherwise take a leaf
different from the root. Its two polygon-boundary sides are not the base
edge, so they are edges of the original boundary arc. Their common vertex
is an ear distinct from the two base endpoints. It has no edge into the
other side of the chord: such an edge would cross the separating chord.
Thus its degree in the whole D is two, not just in the empty-side polygon.

Consequently EVERY boundary chord must have an interior vertex on BOTH
sides. This conclusion uses the boundary lower bound3; it is not valid
for an arbitrary triangulated disk with ears.

## Zero or one interior vertex

With zero interior vertices, any triangulation of the heptagon has a
boundary chord (indeed four), contrary to the empty-side lemma. Equivalently
the usual polygon ear argument already contradicts minimum boundary degree3.

With one interior vertex u, a boundary chord again has an empty side, so
there are no chords. Every boundary edge must then be in a triangle with
third vertex u: a three-boundary-vertex triangle would require a chord
because the boundary cycle has length seven. Hence all seven boundary
vertices are neighbors of u. Its degree seven violates the interior bound5.

## Exactly two interior vertices

Write them u,v. A triangulated disk with B boundary and I interior vertices
has E=3I+2B-3 edges, by Euler and3F=2E-B. For B=7,I=2, exactly ten edges
are not original boundary edges. Let d be the number of boundary chords,
r the number of interior-to-boundary edges, and t the number of interior
edges. Then

    d+r+t=10,  t in{0,1},  degree(u)+degree(v)=r+2t.

If u and v are adjacent, a boundary chord cannot separate them: their edge
would cross it. The empty-side lemma therefore forbids every chord, so
d=0,t=1,r=9. Their total degree is ELEVEN, exceeding the upper bound ten.
The correct count is11, not12; the proof does not need the larger number.

Suppose u,v are nonadjacent. Now t=0 and the interior lower bound4 gives
r>=8, so d<=2. Also every chord separates u from v. The three possibilities
are as follows.

* d=0: There is no triangle containing both interior vertices. A triangle
  on three boundary vertices would require a chord. Thus every triangle
  contains exactly one interior vertex and one ORIGINAL boundary edge.
  Each boundary edge belongs to exactly one triangle, so there can be only
  seven triangles. Euler requires F=2I+B-2=9, a contradiction.

* d=1: The chord splits D into two regions, each with one interior vertex
  and no other boundary chord. Each region is a fan from its interior vertex:
  in a polygon with one interior vertex and no boundary diagonals, all
  boundary edges must have that vertex as their triangular third vertex.
  Both endpoints of the chord therefore neighbor u and v. Each also has
  its two distinct original boundary neighbors and the chord itself, giving
  degree at least five in D, above the allowed four.

* d=2: Noncrossing chords partition D into three polygonal regions. Their
  chord dual is a tree. Since every chord separates u and v, each dual edge
  lies on the path between the regions containing u and v. Thus the dual
  is a three-vertex path; its end regions contain u and v respectively and
  the middle region contains no interior vertex. There is no unused chord
  inside a region. The empty middle region must therefore be a SINGLE
  triangle. Two of its edges are the two chords, so they share an endpoint x.
  Each end region has one interior vertex and no further diagonal, hence
  is a fan. Therefore x neighbors both u and v. In addition x has two
  distinct original boundary neighbors and the two distinct chord neighbors.
  All six neighbors are distinct, so degree_D(x)>=6>4, a contradiction.

These cases exhaust I<=2. Hence I>=3. No catalog minimality, flagness,
automorphism, sphere classification or numerical infeasibility is used.

## Meaningful controls and hypothesis failures

The stdlib controls enumerate polygon triangulations only for orders3..7,
giving1,2,5,14,42 triangulations and414 distinguished-base checks. In every
case an ear exists away from the base endpoints. These tiny controls check
the ear proof; they are not a catalog of the target endpoint surfaces.

Four explicit valid disks check the counts and show why the bounds matter:

* The cone on the heptagon has one interior vertex of degree7 and all
  boundary degrees3. It is a VALID triangulated disk but NOT an all-guards
  positive. It refutes dropping the interior upper bound.
* Split the heptagon by chord03 and fan its quadrilateral/pentagonal sides
  from distinct centers. Their degrees are4 and5; chord endpoints have
  boundary-disk degree5. It refutes dropping the boundary upper bound.
* Chords03 and04, two quadrilateral fans and the empty middle triangle034
  give an actual disk with center degrees4,4 and a boundary vertex degree6,
  checking the d=2 obstruction in a nonvacuous example.
* A disk with adjacent centers, three boundary-edge faces at one and four
  at the other, checks the interior-degree sum11. Its boundary degrees
  satisfy3/4; its centers have degrees5 and6, so it is rejected by the
  interior upper bound.

Each disk is independently checked by literal edge incidences, full boundary,
connected skeleton, connected path/cycle vertex links and Euler1. Malformed
face omissions, duplicate masks, bool/int aliases and wrong bijections are
rejected; a noninvolution coordinate transport and inverse are checked.
The tests explicitly reject the first two disks as purported all-guards
positives. No genuine all-guards disk is asserted or needed for the lemma.

Two earlier tiny attempts to build such a positive from fixed known spheres
failed (two legal flips from a labelled icosahedron, and one split of the
specific old degree6 record(11,762)). They were not complete sphere covers
and give NO nonexistence information. Their failed outputs are preserved
separately; no further construction search is performed.

## Conditional global use, NOT part of this lemma

The independently reviewed core bridge in CORE-DISKS.md concerns three disks with common seven-boundary and
four possible outside interior coordinates, each coordinate used in one or
two disks. It gives at most eight total interior incidences, while
this lemma gives at least nine. Applying that contradiction uses the separately written endpoint-disk topology
and truth/Fourier incidence bridge for the Boolean representative, composed
in UNION12.md under its explicit inherited assumptions. Those claims are not
premises proved by the small controls here; no canonical exclusion follows
from1399 alone. In particular no complete manifold/catalog claim, Boolean
function, human review, proof-assistant formalization or novelty is claimed.
