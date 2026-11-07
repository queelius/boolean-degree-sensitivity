# Independent review: one degree-three vertex in a degree-bounded sphere

Alexander Richard Towell, with substantial OpenAI Codex assistance. This is independent written mathematical review and tiny exact controls, not formal verification, human review, catalog enumeration, target query or case exclusion. Original code MIT; notes/data CC BY4.0.

## Verdict and one required wording qualification

The1514 elementary classification theorem, induction and patch proof are sound. The signed-star consequences are exact: every nonroot positive tip has graph degree7; its three edges to the opposite link triangle have valence5, and its remaining three ordinary incident edges have valence4. These conclusions use genuine S2 vertex links and the one-star exception pattern; they do not apply indiscriminately to a root, negative tip, arbitrary raw row assignment, or a vertex incident with multiple exceptions.

One sentence in frozen1514 Section4 must be read with the producer's fresh wording clarification: deleting the unique degree3 vertex leaves an OCTAHEDRAL DISK with its cap face absent. Deleting AND CAPPING the triangular boundary yields the octahedral sphere. A and the opposite B are opposite faces of the CAPPED sphere. Literal deletion alone does not yield a closed sphere. This is not used to weaken or discard the theorem: the corrected statement follows from its proved inverse-subdivision construction. The clarification binds the unchanged producer proof; no1514 bytes are edited here.

## 1. Local inverse subdivision and induction domain

In a simplicial S2 a degree3 vertex has a triangular link. If that link triangle is also a face, the vertex star plus the triangle is the complete tetrahedral boundary. Its four faces saturate every edge's two cofaces, so dual connectedness forces the entire sphere to have four vertices. Otherwise removing the vertex and capping the triangular boundary is the ordinary inverse face subdivision and preserves S2. Only its three neighbors lose one degree.

Likewise two adjacent degree3 vertices in S2 force the tetrahedral boundary: their common edge has two triangular cofaces, and their degree3 link cycles then supply the other two faces on the same four vertices. The order>4 guard is essential; adjacent degree3 vertices are legitimate in the tetrahedral sphere.

Let L have exactly one degree3 vertex v and all other degrees4/5. Euler curvature gives2n4+n5=9, so its possible orders initially satisfy6<=n<=10. This count is only a sanity check; it does not establish uniqueness. Remove v and cap A to get L'. Every potential degree3 vertex of L' lies in the face A, and each A vertex has degree3 or4. A four-vertex L' is impossible because its vertex outside A would still have degree3, whereas that unchanged vertex had degree4/5 in L. Thus L' has order>4. Since the A vertices are mutually adjacent, the preceding local lemma allows at most one degree3 vertex in L'.

If there is one, call it w. The induction hypothesis is applicable: L' is a smaller S2 with exactly one degree3 vertex and all others4/5. It is therefore an octahedron with one face subdivided, and w's three neighbors all have degree5. But w belongs to A, whose other two vertices are its neighbors of degree at most4. Contradiction. This is a valid strong induction, not a reliance on an unproved finite base case: the tetrahedral order is excluded explicitly, and the statement for any smaller admissible sphere is the induction hypothesis.

Hence L' has no degree3 vertex; its cap face has three degree4 vertices and all remaining degrees4/5. The patch lemma below makes it octahedral. Restoring v gives precisely an octahedron with one face subdivided. Conversely the explicit subdivision has the required pattern, so the classification includes existence.

## 2. Independent check of the seven-face patch argument

Suppose an S2 with all degrees4/5 has face abc with d(a)=d(b)=d(c)=4. Let the other coface vertices through ab,bc,ca be x,y,z. Each avoids a,b,c. If for example x=y, link(b) contains the triangle on a,c,x as a complete cycle, forcing d(b)=3. Thus x,y,z are distinct. The four-cycle links at a,b,c now force axz,bxy,cyz in addition to abc,abx,bcy,caz.

These are exactly seven triangular faces forming an octahedron minus xyz, a disk with boundary xyz. They have six distinct vertices and12 edges. The stars of a,b,c are fully accounted for by their degree4 assumption. The complementary region in S2 is a triangulated disk with the same triangular boundary; none of a,b,c is an interior vertex of that complement. Every boundary vertex already has four distinct neighbors in the patch, so it has at most one additional neighbor inside the complement.

If there are m complement interior vertices, let Eii be their mutual edges and Ebi their edges to xyz. Disk Euler and triangle coface counts give total edges3m+3, hence Eii+Ebi=3m, while Ebi<=3. For m=1 the single interior vertex has degree3, contradicting its global degree>=4. For m=2 simplicity gives Eii<=1 and Ebi>=5. For m>=3 the simple planar interior graph has Eii<=3m-6, even if disconnected, so Ebi>=6. Both contradict Ebi<=3. Thus m=0 and the complementary disk is the single triangle xyz. No cutoff, table, flagness or unproved noncrossing matching is used. The patch is the entire octahedral sphere.

## 3. Exact signed-star normalization

For a positive edge ab with a the common root, link_K(b) contains exactly one degree3 vertex, namely a, because tetrahedral valence of bx equals degree of x in this S2 link. Every other incident edge at nonroot b is ordinary of valence4/5. The theorem gives seven vertices in link_K(b), equivalently d_K(b)=7. Its unique degree3 vertex a has three neighbors A, each of degree5; the other three vertices B have degree4. Thus val_K(bx)=5 for x in A and4 for x in B. These are graph-neighbors of b, not all13 physical vertices; there are precisely three such B neighbors.

The seven-vertex link has f=(7,15,10). Therefore there are15 triangles and10 tetrahedra through b in K. The edges from a to B are absent INSIDE link_K(b), meaning triangles abx are absent. Original graph edges ax need not be absent. The octahedral antipodal matching describes the local link after deleting a and CAPPING A; it is neither a function automorphism nor permission to relabel independent links arbitrarily.

Accepted minimum degree or13 vertices is not needed in the standalone S2 theorem. The actual Boolean application inherits1413/1453 sphere/star premises. The absence-of-A-in-K theorem1508 is a separate statement. Here A absent from link_K(b) means bA is not a tetrahedron in K; it does not mean that triangle A is absent from K. That latter conclusion requires1508. No triangle/tetrahedron normalization is conflated.

## 4. Primary-source and verification boundary

I freshly opened Frick's2015 primary thesis, https://d-nb.info/1076082246/34 , Theorem3.8 on printed43–44 (PDF zero-based48–49). It attributes the eleven max-degree-five sphere triangulations and one projective-plane triangulation to Brinkmann and McKay, and explicitly lists the one-face-stacked octahedron. This corroborates the context and predecessor credit. The independent proof above does not require that enumeration as a premise. I did not re-enumerate all surfaces or establish novelty, and no third-party PDF is redistributed.

The actual1512 inventory remains unchanged at degree>=7; it does not silently acquire equality7, valence5/4 refinements or ten-tetrahedron rows. Any further native rows require a fresh structured source/encoding gate. No target propagation, solver or optimization occurs in1515. The whole-pattern frontier and global OPEN status are unchanged.

## 5. Reproducible tiny controls

The following pure-standard-library block uses literal octahedral faces, face subdivisions and gluing two disks. It checks the classified positive example and corrected deletion/capping, the small-order tetrahedral guard, and genuine sphere countercontrols for dropping uniqueness, max-degree5, or either patch degree bound. These examples corroborate guards; they are not a surface-recognition/classification algorithm.

```python
from itertools import product,combinations
import json

def need(ok,message):
    if not ok: raise ValueError(message)
def mask(xs): return sum(1<<v for v in xs)
def vertices(faces): return sorted({v for f in faces for v in range(f.bit_length()) if f>>v&1})
def edges(faces): return {mask(p) for f in faces for p in combinations(vertices([f]),2)}
def profile(faces):
    vs=vertices(faces);es=edges(faces)
    return {'f':[len(vs),len(es),len(faces)],'degrees':{v:sum(bool(e>>v&1) for e in es) for v in vs},'edge_cofaces':sorted({sum(f&e==e for f in faces) for e in es})}
def subdivide(faces,face,new):
    need(face in faces and new not in vertices(faces),'fresh face subdivision')
    return (faces-{face})|{(face^(1<<v))|(1<<new) for v in vertices([face])}
def relabel(faces,mapping):return {mask(mapping[v] for v in vertices([f])) for f in faces}
O={mask(t) for t in product((0,3),(1,4),(2,5))};A=7;B=56
L=subdivide(O,A,6);p=profile(L)
need(p['f']==[7,15,10] and p['degrees']=={0:5,1:5,2:5,3:4,4:4,5:4,6:3} and p['edge_cofaces']==[2],'unique3 positive example')
deleted={f for f in L if not f>>6&1};capped=deleted|{A}
need(profile(deleted)['f']==[6,12,7] and profile(deleted)['edge_cofaces']==[1,2] and capped==O,'deletion is disk, cap is octahedron')
T={mask(t) for t in combinations(range(4),3)}
need(set(profile(T)['degrees'].values())=={3},'small tetrahedral guard')
two=subdivide(L,B,7);pt=profile(two)
need(pt['f'][0]==8 and sorted(pt['degrees'].values())==[3,3,5,5,5,5,5,5] and pt['edge_cofaces']==[2],'uniqueness guard')
large=subdivide(L,67,7);pl=profile(large)
need(pl['f'][0]==8 and list(pl['degrees'].values()).count(3)==1 and max(pl['degrees'].values())==6 and pl['edge_cofaces']==[2],'maximum5 guard')
minpatch=subdivide(O,B,6);pm=profile(minpatch)
need(all(pm['degrees'][v]==4 for v in (0,1,2)) and min(pm['degrees'].values())==3,'patch minimum4 guard')
patch=O-{B};copy=relabel(patch,{0:6,1:7,2:8,3:3,4:4,5:5});double=patch|copy;pd=profile(double)
need(pd['f']==[9,21,14] and all(pd['degrees'][v]==4 for v in (0,1,2)) and max(pd['degrees'].values())==6 and min(pd['degrees'].values())==4 and pd['edge_cofaces']==[2],'patch maximum5 guard')
for face in O:
    opposite=mask(set(range(6))-set(vertices([face])));d=O-{opposite}
    need(profile(d)['f']==[6,12,7] and len([e for e in edges(d) if sum(t&e==e for t in d)==1])==3,'all eight octahedral patches')
print(json.dumps({'positive':p,'delete':profile(deleted),'cap':profile(capped),'two_degree3':pt,'unique3_but_max6':pl,'patch_minimum_failure':pm,'patch_maximum_failure':pd,'octahedral_patches_checked':8},sort_keys=True))
```

## Actual control receipt

Executed the exact block above in separate normal and optimized Python processes, each bounded3CPU/512MiB with3wall timeout. Explicit exception guards stay active under optimization. No target data, producer code or catalog was imported. Seven positive/guard conditions plus all eight octahedral patch choices passed with identical outputs. This does not claim operational branch coverage or general sphere recognition. Code SHA256 `ec5a632b088a08b23f82f6fe7e98995a9355575c6ea736e8726016ef16bd47be`. Receipt and exact output:

```json
{
  "processes": [
    {
      "mode": "normal",
      "exit_code": 0,
      "wall_seconds": 0.0740930950269103
    },
    {
      "mode": "optimized",
      "exit_code": 0,
      "wall_seconds": 0.07759207603521645
    }
  ],
  "results": {
    "cap": {
      "degrees": {
        "0": 4,
        "1": 4,
        "2": 4,
        "3": 4,
        "4": 4,
        "5": 4
      },
      "edge_cofaces": [
        2
      ],
      "f": [
        6,
        12,
        8
      ]
    },
    "delete": {
      "degrees": {
        "0": 4,
        "1": 4,
        "2": 4,
        "3": 4,
        "4": 4,
        "5": 4
      },
      "edge_cofaces": [
        1,
        2
      ],
      "f": [
        6,
        12,
        7
      ]
    },
    "octahedral_patches_checked": 8,
    "patch_maximum_failure": {
      "degrees": {
        "0": 4,
        "1": 4,
        "2": 4,
        "3": 6,
        "4": 6,
        "5": 6,
        "6": 4,
        "7": 4,
        "8": 4
      },
      "edge_cofaces": [
        2
      ],
      "f": [
        9,
        21,
        14
      ]
    },
    "patch_minimum_failure": {
      "degrees": {
        "0": 4,
        "1": 4,
        "2": 4,
        "3": 5,
        "4": 5,
        "5": 5,
        "6": 3
      },
      "edge_cofaces": [
        2
      ],
      "f": [
        7,
        15,
        10
      ]
    },
    "positive": {
      "degrees": {
        "0": 5,
        "1": 5,
        "2": 5,
        "3": 4,
        "4": 4,
        "5": 4,
        "6": 3
      },
      "edge_cofaces": [
        2
      ],
      "f": [
        7,
        15,
        10
      ]
    },
    "two_degree3": {
      "degrees": {
        "0": 5,
        "1": 5,
        "2": 5,
        "3": 5,
        "4": 5,
        "5": 5,
        "6": 3,
        "7": 3
      },
      "edge_cofaces": [
        2
      ],
      "f": [
        8,
        18,
        12
      ]
    },
    "unique3_but_max6": {
      "degrees": {
        "0": 6,
        "1": 6,
        "2": 5,
        "3": 4,
        "4": 4,
        "5": 4,
        "6": 4,
        "7": 3
      },
      "edge_cofaces": [
        2
      ],
      "f": [
        8,
        18,
        12
      ]
    }
  }
}
```

## Frozen source binding

The complete1514 proof was read and checked at SHA256 `4a6346e2970567e93177fb330005ceed123ba5548d10c4aad1480239bd94a35c`; its handoff is `b071389e8ad403a2ace9f0e5d8b3eb0bb17d828313cc2127b151fce8789567a4`. Acceptance explicitly includes the fresh delete-and-cap clarification, SHA256 `58250aff8e228a3da59c75b4571562f579fbc25bdc59c2cae77fb0b45368f7a7`; the original text remains unchanged. This reader imports no producer code and does not use its finite controls as proof. Declared local source bytes were freshly rehashed before freezing this independent record.
