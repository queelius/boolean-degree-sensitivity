"""Scalar reconstruction and integer verification of a core-envelope Farkas proof.

No LP solver, vectorized core-cube producer, or projection-row producer is
imported. Only the sparse certificate's used rows need reconstruction.
"""
from argparse import ArgumentParser
from functools import lru_cache
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from verify_four_cube_pair_domains import LiteralCubeChecker

H=Path(__file__).resolve().parent


@lru_cache(None)
def literal_words(pairs,core_mask):
    blocks=[]
    for pair in pairs:
        i,j=[v for v in range(4) if pair>>v&1];rest=[v for v in range(4) if not pair>>v&1]
        blocks.append([(base,base|(1<<i),base|(1<<j),base|pair)
                       for base in (0,1<<rest[0],1<<rest[1],(1<<rest[0])|(1<<rest[1]))])
    result=[]
    for word in range(65536):
        delta=None;ts=[]
        for block in blocks:
            a,b,c,d=[((word>>ij)&1)+((word>>x)&1)-((word>>i)&1)-((word>>j)&1) for x,i,j,ij in block]
            difference=b-a
            if a!=d or b!=c or difference not in (-1,0,1) or (delta is not None and difference!=delta):break
            delta=difference;ts.append(a)
        if len(ts)==len(pairs):
            value=sum((1-2*((word>>x)&1))*(-1 if (x&core_mask).bit_count()%2 else 1) for x in range(16))
            result.append((word,delta,tuple(ts),value))
    return tuple(result)


def bounds(point,domains,checker,records):
    values=checker.at(point)
    possible=[{values[i] for i in d['rows']} for d in domains]
    delta=1-(point&1)-((point>>1)&1);ones=zeros=0
    for x in range(16):
        w=point.bit_count()+x.bit_count()
        if w in (0,12,13):zeros|=1<<x
        elif w in (1,2,14):ones|=1<<x
    actual=[value for word,d,ts,value in records if d==delta and word&ones==ones and word&zeros==0
            and all(t in possibilities for t,possibilities in zip(ts,possible))]
    assert actual
    return min(actual),max(actual)


def verify(rows,geometry,record):
    assert record['result']['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
    known=dict(record['initial_known']);columns=record['projection_variables'];domains=record['input_domains']
    assert [d['pair'] for d in domains]==geometry['eligible_pairs']
    assert all(d['rows'] and len(d['rows'])==len(set(d['rows'])) and all(0<=r<len(rows) for r in d['rows']) for d in domains)
    mask=record['core_mask'];assert 0<=mask<16
    core=geometry['positive_doubles'][0]&geometry['positive_doubles'][1]
    vs=[v for v in range(14) if core>>v&1]
    global_core=sum(1<<v for i,v in enumerate(vs) if mask>>i&1)
    supports={q for q in range(1<<14) if q&core==global_core and q.bit_count() in (1,3,5)}
    assert len(columns)==len(set(columns)) and set(columns)==supports-known.keys()
    checker=LiteralCubeChecker(rows);local_pairs,outside=checker.coordinates(geometry)
    records=literal_words(local_pairs,mask);certificate=record['result']['certificate']
    residual=[0]*len(columns);rhs=0;rebuilt={}
    for point,side,multiplier in certificate['terms']:
        assert type(point) is int and 0<=point<1024 and side in (-1,1)
        assert type(multiplier) is int and multiplier>0
        if point not in rebuilt:
            low,high=bounds(point,domains,checker,records)
            x=sum(1<<v for i,v in enumerate(outside) if point>>i&1)
            parity={q:(-1 if (q&x).bit_count()%2 else 1) for q in supports}
            constant=sum(known[q]*parity[q] for q in supports&known.keys())
            constant+=sum(parity[q] for q in columns if q.bit_count()==1)
            coefficients=[parity[q]*(-1 if q.bit_count()==3 else 1) for q in columns]
            rebuilt[point]=(low-constant,high-constant,coefficients)
        low,high,coefficients=rebuilt[point]
        rhs+=multiplier*(high if side==1 else -low)
        for i,value in enumerate(coefficients):residual[i]+=multiplier*side*value
    for column,side,multiplier in certificate['box_terms']:
        assert type(column) is int and 0<=column<len(columns) and side in (-1,1)
        assert type(multiplier) is int and multiplier>0
        residual[column]+=multiplier*side
        if side==1:rhs+=multiplier
    assert all(value==0 for value in residual) and rhs<0 and rhs==certificate['integer_rhs']
    return dict(integer_rhs=rhs,projection_variables=len(columns),envelope_rows_rebuilt=len(rebuilt),
                core_truth_words_enumerated=65536,numerical_solver_imported=False)


def run(output):
    b=Bindings();data=b.read(H/'two-positive-pair-embeddings.json',
                            '0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')
    pilot=b.read(H/'core-fourier-envelope-lp-pilot.json',
                 '6124d9ff4afdb9c8d30b8fc06fe553a0b758f0fa884089e4f6afe401c44829d1')
    record=pilot['records'][8]
    assert record['geometry']==82 and record['core_mask']==0
    authority_path=H/'two-positive-complete-companions-g82-independent-manifest.json'
    authority=b.read(authority_path,'2e50bd7f269340513702559b4e57c21e1c9542425d9db00974059748b98d05e0')
    assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_TWO_POSITIVE_SECOND_PAIR_FRONTIER'
    key=[0,1026,0];assert key in authority['remaining_keys']
    source=b.read(authority['source']['path'],authority['source']['sha256'])
    matches=[r for r in source['records'] if [r['first_row'],r['second_pair'],r['second_row']]==key];assert len(matches)==1
    parent=b.read(matches[0]['proof']['path'],matches[0]['proof']['sha256'])
    assert record['initial_known']==parent['proof']['known'] and record['input_domains']==parent['proof']['domains']
    checked=verify(data['domain']['rows'],data['representatives'][82],record)
    for name in ('verify_core_fourier_envelope_certificate.py','test_verify_core_fourier_envelope_certificate.py',
                 'verify_four_cube_pair_domains.py','core-fourier-envelope-lemma.md'):
        b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_SCOPED_CORE_FOURIER_ENVELOPE_EXCLUSION',
                global_status='UNRESOLVED',geometry=82,parent_key=key,core_mask=0,
                conditional_parent_excluded=True,whole_positive_geometry_excluded=False,
                parent_authority=b.bind(authority_path),verification=checked,
                source_binding_checks=b.checks,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],verification=checked)))


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
