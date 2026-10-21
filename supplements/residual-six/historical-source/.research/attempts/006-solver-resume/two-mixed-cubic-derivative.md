# Adjacent mixed cubic exceptions at a free coordinate

Status: candidate local reduction; independent mathematical and row audits
are required before any branch exclusion is promoted.

Let p on thirteen variables take values in {-1,0,1}, with p(0)=1 and
every unit value zero. Its scale-sixteen even Fourier expansion has
constant c in {1,2}, quartic numerators 0/1, pair numerators -1/0 except
k_ax=1 and k_bx=-2. The vertices a,b,x are distinct.

First assume every ordinary quadratic coefficient is 0/1. Pair inversion
forces the ax link to be C3 and the bx link to have six edges. Every
triangle has a baseline pair, so each present triangle has exactly two
incident tetrahedra. At b the accepted one-six-edge splitting argument
excludes two disjoint C3s; hence the bx link is C6. Every vertex link is
now a union of closed surfaces of total characteristic two.

At a there is exactly one degree-three link vertex and all other degrees
are four or five. A projective-plane component containing that vertex
would satisfy n+n4=4 and cannot have the minimum six vertices. A separate
projective plane would consume six vertices, leaving at most six for a
sphere with exactly one degree-three vertex; neither of the two complete
six-vertex sphere types, nor any smaller sphere, has those degrees.
Thus link(a) is a sphere, of order at least seven. The accepted one-six-
edge argument makes link(b) a flag sphere of order nine, ten, or eleven.
At x, a component containing the degree-three vertex again cannot be a
projective plane, even allowing the one degree-six vertex: curvature
would give n+n4<=5. All components have positive characteristic, so
link(x) is also a sphere.

An ordinary vertex with a disconnected link would have two six-vertex
projective-plane components on A and B. Their forced skeleton has 42
edges. Since the total is 49+c<=51, there are at most nine cross edges.
Every good vertex needs a cross edge by the six-vertex-link obstruction.
The three exceptional vertices have degrees at least seven, nine, seven,
respectively; since their side plus the original center gives only six
neighbors, their cross degrees are at least one, three, one. If every
good vertex had cross degree at least two, the total cross-degree sum
would be at least 18+1+3+1=23>18. A good cross-degree-one vertex forces
its cross neighbor universal to the opposite six-set by the accepted
seven-vertex sphere classification. The other five vertices on that
neighbor's side each need a cross edge, requiring at least eleven.
This is impossible. All vertex links are spheres.

Root at x. Its link has one vertex of degree three, one of degree six,
and all others of degree four or five. Curvature gives n+n4=11, hence
order at most eleven. The independently complete sphere catalogs contain
exactly two such types: order eight/index six and order nine/index ten.
Necessary extension models use face indicators, two tetrahedra per
triangle, the stated pair valences, the fixed root link, and every
induced Euler bound. Local flagness is imposed only at ordinary vertices
and at b; neither a nor x is assumed to have a flag link.

Now allow the ordinary coefficient at ab to be two, with all others
still 0/1. The ax link remains C3. Thus even the triangle abx has
incidence zero or two, so every present triangle has incidence two.
The ab link has s=8 or9 edges. In link(a), b has degree s, x has degree
three, and every other vertex has degree four or five. Its characteristic
is one by the origin/unit and pair identities. Let n count its vertices
other than b, and n4 the degree-four vertices. Curvature gives

    s + 3 + 4 n4 + 5(n-1-n4) = 6n,
    n+n4 = s-2.

But b has s distinct neighbors, so n>=s. This contradiction excludes
the special-coefficient-two case without a surface classification or a
finite model. This separate argument is specific to the exceptions
meeting across the special edge; it does not claim other placements.
