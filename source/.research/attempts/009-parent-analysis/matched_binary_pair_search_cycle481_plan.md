# Next: preserve complete whole-row pair compatibility during search

GLOBAL STATUS: OPEN. No new first row or signed geometry closed in the
geometry-34 pilot. First row 58 is still open; all its nonzero product
groups are excluded and its zero group is UNKNOWN. The accepted full
selected-slice zero restriction is cycle 471.

The exact pair lists carry correlations lost by projection to individual
component domains. Preserve these lists as binary constraints between
whole candidate rows. Do not run another 94-million-pair join or merely
extend the unchanged 3,000-node tree. The cycle-474 inventory derives the
two nontrivial relation sizes from the accepted support-sum certificate.

Build the new solver as an explicit version over the existing pointwise
model. Retain all old raw, count, safe-count, cross, and zero-product
relations. Obtain the parent component indices, complete pair IDs, and
retained domains from the accepted cycle-469 certificate. For each side,
keep exactly those original Cartesian pairs whose support-vector label
occurs in a matching sum triple. Map original row IDs to local retained
row indices with validated bijections. Record every resulting pair; do
not infer compatibility from a sample or from marginal domains.

Use a typed binary-relation structure with two component indices and an
exact allowed-pair array. Store adjacency as integer bitsets in the
producer. During each node, alternate existing pointwise propagation with
binary arc consistency until a fixed point: a row survives only if at
least one compatible row remains in the other component's domain. Each
recorded propagation event identifies its relation and whether it is
pointwise or binary. A binary contradiction requires no surviving edge.
Check binary constraints explicitly at every proposed singleton witness.

Write a separate set-domain reader that reconstructs the allowed-pair
lists from the accepted source certificates and replays every propagation,
split, contradiction, and witness using ordinary sets. It must not import
the producer's adjacency construction or propagation code. A complete
two-child split must cover its parent domain, and LIMIT remains UNKNOWN.
No original point or cross relation may be omitted.

Before the real search, test positive singleton cases, empty binary
relations, an inconsistent equality/inequality cycle that pointwise
constraints alone cannot exclude, complete small Cartesian enumerations,
wrong candidate indices, damaged propagation events, and UNKNOWN
preservation. Record coverage honestly. Run the focused research tests
and repository suite, then a fresh 1,000-node pilot. The old search used
different local row indices, so do not reuse its tree without a proved
mapping. The lower fresh budget tests whether the added correlation
changes propagation, rather than paying for an unchanged search.

If the conditional zero group is independently UNSAT, compose it with
all 496 accepted nonzero-group exclusions from cycle 465. Only a complete
group cover for the same first row, geometry, and coordinate quotient
permits a whole-first-row exclusion and a frontier update. If it remains
UNKNOWN, inspect its explicit residual domains and binary neighborhoods
before selecting another experiment.

The abstract degree-shift lemma at cycle 473 is available for a later
algebraic classification: division by the Q4 support factor lowers degree
by exactly three, so a supported degree-six product has a cubic quotient
in five free signs. It adds no pruning to the already exact support-vector
cover and is not a reason to count another case as solved.

This plan is unexecuted at checkpoint 480. No binary solver, reader, or
binary search certificate has been created yet. The larger signed frontier
remains 59/87 closed, geometry 34 remains 194/292 first rows closed, and
the original 14-variable Boolean-function existence goal remains active.
