# 016: the one-free residual-six case (Types I, II, III)

Claude Code (Anthropic), 2026-10-23, for Alexander Richard Towell. The
source theorems are OpenAI Codex-assisted work. Every result here is a
written argument or a small exact check, reviewed by fresh AI subagents
(not human review). Accepted into checkpoint 1532 through
`H/one-free-residual6-acceptance-cycle1532.json`, with the typed frontier
`H/one-free-residual6-frontier-cycle1532.json`. No solver was run. Global
status: OPEN; the 29 open original magnitude patterns are unchanged.

## Why not the 014 pipeline

The two-free branch had a proved structural theorem (1412: the centre link
is a 2-sphere) that gave a native row model for the CP-SAT/LRAT pipeline.
The one-free case has no such theorem; 1513 classifies it into three
necessary types, each a local problem about one derivative p = Delta_u f.
So the work here is local theorems, extended or new.

## Results

| Case | Result | Note | Review |
|---|---|---|---|
| Type III, c = 0, 3 | excluded (9 subcases) | TYPE-III-CLOSURE.md, EXTENSION-plus-plus-c3.md | REVIEW-closure.md, REVIEW-plus-plus-c3.md (both sound after fixes) |
| Type I, c = 1, 2 | excluded | TYPE-I-CLOSURE.md | REVIEW-typeI.md (sound) |
| Type II, doubled quartic with a private vertex | excluded (105 of 136 shapes) | TYPE-II-PRICING.md | argument reviewed for two departures in REVIEW-closure.md and with three in REVIEW-star.md; the shape list re-derived in REVIEW-rigid.md |
| Type II, six covered doubled-quartic shapes | excluded | TYPE-II-RIGID-SHAPES.md | REVIEW-rigid.md (sound after fixes) |
| Type II, three +1 pairs at one vertex | excluded | TYPE-II-PLUS-STAR.md | REVIEW-star.md (sound) |
| Type II, 23 pair-only shapes and rigid shape 1 | OPEN | TYPE-II-PRICING.md | |

Type III: the constant enters the accepted c in {1,2} theorems only through
the cross-edge bound M = E - 42 = 7 + c (and, for (+1,+1), the catalog scan
range E <= 52); at c = 3 the bounds still contradict, except (+1,+1), which
needed a new argument (cases (a)/(b) with link lemmas L7, L8). The doubled
quartic proofs never use c. 1527 already covered adjacent -2,-2.

Type I: the accepted reductions (1395, 1513/1523) force each endpoint link
of the -3 pair to be a sphere with one degree-7 vertex and all others of
degree 4 or 5. No such sphere exists at any order (hand proof supplied by
the reviewer and checked; enumeration and an independent disk search agree).

## Checks and tests

All run with `.research/venv-exact/bin/python`, from this directory, with
`PYTHONPATH=../015-sphere-catalog-audit`, in normal and `-O` mode:

- `link_lemmas.py` / `test_link_lemmas.py` (L7, L8; 6 tests)
- `one_seven_spheres.py` / `test_one_seven_spheres.py` (Type I controls; 4 tests)
- `type2_shapes.py` / `test_type2_shapes.py` (136 Type II shapes, private
  filter, brute-force cross-check of the 24 pair-only classes; 4 tests)
- `rigid_shape_facts.py` / `test_rigid_shape_facts.py` (S3, S4, S6; 2 tests)
- `vertex_type_screen.py` / `test_vertex_type_screen.py` (one-vertex screen; 2 tests)
- `one_free_frontier.py` (producer) / `one_free_frontier_reader.py`
  (independent reader: enumerates shape classes by Venn-region sizes, no
  pynauty, no shared code) / `test_one_free_frontier.py` (10 tests,
  including negative controls)

## Premises

Each closure inherits its source theorem's accepted premises (listed in
each note): the 1513/1523 trichotomy and its chain, the local one-six-edge
and one-three-edge arguments, endpoint sphere catalogs and their
inverse-cover completeness (now independently re-proved in 015 for orders
up to 12), the 76-record scan and the Frick 2015 catalog for (+1,+1), and
the 1526/1527 acceptance. Old finite certificates were replayed only by AI
reviewers into scratch files, not by a frozen successor checker.

## Next

The 24 remaining Type II shapes need what the two-exception theorems had:
a structural step for three exceptions, a root-link and placement cover,
a model producer with an independent row reader, and certificates (the 014
LRAT pipeline can do the last step). That build is attempt 017.
