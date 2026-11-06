# Controls from the n = 13 witnesses

Claude Code (Anthropic), 2026-10-23. Exact computation on saved truth
tables (`controls_n13.py`, result `controls-n13.json`); no solver.

All 104 self-dual degree-5 witnesses on 13 variables from attempt 012 have,
at scale k_S = 16 hat g(S) with g = 1 - 2f: weight only on levels 1, 3, 5,
level sums (4, -72, 84), sum of squares 256. Their negative quintics number
6 to 17 (magnitudes 1 to 3), and 102 of the 104 have negative-support union
13: at n = 13 the no-free situation is realizable.

Only four witnesses have a coordinate in exactly one negative quintic (five
coordinates in all). At each, the derivative 16 Delta_u f has one negative
quartic of magnitude 1 or 2, but also many other departures: pair
numerators -3, -2, +1, +2, quartic numerators +2, constants 0 to 3. None is
in the clean regime targeted by PLAN.md step (c) (one negative quartic,
everything else incident baseline), so they are consistent with such a
lemma, not counterexamples. They are the controls any proposed version of
step (c) must survive once the coordinate count is adjusted (they live on
12 coordinates, not 13).
