# Independent audit: two positive cubic exceptions at a negative-free coordinate

**PASS, conditional local theorem. The global decision remains unresolved.**

I checked `../006-solver-resume/two-positive-cubic-free-derivative.md`
after its cross-edge wording was clarified. The hypotheses are exactly
those stated there: a ternary even derivative on thirteen variables,
p(0)=1, p(units)=0, c<=2, quartic Fourier numerators zero or one, exactly
two pair numerators +1 with all others -1/0, and ordinary quadratic
coefficients zero/one with at most one coefficient two.

All triangle incidences are two. In the special-edge case, this remains
true when the two exceptional pairs and the special pair form a
triangle: an ordinary exceptional pair has a C3 link, which is still
2-regular. No missing baseline-pair assumption is needed.

With no special pair, the Euler formula is p=1-chi and E=49+c<=51.
A disconnected vertex link can only consist of two six-vertex
characteristic-one surfaces; the edge count then leaves at most nine
cross edges between their vertex sets A and B. The good/singly-bad degree
arguments are valid. In particular the impossible singly-bad six-vertex
link would require a triangulated pentagon with disjoint diagonals.
A good cross-degree-one vertex y in A forces its neighbor z in B to be
joined to all six A vertices; the other five vertices **of B** require
at least four additional cross edges. This correctly contradicts nine.
All vertex links are spheres and the complex is connected. Its catalog
obstruction is covered by the already independently checked 76
thirteen-vertex records with E<=52; this retains the published catalog
completeness dependency.

With a special pair, an incident ordinary positive exception is excluded
by the endpoint curvature identity. Otherwise both endpoint stars are
capped strips. A shared strip face creates an ordinary exceptional C3
at its unique boundary edge, and distinct faces use distinct such edges.
The independent control obtains one/eight/one roots at sizes seven/eight/
nine. Among the 64 ordered size-eight pairs, those with at most two
common faces have at most four common interior edges. The core thus has
at least 37 edges. The remaining three vertices form a clique by the
independent-triple range obstruction and contribute at least 14 more
edges. This contradicts E=48+c<=50.

`audit_two_positive_cubic.py` separately enumerates the strip roots and
all 120 three-triangle subsets on a pentagon. Exactly five triangulated
pentagons have the required boundary, and each pair of diagonals shares
an endpoint. The root-intersection histograms agree with the producer.
The proof uses exact finite enumeration and the explicit existing
Frick2015 Theorem3.10 catalog dependency, not a solver status.

The accepted conclusion applies only after an application binds all
these local hypotheses. The residual two-star cases themselves are
not declared excluded by this audit.
