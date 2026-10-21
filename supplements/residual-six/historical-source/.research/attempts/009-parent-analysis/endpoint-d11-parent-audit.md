# Independent audit: baseline negative-free endpoint, codegree eleven

**PASS, conditional local theorem. The fourteen-variable existence question remains unresolved.**

I checked the normalization argument in
`../008-sparse-spectrum-proof/negative-free-endpoint-codegree-eleven.md`
and independently replayed every finite step relevant to its conclusion.
The accepted scope is a self-dual one-zero-pair representative, an endpoint
with incident cubic numerators in {-1,0}, incident quintic numerators in
{0,1}, and singleton numerator at most three.

The unit and quadratic identities give eighteen tetrahedra through the
opposite endpoint b, two incident negative pair numerators, and one
positive extension w. These are precisely the local hypotheses used by
the earlier codegree-eleven classification; its old disjoint-profile
introduction adds no hypothesis used in that classification. The
octahedron/bipyramid forms are therefore an applicable complete cover.

The induced-Euler formula has the required corrections
`p(X)=1-chi(K[X])-1[b in X]+1[b,w in X]`. In particular chi(K)=0,
E=53+c, P=40+c, and the split complex has E+1 edges. The apex form
fails the strip boundary test. In the rim form all eight possible strips
normalize the link of w to a connected sphere with f-vector (10,24,16).
Other vertex links cannot be two projective planes: ordinary rim or
octahedral vertices have a degree-four vertex in the link; for a
bipyramid apex the putative six-clique would force the two far rim edges
at w which its exact strip star omits. Thus the normalized complex is
indeed a closed simplicial three-manifold, not just a pseudomanifold.

The new verifier `audit_endpoint_d11.py` uses the parent's structured
catalog parser and permutation-based strip enumeration, independently of
the producer's parser and reciprocal-neighborhood enumeration. It
reconstructs all 4,787 records: 111 have fourteen vertices; nineteen have
all edge valences four or five; all nineteen have at most 57 edges.
It scans every unordered pair, orients any degree-six/degree-seven pair,
and checks nonadjacency and exactly one common neighbor. There are exactly
four possibilities, in records 436,454,467,470. It checks identification
directly against facets and finds the same four independent triples,
each giving the literal forbidden value -2. No optimization or UNKNOWN
result is used.

This proof inherits the explicit external completeness theorem:
Frick (2015), Theorem 3.10, https://d-nb.info/1076082246/34, and the
author-hosted small-valence manifold catalog. Its historical enumeration
has not been regenerated. The frozen compressed source hash is
41071b36a731396d5273c60748aea7937c876136684ac479971e87e27e2fbb59.
The finite replay, controls, hashes, and test results are bound in the
cycle64 local-audit manifest. This does not close any unbound global
support family by itself.
