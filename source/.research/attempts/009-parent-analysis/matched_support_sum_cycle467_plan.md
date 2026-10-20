# Resolve the remaining product group using its full 32-point support

GLOBAL STATUS: OPEN. Geometry 34, first row 58 remains open. Cycle 465
independently verifies all 496 nonzero product groups UNSAT and the sole
zero group UNKNOWN at 3,000 nodes with nine LIMIT subtrees. No complete
first-row exclusion follows.

Adapt the cycle-424 contingency with one essential scope change: the
component c complementary to the marked component is not a safe component
in this path geometry. Use its actual accepted domain, with no Q4 count
restriction. The existing delta-zero relation tuples still prove

    L - R + m*c = 0,

where the two products use the original join's signs L=B_i B_j/64 and
R=-B_k B_l/64. The marked value m and complementary value c are divided
by 8. Derive all indices from the accepted instance. On the 32 inputs S
where the fixed marked row is nonzero, check literally that m is +/-1
and all components have integral normalization. Then R=L+m*c is necessary.

Use exactly the accepted zero group's original Cartesian pair indices.
Evaluate each pair on S and group identical vectors while retaining every
pair ID. Evaluate m*c for every original complementary candidate, retaining
duplicates. Exhaust every distinct L vector and every complementary
candidate and look up the exact sum among all R vectors. Preserve all
matching triples and project them back to the five unfixed components.
If no triple exists, this conditional group is excluded. Otherwise inspect
the reduction before choosing a refined search or a second complete
partition. No higher-degree quotient theorem or symmetry is assumed.

The independent reader must reconstruct S as the complement of the marked
zero set within the selected opposite-apex slice, recalculate every pair
product and every m*c, verify the product-vector grouping and all original
row maps, and check the entire L/c Cartesian cover using Python integer
tuple arithmetic. The producer uses bounded int64 vector addition and byte
keys; duplicate rows must retain all IDs. Positive, negative, duplicate,
empty-match, wrong-index, and arithmetic-overflow controls precede use.

The support experiment has about 44 thousand left pairs and 985 thousand
right pairs, each with just 32 entries, so its raw product arrays should
be much smaller than another 94-million-pair zero-slice experiment. Derive
the actual distinct-vector count before interpreting search cost. Exact
necessary filtering is not itself a Boolean construction.
