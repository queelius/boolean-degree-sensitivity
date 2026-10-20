# First-row-58 consequence: all three products vanish on the selected slice

GLOBAL STATUS: OPEN. This is a necessary restriction in geometry 34,
first-row representative 58. It does not exclude that first row.

Cycle 465 independently checks a complete partition into 497 product
vectors on the marked component's 224-point zero slice Z. Every nonzero
vector has a complete UNSAT proof. Thus any actual completion has the
zero vector there. The zero group's search remains UNKNOWN, with nine
LIMIT subtrees, and is not promoted to UNSAT.

Cycle 469 independently checks the remaining support S of size 32. There
are 43,744 original left pairs and 984,649 original right pairs, yielding
71 and 1,096 distinct product vectors on S. Every one of the 2,136
complementary candidates is zero on S. The complete 71*2,136=151,656
vector/candidate sum cover has exactly 2,136 matching triples. Every one
uses the zero left vector and zero right vector. Duplicate complementary
target vectors retain all their original candidate IDs.

Consequently both joined products vanish on S and Z. The third product
also vanishes: its marked factor is zero on Z, and its complementary
factor is zero on S. Therefore all three complementary products vanish
on the entire 256-input slice with the two apex bits fixed to (0,1).
No assertion about the other apex orientation is needed here.

The retained component-domain sizes are [2080,3896,2136,1,3704,3672],
compared with [2120,3896,2136,1,3704,3912] in the open product group.
The original Cartesian pair indices provide more information than these
unary projections: each pair of entire component rows must belong to its
complete accepted compatibility list. That correlation across all 256
inputs is the next search target. A new search must retain every old
relation and independently verify its binary-pair deductions.

The consequence checker composes the two already accepted finite covers,
checks every other product group is UNSAT, checks all matched product and
complement vectors are zero, and checks that Z and S exactly partition the
selected slice. It does not replay the old enumerations or invent a
Boolean function. Counts remain 194/292 first rows excluded in geometry
34, and 59/87 signed geometries excluded in the larger scoped frontier.
