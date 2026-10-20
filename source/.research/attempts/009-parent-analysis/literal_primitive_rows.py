"""Reconstruct gcd division from independent integer rows, never saved divisors."""
from collections import Counter
from math import gcd
from literal_core_slice_rows import LiteralRows


class LiteralPrimitiveRows:
    def __init__(self,base):
        self.base=base;self.variable_count=base.variable_count;self.row_count=base.row_count
        divisors=[];max_old=max_new=max_old_rhs=max_new_rhs=0;self.nonzeros=0
        for i in range(self.row_count):
            terms,lower,upper=base.row(i);divisor=0
            for value in list(terms.values())+[lower,upper]:divisor=gcd(divisor,value)
            divisor=max(1,divisor);divisors.append(divisor);self.nonzeros+=len(terms)
            old=max((abs(v) for v in terms.values()),default=0);max_old=max(max_old,old);max_new=max(max_new,old//divisor)
            max_old_rhs=max(max_old_rhs,abs(lower),abs(upper));max_new_rhs=max(max_new_rhs,abs(lower)//divisor,abs(upper)//divisor)
        self.divisors=tuple(divisors)
        self.scaling=dict(divisor_counts=[dict(divisor=d,rows=n) for d,n in sorted(Counter(divisors).items())],
            maximum_original_coefficient=max_old,maximum_primitive_coefficient=max_new,
            maximum_original_bound=max_old_rhs,maximum_primitive_bound=max_new_rhs)

    def row(self,index):
        assert type(index) is int and 0<=index<self.row_count
        terms,lower,upper=self.base.row(index);d=self.divisors[index]
        return {i:v//d for i,v in terms.items()},lower//d,upper//d

    def scaling_inventory(self):return self.scaling

    def verify(self,certificate):return LiteralRows.verify(self,certificate)
