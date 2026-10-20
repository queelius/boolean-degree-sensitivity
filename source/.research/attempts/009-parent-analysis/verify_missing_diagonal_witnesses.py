"""Solver-free scalar verification of necessary missing-diagonal projections."""
from argparse import ArgumentParser
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_four_cube_pair_domains import LiteralCubeChecker
from verify_core_fourier_envelope_certificate import literal_words

H=Path(__file__).resolve().parent


def verify_spectrum(n,apices,spectrum,allowed):
    assert len(apices)==len(set(apices))==2 and all(0<=i<n for i in apices)
    spectrum=[tuple(p) for p in spectrum];assert spectrum==sorted(set(spectrum)) and len(dict(spectrum))==len(spectrum)
    assert len(allowed)==1<<n and all(v==sorted(set(v)) and v for v in allowed)
    assert all(type(q) is int and 0<q<1<<n and type(k) is int and ((q.bit_count()==1 and k==-1) or (q.bit_count()==3 and k in (-2,1))) for q,k in spectrum)
    assert sum(k==-2 for q,k in spectrum)==1 and sum(k for q,k in spectrum)==4
    values=[]
    for x,possibilities in enumerate(allowed):
        value=sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in spectrum)
        assert value in possibilities and (value-4*(1-sum((x>>v)&1 for v in apices)))%8==0
        values.append(value)
    norm=sum(k*k for q,k in spectrum);assert sum(v*v for v in values)==(1<<n)*norm
    return dict(inputs_checked=1<<n,exact_degree=max(q.bit_count() for q,k in spectrum),negative_count=1,
        coefficient_norm=norm,linear_count=sum(q.bit_count()==1 for q,k in spectrum),positive_count=sum(k==1 for q,k in spectrum),
        value_set=sorted(set(values)),solver_imported=False)


class ScalarValues:
    def __init__(self,rows,g):
        self.rows=rows;self.g=g;self.pairs,self.outside=LiteralCubeChecker.coordinates(g)

    @lru_cache(None)
    def allowed(self,chosen,mask):
        assert len(chosen)==len(self.pairs)
        groups=defaultdict(list)
        for word,delta,derivatives,value in literal_words(self.pairs,mask):groups[delta,derivatives].append((word,value))
        polynomials=[]
        for i in chosen:
            row=self.rows[i];polynomials.append([(q,1) for q in row['unit_faces']]+[(13,2),(14,2)]+[(1<<v,k) for v,k in enumerate(row['linear_numerators']) if k])
        result=[]
        for point in range(1024):
            x=(point&3)|((point>>2)<<4);derivatives=[]
            for polynomial in polynomials:
                numerator=-sum(k*(-1 if (q&x).bit_count()%2 else 1) for q,k in polynomial);assert numerator%8==0;derivatives.append(numerator//8)
            delta=1-(point&1)-((point>>1)&1);ones=zeros=0
            for y in range(16):
                weight=point.bit_count()+y.bit_count()
                if weight in (0,12,13):zeros|=1<<y
                elif weight in (1,2,14):ones|=1<<y
            values=sorted({value for word,value in groups[delta,tuple(derivatives)] if word&ones==ones and word&zeros==0});assert values;result.append(values)
        return result


def run(output):
    b=Bindings();path=H/'missing-diagonal-control-embeddings-cycle107.json';source=b.read(path)
    authority=b.read(source['authority']['path'],source['authority']['sha256']);assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_SCOPED_FOUR_CYCLE_FIXED_FRONTIER'
    g=source['geometry'];assert g==authority['geometry'];control=b.read(source['control']['path'],source['control']['sha256'])['control']
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];checker=ScalarValues(rows,g);results=[]
    accepted={(r['third_row'],r['fourth_row']):r for r in authority['records']}
    for record in source['records']:
        if record['first_map'] is None:continue
        assert record['parent']==accepted[record['third_row'],record['fourth_row']]['propagation'];parent=read_certificate(b,record['parent'])
        image=record['first_map'];assert len(image)==control['n'] and len(set(image))==len(image) and all(type(v) is int and 0<=v<10 for v in image)
        assert {image[i] for i in control['apices']}=={0,1}
        def move(q):return sum(1<<image[i] for i in range(len(image)) if q>>i&1)
        spectrum=sorted([(move(q),1) for q in control['positive']]+[(move(q),-2) for q in control['negative']]+[(move(q),-1) for q in control['linear']])
        assert [d['pair'] for d in parent['domains']]==g['eligible_pairs'] and all(len(d['rows'])==1 for d in parent['domains'])
        values=checker.allowed(tuple(d['rows'][0] for d in parent['domains']),record['core_mask']);verification=verify_spectrum(10,[0,1],spectrum,values)
        results.append(dict(third_row=record['third_row'],fourth_row=record['fourth_row'],core_mask=record['core_mask'],parent=record['parent'],spectrum=spectrum,verification=verification))
    integer_path=H/'missing-diagonal-integral-pilot-cycle107.json';integer=b.read(integer_path);integer_results=[]
    assert integer['geometry']==g and integer['source']==b.bind(path)
    for record in integer['records']:
        assert record['parent']==accepted[record['third_row'],record['fourth_row']]['propagation']
        if record['status']!='EXACTLY_CHECKED_NECESSARY_CUBIC_PROJECTION_WITNESS':
            assert record['solver_status']=='UNKNOWN' and not record['accepted_exclusion'];continue
        parent=read_certificate(b,record['parent']);values=checker.allowed(tuple(d['rows'][0] for d in parent['domains']),record['core_mask'])
        check=verify_spectrum(10,[0,1],record['spectrum'],values);integer_results.append({**record,'independent_verification':check})
    for name in ('verify_missing_diagonal_witnesses.py','test_verify_missing_diagonal_witnesses.py','verify_core_fourier_envelope_certificate.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_SCOPED_MISSING_DIAGONAL_PROJECTION_WITNESSES',global_status='UNRESOLVED',
        authority=source['authority'],source=b.bind(path),integer_source=b.bind(integer_path),geometry=g,control_witnesses=results,integer_witnesses=integer_results,
        no_function_excluded=True,boolean_function_on14_constructed=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(control_witnesses=len(results),integer_witnesses=len(integer_results))),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
