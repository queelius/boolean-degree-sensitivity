from itertools import product
from fixed_projection_cube_domains import conditioned_relation,projection_values
from verify_core_fourier_envelope_certificate import literal_words


def test_conditioned_relation_matches_independent_boolean_words():
    pairs=(5,9,6,10);records=literal_words(pairs,3)
    for weight,delta in product((0,1,2,5,8,9,10),(-1,0,1)):
        for value in range(-16,17,4):
            expected=set()
            for word,d,ts,v in records:
                if d!=delta or v!=value:continue
                if all(not ((weight+y.bit_count() in (0,12,13) and word>>y&1) or
                            (weight+y.bit_count() in (1,2,14) and not word>>y&1)) for y in range(16)):expected.add(ts)
            assert set(conditioned_relation(pairs,weight,delta,3,value))==expected
    assert conditioned_relation(pairs,5,0,3,1)==()
    assert conditioned_relation(pairs,5,0,3,0)


def test_projection_transform_matches_literal_parities():
    spectrum=[(1,-1),(2,-1),(4,-1),(7,-2),(11,1),(13,1),(14,1)]
    assert projection_values(spectrum,4)==[sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in spectrum) for x in range(16)]
