# Adversarial review of the residual-six/four-free-coordinate draft

Alexander Richard Towell, substantial OpenAI Codex assistance;21October2026. This is an independent mathematical falsification attempt and small combinatorial controls, not formal verification or human peer review. No gap was found **under the explicitly inherited baseline-constant local derivative theorems**. No whole-pattern or global exclusion is accepted by this note.

Reviewed draft: `residual6-four-free-derivative-draft-cycle1382.md`, SHA256b85d2e49a1b410d1af8c66e9a020dc0aa2e29479f077bac0f509b237c34003c2. Parent intends a dependency simplification after this snapshot; this note supplies that simplification explicitly. The original local proof `../006-solver-resume/two-exception-positive-extension.md` was read directly rather than inferring its scope from a theorem label. No1382/1386 file is edited or imported. Static42 and maximal-state implementations are held.

## Derivative identities and signs

For a coordinate v in no negative quintic, the accepted selfdual-empty existence representative gives p=Delta_v f, p(0)=1, p(e_i)=0, range{-1,0,1}, with

    16p=c+sum_A a_A chi_A+sum_D b_D chi_D,
    c=k_v, a_A=k_(A+v), b_D=k_(D+v)>=0.

The Fourier normalization is consistent: Delta_v f=sum_(S contains v) ghat(S) chi_(S-v), for g=1-2f. Only orders0,2,4 remain in this proved representative. This is not an assumption that every original function is selfdual. Expanding chi_i=1-2x_i gives ordinary quadratic coefficient m_A=(a_A+sum_(D contains A)b_D)/4. Also p(ij)=f(vij)-1 and p(0)=1, p(i)=p(j)=0, so m_A=f(vij), genuinely0/1. Ordinary cubic coefficient is -sum_(D contains T)b_D/2; integrality therefore gives even weighted degrees in every pair link. The signs and factors4/2 are correct.

Residual coefficient costs are nonnegative even integers. Their cost-zero domains are c in{1,2},a in{-1,0},b in{0,1}; cost2/cost6 domains agree with the draft and there is no single cost4. Every repeated exception type refers to a distinct actual coefficient; one coefficient cannot simultaneously take two exceptional values. Negatives already fixed are absent from derivatives at v in F and are not residual departures.

## Tripled quartic: attempted parity counterexamples fail

With one quartic D0 of weight3, all other quartics unit/simple, and baseline a, every pair A subset D0 has total link weight4m_A-a_A in{0,1,4,5}. It contains weight3, so only4 or5 are possible. In weight4, its sole residual unit edge would have to join the two heavy endpoints to restore parity, duplicating the heavy edge and hence impossible. Weight5 leaves exactly two distinct residual unit edges. Odd parity at the heavy endpoints and even parity elsewhere forces a length-two path between them through one outside vertex z.

Writing D0=abcd and starting at ab produces abcz,abdz. The pair ac then has residual edge bz and heavy endpoints b,d; its unique second residual edge is zd, with the **same** z, forcing acdz. Pair bc forces bcdz similarly. At pair az, no heavy quartic occurs, and its simple unit link contains the triangle bc,bd,cd. Total size must be0,1,4 or5; therefore this triangle would need one or two additional distinct simple edges. The triangle is already even, while a nonempty simple even graph cannot have one or two edges. The additional edges cannot duplicate triangle edges because each nonheavy quartic has coefficient0/1. This is a contradiction, with no use of c or a manifold catalog.

Tiny controls exhaust residual one/two-edge completions for link sizes3 through7: no one-edge parity repair, exactly15 length-two paths (one per outside vertex), and no even triangle extension by one/two extra distinct edges. Ordinary simple even links with allowed sizes0,1,4,5 are exhaustively checked on six vertices:4384 graphs, with every nonempty solution a C4 or C5. These are mechanisms of the proof, not an exhaustive derivative or Boolean-function classification.

## Private-tip extraction: locality is sufficient

The old006 proof uses only pair/triangle/unit equations incident with its chosen private coordinate w. Other exceptional quadratic pairs and doubled quartics that avoid w therefore do not affect the argument. This statement needs actual locality, not a claim that the entire unit-quartic complex is a manifold.

Suppose exactly one doubled quartic D contains w, all other quartics through w are0/1, and all a_(w,x) are baseline. A pair wx inside D has unit residual link C3; a pair wx outside D has empty/C4/C5 link. To exclude a unit tetrahedron T+r containing a triple T subset D with w in T, use the two pairs in T containing w. Their residual triangles and parity at T force the same fourth vertex s, then force both corresponding pair+r+s tetrahedra. Pair wr consequently has a triangle in its ordinary C4/C5 link, impossible. All of these pairs contain w. No doubled quartic avoiding w enters one of them.

Now take just the unit-tetrahedron link at w. Its vertex links are connected cycles: C3 for the three vertices D minus w, and C4/C5 for every other occurring vertex. Every edge lies in two triangles. Thus **this two-dimensional link** is a disjoint union of closed triangulated surfaces, even if the global quartic complex away from w is singular. Exactly three link vertices have degree3; the rest have degree4/5; it uses at most12 vertices.

Let A_w=sum a_(w,x), P_w=sum_(D' contains w)b_D'. The difference p(0)-p(e_w)=1 cancels every coefficient avoiding w and gives A_w+P_w=8. Every nonempty pair link through w has m_(w,x)=1, and conversely m=1 forces such a nonempty link (the apparent weight1 alternative for m=0 fails parity). Hence if d is the unit-link vertex count, summing pair inversion gives4d=A_w+3P_w. Therefore P_w=2d-4, and removing the one weight2 quartic leaves2d-6 unit triangles. Euler characteristic is d-(2d-6)/2=3. The constant c and exceptions avoiding w do not enter this calculation.

Each surface component has positive Euler characteristic because all its vertex degrees are at most5. A connected closed triangulated surface has chi<=2: over F2 its0th and2nd Betti numbers are1 (edge-adjacency forces all face coefficients of a2-cycle equal), and chi=2-beta1. Thus components have chi1 or2; no orientation assumption is needed. A chi1 component has exactly6 vertices, all degree5: E=3(V-1)<=binom(V,2) gives V>=6, while sum(6-degree)=6 gives V<=6. Three chi1 components require18vertices and are impossible. Total chi3 therefore forces one chi1 component and one chi2 component. The latter has at most6vertices and contains all three degree3 vertices.

Its curvature equation leaves either a five-vertex pattern requiring degree5 (impossible), or degree pattern(3,3,3,5,5,5). In the six-vertex case the three degree5 vertices are universal; each degree3 vertex must be adjacent exactly to them. Its triangular link forces all three pairs of universal vertices as faces through it, giving9 distinct faces, but chi2 and V6 require only8. Contradiction. Integer degree/edge/curvature controls recover exactly the chi1 pattern(0,0,6) and the sole feasible chi2 pattern(3,0,3). The central cyclic-link and local-incidence guards remain essential.

## Coupled allocation: no separate residual-four theorem needed

Choose four distinct negative-free coordinates F0. For a single cost6 departure, a singleton support has size1 and a cubic support size3, so some v in F0 avoids it and has a completely baseline derivative at c in{1,2}. For a positive quintic3, either some v avoids it (same baseline contradiction), or every v of F0 lies in it and the new single-tripled-quartic lemma applies.

Otherwise there are at most three cost2 departures. If any is a singleton, choose v in F0 avoiding all exceptional singleton coordinates (at most3). Its c is baseline1/2 and it sees at most two nonsingleton departures. The already accepted local0/1/2-exception guards at **exactly these baseline constants** suffice. If there is no singleton departure and at most two nonsingleton departures, the same argument works for any v. This covers residual0/2/4 too, eliminating a separate global residual-four covering theorem from the necessary premise list.

Only exactly three nonsingleton cost2 departures remain. All constants are baseline. If any v in F0 avoids any one support, its derivative has at most two nonsingleton departures and is impossible by the old local guard. Consequently all three support sets contain F0. A cubic support has size3 and cannot contain four coordinates, so all three are distinct doubled positive quintics S_i=F0+{t_i}, with distinct tips outside F0. At any v in F0, their derivative quartics are D_i=(F0 minus v)+{t_i}. Each tip t_i belongs to exactly one doubled quartic, all incident quadratics are baseline, and the private-tip lemma applies. Other doubled quartics avoid that tip. This is a coupled support argument; it does not assign independent cost charges to different free coordinates.

Therefore the reviewed deductions give |F|<=3 under residual<=6, conditional on the old local zero/one/two-exception results at constants **c in{1,2}** and accepted normalization. A connected Johnson-four family of six distinct five-sets has union at most10 (add at most one coordinate per spanning-tree edge), while |F|<=3 on14coordinates requires negative union at least11. This would exclude the connected branch of(3,1,1,1,1,1) when combined with accepted1363 connected necessity. Parent/independent1386 must still bind every old local guard and the final revised1382 source before any scientific closure; this adversarial review itself updates no case or ledger. All259 remaining native cases remain accepted OPEN until that gate.

## Controls and limits

Three named unittest controls pass normally and optimized; assertions use unittest methods and remain active under optimization.13 project tests pass. Final small controls cost about0.005CPU; the initial expected missing-module red control and all source pins are retained in the handoff. Coverage is reported honestly. No1385 maximal-cover implementation,42static probe, solver, new H table, actual Boolean function, novelty, formal verification or human review is claimed. The proposed maximal-state method remains unused prospective work; if this theorem passes it is unnecessary for this particular pattern.
