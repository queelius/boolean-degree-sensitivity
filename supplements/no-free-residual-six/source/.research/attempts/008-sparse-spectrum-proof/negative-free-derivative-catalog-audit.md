# A thirteen-variable derivative obstruction

The parent reduction and the published-manifold filter have been
independently checked. The following formulation also includes singleton
numerators zero and three. It is conditional on the explicitly cited
complete manifold enumeration; no claim of independently regenerating
that historical enumeration is made.

Let p be a polynomial on thirteen Boolean variables taking values in
{-1,0,1}, with p(0)=1 and p(e_w)=0 at every unit vector. Suppose its
Fourier expansion, in characters chi_S(x)=(-1)^(sum_(i in S) x_i), is

    16p=c+sum_(|S|=2) a_S chi_S+sum_(|S|=4) b_S chi_S,

where a_S belongs to {-1,0}, b_S belongs to {0,1}, and c<=3. Suppose
also that every ordinary multilinear quadratic coefficient of p is zero
or one. **No such p exists.**

## Reduction to a manifold

Take the b_S=1 four-sets as tetrahedra of a simplicial complex K. For
each pair A, its link graph has sum b=4m_A-a_A edges, where m_A is the
ordinary quadratic coefficient. Integer cubic coefficients of p force
even degrees in this simple graph. Thus m_A=0 gives an empty link, and
m_A=1 gives a C4 or C5. In particular K has an edge A precisely when
m_A=1; every triangle belongs to two tetrahedra.

For a vertex w, let y_w count the negative a_S containing w, and let
P_w count tetrahedra containing w. The origin/unit equations give

    -y_w+P_w=8.

Summing the quadratic inversion equation over pairs containing w gives
4deg_K(w)=-y_w+3P_w. Hence

    P_w=2deg_K(w)-4,   y_w=2deg_K(w)-12.

All thirteen vertices are active and have degree at least six. Each
vertex link has Euler characteristic two, with every vertex degree four
or five. The independent proof in
`negative-free-vertex-manifold-audit.md` rules out a disconnected link
by comparing two six-vertex projective-plane links with the skeleton's
edge budget. That proof works unchanged with **at most ten**, rather
than nine, cross edges: minimum cross degree one forces a degree-one
vertex on each side since ten is less than twelve, and their two
universal stars require eleven edges.

Let N count all negative a_S, P all tetrahedra, and E all K-edges.
The same equations give P=E-13 and N=2E-78. Evaluating p at zero yields

    E=49+c<=52.

The disconnected-link calculation therefore has at most E-42<=10
cross edges and is contradictory. K is a closed combinatorial
three-manifold. It is connected because every component contains a
vertex and its at least six neighbors, while K has thirteen vertices.

## Exact finite contradiction

The multilinear coefficients now give p(1_X)=1-chi(K[X]) for every
induced subcomplex. Hence every induced Euler characteristic lies in
{0,1,2}. The complete published list of manifolds with all edge valences
at most five contains4,787 records. A producer-independent scan checks
all records;77 have thirteen vertices,10 of these have minimum edge
valence four, and exactly9 of these have at most52 edges.

Eight of the nine have an explicit independent triple, whose induced
Euler characteristic is three. The only remaining record,3804, has an
induced subcomplex with Euler characteristic minus one; for example,
vertices {1,2,4,9,11,12} induce face vector (6,9,2,0). All nine are
therefore impossible. The source-bound scripts also evaluate all73,728
induced subsets, and each saved contradiction is rechecked by a separate
literal-face count. No optimization solver or graph-isomorphism package
is needed for the finite scan.

The dataset is the author's `manifolds_lex_d3_deg5.txt.gz`, SHA256
41071b36a731396d5273c60748aea7937c876136684ac479971e87e27e2fbb59.
Its completeness is explicitly stated in Florian Frick,
*Combinatorial restrictions on cell complexes* (2015), Theorem3.10,
printed page44 / zero-based PDFpage49: <https://d-nb.info/1076082246/34>.
It is also reported by Frank H. Lutz in *Triangulated Surfaces and
Higher-Dimensional Manifolds*, Oberwolfach Reports12/2006, page706:
<https://oa.tib.eu/renate/server/api/core/bitstreams/5e8dec33-aefd-438d-8e6d-7517a9a00a61/content>.
The author's data page identifies the complete set:
<https://www3.math.tu-berlin.de/IfM/Nachrufe/Frank_Lutz/stellar/3-manifolds.html>.
These primary sources were independently opened on2026-10-14. The
Walkup sphere theorem and global flagness are unnecessary for this proof.
The primary thesis PDF and extracted theorem page are archived in008 as
`frick2015-combinatorial-restrictions.pdf`, `frick2015-theorem310.txt`,
and `frick2015-source.json`.

## Transfers to the Boolean-polynomial problem

For p=partial_v f, self-duality gives the displayed even Fourier form,
with c=k_v, a_S=k_(S union {v}), b_S=k_(S union {v}). If v occurs in
no negative quintic, the positive quintic domain is {0,1}; the cubic
baseline gives a_S in {-1,0}. A nonzero-pair coordinate v has p(0)=1
and p(e_w)=0. In the empty-pair case all quadratic derivative coefficients
are f(v,w,t), so the obstruction applies whenever k_v<=3.

In the one-zero-pair case, take v outside that pair e. All quadratic
derivative coefficients are Boolean except possibly at e, where the
coefficient equals f(e union {v})+1. If that truth value is zero, the
coefficient is one and the obstruction applies. Thus every such
negative-free v with k_v<=3 and the stated cubic/top baseline domains
must satisfy f(e union {v})=1. The coefficient domains are essential;
no transfer is made when an incident cubic or positive quintic has an
exceptional numerator.

Reproduce the two independent scans and their controls with

    python .research/attempts/008-sparse-spectrum-proof/audit_small_valence_catalog.py
    python .research/attempts/008-sparse-spectrum-proof/audit_small_valence_euler.py
    python -m pytest -q .research/attempts/008-sparse-spectrum-proof/test_small_valence_catalog.py .research/attempts/008-sparse-spectrum-proof/test_small_valence_euler.py
