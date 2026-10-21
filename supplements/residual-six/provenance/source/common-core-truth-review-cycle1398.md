# Independent common-core audit, conditional on the proposed C7 setting

Alexander Richard Towell.21 October2026. Substantial OpenAI Codex assistance.
This is a necessary-condition derivation and tiny exact controls. It does not
accept the proposed topology, construct a Boolean function, exclude a branch,
or change a ledger. The1394 publication packet is unchanged.

Assume the precise1391 minus-three setting: F={a,b,c} is the set of three
negative-free coordinates; k_F=-3; all other cubic numerators are-1/0; all
nonnegative quintic numerators are0/1; the constant singleton numerators are1/2.
Use g=1-2f and k_S=16*g_hat(S) in the accepted selfdual-empty representative.
In particular f(0)=0 and every singleton/pair truth is1. The original unknown
function is not independently assumed selfdual. **Conditionally** suppose the
common physical graph on the eleven outside coordinates is a seven-cycle L,
with positive coefficient k_{F+x+y}=1 exactly on its seven edges, and f(F)=1.
The validity of reaching this setting remains a separate mathematical gate.

## Exact core Fourier normalization

For U contained in F and outside word y, define the exact-intersection block

    B_U(y)=sum_{S intersect F=U} k_S chi_{S minus F}(y).

These are coefficients of the actual shared global polynomial, not independent
scalar unknowns. For any core word x,

    16 g(x,y)=sum_{U subset F} B_U(y) chi_U(x).

Thus, writing t_X=f(1_X,y), ordinary eight-point Fourier inversion gives

    B_U(y)=2 sum_X (-1)^|U intersect X| (1-2t_X).

For nonempty U this is minus four times the alternating f sum. For U empty
it is16-4*sum_X t_X. In particular the proposed identity has the correct
**negative sign and factor four**:

    B_F(y)=-4 sum_{X subset F} (-1)^|X| f(1_X,y).        (1)

There is no extra factor from averaging over the eleven outside coordinates;
they have already been fixed. All256 Boolean three-core words are checked
against exact inverse reconstruction at all eight core inputs.

At y=0, the core block is OR3: zero at empty, one at all other seven inputs.
Consequently

    B_empty(0)=-12; B_U(0)=4 for every nonempty U.       (2)

The assumed physical cycle gives

    B_F(y)=-3+sum_{xy edge of L} chi_{xy}(y).

At a unit e_z on the cycle this is0, because exactly two edge characters flip;
at an off-cycle unit it is4. The control checks these eleven units and the
entire2048-input scalar table, without claiming it extends to f.

## All eight core truths at an on-cycle unit

Fix z on L and A a core pair. The global cubic k_{A+z} is baseline-1/0.
Ordinary pair inversion in a derivative at either member of A gives

    4 f(A+z)=k_{A+z}+sum_{Q5 contains A+z} k_Q.         (3)

All quintics in this sum meet a negative-free coordinate, so their numerators
are nonnegative0/1. The two cycle edges at z already contribute two known
positive quintics F+z+z_previous and F+z+z_next. If the truth were0, the right
side would be at least1, a contradiction. Therefore all three f(A+z) equal1.
This argument uses no unproved flagness and no independent endpoint symmetry.

The empty and three core-singleton truths at e_z are already1 from the global
singleton/pair layers. Equation(1) now reads

    0=-4*(1-f(F+z)),

so the top truth is also1. **All eight core truths are1**. Their complete
Fourier block is therefore

    B_empty(e_z)=-16; B_U(e_z)=0 for nonempty U.        (4)

Equations(2),(4) imply a useful additional shared-core equality, for all eight
sectors U, including empty:

    sum_{S intersect F=U, z in S minus F} k_S=2.        (5)

Indeed B_U(0)-B_U(e_z) is twice this signed incidence sum, and is4 in every
sector. For U empty the sum includes any negative outside quintics; they must
not be silently dropped. For singleton U it involves the true shared cubic
and quintic families. These are necessary linear endpoint-compatibility rows,
stronger than checking B_F alone, though already implicit in a complete actual
core truth-word model.

## Off-cycle unit: exactly one or two active core pairs

There are exactly four off-cycle outside coordinates. At any such e_z, write
r_A=f(A+z) for the three core pairs and h=f(F+z). The empty/core-singleton
truths are again1. Since B_F(e_z)=4, equation(1) gives

    sum_{|A|=2} r_A-h=1.                              (6)

Booleanity leaves exactly six words: one of the three pair truths is1 and
h=0, or two of the three pair truths are1 and h=1. **Never zero or all three
pair truths are1.** This is a complete eight-truth-word conclusion, not only
an inequality on their sum. In mask order(empty,a,b,ab,c,ac,bc,abc), all six
literal words and full B_U vectors are saved by the executable control.

The remaining seven Fourier sectors are also determined, without assuming
any local catalog:

    B_empty(e_z)=-4-8h,
    B_i(e_z)=-4+8h-8r_{F minus{i}},
    B_A(e_z)=4-8r_A for |A|=2,
    B_F(e_z)=4.                                      (7)

The singleton sector is an exact-core-intersection polynomial on eleven
outside coordinates. It must not be identified with an older ten-coordinate
singleton catalog having different normalization or origin hypotheses.

## Pair-row projection and the interior-vertex meaning of r_A

For a fixed core pair A, let D_A be the simple three-graph on eleven outside
coordinates whose triples T have k_{A+T}=1. Let q_A count the baseline-1
cubics A+z, and let P_A be its number of triples. There is no even-level
constant in this sector: exactly

    B_A(y)=sum_z k_{A+z} chi_z(y)
            +sum_{T in D_A} chi_T(y).

Equation(2) gives P_A-q_A=4. At an on-cycle vertex z, the two known all-core
quintics in(3) give

    k_{A+z}+degree_{D_A}(z)=2.                        (8)

Here degree means triangle incidence. At an off-cycle vertex, no all-core
quintic is incident, and(3) gives

    k_{A+z}+degree_{D_A}(z)=4r_A.                     (9)

It is important to prove that r_A=0 means the vertex is absent, not just that
a signed sum happens to vanish. In a derivative at a member of A, take the
ordinary pair consisting of its other member and z. Its unit-quartic link
is exactly the link of z in D_A when z is off-cycle. It is simple, has even
degrees, and by(9) has size0/1/4/5. A one-edge simple graph cannot be even.
Thus r_A=0 forces k_{A+z}=0 and the link empty. If r_A=1, that link is a
four-cycle or five-cycle, with k_{A+z}=0 or-1 respectively. Hence r_A=1 is
**equivalent** to this off-cycle coordinate occurring as an interior vertex
of the pair-row surface/disk.

For on-cycle z, the same full pair link contains the two-edge segment
z_previous--(third core vertex)--z_next. Its total graph is a four-cycle or
five-cycle. Removing the third core vertex leaves the D_A link: a path of
length two or three between the two fixed cycle neighbors. There are8 and56
local labeled paths respectively (eight available intermediate vertices).
Those64 local options are mechanisms only; independently choosing them does
not ensure they come from one common triangle family.

These link descriptions show D_A is a compact triangulated surface with
boundary exactly L. An edge has one incident triangle precisely when it is
a boundary-cycle edge; every other occurring edge has two. All seven cycle
vertices lie in one component. Any other component would use only the four
off-cycle vertices and have all degrees4/5, impossible on at most four vertices.
The surface is therefore connected. If the separately reviewed endpoint link
is a sphere, D_A is directly its disk after deleting the open star of the
degree-seven exceptional vertex. This route needs only that endpoint sphere,
not the entire13-coordinate quartic complex being a manifold.

There is also an independent Euler calculation. Let M_A=sum_offcycle r_A.
Summing(8),(9) and using P_A-q_A=4 gives

    3P_A-q_A=14+4M_A,
    q_A=1+2M_A, P_A=5+2M_A.                           (10)

Thus D_A has7+M_A vertices, P_A triangles and7 boundary edges. Since
3P_A=2E_A-7, its Euler characteristic is1. A connected compact surface with
one boundary component and Euler characteristic1 is a disk, by the standard
classification of compact surfaces. No finite sphere/manifold catalog is
needed for this particular inference. The arithmetic tuples M=0..4 in(10)
are necessary possibilities, **not actual realizable disks**.

Now apply(6) simultaneously to all three pair rows. Each of the four labeled
off-cycle coordinates is an interior vertex in exactly one or two of the
three disks, never zero or three. Therefore

    4 <= M_ab+M_ac+M_bc <= 8.                         (11)

The control exhausts all6^4=1296 allowed off-unit block choices and obtains
total interior incidence counts4,5,6,7,8 with multiplicities81,324,486,324,81.
If a separate rigorous disk theorem requires M_A>=3 in every row, then(11)
contradicts it. That lower-bound proof is assigned independent cycle1399;
this packet does not claim its acceptance, nor acceptance of reaching C7.
No target disk catalog, compatible-path family enumeration or solver is run.

## Failed extrapolations and scope

* B_F(e_z)=0 alone does not force all eight truths1: with the four low truths1,
  it admits four core words. The known two positive cofaces and(3) are needed
  to force the three pair truths. The saved counterword has pair truths(1,1,0)
  and top truth0, and still has B_F=0.
* Off-cycle units are not all-one blocks. Equation(6) forbids three active
  pair rows; forcing all pairs1 would give a scalar coefficient0, not4.
* The odd counts q=1+2M and P=5+2M by themselves are not a contradiction or
  a component construction. They do not impose compatibility of different
  vertex links or of the three disk triangle families.
* A scalar2048-input C7 table, a locally valid path or an allowed eight-bit
  block is not an actual14-variable Boolean extension. The global free-set
  classification and C7 endpoint topology remain independently gated premises.

The code imports only Python's standard library and neither1391 producer nor
any search engine. Its tiny normal/optimized controls are recorded separately.
No publication, formal verification, human review or novelty claim is made.
