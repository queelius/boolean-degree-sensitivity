# Three exceptions: no ordinary vertex has a disconnected link

Alexander Richard Towell, with Claude Code (Anthropic) assistance. Proposed
written argument with an exact search (PLAN.md step 4). Independently
reviewed by Codex (OpenAI; REVIEW-cross-edges-codex.md): sound after the
fixes recorded there, which are applied. No original magnitude pattern is excluded.

## Claim

In each of the 23 pair-only open Type II shapes, at c = 1 and c = 2, the
unit link of every ordinary vertex is a sphere. With VERTEX-TYPES.md this
makes every vertex link a sphere outside the triangle --- shape (where
exceptional links may still split or form bowties).

## Setting

As in VERTEX-TYPES.md. An ordinary vertex w (in no exceptional pair) has
all pair links C4 or C5, so its unit link is a union of closed surfaces
with chi = 2 and all degrees 4 or 5. If it is disconnected it is two
six-vertex projective planes (K6, all degrees 5) on sets A and B, which
together hold all twelve other vertices. Every pair inside A, inside B,
or through w is an edge, 42 in all, so with E = 49 + c there are
M = 7 + c cross edges between A and B. A vertex v in A has its five
A-neighbours, w and cross(v) neighbours in B, so D_v = 6 + cross(v), and
since every cross edge has one end in each side,

    M = sum over A of cross(v) = sum over B of cross(v).

For v in A the link of vw is the link of v in the K6 on A, a C5 on A - v,
so w has degree 5 in the link L_v of v, adjacent to exactly A - v.

## Local facts

Sphere premise for F2 and F3. An ordinary vertex with cross degree 0 or 1
has a link on 6 or 7 vertices, and its only disconnected alternative needs
twelve, so its link is a sphere. An exceptional vertex outside triangle
--- has a sphere link by VERTEX-TYPES.md. An exceptional vertex of
triangle --- has cross degree at least 2 by F1, so F2 and F3 never apply
to it.

(F1) Exceptional vertices. Outside triangle ---, L_v is a sphere of an
order allowed by VERTEX-TYPES.md for the type of v. In triangle --- each
vertex has d >= 6 + 2 = 8 by P_x = 2d - 4 and pair inversion (REVIEW-
vertex-types.md), so cross >= 2.

(F2) Cross degree 0. Then L_v has the six vertices (A - v) + w, with w
adjacent to the other five. Removing the open star of w leaves a
triangulated pentagon with no interior vertex; its two ears have degree 3
in L_v, and the other degrees are 4, 4, 5. A link degree 3 means a +1
partner and no partner can have degree 6. So v has exactly two +1
partners, both in A, and no -2 partner: v has type (0,0,2). In
particular an ordinary vertex has cross degree at least 1.

(F3) Cross degree 1. Let z in B be the cross neighbour of v in A, with L_v
a sphere on (A - v) + w + z. Removing the open star of w leaves a disk
with boundary the 5-cycle on A - v and one interior vertex z. If z is not
adjacent to all five boundary vertices, the disk has a chord (if there is
no chord, every boundary edge has its disk triangle through z), and the
side of the chord without z is a triangulated polygon. Choose an ear of it
whose tip is not an endpoint of the chord: the third vertex if it is a
triangle, otherwise one of two non-adjacent ears. That tip has degree 2 in
the disk, so degree 3 in L_v, hence it is a +1 partner of v in A. So if v
has no +1 partner in A, then z is adjacent to all of A - v and to v:
cross(z) = 6. This covers every ordinary v (degrees 4 and 5 only).

## Search

`step4_count.py` enumerates, for each shape and constant, every side
assignment of the exceptional vertices, every cross value allowed by F1
and F2 for them, and every multiset of ordinary cross values in 1..6 on
each side. It requires both side sums to equal M = 7 + c and, for every
vertex of cross degree 1 to which F3 applies, a vertex of cross degree 6
on the other side. No configuration survives, for any shape at either
constant.

Controls: without the F3 rule 32 shape-constant pairs survive; without
the F2 side rule P4 +++ survives at c = 2. Both rules are load-bearing,
and both are proved above in exactly the form used.

## Premises and scope

Conditional on VERTEX-TYPES.md (and its premises), the identities
Q_v = 2D_v - 4 and E = 49 + c, and the K6 description of a disconnected
ordinary link (as in the accepted two-exception theorems, where it uses
only degrees 4 and 5). The doubled-quartic shape 1 is not covered.
Global status: OPEN.
