# Empty3211111: connected odd-support branch

This is a proposed conditional exclusion pending independent audit. The
Boolean14 problem and the magnitude pattern3211111 remain open. This note
handles only the case where the six odd-weight negative supports are connected
under intersection in four coordinates.

Write Q for the negative quintic of magnitude3, P for the one of magnitude2,
and R1,...,R5 for the units. Their total Fourier defect is28. Consequently
all other quintics are0/1, all cubics are-1/0, and every singleton is1/2.
The empty representative's zero-triple graph H has130 edges and
deg_H(i)=29-k_i, so every vertex deletion has101+k_i>=102 edges.
The accepted negative-free derivative theorem requires these seven supports
to cover all14 coordinates.

First, Q intersects P. Otherwise the top Fourier convolution on Q union P
has the positive term6. Only the other five unit negatives can give negative
terms, each of size at most1 because all nonnegative quintics are0/1. Every
negative-negative term is nonnegative. The sum is therefore at least1,
contradicting g squared being1. This deduction applies to the entire magnitude
pattern, not merely the connected branch.

Let S be the union of the six odd supports Q,R1,...,R5. If their Johnson-four
graph is connected, then |S|<=10 by a spanning-tree union count. The ordinary
intersection graph of all negative supports is connected, so P meets S.
Covering14 coordinates now forces |S|=10 and P intersection S={s}. Since Q
meets P, s belongs to Q. The complete, independently audited connected-six
support catalog in006 has64 classes of union size10. Marking Q and choosing
s in Q gives64*6*5=1920 literal placements. No invariance of f is assumed.

## Exact support and deletion checks

For a ten-set T, the sum of k_L*k_(T minus L) over its126 unordered five-set
partitions is zero. In each term the negative coefficients are fixed and
each other coefficient independently lies in{0,1}. Taking each term's
minimum gives a rigorous lower bound, even without requiring consistency
between different ten-sets. This excludes1172 placements. In654 more, s
belongs to every negative support. After deleting s, the only possible bad
quartets are Q-s and P-s, both nonfull, which contradicts the accepted
order13 bound for at most two nonfull bad quartets.

The remaining94 placements are checked literally. A quartet U can have
excess max(0,Z_H(U)-2) at most

    min(2, floor(sum of negative magnitudes on quintics containing U / 2)).

Indeed a_U=Z_H(U)+f(U)-2, while self-duality gives
a_U=-(sum of quintic numerators above U)/2. Dropping all nonnegative
contributions proves the displayed upper bound. Deleting a coordinate
removes exactly the quartet permissions containing it.

For80 placements the checker supplies a deleted coordinate and a five-set
window such that all surviving permissions are nonfull and at most two
quartets lie outside that window. The two outside quartets, if both exist,
meet in at most two coordinates. The independently accepted
`two-quartets-five-window.md` theorem bounds the remaining graph by101 edges,
contradicting101+k_i>=102.

For the final14, deleting s leaves one possibly full quartet A=Q-s and
the disjoint nonfull quartet B=P-s. Such a13-vertex graph also has at most101
edges. Here is the short catalog argument. It suffices to consider102 edges,
since deletion preserves these permissions. At most three triple deletions
repair A and B. A one-deletion repair gives G101, where any missing triple
creates at least four obstructions, exceeding the two permitted quartets.
A two-deletion repair gives G100=G101 minus an old edge; at least one of the
two restored triples is not that old edge and creates at least three
obstructions, again impossible. For a minimum three-deletion repair, A must
be full and B must be bad; the repair consists of two A-triples and one
B-triple. Each removed A-triple individually creates exactly one obstruction,
namely A. This contradicts the complete G99 catalog property that at most one
missing triple has exactly one obstruction. The same proof allows A and B
to meet in at most two coordinates.

Thus all1920 placements in this branch are excluded. The full pattern is
not excluded: its six odd supports may have two or more Johnson components.

## Reproduction and external inputs

The first screen is `empty_3211111_connected_odd.py` and its immutable result
`empty-3211111-connected-odd-verification.json`. The follow-up
`empty_3211111_connected_odd_finish.py` reconstructs the raw cases and records
all94 explicit deletion witnesses. Tests compare the top interval formula
against every binary completion in small controls, preserve a genuinely
inconclusive interval example, reject use of the nonfull theorem on full
permissions, and replay the complete cover. An initial test fixture had
incorrectly predicted a top contradiction; exact evaluation showed the
interval was inconclusive, so the fixture was corrected before any exclusion
or report was claimed. It is retained as the inconclusive control.

The external completeness input remains the already audited Markstrom--Talbot
order13 extremal catalogs and the published small-valence manifold catalog
used by the negative-free derivative theorem. Connected support coverage is
proved by the separate explicit transition-bijection audit in006. Every
dependency is hash-bound in the accompanying report and manifest. No solver
status, averaging assumption, or unverified candidate classification is used.
