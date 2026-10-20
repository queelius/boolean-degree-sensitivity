"""Exact finite-domain propagation across eligible positive-double pairs."""
from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class DomainIndex:
    size: int
    ones: dict


@dataclass(frozen=True)
class PairDomain:
    pair: int
    size: int
    # Each column is (global odd support, signed unit value, row bit mask).
    columns: tuple


def vertices(mask):return [v for v in range(14) if mask>>v&1]


def index_rows(rows):
    assert rows
    ones={}
    for i,row in enumerate(rows):
        for q in row['unit_faces']:
            ones[q]=ones.get(q,0)|(1<<i)
        for v,k in enumerate(row['linear_numerators']):
            assert k in (-1,0)
            if k:ones[1<<v]=ones.get(1<<v,0)|(1<<i)
    return DomainIndex(len(rows),ones)


def make_domains(geometry,index):
    result=[]
    p,r=geometry['positive_doubles'];common=p&r
    assert (p^common).bit_count()==(r^common).bit_count()==1 and common.bit_count()==4
    for pair in geometry['eligible_pairs']:
        assert pair.bit_count()==2 and common&pair==pair
        assert all(q&pair!=pair for q in geometry['negative_supports'])
        image=vertices(p^common)+vertices(r^common)+vertices(common^pair)
        image+=sorted(set(range(14))-set(vertices(pair))-set(image))
        columns=[]
        for degree,sign in ((1,-1),(3,1)):
            for local_vertices in combinations(range(12),degree):
                local=sum(1<<v for v in local_vertices)
                if local in (13,14):continue
                global_support=pair|sum(1<<image[v] for v in local_vertices)
                columns.append((global_support,sign,index.ones.get(local,0)))
        result.append(PairDomain(pair,index.size,tuple(columns)))
    assert len({domain.pair for domain in result})==len(result)
    return result


def compatible_rows(domain,known):
    live=(1<<domain.size)-1
    for q,sign,ones in domain.columns:
        if q in known:
            value=sign*known[q]
            assert value in (0,1)
            live &= ones if value else ~ones
            if not live:break
    return live


def propagate_domains(initial,domains):
    known=dict(initial);steps=[]
    while True:
        changed=False;counts=[]
        for domain in domains:
            live=compatible_rows(domain,known)
            counts.append([domain.pair,live.bit_count()])
            if not live:
                return dict(status='EXACT_PAIR_DOMAIN_CONTRADICTION',steps=steps,
                            contradiction_pair=domain.pair,known=sorted(known.items()))
            forces=[]
            for q,sign,ones in domain.columns:
                if q in known:continue
                values=live&ones
                if not values or values==live:
                    value=sign*int(bool(values))
                    known[q]=value;forces.append([q,value])
            if forces:
                steps.append(dict(pair=domain.pair,remaining_rows=live.bit_count(),forces=forces))
                changed=True
        if not changed:
            return dict(status='NECESSARY_PAIR_DOMAIN_FIXED_POINT',steps=steps,
                        domain_sizes=counts,known=sorted(known.items()))
