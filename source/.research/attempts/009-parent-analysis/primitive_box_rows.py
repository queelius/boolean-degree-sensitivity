"""Positive integer gcd division preserves a bounded row exactly."""
from math import gcd
from numbers import Integral
from baseline_full_truth_model import Row


def primitive_row(row):
    if not isinstance(row.lower,Integral) or not isinstance(row.upper,Integral) or row.lower>row.upper:
        raise ValueError('Require ordered integer bounds.')
    if any(not isinstance(i,Integral) or i<0 or not isinstance(a,Integral) for i,a in row.terms):
        raise ValueError('Require integer coefficients and nonnegative integer column indices.')
    divisor=gcd(int(row.lower),int(row.upper))
    for _,coefficient in row.terms:divisor=gcd(divisor,int(coefficient))
    divisor=divisor or 1
    normalized=Row(tuple((int(i),int(a)//divisor) for i,a in row.terms),
        int(row.lower)//divisor,int(row.upper)//divisor,{**row.reason,'primitive_divisor':divisor})
    return normalized,divisor
