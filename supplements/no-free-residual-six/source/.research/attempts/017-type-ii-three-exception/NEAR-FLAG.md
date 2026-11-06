# Three exceptions: near-flag vertex links

Alexander Richard Towell, with Claude Code (Anthropic) assistance. Proposed
lemma with an exact check (`near_flag.py`, result `near-flag-result.json`).
Reviewed by Codex (OpenAI; REVIEW-special-codex.md): sound after the scope
fix below. No original magnitude pattern is excluded.

## Lemma

In the pair-only setting of VERTEX-TYPES.md, outside the triangle ---
shape (so not for the doubled-quartic shape 1, whose D0 vertices get no
flag rows), let v be a vertex meeting n(-2) pairs with
numerator -2 and n(+1) with +1, with (n(-2), n(+1)) one of (0,0), (0,1),
(0,2), (1,0), (1,1), (2,0). Then every 3-cycle of the link L_v that is not a
face is the neighbourhood in L_v of a +1 partner of v. In particular, for
every three vertices a, b, d other than v,

    t_vab + t_vbd + t_vad - l_vabd - sum over +1 partners y of v outside {a,b,d} of l_vyab <= 2.

## Proof

L_v is a sphere: for an exceptional v by VERTEX-TYPES.md (corollary), for
an ordinary v by CROSS-EDGES.md. It has at most 12 vertices, its degree-6
vertices are exactly the -2 partners, its degree-3 vertices exactly the +1
partners, and all other degrees are 4 or 5 (pair links C6, C3, C4/C5). So
L_v is one of the spheres on at most 12 vertices with exactly n(-2)
degree-6 and n(+1) degree-3 vertices, others 4 or 5. `near_flag.py`
lists them all from the 015 enumeration and finds every one near-flag:

| type | spheres | orders | flag |
|---|---|---|---|
| (0,0) ordinary | 6 | 6, 7, 8, 9, 10, 12 | all |
| (0,1) | 1 | 7 | none |
| (0,2) | 3 | 5, 6, 8 | none |
| (1,0) | 3 | 9, 10, 11 | all |
| (1,1) | 2 | 8, 9 | none |
| (2,0) | 9 | 8 to 12 | all |

(The (0,0) spheres are the six deltahedra; there is none with 11
vertices.) The types (1,2), (2,1), (3,0) each have one link that is not
near-flag, so no flag row is used there; they occur only at a star
centre, which is always the root, whose link is fixed.

For the row: t_vab = 1 means ab is an edge of L_v. If the three t are 1,
abd is a 3-cycle of L_v. Either it is a face (l_vabd = 1), or it is the
neighbourhood of a degree-3 vertex y, a +1 partner outside {a,b,d}, and
then vyab is a tetrahedron (yab is a face of L_v). Either way the
left-hand side is at most 2.

## Use

`model.py` adds these rows (key `flag`) at every non-root vertex of an
allowed type; `reader017.py` accepts a flag row only at such a vertex and
rebuilds it from this definition. In the 3K2 --- pilot they turn CP-SAT
UNKNOWN at 300 s into INFEASIBLE in about 3 s.

Conditional on VERTEX-TYPES.md, CROSS-EDGES.md and the 015 enumeration.
Global status: OPEN.
