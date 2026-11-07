# Independent audit: filled opposite triangles of positive edges

Alexander Richard Towell, with substantial OpenAI Codex assistance. Cycle1508 is independent written mathematics and tiny literal controls only. No target query, native filter, row application, case exclusion, publication or ledger change. Original code MIT; original notes/data CC BY4.0. Novelty, formal verification and human review are not established.

## Verdict and actual hypothesis

The proposed1507 strengthening is sound. Let K be a finite simplicial triangulation of S3, with minimum graph degree at least6. Suppose ab is an edge with link the three-cycle boundary A. If the three edges inside A have tetrahedral valences at most5, then A is not a face. This statement needs neither13 vertices nor alpha<=2, no signed counts, no assumption about another positive tip, and no symmetry imposed on a function. For the accepted signed-star contexts, a is the root and A avoids a, so every A edge is ordinary, hence has valence4/5. Thus every positive edge has a missing opposite triangle, at all accepted root orders.

This is a necessary structural statement about genuine spheres. It is not claimed to follow already from the relaxed rows or to settle any signed-star model. The separate1497 root7 result remains correct but is weaker.

## 1. The cap tetrahedra are genuinely missing

Assume for contradiction that A is present. Neither aA nor bA can be a tetrahedron. If aA existed, link(a) would contain b*boundary A together with A, the entire tetrahedral boundary on b union A. In a connected S2, a closed top-dimensional subcycle of this form occupies the whole sphere: every edge already has its two incident triangles, and the facet-dual graph is connected. Hence a would have precisely four neighbors, contrary to minimum degree6. The same argument applies to b. This explicitly checks cap absence; it is not inferred merely from the terminology opposite triangle.

## 2. A safe construction of the two capped pieces

The closed edge star ab*boundary A is a simplicial3-ball. Its boundary is the union of the two disks a*boundary A and b*boundary A. The complement of its open interior in S3 is a PL3-ball B. The present triangle A meets this boundary precisely in boundary A, and its interior is disjoint from the edge star, so it is a properly embedded PL disk in B. Cutting B along A yields two3-balls B_a,B_b, whose boundaries are respectively boundary(aA), boundary(bA). Cap by the missing tetrahedra aA,bA to obtain simplicial3-spheres C_a,C_b.

Here the standard PL3-dimensional Schoenflies/disk separation theorem is explicit. It concerns locally flat finite PL embeddings, so no wild sphere or disk is silently allowed. A primary author-hosted reference is Hatcher, Notes on Basic3-Manifold Topology, Theorem1.1 and its immediately following discussion of the PL version, printed1–2: https://pi.math.cornell.edu/~hatcher/3M/3Mfds2014.pdf . The properly embedded disk version follows by adjoining one boundary disk and applying sphere separation, or doubling the ball along its boundary. No PDF is redistributed. The proof below in fact only needs connected closed capped3-manifolds with S2 vertex links, but the stronger sphere conclusion is legitimate here.

This disk construction avoids treating the two missing-tetrahedron spheres as disjoint: they share the face A. Sequential connected-sum notation C_a # boundaryDelta4(a,b,A) # C_b is valid, with the two middle gluing facets sharing A. In direct facet language, remove aA from C_a and bA from C_b, and add the three tetrahedra abij for ij in boundary A. The pieces meet along A after cutting/gluing, and all old nonboundary vertex stars stay unchanged. No new vertex is added by either cap. In particular a vertex of C_a outside a union A has precisely the same original neighbors in K.

## 3. The valence formula includes a minus one

Fix an edge ij inside A. Its incident tetrahedra in K consist of all C_a tetrahedra except the cap aA, all C_b tetrahedra except the cap bA, and exactly the single middle tetrahedron abij. Thus

    val_K(ij)=val_Ca(ij)+val_Cb(ij)-1.

The pieces are simplicial3-spheres, so each edge link is a simple cycle of length at least3. Since val_K(ij)<=5, both capped valences must be3, and val_K(ij)=5. If an A edge had valence4, contradiction would already follow at this step. There is no unproved assertion that valences are invariant under connected sum.

## 4. Local degree-three adjacency forces an entire component

For v in A, the other two A vertices are adjacent in link_Ca(v), since A is a face. Their degrees in that link are the two capped edge valences just shown to be3. In a triangulated S2, two adjacent degree3 vertices force the whole sphere to be the tetrahedral boundary: the two common adjacent triangles determine the two remaining common neighbors, and the remaining faces around the degree3 vertices give all four tetrahedral-boundary triangles. These already saturate every edge coface, so connectedness excludes further triangles. Therefore every v in A has graph degree4 in C_a.

The triangle A has exactly two tetrahedral cofaces in C_a, namely the cap aA and another tetrahedron cA. This supplies the SAME vertex c for all three vertex-link arguments; it cannot be chosen separately at the three vertices. Each link_Ca(v) is the tetrahedral boundary on a,c and the other two A vertices. It follows that C_a contains all five tetrahedra of boundaryDelta4(a,c,A): aA,cA and the three acij for ij inside A.

Those five tetrahedra form a closed connected3-sphere subcomplex. Every triangle already has two tetrahedral cofaces inside that subcomplex; connectedness of the facet-dual graph of C_a forces it to be all of C_a. Thus c has degree4 there. The vertex c is not on the cap boundary a union A, so its entire original star is unchanged in K. Its degree in K is consequently4, contradicting minimum degree6. The same argument could be made on the other side, but one side suffices.

Minimum degree>=5 would in fact suffice in this argument; the applied statement retains the accepted minimum6 guard rather than broadening any source contract. The ordinary-valence bound on all three A edges is essential, as the explicit countercontrol below shows.

## 5. Comparison with the producer statement

I separately read the full1507 written proof. Its still stronger formulation is also sound: under just the sphere, valence3 edge and the three A-edge upper bounds, a filled A forces SOME vertex of graph degree4. If an endpoint cap exists, Section1 gives that endpoint; if neither cap exists, Sections2–4 give the private vertex c. Thus minimum degree is a corollary guard, not a hidden premise of this stronger statement. The optional seven-vertex description when both caps are absent follows by applying the same proof to C_b; the two private vertices lie on different sides. No gap was found in1507, and the two shared-face cap spheres are handled by the proper-disk construction rather than incorrectly declared disjoint. Final source pins are supplied separately after the producer freezes.

## 6. Guard controls, not target enumerations

The first literal sphere is obtained from two tetrahedral boundaries as C_a,C_b and the middle three tetrahedra. It has seven vertices, filled A, valence3 on ab, and valence5 on each A edge. It has two private degree4 vertices, so it violates the minimum-degree hypothesis. The second takes C_a,C_b to be C4*C4 joins, glued in the same way. It is a genuine13-vertex connected sum with minimum degree6, filled A and valence3 edge ab, but its three A-edge valences are7. It demonstrates why the ordinary-edge bound cannot be omitted, even at the target vertex count. Neither is a signed-star Boolean witness.

The following pure-standard-library replay independently constructs the two controls. Closure/coface/degree calculations are literal. Spherehood follows from the displayed joins and connected-sum construction; these checks are not offered as a general sphere recognizer. No solver or native model is imported.

```python
from itertools import combinations
import json

def need(ok,message):
    if not ok: raise ValueError(message)
def mask(xs): return sum(1<<x for x in xs)
def boundary(xs): return {mask(s) for s in combinations(xs,4)}
def join4(c,d): return {mask((c[i],c[(i+1)%4],d[j],d[(j+1)%4])) for i in range(4) for j in range(4)}
def closure(facets):
    return {mask(s) for f in facets for k in range(1,5) for s in combinations([i for i in range(f.bit_length()) if f>>i&1],k)}
def inspect(Ca,Cb):
    A=mask((2,3,4));aA=A|1;bA=A|2
    middle={mask((0,1,*s)) for s in combinations((2,3,4),2)}
    K=(Ca-{aA})|(Cb-{bA})|middle;faces=closure(K)
    vertices=[v for v in range(13) if 1<<v in faces]
    edges={s for s in faces if s.bit_count()==2}
    triangles={s for s in faces if s.bit_count()==3}
    degree={v:sum(bool(e>>v&1) for e in edges) for v in vertices}
    val=lambda e,F:sum(t&e==e for t in F)
    need(all(val(t,K)==2 for t in triangles),'triangle cofaces')
    need(A in faces and aA not in K and bA not in K and val(3,K)==3,'filled opposite triangle with absent caps')
    rows=[]
    for edge in combinations((2,3,4),2):
        e=mask(edge);p=val(e,Ca);q=val(e,Cb)
        need(val(e,K)==p+q-1,'capped edge valence formula')
        rows.append([e,p,q,val(e,K)])
    return {'f':[len(vertices),len(edges),len(triangles),len(K)],'degrees':degree,'A_edge_cap_valences_and_original':rows,'filled_A':True,'ab_valence':val(3,K)}
result={'minimum_degree_guard':inspect(boundary((0,2,3,4,5)),boundary((1,2,3,4,6))),'ordinary_A_valence_guard':inspect(join4((0,2,5,6),(3,4,7,8)),join4((1,2,9,10),(3,4,11,12)))}
need(result['minimum_degree_guard']['f']==[7,18,22,11] and min(result['minimum_degree_guard']['degrees'].values())==4,'minimum degree countercontrol')
need(result['ordinary_A_valence_guard']['f']==[13,46,66,33] and min(result['ordinary_A_valence_guard']['degrees'].values())==6 and all(r[-1]==7 for r in result['ordinary_A_valence_guard']['A_edge_cap_valences_and_original']),'ordinary valence countercontrol')
print(json.dumps(result,sort_keys=True))
```

## 7. Scope of acceptance

The accepted1413/1453 sphere and signed-star premises are inherited. The argument neither uses nor transfers the old one-exception certificate or the c1 UNSAT proof. It produces no assignment to an actual function and no mathematical global solution. Applying these forced-zero triangles to additional root contexts requires separately derived physical masks, exact encoding review, and authorization. The original29 whole patterns remain open at the current checkpoint. The absence of A makes the combinatorial3-to-2 move admissible, but it does not establish preservation of the exceptional-star pattern or induced-Euler/Fourier constraints. The earlier1487 failure of direct c2-to-c1 transfer therefore remains a real obstruction; no solver certificate is transferred here.

## Actual literal-control receipt

Executed the exact Python block above, read from this note, in fresh normal and optimized exact-Python subprocesses. Explicit exception guards remain active under optimization. The two guard countercontrols passed with identical output; all triangle coface counts are2 and all capped valence equations agree. This is a tiny standard-library calculation, not a target/native query or general sphere recognition. Receipt:

```json
{
  "processes": [
    {
      "mode": "normal",
      "exit_code": 0,
      "wall_seconds": 0.12015676195733249
    },
    {
      "mode": "optimized",
      "exit_code": 0,
      "wall_seconds": 0.12109631800558418
    }
  ],
  "results": {
    "minimum_degree_guard": {
      "A_edge_cap_valences_and_original": [
        [
          12,
          3,
          3,
          5
        ],
        [
          20,
          3,
          3,
          5
        ],
        [
          24,
          3,
          3,
          5
        ]
      ],
      "ab_valence": 3,
      "degrees": {
        "0": 5,
        "1": 5,
        "2": 6,
        "3": 6,
        "4": 6,
        "5": 4,
        "6": 4
      },
      "f": [
        7,
        18,
        22,
        11
      ],
      "filled_A": true
    },
    "ordinary_A_valence_guard": {
      "A_edge_cap_valences_and_original": [
        [
          12,
          4,
          4,
          7
        ],
        [
          20,
          4,
          4,
          7
        ],
        [
          24,
          4,
          4,
          7
        ]
      ],
      "ab_valence": 3,
      "degrees": {
        "0": 7,
        "1": 7,
        "2": 10,
        "3": 10,
        "4": 10,
        "5": 6,
        "6": 6,
        "7": 6,
        "8": 6,
        "9": 6,
        "10": 6,
        "11": 6,
        "12": 6
      },
      "f": [
        13,
        46,
        66,
        33
      ],
      "filled_A": true
    }
  }
}
```

## Frozen producer binding

Read and checked the complete final1507 proof, SHA256 `ac58e2c620c96d9496c39a01cf1776d96b75f3012c02fe865dc91eb8efbf2046`. Producer handoff SHA256 `c26bd3d5e4c5c81cc1838d182fb8a31a52793d528c39aad99e38ceb6d1951133`; manifest SHA256 `c280ffe390f68f93cc6c85afe8ef6fd8198fc103f474030a1c634de4140230db`. All declared local source pins were rebound before this independent freeze. No producer controls or code are imported. The standard external PL separation theorem is explicitly retained, not purportedly reproved by the literal controls.
