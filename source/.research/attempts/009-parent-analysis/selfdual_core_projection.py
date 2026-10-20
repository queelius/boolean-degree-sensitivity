"""Exact coefficient coordinates for an odd spectrum on a complementary face."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectedCoefficient:
    feature: int
    character: int
    support: int
    values: tuple


def projected_coefficients(core,outside,degree,fixed,domains):
    n=len(core)+len(outside)
    if not core or not outside or any(type(v) is not int for v in core+outside):
        raise ValueError('Need nonempty integer coordinate lists.')
    if len(set(core+outside))!=n or set(core+outside)!=set(range(n)):
        raise ValueError('Core and outside coordinates must partition the full cube.')
    if type(degree) is not int or degree<1 or degree%2!=1:
        raise ValueError('This face projection requires a positive odd total-degree bound.')
    if set(domains)!=set(range(1,degree+1,2)):
        raise ValueError('Supply a coefficient domain for each odd total degree.')
    if any(not 1<=len(vs)<=2 or any(type(v) is not int for v in vs) or tuple(sorted(set(vs)))!=tuple(vs) for vs in domains.values()):
        raise ValueError('Domains must be sorted one- or two-value integer sets.')
    if any(type(s) is not int or not 0<s<1<<n or s.bit_count()%2!=1 or s.bit_count()>degree or type(v) is not int for s,v in fixed.items()):
        raise ValueError('Fixed coefficients need odd supports within the stated degree and integer values.')
    records=[]
    for feature in [0]+[1<<i for i in range(len(core))]:
        for character in range(1<<(len(outside)-1)):
            if character.bit_count()>degree-feature.bit_count():continue
            support=sum(1<<core[i] for i in range(len(core)) if feature>>i&1)
            support+=sum(1<<v for i,v in enumerate(outside[:-1]) if character>>i&1)
            if support.bit_count()%2==0:support+=1<<outside[-1]
            values=(fixed[support],) if support in fixed else tuple(domains[support.bit_count()])
            records.append(ProjectedCoefficient(feature,character,support,values))
    return tuple(records)
