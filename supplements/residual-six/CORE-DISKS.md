# Common physical pair disks and exact core truth blocks

Use the three-free classification in THREE-FREE.md and the endpoint reduction
in ENDPOINT.md. Thus F={a,b,c}, k_F=-3 is the sole departure, f(F)=1, and
the coefficients k_{F+xy}=1 form one physical seven-cycle L on eleven outside
coordinates. Four outside coordinates R are off the cycle. Equality of these
coefficients is literal, not a symmetry imposed on the unknown function.

For each core pair A, let D_A consist of the outside triples T with k_{A+T}=1.
Choose v in A and take the endpoint link at A minus{v} in the unit-quartic
complex of Delta_v f. By ENDPOINT.md that link is a sphere. Its triangles
through the remaining core coordinate F minus A are exactly the cone on L;
all its other triangles are exactly D_A. Deleting the open star of that
degree-seven vertex therefore leaves the triangulated disk D_A with boundary L.
The boundary degrees decrease from4/5 to3/4. Its interior degrees remain4/5.
Only the four labeled coordinates in R can be interior vertices. This uses
only the endpoint spheres; no whole-complex three-manifold or Walkup theorem
is needed. Different pairs give three actual families of the same polynomial.

For U contained in F, define the exact-intersection Fourier block

    B_U(y)=sum_{S intersect F=U} k_S chi_{S minus F}(y).

With outside assignment y fixed,16g(x,y)=sum_U B_U(y)chi_U(x). The core has
eight inputs. Fourier inversion and g=1-2f give, for nonempty U,

    B_U(y)=-4 sum_{X subset F} (-1)^|U intersect X| f(1_X,y).

For U empty, the formula is16-4*sum_X f(1_X,y). In particular

    B_F(y)=-3+sum_{xy edge of L}chi_{xy}(y)
          =-4 sum_{X subset F}(-1)^|X| f(1_X,y).       (1)

There is no outside averaging factor: y is fixed. The negative sign and
factor four are essential. At y=0 the core is OR3, so B_empty(0)=-12 and
every nonempty B_U(0)=4.

For a cycle unit y=e_z, the two incident cycle characters flip and B_F(e_z)=0.
For each core pair A, ordinary pair inversion in Delta_v f, v in A, gives

    4 f(A+z)=k_{A+z}+sum_{Q5 contains A+z} k_Q.       (2)

The two edges at z already contribute two positive quintics through F+z.
Every term in the sum is nonnegative because Q meets a negative-free coordinate,
and k_{A+z} is-1/0. Thus f(A+z)=0 is impossible. All three pair truths equal1.
The empty and singleton core truths at e_z also equal1 by the global low layers.
Equation(1) then forces f(F+z)=1. All eight truths are1, giving B_empty(e_z)=-16
and every nonempty B_U(e_z)=0. In each exact-core sector the signed incidence
sum over outside supports containing z is consequently2. For the empty sector
this includes any negative outside quintics; they cannot be discarded.

Now take r in R. No cycle edge is incident with r, so B_F(e_r)=4. Put
r_A=f(A+r) and h=f(F+r). The four empty/singleton core truths are1. Equation(1)
therefore says

    r_ab+r_ac+r_bc-h=1.                              (3)

Exactly one pair truth is1 and h=0, or exactly two pair truths are1 and h=1.
There are six possible complete Boolean core words. Neither zero nor all three
pair truths may be1. Scalar B_F=0 at a cycle unit would not alone imply all
eight truths1; equation(2) was needed. The controls preserve this counterexample
and check all256 Boolean core words.

At an off-cycle r, the quintic sum in(2) contains no all-core term F+r+x.
It is exactly the number of triangles of D_A containing r. Its link graph is
simple and even by ordinary cubic integrality. If r_A=0, k_{A+r} in{-1,0}
would make this graph have zero or one edge. One edge is not even, so it is
empty and k_{A+r}=0. Thus r does not occur in D_A. If r_A=1, the graph has
four or five edges and is a C4 or C5; r occurs and is interior because it is
off the boundary. Hence r_A is **exactly the indicator of interior occurrence**.

Each of the four actual coordinates in R is therefore interior to exactly one
or two of the three disks. The total number of interior-vertex incidences is
between four and eight. This cannot be replaced by choosing each disk's
interior set independently.

As additional necessary counts, let q_A count the-1 cubic numerators A+z,
P_A the positive quintics A+T, and M_A the interior count. The exact sector
B_A(0)=4 gives P_A-q_A=4. Summing its signed incidences over outside vertices
gives3P_A-q_A=14+4M_A, because the seven cycle vertices contribute2 each and
the off-cycle vertices contribute4r_A each. Therefore

    q_A=1+2M_A, P_A=5+2M_A.

These counts do not construct a disk or a Boolean extension. The standard-
library controls check all1,296 combinations of the six off-unit words, with
interior-incidence totals4..8; they do not enumerate compatible global triangle
families. The written disk theorem in DISK-LEMMA.md supplies the complementary
lower bound, composed in UNION12.md.
