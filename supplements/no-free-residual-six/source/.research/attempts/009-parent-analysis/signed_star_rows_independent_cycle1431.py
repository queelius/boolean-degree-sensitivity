"""Independent face-row reconstruction. No producer or legacy constructor import.

The only mathematical helper imported is the already accepted independent
cycle1424 literal sphere validator. All row formulas below are reconstructed.
"""
from collections import Counter
from enum import Enum
from functools import lru_cache
from itertools import combinations
from math import comb
from typing import NamedTuple

from signed_star_reader_cycle1424 import sphere


class Family(str, Enum):
    DOWNWARD='DOWNWARD'
    TRIANGLE_COFACES='TRIANGLE_COFACES'
    VERTEX_QUARTICS='VERTEX_QUARTICS'
    VERTEX_TRIANGLES='VERTEX_TRIANGLES'
    INDUCED_EULER='INDUCED_EULER'
    EDGE_VALENCE='EDGE_VALENCE'
    SPECIAL_PRESENT='SPECIAL_PRESENT'
    GLOBAL_COUNT='GLOBAL_COUNT'
    FIX_ROOT='FIX_ROOT'


class Row(NamedTuple):
    family: Family
    subject: int
    detail: int
    terms: tuple
    lower: int
    upper: int

    def record(self):
        return dict(key=dict(family=self.family.value,subject=self.subject,detail=self.detail),
                    terms=[list(term) for term in self.terms],lower=self.lower,upper=self.upper)


def need(ok, message):
    if not ok:
        raise ValueError(message)


@lru_cache(None)
def layer(n, cardinality):
    return tuple(sum(1<<v for v in choice) for choice in combinations(range(n),cardinality))


def variables(n):
    need(type(n) is int and 5<=n<=13,'native variable order5..13 required')
    return layer(n,2)+layer(n,3)+layer(n,4)


@lru_cache(None)
def variable_set(n):
    return frozenset(variables(n))


def make_row(n, family, subject, detail, terms, lower, upper):
    need(isinstance(family,Family) and type(subject) is int and subject>=0 and type(detail) is int and detail>=0,'typed native row key required')
    need(type(lower) is int and type(upper) is int and lower<=upper,'integer row bounds required')
    coefficients=Counter()
    for f,value in terms:
        need(type(f) is int and f in variable_set(n) and type(value) is int,'invalid native term')
        coefficients[f]+=value
    return Row(family,subject,detail,tuple((f,value) for f,value in sorted(coefficients.items()) if value),lower,upper)


def extension_masks(n, face, size):
    complement=[v for v in range(n) if not face>>v&1]
    return (face|sum(1<<v for v in add) for add in combinations(complement,size-face.bit_count()))


def common_rows(n):
    variables(n)
    for cardinality in (3,4):
        for face in layer(n,cardinality):
            remaining=face
            while remaining:
                bit=remaining&-remaining; remaining^=bit; subface=face^bit
                yield make_row(n,Family.DOWNWARD,face,subface,((face,1),(subface,-1)),-1,0)
    for triangle in layer(n,3):
        yield make_row(n,Family.TRIANGLE_COFACES,triangle,0,
                       [(q,1) for q in extension_masks(n,triangle,4)]+[(triangle,-2)],0,0)
    for v in range(n):
        bit=1<<v; edges=[(e,-2) for e in extension_masks(n,bit,2)]
        yield make_row(n,Family.VERTEX_QUARTICS,bit,0,[(q,1) for q in extension_masks(n,bit,4)]+edges,-4,-4)
        yield make_row(n,Family.VERTEX_TRIANGLES,bit,0,[(t,1) for t in extension_masks(n,bit,3)]+[(e,-3) for e,_ in edges],-6,-6)
    for subset in range(1<<n):
        size=subset.bit_count()
        if size<3:
            continue
        terms=[]; face=subset
        while face:
            cardinality=face.bit_count()
            if 2<=cardinality<=4:
                terms.append((face,1 if cardinality==3 else -1))
            face=(face-1)&subset
        yield make_row(n,Family.INDUCED_EULER,subset,0,terms,-size,2-size)


def context(n, constant, root, root_link, signed):
    variables(n)
    need(type(constant) is int and type(root) is int and 0<=root<n and type(signed) is bool,'typed context required')
    need(type(root_link) in (list,tuple) and all(type(f) is int and 0<f<1<<n and f.bit_count()==3 and not f>>root&1 for f in root_link),'invalid root-link face')
    need(len(root_link)==len(set(root_link)),'duplicate root-link face')
    active=sorted({v for face in root_link for v in range(n) if face>>v&1})
    physical_to_local={v:i for i,v in enumerate(active)}
    local=[sum(1<<physical_to_local[v] for v in active if f>>v&1) for f in root_link]
    checked=sphere(len(active),local)
    need(set(checked['degrees'])<={3,4,5,6},'invalid root edge valence')
    special={(1<<root)|(1<<v):d for v,d in zip(active,checked['degrees']) if d in (3,6)}
    if signed:
        need(n==13 and constant in (1,2),'global target requires13 coordinates and c1or2')
        counts_=Counter(checked['degrees']);q=counts_[6];order=len(active)
        expected={3:3-q,4:6+3*q-order,5:2*order-9-3*q,6:q}
        need(1<=q<=3 and all(counts_[d]==count for d,count in expected.items()),'wrong signed root profile')
    totals={2:constant+5*n-16,3:2*(constant+4*n-16),4:constant+4*n-16}
    need(all(0<=value<=comb(n,k) for k,value in totals.items()),'invalid global face totals')
    return dict(n=n,constant=constant,root=root,root_link=tuple(sorted(root_link)),special=dict(sorted(special.items())),signed=signed)


def context_rows(layout):
    need(type(layout) is dict,'structured context required')
    expected=context(layout['n'],layout['constant'],layout['root'],layout['root_link'],layout['signed'])
    need(layout==expected and all(type(e) is int and type(v) is int for e,v in layout['special'].items()),'forged context')
    n=layout['n'];root=layout['root'];special=layout['special']
    for edge in layer(n,2):
        terms=[(q,1) for q in extension_masks(n,edge,4)]
        if edge in special:
            yield make_row(n,Family.EDGE_VALENCE,edge,0,terms,special[edge],special[edge])
            yield make_row(n,Family.SPECIAL_PRESENT,edge,0,[(edge,1)],1,1)
        else:
            yield make_row(n,Family.EDGE_VALENCE,edge,0,terms+[(edge,-4)],0,1)
    for k,total in ((2,layout['constant']+5*n-16),(3,2*(layout['constant']+4*n-16)),(4,layout['constant']+4*n-16)):
        yield make_row(n,Family.GLOBAL_COUNT,k,0,[(f,1) for f in layer(n,k)],total,total)
    vertices={1<<v for f in layout['root_link'] for v in range(n) if f>>v&1}
    edges={f^(1<<v) for f in layout['root_link'] for v in range(n) if f>>v&1}
    root_faces=vertices|edges|set(layout['root_link']);root_bit=1<<root
    for face in variables(n):
        if face&root_bit:
            value=int(face^root_bit in root_faces)
            yield make_row(n,Family.FIX_ROOT,face,0,[(face,1)],value,value)


def counts(n, special_count):
    variables(n)
    need(type(special_count) is int and 0<=special_count<=n-1,'invalid special-edge count')
    e,t,q=(comb(n,k) for k in (2,3,4));fix=sum(comb(n-1,k) for k in (1,2,3))
    downward=3*t+4*q;truth=(1<<n)-1-n-e
    truth_terms=e*((1<<(n-2))-1)+t*(1<<(n-3))+q*(1<<(n-4))
    shared_terms=2*downward+t*(n-2)+n*(comb(n-1,3)+n-1)+n*(comb(n-1,2)+n-1)+truth_terms
    return dict(common_rows=downward+t+2*n+truth,context_rows=e+special_count+3+fix,
                common_terms=shared_terms,context_terms=e*comb(n-2,2)+(e-special_count)+special_count+e+t+q+fix,
                omitted_boolean_tautologies=1+n+e)


def accepts(rows, assignment):
    return all(r.lower<=sum(c for f,c in r.terms if f in assignment)<=r.upper for r in rows)


def cycle_join(a,b):
    left=[(1<<i)|(1<<((i+1)%a)) for i in range(a)]
    right=[(1<<(a+j))|(1<<(a+(j+1)%b)) for j in range(b)]
    return sorted(e|f for e in left for f in right)


def face_assignment(facets):
    result=set()
    for facet in facets:
        face=facet
        while face:
            if face.bit_count()>=2:
                result.add(face)
            face=(face-1)&facet
    return result


def q1_fixture():
    return sorted([sum(1<<v for v in (6,i,(i+1)%6)) for i in range(6)]+
                  [sum(1<<v for v in f) for f in ((0,1,2),(0,2,5),(2,3,5),(3,4,5))])


def positive_control(a,b):
    n=a+b;facets=cycle_join(a,b);assignment=face_assignment(facets);c=16-4*n+len(facets)
    layout=context(n,c,0,[f^1 for f in facets if f&1],False)
    common=list(common_rows(n)); contextual=list(context_rows(layout));rows=common+contextual
    need(len({(r.family,r.subject,r.detail) for r in rows})==len(rows),'duplicate row identity')
    need(accepts(rows,assignment),'positive control violates a row')
    values=[1-x.bit_count()+sum((1 if f.bit_count()%2==0 else -1) for f in assignment if f&x==f) for x in range(1<<n)]
    need(set(values)<={-1,0,1} and values[0]==1 and all(values[1<<v]==0 for v in range(n)),'positive control not ternary/origin/unit normalized')
    numerators=[]
    for character in range(1<<n):
        total=sum(value if (character&x).bit_count()%2==0 else -value for x,value in enumerate(values))
        need((16*total)%(1<<n)==0,'nonintegral scale16 Walsh coefficient')
        numerators.append(16*total//(1<<n))
    need(numerators[0]==c,'wrong Walsh constant')
    need(all(value==0 for support,value in enumerate(numerators) if support.bit_count() not in (0,2,4)),'unexpected Walsh support')
    need(all(value in (-1,0) for support,value in enumerate(numerators) if support.bit_count()==2),'wrong ordinary Walsh pairs')
    need(all(value in (0,1) for support,value in enumerate(numerators) if support.bit_count()==4),'wrong Walsh quartics')
    return dict(n=n,constant=c,cube_inputs=1<<n,direct_character_coefficients=1<<n,
                all_rows_accept=True,ternary_and_exact_scale16_Walsh=True,
                common_rows=len(common),context_rows=len(contextual),common_terms=sum(len(r.terms) for r in common),
                context_terms=sum(len(r.terms) for r in contextual),actual_n13_signed_target_witness=False)
