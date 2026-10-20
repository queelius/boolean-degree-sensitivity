# Reading first-row coverage from a partial search

GLOBAL STATUS: OPEN.

The accepted first-row quotient supplies a representative for every actual
function in its signed geometry, without requiring a function to be invariant
under any permutation. The accepted partial constraint tree partitions that
quotient instance. Its closed subtrees have independently checked
contradictions; its remaining LIMIT leaves are not decided.

Replay the recorded point cuts and binary splits along every open path.
Let R be the union of the marked component's candidate-index domains at
the LIMIT leaves. Any solution of the necessary component problem must use
a marked row in R. Therefore every quotient representative outside R is
excluded. Keeping all indices in R is conservative: some LIMIT states may
also close after further propagation.

The reader extracts all LIMIT paths, checks their count against the accepted
search manifest, and reconstructs their domains with the independent array
replayer. It translates candidate indices back through the exact accepted
quotient row map. This gives a necessary residual first-row cover, not a
Boolean construction and not an exclusion of the whole signed geometry.
Representative counts are not proportional to the number of possible functions.
