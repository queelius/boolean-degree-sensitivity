"""Exact integer truth rows for an odd degree-five normalized spectrum.

Write 1-2f = (sum k_S chi_S)/16 with odd |S| <= 5. Unfixed singleton,
cubic and quintic numerators respectively have domains {1,2}, {-1,0}, {0,1}.
Literal fixed coefficients may be arbitrary integers; their application
guards are separate. The normalization is f(0)=0 and f=1 at every singleton
and pair. Truth rows through weight ceil(n/2) suffice, by the explicit odd
spectrum, to make every integral completion a Boolean function.
"""
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from math import comb


class Kind(str, Enum):
    COEFFICIENT = 'coefficient_bit'
    TRUTH = 'truth'


@dataclass(frozen=True)
class Variable:
    kind: Kind
    support: int


@dataclass(frozen=True)
class Row:
    terms: tuple
    lower: int
    upper: int
    reason: dict


@dataclass(frozen=True)
class Model:
    n: int
    fixed: tuple
    variables: tuple
    rows: tuple


def mask(vertices):
    return sum(1 << v for v in vertices)


def affine(degree):
    assert degree in (1, 3, 5)
    return (1 if degree == 1 else 0), (-1 if degree == 3 else 1)


def coefficient_value(model, support, assignment):
    fixed = dict(model.fixed)
    if support in fixed:
        return fixed[support]
    index = model.variables.index(Variable(Kind.COEFFICIENT, support))
    offset, sign = affine(support.bit_count())
    return offset + sign*assignment[index]


def build(fixed, *, n=14, max_truth_weight=7):
    if type(n) is not int or n < 5 or not 5 <= max_truth_weight <= n:
        raise ValueError('Require n>=5 and a truth weight between five and n.')
    fixed = dict(fixed)
    if any(type(s) is not int or not 0 <= s < 1 << n or s.bit_count() not in (1, 3, 5)
           or type(value) is not int for s, value in fixed.items()):
        raise ValueError('Fixed spectrum must contain integer odd supports and numerators.')
    sets = {size: tuple(mask(vs) for vs in combinations(range(n), size)) for size in range(1, 6)}
    variables = tuple(Variable(Kind.COEFFICIENT, q) for size in (1, 3, 5) for q in sets[size] if q not in fixed)
    variables += tuple(Variable(Kind.TRUTH, q) for size in (3, 4, 5) for q in sets[size])
    index = {v: i for i, v in enumerate(variables)}
    rows = []

    def add(coefficients, truths, lower, upper, kind, support=None):
        terms = Counter()
        constant = 0
        for q, a in coefficients:
            if q in fixed:
                constant += a*fixed[q]
            else:
                offset, sign = affine(q.bit_count())
                constant += a*offset
                terms[index[Variable(Kind.COEFFICIENT, q)]] += a*sign
        for q, a in truths:
            terms[index[Variable(Kind.TRUTH, q)]] += a
        rows.append(Row(tuple(sorted((i, a) for i, a in terms.items() if a)),
                        lower-constant, upper-constant,
                        dict(kind=kind, **({} if support is None else dict(support=support)))))

    def cofaces(size, support, coefficient=1):
        return [(q, coefficient) for q in sets[size] if q & support == support]

    def subsets(size, support, coefficient=1):
        return [(q, coefficient) for q in sets[size] if q & support == q]

    k5 = (n-1)*(n-6)
    k3 = 8*(n-1)-2*k5
    k1 = 16-k3-k5
    for size, value in ((5, k5), (3, k3), (1, k1)):
        add(cofaces(size, 0), (), value, value, 'total_spectral_sum', size)
    for vertex in sets[1]:
        add(cofaces(5, vertex)+[(vertex, -1)], (), 4*n-20, 4*n-20, 'vertex_top_sum', vertex)
        add(cofaces(3, vertex)+[(vertex, 2)], (), 36-4*n, 36-4*n, 'vertex_cubic_sum', vertex)
    for pair in sets[2]:
        add(cofaces(5, pair)+cofaces(3, pair), (), 8, 8, 'pair_inversion', pair)
    for triple in sets[3]:
        add(cofaces(5, triple)+[(triple, 1)], [(triple, -4)], 0, 0, 'triple_inversion', triple)
    for quartet in sets[4]:
        add(cofaces(5, quartet), [(quartet, 2)]+subsets(3, quartet, -2),
            -4, -4, 'quartet_truth', quartet)
    for quintet in sets[5]:
        add([(quintet, -1)], [(quintet, 1)]+subsets(4, quintet, -1)+subsets(3, quintet),
            5, 5, 'quintet_truth', quintet)
    for size in range(6, max_truth_weight+1):
        constant = size-comb(size, 2)+2*comb(size, 4)
        for ground in combinations(range(n), size):
            support = mask(ground)
            # Enumerate subsets of this ground set rather than scan a global table.
            tops = [(mask(vs), 1) for vs in combinations(ground, 5)]
            truths = [(mask(vs), 4-size) for vs in combinations(ground, 3)]
            truths += [(mask(vs), 1) for vs in combinations(ground, 4)]
            add(tops, truths, -constant, 1-constant, 'upper_boolean_truth', support)
    return Model(n, tuple(sorted(fixed.items())), variables, tuple(rows))
