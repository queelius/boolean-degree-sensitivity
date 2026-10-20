"""Literal-word values of one projection after fixing another and all pair rows."""
from collections import defaultdict
from functools import lru_cache
from cubic_partial_scalar import PartialScalarValues
from verify_core_fourier_envelope_certificate import literal_words


class ConditionalCubicScalar:
    def __init__(self,rows,g,fixed_mask=3,target_mask=12):
        self.rows=PartialScalarValues(rows,g);self.fixed_mask=fixed_mask;self.target_mask=target_mask
        target={w:v for w,d,ts,v in literal_words(self.rows.pairs,target_mask)};self.groups=defaultdict(list)
        for w,d,ts,v in literal_words(self.rows.pairs,fixed_mask):self.groups[d,ts,v].append((w,target[w]))

    @lru_cache(None)
    def at_signature(self,weight,delta,ts,fixed_value):
        values=set()
        for word,value in self.groups[delta,ts,fixed_value]:
            valid=True
            for y in range(16):
                w=weight+y.bit_count()
                if (w in (0,12,13) and word>>y&1) or (w in (1,2,14) and not word>>y&1):valid=False;break
            if valid:values.add(value)
        return tuple(sorted(values))

    def allowed(self,row_ids,spectrum):
        polynomials=[self.rows.polynomial_values(i) for i in row_ids];result=[]
        for x in range(1024):
            fixed=sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in spectrum)
            values=self.at_signature(x.bit_count(),1-(x&1)-((x>>1)&1),tuple(p[x] for p in polynomials),fixed)
            assert values;result.append(list(values))
        return result
