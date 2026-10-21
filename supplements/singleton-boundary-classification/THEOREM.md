# A divisible singleton Fourier component on ten coordinates

Alexander Richard Towell, with substantial OpenAI Codex assistance.
Written 21 October 2026. License: CC-BY-4.0.

This is a standalone component lemma. It does not construct a fourteen-
variable Boolean function or settle the degree/sensitivity existence problem.
Novelty, human peer review, and formal verification are not established.

## Theorem

For subsets of ten coordinates write `chi_S(x)=(-1)^(sum_{j in S}x_j)`.
Suppose

    B(x)=a-sum_{e in M}chi_e(x)+sum_{F in P}chi_F(x),

where `a` is 1 or 2, M is a simple family of pairs, and P is a simple family
of four-sets. There are no other Fourier terms. Assume every cube value
is divisible by 8, `B(0)=0`, precisely two singleton inputs `e_u,e_v`
have value -8, and the other eight singleton inputs have value 0.

Then `a=1` and

    B=(1-chi_{uv})(1-sum_{e in C}chi_e),

where C is a simple five-cycle on five of the eight coordinates outside
`{u,v}`. Conversely every such cycle satisfies all hypotheses, with values
in `{-8,0,8}`. There are 672 distinct forms for a prescribed pair and 30,240
over all exceptional pairs. Each has six negative pair coefficients,
five positive quartic coefficients, and exact real degree 4.

## Common incidence and parity facts

Let `m_j,p_j` be the incidences of j in M,P. Origin and singleton
evaluation give

    |P|=|M|-a,  p_j=m_j+4[j in {u,v}].

Summing incidences gives `4|P|=2|M|+8`, hence

    |M|=2a+4,  |P|=a+4.                                      (1)

Integer Mobius inversion expresses every ordinary multilinear coefficient
of B as an alternating sum of cube values, so each is divisible by 8.
The coefficient of `x_i*x_j` is

    4(#{F in P:{i,j} subset F}-[ij in M]).

Because M is simple, its edge set is therefore exactly

    M = symmetric_difference_{F in P} E(K_F).                 (2)

Here `K_F` is the complete graph on F. All graph sums below mean symmetric
difference; unqualified degrees mean ordinary nonnegative graph degrees.

A simple nonempty even graph decomposes into edge-disjoint simple cycles:
follow unused edges until a vertex repeats, remove the resulting cycle,
and repeat. Every such cycle has at least three edges. Consequently an
even simple graph with four edges is C4 and with five edges is C5.

We also use the elementary fact that a subgraph of a complete bipartite
graph on disjoint parts K,D cannot have degree 0 on K and positive degree
on D. Every edge meeting D also meets K.

## Classification when a=1

Equation (1) gives `|M|=6, |P|=5`, and `p_u,p_v` are 4 or 5.

Suppose `p_u=4`. Then `m_u=0`. At least three quartics contain both u,v,
and their number is even by (2), so exactly four do. Write these as
`uv union e` for four distinct ordinary edges e of a graph G. Parity at
each pair `u,w` makes every degree of G even; hence G is C4.

If `p_v=5`, the fifth quartic is v plus three ordinary vertices. G has
even degrees, so (2) puts all three pairs from v to these vertices in M,
contrary to `m_v=1`.

If `p_v=4`, the fifth quartic F avoids u,v. The ordinary negative graph
is `G symmetric_difference K_F`. At every ordinary vertex w,

    p_w=deg_G(w)+[w in F],
    m_w=deg_G(w)+3[w in F]-2deg_(G intersect K_F)(w).

Thus `G intersect K_F` has degree 1 at all four vertices of F. Every such
vertex belongs to G, so F equals G's four-vertex support. The intersection
is then the entire four-cycle, whose degrees are 2: a contradiction.
Interchanging u,v also rules out `p_v=4`.

It follows that `p_u=p_v=5` and `m_u=m_v=1`. All five quartics are
`uv union e` for a simple five-edge graph G. Parity places uv in M,
exhausting both exceptional negative incidences. Parity at `u,w` now
forces G even, hence C5. Equation(2) gives exactly
`M={uv} union E(G)`, proving the displayed factorization.

## Exclusion when a=2

Now (1) gives `|M|=8, |P|=6`, and each exceptional positive incidence
lies in `{4,5,6}`. Let k be the number of quartics containing both u,v.
The four classes containing both, u only, v only, neither have sizes

    k, p_u-k, p_v-k, 6-p_u-p_v+k.

The edge uv is negative exactly when k is odd. If either exceptional
incidence is 4 its negative degree is 0, so k is even. Swapping the names
u,v covers both orders of unequal incidences without assuming symmetry
of an unknown function.

### An incidence 6

Take `p_u=6`.

* If `p_v=6`, all quartics are `uv union e` for six ordinary edges G.
  The ordinary M graph is G and uv is absent. The two exceptional negative
  degrees are both 2, so M would have `6+2+2=10` edges, contrary to 8.
* If `p_v=5`, five quartics are shared edges of G and the last is `u union A`
  for a triple A. The negative edge uv exhausts `m_v=1`, forcing G even.
  Equation(2) then puts all three edges u-A in M as well as uv, contrary
  to `m_u=2`.
* If `p_v=4`, four shared quartics give G and two are `u union A,u union B`.
  G is even because `m_v=0`. The required `m_u=2` forces `A triangle B`
  to be a two-set D; `K=A intersect B` is a two-set disjoint from D.
  Their triangle graphs differ by `J=K_(K,D)`. Ordinary M is `G triangle J`,
  with the additional edges u-D. If `I=G intersect J`, the ordinary
  incidence equations give `deg_I=0` on K and `deg_I=1` on D. This is
  the impossible bipartite degree pattern above.

### Incidences 5 and 4

For `(p_u,p_v)=(5,4)`, counting and parity give k=4. Four shared quartics
give an even G, one is `u union A` for a triple A, and one is ordinary.
Parity puts three edges u-A in M, contrary to `m_u=1`.

For `(5,5)`, k is 4 or 5.

* If k=5, the five shared quartics give G and the remaining quartic F
  is ordinary. The edge uv exhausts both negative degrees, making G
  even and therefore C5. Equality of ordinary incidences forces
  `G intersect K_F` to have degree 1 at all four vertices of F. They must
  lie on the cycle. Its induced graph on any four vertices is a
  three-edge path, not a perfect matching: a contradiction.
* If k=4, the other quartics are `u union A,v union B`. Let H be G's
  odd-degree vertex set. Since both negative degrees are 1 and uv is
  absent, there are ordinary vertices p,q with
  `A=H triangle {p}`, `B=H triangle {q}`. If p=q, the triangle graphs
  cancel and M has only four ordinary edges plus u-p,v-p, totaling 6.
  Otherwise `A triangle B={p,q}=D` and their intersection is a two-set K
  disjoint from D. Their triangle difference is `J=K_(K,D)`. Ordinary
  M is `G triangle J`, with additional edges u-p,v-q. The ordinary
  incidence equations again force intersection degree 0 on K and 1 on D,
  impossible. This argument does not assume G even.

### Incidences 4 and 4

Both exceptional negative degrees vanish. Counting and parity leave
only k=2 or 4.

If k=4, the shared G is an even four-edge graph, hence C4. The two other
quartics A,B are ordinary and distinct. Put `r=|A intersect B|`,
`J=K_A triangle K_B`, and `I=G intersect J`. On a vertex belonging to just
one of A,B, J has degree 3 and its extra positive incidence is 1, so I
must have degree 1. On a common vertex J has degree `8-2r` and its extra
positive incidence is 2, so I must have degree `3-r`. For r=0,1,2 this
requires respectively 8,7,6 vertices of positive I degree, exceeding G's
four-vertex support. For r=3, I needs degree 1 on the two exclusive
vertices and 0 on the common three-set, while J is the complete bipartite
graph between these parts. This is impossible.

If k=2, the shared G has two ordinary edges. The remaining quartics
are `u union A1,u union A2,v union B1,v union B2`. Their triples obey

    A1 triangle A2 = H = B1 triangle B2,

where H is G's odd-degree vertex set.

* If G's edges meet, write them ac,bc, so H={a,b}. There are ordinary
  two-sets K,L disjoint from H such that the A triples are K+a,K+b and
  the B triples L+a,L+b. Ordinary M is
  `G triangle K_(H,K triangle L)`. A vertex in `K intersect L` would have
  the same negative degree as in G but four additional positive incidences,
  so K,L are disjoint. If c lies in their union, its two G edges cancel
  and its negative degree is 0 versus positive incidence 4. If c does not,
  each vertex of H has negative degree 5 versus positive incidence 3.
* If G's edges are disjoint, H has four vertices. Each triple pair has
  one common center outside H and partitions H into two pairs. The
  triangle sum consists of a matching on H and the four-edge star from
  the center to H. Equal centers cancel both stars, giving negative
  degree 0 versus positive incidence 4 at that center. Distinct centers
  each have negative degree 4 versus positive incidence 2. G has no edge
  at either center.

These contradictions cover every exceptional incidence pair, every
permitted k, and both two-edge graph shapes. Therefore a=2 is impossible.
This is a written completeness proof; the catalog checker does not
purport to brute-force every six-quartic family.

## Converse, distinctness, and count

For a cycle C, the product of its edge characters is 1 because every
vertex has degree 2. There are therefore 0, 2, or 4 negative edge signs,
whose sums are 5, 1, or -3. The product in the theorem is 0 when `chi_uv=1`
and otherwise is respectively -8,0,8. Its origin and singleton values
are exactly the prescribed ones. Expanding it gives six distinct negative
pairs and five distinct positive quartics, proving every hypothesis.

The exceptional pair is distinguished by its two negative singleton
values. For a fixed pair the cycle is distinguished by its quartic
Fourier supports. Choose five of the other eight coordinates and one of
`(5-1)!/2=12` unoriented cycles on them. This gives `binom(8,5)*12=672`
forms per pair and `binom(10,2)*672=30,240` in total. No quotient by a
symmetry of a fourteen-variable function is assumed.

## Verification scope

The standalone scripts independently generate/enumerate this entire cycle
family and verify every input, Fourier coefficient, and required zero.
Those finite checks establish the catalog and converse; classification
completeness, including a=2, rests on the written proof above. Earlier
independent AI reviews of its two parts are recorded in PROVENANCE.json
and REVIEW_HISTORY.md. The parent reviewed the written case split and independently replayed the
portable catalog; qa/root-portable-replay.json records that scope. This is
AI review and finite verification, without human or formal verification.
