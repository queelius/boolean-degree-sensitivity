# Independent extension of the adjacent two-minus-two derivative obstruction

Alexander Richard Towell; substantial OpenAI Codex assistance. 21 October 2026.

**Accepted at constants zero and three, with the same ordinary-coefficient
guards as the older constants-one/two theorem.** The structural extension
and a fresh independent replay of all nine retained contradictions pass.
This excludes only the adjacent `-2,-2` subcase of the cycle1513 Type III
one-free allocation. It does not exclude all Type III cases, a whole
magnitude pattern, or the original Boolean14 problem. All 29 whole
patterns remain open.

The new proposal is
`009-parent-analysis/adjacent-two-negative-constant-extension-cycle1526.md`,
SHA256 `f08efaee4026d47ce3be2c1ad167dfcc65893aedd1696d3e3dc4e6071998f78b`.
Its handoff SHA256 is
`e6bb82b7832d7e9298c9b7aeb6602d04e32bb925670cfadefb1b785727a4a5cf`.
The accepted old compact verification report is
`12f650e0fcfc141de7195d46641342704cea93255093c20e43dbfaea4db6c090`;
the unchanged literal compact proofs are
`d98b5ca81b5b848dd36977b637c658284edc9138aa093132ac88ceae6d1e7d50`.
All predecessors remain immutable.

## Exact theorem and local identities

Let `p` be a ternary polynomial on thirteen Boolean coordinates, origin
one and units zero, with

```
16p=c+sum_(|A|=2) k_A chi_A+sum_(|D|=4) h_D chi_D.
```

Assume `c in {0,1,2,3}`, every `h_D in {0,1}`, exactly two distinct
adjacent pairs have `k_A=-2`, all other pair numerators are `-1/0`, and
all ordinary quadratic coefficients are `0/1`. No such polynomial exists,
conditional on the explicitly inherited complete sphere cover. This is
a theorem about a local derivative; it assumes neither an ordinary
coefficient two nor a global symmetry of an unknown function.

For the complex `K` of unit quartics, pair inversion gives
`4m_A=k_A+sum_(D contains A) h_D`. Integrality of the ordinary cubic
coefficient makes each pair link even. Baseline links are empty, `C4`,
or `C5`. An exceptional pair must have `m_A=1`, since otherwise its
even simple link would have exactly two edges. Every triangle contains
a baseline pair, so every present triangle has exactly two tetrahedral
cofaces. Each exceptional link is therefore `C6` or two disjoint `C3`s.

The ordinary coefficients are the alternating face indicators; thus
`p(1_X)=1-chi(K[X])` and every induced Euler characteristic lies in `[0,2]`.
Writing `A` for the total quadratic Fourier sum and `P` for the number
of tetrahedra, the origin and summed unit equations are
`c+A+P=16`, `2A+4P=104`. They give

```
P=36+c,  E=49+c,  F_2=72+2c,
P_v=2D_v-4.
```

All thirteen vertices are active. If `v` meets `z` exceptional pairs,
then `4D_v+2z <= 3P_v=6D_v-12`, giving `D_v>=6+z`. These calculations
are independent of any whole-complex manifold assertion.

The previously accepted splitting proof at each private endpoint is local
and independent of `c`: a split exceptional link would need a sphere
with at least eight vertices and another positive-characteristic component
with at least six, exceeding thirteen split vertices. Thus both exceptional
links are `C6`. Private endpoint links are spheres by the accepted one-six
component obstruction. At the common endpoint, two separated degree-six
vertices invoke that same obstruction; if they lie in one component,
that component needs at least seven vertices and an additional component
at least six, exceeding twelve. This part reuses the accepted written
local argument, not the old final theorem outside its declared constants.

## The new cross-edge bound

Suppose an ordinary center `w` has disconnected link. Its two components
have six vertices each and complete skeletons. Denote those sets by `A,B`.
The twelve center edges and two fifteen-edge cliques account for 42
edges. Since these vertices exhaust all thirteen coordinates, every
remaining edge joins `A` to `B`; hence

```
M <= (49+c)-42 <= 10.
```

Among `A union B` there are nine ordinary vertices, two private exceptional
endpoints, and one common exceptional endpoint. A private endpoint needs
at least one cross neighbor and the common endpoint at least two, because
its own clique and `w` supply only six neighbors. Every ordinary vertex
also needs a cross neighbor. Otherwise its six-vertex link would be a
sphere, necessarily the octahedron, but the vertex `w` in that link has
degree five, a contradiction.

If all nine ordinary vertices had cross degree at least two, the total
cross degree would be at least `9*2+1+1+2=22`, forcing `M>=11`.
Consequently an ordinary vertex `a` has exactly one cross neighbor `b`.
Its seven-vertex link is the accepted pentagonal bipyramid. Within that
link, `w` has degree five and is nonadjacent to `b`, since triangles
through `w` never cross the two components of `link(w)`. Thus `w,b`
are the bipyramid's two apices. The vertex `b` is adjacent in `K` to
the five other vertices of `a`'s clique, as well as to `a` itself.
These are six cross edges incident with `b`.

Each of the other five vertices on `b`'s side still requires a cross
neighbor. Their edges are distinct from those six, giving `M>=6+5=11`,
again contradictory. This argument uses only the small ordinary link
types already covered in the accepted sphere classification. It proves
all ordinary links spherical with `M<=10`, so applies to `c=0,3` as
well as the old `c=1,2` cases.

No global flagness, Walkup theorem, whole-complex three-sphere assertion,
or geometric realization is used. The common root link has two
degree-six vertices and all other degrees four/five. Curvature and the
twelve available coordinates give the same order-eight-through-twelve
cover, with no constant dependence.

## Inherited cover and newly reconstructed rows

The accepted inverse-contraction sphere cover and its prior complete filter
are explicit inherited premises. Their nine literal common-root types are

```
(8,12), (9,32), (10,74), (10,75), (10,168),
(11,499), (11,764), (12,2537), (12,5741).
```

The new reader binds that accepted report, checks the nine saved literals
against it with exact identities, and freshly checks each literal's face
counts, edge incidences, vertex-circle links, connectivity and degree
metadata. It does not re-enumerate the sphere catalogs or their inverse
transitions. The six ordinary flag link types and three private flag link
types of orders 9/10/11 remain inherited completeness premises.

Only the retained 945 rows are reconstructed, from their literal supports
as sets of coordinates. No full row model is built. Saved original row
indices serve only as historical provenance; the present proof depends
on the row formulas themselves. The fresh family counts are:

| Necessary row family | Rows |
|---|---:|
| Fixed root-link values | 457 |
| Downward face inclusion | 98 |
| Triangle coface equations | 78 |
| Ordinary edge valence bounds | 97 |
| Ordinary vertex-link flag inequalities | 102 |
| Private endpoint-link flag inequalities | 63 |
| Private endpoint degree 9–11 | 2 |
| Induced Euler bounds | 47 |
| No independent triple | 1 |

The root rows come from the exact root triangle closure. Downward rows
assert `x_F<=x_G` for a codimension-one subface. The coface equation is
`sum_(Q contains T)x_Q=2x_T`. Ordinary valence rows assert
`0<=sum_(Q contains e)x_Q-4x_e<=1`, explicitly rejecting exceptional
edges. For an induced set `X`, the Euler row is exactly
`-|X|<=-sum edges+sum triangles-sum tetrahedra<=2-|X|`.
Flag rows are used only at classified ordinary or private vertices;
the common exceptional root is explicitly rejected. Private degree
rows use the accepted complete 9/10/11 endpoint cover. The no-independent-
triple row is also a necessary consequence of the induced Euler bound.

No retained family uses `E`, `P`, `F_2` or another global count. The reader
rejects an attempted `face_count` row rather than silently ignoring it.
All reconstructed rows are therefore valid under the new structural
premises at constants zero and three.

## Independent exact replay and controls

For each saved deduction `x_v=b`, the new reader assigns the opposite
value `1-b` and computes exact bounds on its reason row. If the assigned
part sums to `s` and the remaining coefficients are `c_i`, its doubled
center and radius are

```
C=2s+sum c_i,     R=sum |c_i|,
[minimum,maximum]=[(C-R)/2,(C+R)/2].
```

The opposite interval must miss the allowed interval. The reader then
records the forced bit and finally requires a contradictory terminal row.
All 1,111 deductions and nine terminal contradictions pass. This is a
fresh algebraically equivalent interval implementation, not a call to
the old verifier or its assertion-based helpers. Every check remains
active under `-O`; the old verifier was neither imported nor executed.

The controls were written before the new reader. The preserved initial
run fails because the reader did not yet exist. Six small controls then
passed before the first retained-row replay, and a seventh cover-corruption
control was added before final validation. The final seven tests pass in
normal and optimized modes. They independently compare interval extrema
against all completions of a three-variable fixture; accept a genuine
binary contradiction; reject a wrong forced bit, repeated assignment,
absent variable, noncontradictory final row, Boolean/integer alias, altered
coefficient, global-count row, wrong common-root flag row, malformed root,
omitted/duplicated case, and changed literal cover. The cross-edge control
also records that an upper bound of eleven would no longer contradict
either lower bound, preserving the essential constant guard.

Normal and optimized full reports agree exactly apart from timing. The
normal replay used about 0.143 CPU seconds; the instrumented replay about
0.774. Every checker/test process enforces five CPU seconds, fifteen wall
seconds, and 512 MiB. Coverage of the new reader is 251/251 statements and
50/50 branches; this is software-control coverage, not formal proof.
There was no solver query, full-model construction, catalog re-enumeration,
or new contradiction search.

Reproduce from the repository root:

```
/home/spinoza/venv/bin/python .research/attempts/008-sparse-spectrum-proof/test_adjacent_negative_extension_cycle1527.py -v
/home/spinoza/venv/bin/python -O .research/attempts/008-sparse-spectrum-proof/test_adjacent_negative_extension_cycle1527.py -v
/home/spinoza/venv/bin/python .research/attempts/008-sparse-spectrum-proof/adjacent_negative_extension_cycle1527.py --output /tmp/adjacent-negative-replay-cycle1527.json
/home/spinoza/venv/bin/python -O .research/attempts/008-sparse-spectrum-proof/adjacent_negative_extension_cycle1527.py --output /tmp/adjacent-negative-replay-O-cycle1527.json
```

The conditional strengthening is suitable for the next coherent archival
research version, with the historical cover and source pins retained.
This is independent AI mathematical review plus exact finite computation,
not human peer review, proof-assistant formalization, a novelty assessment,
or a whole-pattern result. No publication action or ledger edit occurred.
