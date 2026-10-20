from itertools import product,combinations


def test_signed_eight_divisibility_against_all_small_integer_polynomials():
    # Exhaust every signed coefficient choice on the seven nonconstant
    # characters of a three-cube, and every constant residue modulo eight.
    n=3;supports=list(range(1,1<<n));pairs=[(1<<i)|(1<<j) for i,j in combinations(range(n),2)]
    checked=0
    for coefficients in product((-1,0,1),repeat=len(supports)):
        incidence=all(sum(k for q,k in zip(supports,coefficients) if q>>i&1)%4==0 for i in range(n))
        incidence&=all(sum(k for q,k in zip(supports,coefficients) if q&pair==pair)%2==0 for pair in pairs)
        evaluations=[sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in zip(supports,coefficients)) for x in range(1<<n)]
        for c in range(8):
            criterion=(c+sum(coefficients))%8==0 and incidence
            assert criterion==all((c+v)%8==0 for v in evaluations);checked+=1
    assert checked==17496
