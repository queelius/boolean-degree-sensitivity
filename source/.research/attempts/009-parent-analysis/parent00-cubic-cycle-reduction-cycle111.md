# Sparse triangle-cycle reduction for parent0/0, negative triple7

This is a mathematical reduction; the finite enumeration still needs its own
execution and independent audit before accepting an exclusion.

Let P be the positive cubic family, u_i the negative linear flags, and
N={0,1,2} the sole negative cubic. Put d_i=|{T in P:i in T}| and
n_i=1_{i in N}. Then B(e_i)=4-2(d_i-2n_i-u_i). The independently computed
parent0/0 scalar sets at the singleton inputs are:

- i=0,1: {0,8};
- i=2,3,4: {4};
- i=5,6,7,8,9: {-4}.

The signed divisibility criterion makes every pair incidence in P even.
Consequently, the link of any vertex is a simple graph with all degrees even.
If nonempty, that graph has at least three edges. Hence d_i is0 or at least3.
Combining this with the singleton values and u_i in{0,1} proves:

- d_3=d_4=u_3=u_4=0;
- d_2=3 and u_2=1;
- for i=5,...,9, d_i=4+u_i;
- for i=0,1, either d_i=u_i=0, or d_i=4+u_i.

In particular, all positive and linear supports lie in
A={0,1,2,5,6,7,8,9}. If a is the number of apices0,1 occurring in P,
then sum_i d_i=22+4a+Q, where Q=sum_i u_i. Since B(0)=4 implies
|P|=Q+6, degree counting gives Q=2+2a. Thus only Q=2,4,6 can occur.
The linear flags are uniquely determined by P.

The link at vertex2 has exactly three edges and all degrees even, so it is
a triangle on some triple T in W=A minus{2}. There are precisely the three
positive faces 2xy,2yz,2zx containing2. Toggle the four faces of the tetrahedron
{2} union T. The resulting family Z is a binary triangle cycle on W.

T must belong to Z. Otherwise the original P contains all four tetrahedron
faces, and removing them reduces the degree of each vertex of T by3. Those
vertices have degree4 or5 in P, giving degree1 or2 in Z. That contradicts the
even-link property of a binary triangle cycle. Therefore P is obtained from
Z by removing T and adding2xy,2yz,2zx. Its size increases by2, so
|Z| belongs to{6,8,10}.

Every binary triangle cycle on seven labeled vertices has a unique description
using20 bits. Fix an anchor vertex w. Freely choose the20 triangles avoiding w.
For each edge ij avoiding w, include wij exactly when the number of chosen
triangles containing ij is odd. This cancels the boundary on every such edge;
the remaining anchor-edge boundaries cancel because each chosen triangle is
counted twice. Conversely every cycle has these uniquely forced anchor faces.

Thus all2^20 binary triangle cycles Z can be enumerated, retaining weights6,8,10.
For every face T of each retained Z, perform the stellar replacement above.
Check the derived vertex degrees, forbidden positive face7, determined linear
count, and |P|=Q+6. For every survivor, evaluate the uniquely determined B on
all1024 outside inputs against the independently enumerated parent scalar sets.
This is exhaustive for the stated negative triple and parent. A successful
projection is still only necessary for a14-variable Boolean function; if all
candidates fail and completeness is independently verified, this would exclude
the single negative-position representative, not the whole parent.
