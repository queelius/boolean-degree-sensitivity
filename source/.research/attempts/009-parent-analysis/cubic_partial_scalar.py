"""Scalar necessary Fourier values for arbitrary nonempty pair-row domains."""
from verify_four_cube_pair_domains import LiteralCubeChecker
from verify_core_fourier_envelope_certificate import literal_words


class PartialScalarValues:
    def __init__(self,rows,g):
        self.rows=rows;self.g=g;self.pairs,self.outside=LiteralCubeChecker.coordinates(g);self.row_values={}

    def polynomial_values(self,index):
        if index not in self.row_values:
            row=self.rows[index];terms=[(q,1) for q in row['unit_faces']]+[(13,2),(14,2)]+[(1<<v,k) for v,k in enumerate(row['linear_numerators']) if k]
            values=[]
            for point in range(1024):
                x=(point&3)|((point>>2)<<4);numerator=-sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in terms)
                assert numerator%8==0 and -16<=numerator<=16;values.append(numerator//8)
            self.row_values[index]=tuple(values)
        return self.row_values[index]

    def allowed(self,domains,mask):
        assert [d['pair'] for d in domains]==self.g['eligible_pairs']
        assert all(d['rows'] and d['rows']==sorted(set(d['rows'])) and all(type(i) is int and 0<=i<len(self.rows) for i in d['rows']) for d in domains)
        polynomials=[[self.polynomial_values(i) for i in d['rows']] for d in domains];records=literal_words(self.pairs,mask);cache={};result=[]
        for point in range(1024):
            possibilities=tuple(tuple(sorted({p[point] for p in block})) for block in polynomials);delta=1-(point&1)-((point>>1)&1)
            weight=point.bit_count();key=(weight,delta,possibilities)
            if key not in cache:
                ones=zeros=0
                for y in range(16):
                    if weight+y.bit_count() in (0,12,13):zeros|=1<<y
                    elif weight+y.bit_count() in (1,2,14):ones|=1<<y
                allowed=sorted({value for word,d,ts,value in records if d==delta and word&ones==ones and word&zeros==0 and all(t in possible for t,possible in zip(ts,possibilities))})
                assert allowed;cache[key]=allowed
            result.append(cache[key])
        return result
