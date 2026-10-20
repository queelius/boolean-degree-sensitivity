# One-negative exclusion for one fixed quartet and one missing diagonal

The scope is the accepted four-cycle geometry with safe pairs513,1025,514,1026
and catalog rows56,56,170,310 respectively. The missing diagonal has local core
mask3. This theorem concerns its cubic outside Fourier numerator B only.

The complete120-position interval proof leaves negative triples13 and14.
Suppose B has exactly one negative cubic, at either remaining position. Write
Q for its number of negative linear coefficients and P for its number of
positive cubic coefficients. The signed divisibility criterion gives Q even,
and B(0)=4 gives P=Q+6. Thus Q is one of0,2,4,6,8,10.

For each of these twelve position/count cases, retain every allowed B value
from the exact Boolean core words. At outside points whose allowed values have
more than one square, introduce convex weights on those values, with total
mass one and first moment equal to B. Their weighted square is B squared for
an actual Boolean core word. Where every allowed value has the same square,
that square is fixed. The odd polynomial B has equal squares at complementary
outside inputs; use one representative from each of512 pairs.

Parseval is exact for the actual flags:

    sum_{512 points} B(x)^2 = 512*(Q+P+4).

Together with the coefficient domain, interval rows and exact counts, these
give a necessary linear relaxation. Each of the twelve relaxations has an
integer Farkas certificate. The independent reader rebuilds the allowed
values by scalar Boolean-core enumeration, validates every value-state column,
reconstructs the mass, first-moment, energy and count rows, and checks exact
coefficient cancellation and a negative right side.

Combining the118 earlier positional certificates with these twelve certificates
covers every possible single-negative B in this fixed quartet. In the actual
exact-four-cycle scope a missing diagonal has at least one negative, so this
diagonal must have at least two. The other missing diagonal requires at least
one, and there are four negatives globally; hence two and three remain possible
here. The fixed quartet itself and the global14/5 existence problem remain open.
Direct value-set containment does not transfer this theorem to the other17
fixed quartets under56/56; their projections need separate treatment.
