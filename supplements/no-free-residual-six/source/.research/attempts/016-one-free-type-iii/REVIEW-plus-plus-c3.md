# Independent adversarial review of EXTENSION-plus-plus-c3.md (2026-10-23)

Reviewer: a fresh Claude subagent given the note, the source theorem and
audit, the 76-record scan and the link-lemma checker, and asked to break
each step. AI review, not human review. Verdict: SOUND, with one checker
fix and wording fixes.

## What the reviewer independently did

- Re-derived 4m_A = k_A + t_A, P_v = 2D_v - 4, y_v = 2D_v - 12 + z,
  Q = E - 13 = 36 + c, link chi = 2, and the f-vector (13, 52, 78, 39) at
  c = 3.
- Checked that cases (a) and (b) are exhaustive, including every position
  of the doubly bad vertex t in case (b) (t = z, t in A, no t, t in B\z).
- Wrote its own sphere enumerator (edge completion with pynauty canonical
  forms, no shared code): counts 1, 1, 2, 5, 14 for n = 4..8. The unique
  degree-{4,5} 7-sphere is the pentagonal bipyramid and L7 holds; the
  unique degree-{4,5} 8-sphere is the snub disphenoid, and exactly 7 edges
  join the two non-neighbours of each degree-5 vertex to its neighbours
  (L8, tight). It also confirmed the pentagon fact: no 6-vertex sphere has
  degrees (5,3,4,4,4,4).
- Rescanned the published catalog file: 4,787 records, 76 targets with 13
  vertices and E <= 52 (by E: 47:1, 48:3, 49:15, 50:25, 51:29, 52:3), each
  with an induced subcomplex of Euler characteristic outside {0,1,2} by
  brute force over all 8,192 subsets. E = 52 is non-vacuous (3 records).
- Confirmed the application: the (+1,+1) Type III derivative meets every
  hypothesis, and found no other use of c <= 2 in the part of the source
  that is used.

## Issues and response

1. Needs fix: `link_lemmas.py` certified only >= 3 edges for L8 while the
   proof uses 7. Fixed: `lemma8` now defaults to need = 7 and the
   docstring says so; tests still pass in normal and -O mode.
2. Wording: why w is good, and M = E - 42 is an equality. Fixed.
3. Wording: the 0/1 ordinary quadratic coefficients come from the general
   one-free derivative (Mobius inversion), not from Type III. Fixed; the
   note now says this also rules out the source's coefficient-two branch,
   which does need c <= 2.
4. Wording: two compressed steps in section 1 (cycle pair links give two
   tetrahedra per triangle; sum(6 - deg) = 6 chi gives the six-vertex
   projective plane). Expanded.
