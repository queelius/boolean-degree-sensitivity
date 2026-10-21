# Two local exceptions including a positive doubled quartic

Let p on thirteen Boolean variables take values in {-1,0,1}, with
p(0)=1 and p(e_i)=0, and let

    16p=c + sum_(|A|=2) k_A chi_A + sum_(|D|=4) l_D chi_D.

All ordinary quadratic coefficients are0 or1 except m_ab=2. Consider
either two distinct l_D equal to two with every k_A in{-1,0}, or one
l_D equal to two together with one k_J in{+1,-2}. All other l_D are0
or1 and all other k_A are-1 or0. Both alternatives are impossible.
This local argument needs no bound on c and no manifold catalog.

The already independently accepted ordinary-coefficient0/1 version
is in `006-solver-resume/two-exception-positive-extension.md`. The
present note adds the special ordinary coefficient two. It is a
candidate theorem until a separate audit is bound.

## A reusable private-vertex obstruction

Suppose w lies in exactly one doubled quartic D, lies outside{a,b},
and is incident to no exceptional quadratic numerator. Every pair
through w is then an ordinary baseline pair. The inversion identity
`4m_A=k_A+sum_(Q containing A) l_Q` and even weighted link degrees imply
that a pair in D has a residual unit C3 after deleting its doubled
edge. Every other nonempty pair link through w is C4 or C5.

The link at w formed only from unit tetrahedra is consequently a
disjoint union of closed triangulated surfaces, with exactly three
degree-three vertices and all other degrees four or five. Its vertex
set is unchanged by deleting the doubled tetrahedron. If d is its
number of vertices, the origin/unit and pair identities give weighted
incidence2d-4; deleting weight two leaves2d-6 faces. The link has Euler
characteristic three on at most twelve vertices. The independently
accepted elementary surface lemma excludes it. This calculation uses
only coefficients incident to w; an exception elsewhere is irrelevant.

## Two doubled quartics

Let the two doubled quartics be D1,D2. If their symmetric difference
contains a vertex outside{a,b}, the private-vertex obstruction applies.
Otherwise, after exchanging the two quartics if needed,

    D1=C union{a}, D2=C union{b}, |C|=3, C disjoint{a,b}.

Take x in C. The pair links at ax and bx each have a single doubled
edge and residual C3. Thus m_ax=m_bx=1. On the triple abx the ordinary
expansion is `p(abx)=2+a_abx`. No doubled tetrahedron contains abx.
The residual C3 above ax gives unit incidence at b either zero or two,
so a_abx is0 or-1. The range of p forces a_abx=-1.

There are therefore unit tetrahedra abxr,abxs for distinct r,s. The
residual C3 above ax also forces axrs; that above bx forces bxrs.
Neither r nor s belongs to C: if, for example, r did, the ordinary
pair xr would have two doubled link edges. Their total weight four
leaves at most one unit edge, and even incidence allows none, contrary
to the existing unit tetrahedron abxr. Thus xr is an ordinary baseline
pair lying in no doubled quartic. But its unit link contains the
triangle on a,b,s, from abxr,axrs,bxrs. An empty/C4/C5 link cannot do
this. The two-double alternative is excluded.

## One exceptional quadratic and one doubled quartic

Let J be the exceptional quadratic pair and D the doubled quartic.
If D has a vertex outside J union{a,b}, the private-vertex obstruction
applies. The only remaining geometry is therefore

    J={x,y}, D={a,b,x,y}, with a,b,x,y distinct.

The numerator at xy cannot be+1: its weighted link would have size
4m_xy-1, whereas removing the doubled edge would leave negative size
or one unit edge. Neither is an even simple graph. Hence k_xy=-2.
The ordinary coefficient m_xy can be zero or one; both are retained.

No unit tetrahedron contains a triple T inside D. Indeed, such a T
contains exactly one of the exceptional pairs ab and xy. Its other
two pairs are ordinary baseline pairs sharing a vertex w. If T+r is
a unit tetrahedron, their residual C3 links force another T+s, with
r,s outside D, and both unit tetrahedra formed from those two pairs
and r,s. The ordinary baseline pair wr lies in no doubled quartic;
its link now contains the triangle on (T minus{w}) union{s}. This is
impossible. This argument treats all four triples of D and uses no
assumption on m_xy.

Consequently each cubic ordinary coefficient inside D is-1, supplied
solely by weight two from D. All four cross-pair ordinary coefficients
ax,ay,bx,by are one. The special coefficient at ab is two. Evaluating
the ordinary polynomial at D now gives

    p(D)=1-4+(6+m_xy)-4+2=1+m_xy.

The range bound forces m_xy=0. Its residual unit link is empty, since
the full weighted link size is two.

Consider the unit-tetrahedron link L at a. Every nonempty pair through
a survives deletion of D. The link vertex b has degree s=6 or7: the
weighted ab link has size8 or9 and D removes weight two. Every present
triangle through a is in exactly two unit tetrahedra, since triples
inside D have no unit tetrahedra and every other such triangle has an
ordinary baseline pair outside D. Thus link_L(b) is2-regular. The link
vertices x,y have degree three and cycle links; every other vertex has
degree four or five and a cycle link.

Let d be the number of vertices of L. At a, the ordinary quadratic
sum is d+1, so the weighted incidence is2d-2. Removing D's weight two
leaves2d-4 faces in L, hence chi(L)=2. Write n=d-1 for its vertices
other than b and n4 for their degree-four count. Curvature gives

    (6-s)+3+3+(n-2)+n4=12, or n+n4=s+2.

There is no unit tetrahedron on any triple of D, so x and y are both
nonneighbors of b in L and are nonadjacent to each other. Besides them,
b already has s neighbors T. Hence n>=s+2, forcing equality and n4=0.
All vertices of L other than b,x,y are exactly T and have degree five.

Delete b and its incident triangles. Each vertex in T then has a
four-vertex path as link, with its two boundary neighbors at the path
ends and its two interior-edge neighbors in the middle. The vertices
x,y are interior, nonadjacent, and each has degree three. Every neighbor
v of x belongs to T. The unique edge between the two middle vertices
in link(v) gives exactly one zero-boundary face through xv. Its third
edge is interior because x is an interior vertex. The other faces at v
have a boundary edge at v, so there is no second such face through xv.

Summing these incidences over the three distinct neighbors of x gives
three. But every zero-boundary face containing x contributes exactly
two incidences, one at each of its other vertices. This odd-even
contradiction excludes the final mixed geometry. It remains valid if
link_L(b) is two disjoint C3s: only the ordinary path links are used.

## Consequence for residual four

In a self-dual one-zero-pair representative, suppose the residual defect
after fixing all negative quintics is at most four. Singleton numerators
are then at most three. Let F be the coordinates outside the zero pair
and outside all negative quintic supports. The accepted one-exception
theorem forces every u in F to occur in at least two nonsingleton
cost-two exceptions. If there are two such exceptions, every singleton
is baseline; if there are fewer, F is empty.

If the two exceptions include a doubled positive quintic, the present
special-edge theorem and the accepted ordinary-coefficient0/1 theorem
exclude any u occurring in both. Thus F is again empty. If both
exceptions are cubics, F is contained in their intersection, of size
at most two. In all cases

    |F|<=2.

In the positive-quintic alternatives the stronger conclusion is F empty.
This is a conditional covering theorem only. Its transfer retains the
published-catalog dependencies of the earlier one-exception theorem;
the new two-exception local arguments are elementary. No disconnected
support family is excluded without separately checking this hypothesis
and its literal coverage.
