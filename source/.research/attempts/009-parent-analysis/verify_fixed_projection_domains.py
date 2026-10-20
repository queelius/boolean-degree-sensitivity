"""Scalar, literal-Boolean replay of fixed-projection domain certificates."""
from argparse import ArgumentParser
from functools import lru_cache
from pathlib import Path
from collections import Counter
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_four_cube_pair_domains import LiteralCubeChecker
from verify_core_fourier_envelope_certificate import literal_words

H=Path(__file__).resolve().parent


@lru_cache(None)
def literal_conditioned(pairs,weight,delta,mask,value):
    result=set()
    for word,d,ts,v in literal_words(pairs,mask):
        if d!=delta or v!=value:continue
        if any((weight+y.bit_count() in (0,12,13) and word>>y&1) or
               (weight+y.bit_count() in (1,2,14) and not word>>y&1) for y in range(16)):continue
        result.add(ts)
    return result


class FixedProjectionReader:
    def __init__(self,rows,g):
        self.checker=LiteralCubeChecker(rows);self.g=g;self.pairs,self.outside=self.checker.coordinates(g)

    def reductions(self,live,spectrum,mask,point):
        assert type(point) is int and 0<=point<1024
        value=sum(k*(-1 if (q&point).bit_count()%2 else 1) for q,k in spectrum)
        values=self.checker.at(point);available=[{values[r] for r in domain} for domain in live]
        allowed=literal_conditioned(self.pairs,point.bit_count(),1-(point&1)-((point>>1)&1),mask,value)
        possible=[ts for ts in allowed if all(v in a for v,a in zip(ts,available))]
        supports=[{ts[j] for ts in possible} for j in range(len(live))]
        return [{r for r in domain if values[r] in supports[j]} for j,domain in enumerate(live)],value

    def replay(self,domains,spectrum,mask,proof):
        assert [d['pair'] for d in domains]==self.g['eligible_pairs']
        assert all(d['rows'] and d['rows']==sorted(set(d['rows'])) for d in domains)
        assert len({q for q,k in spectrum})==len(spectrum) and all(type(q) is int and 0<=q<1024 and type(k) is int for q,k in spectrum)
        live=[set(d['rows']) for d in domains]
        for step in proof['steps']:
            updated,value=self.reductions(live,spectrum,mask,step['point'])
            cuts=[dict(pair=d['pair'],remaining_rows=len(updated[j])) for j,d in enumerate(domains) if updated[j]!=live[j]]
            assert cuts and cuts==step['cuts'] and all(updated);live=updated
        if proof['status']=='EXACT_FIXED_PROJECTION_CUBE_CONTRADICTION':
            updated,value=self.reductions(live,spectrum,mask,proof['contradiction_point'])
            assert not any(updated) and value==proof['projection_value'];return dict(excluded=True)
        assert proof['status']=='NECESSARY_FIXED_PROJECTION_CUBE_FIXED_POINT'
        expected=[dict(pair=d['pair'],rows=sorted(live[j])) for j,d in enumerate(domains)];assert proof['domains']==expected and all(live)
        # The trace proves these remaining domains, without relying on whether
        # the producer's iteration actually reached its strongest fixed point.
        return dict(excluded=False,domains=expected,fixed_point_maximality_claimed=False)


def run(output):
    b=Bindings();source_path=H/'parent00-fixed-projection-pilot-cycle113.json';source=b.read(source_path)
    assert source['status']=='PARENT00_FIXED_CUBIC_PROJECTION_PROPAGATION_PILOT'
    frontier=b.read(source['frontier']['path'],source['frontier']['sha256']);assert frontier['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER'
    assert source['geometry']==frontier['geometry'] and source['parent']==frontier['parent'] and source['core_mask']==3
    parent=read_certificate(b,source['parent']);rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows']
    reader=FixedProjectionReader(rows,source['geometry']);expected={};catalogs={}
    for c in frontier['complete_projection_catalogs']:
        authority=b.read(c['authority']['path'],c['authority']['sha256']);record=next(r for r in authority['records'] if r['index']==c['index'])
        assert len(record['survivors'])==c['survivors'];catalogs[c['index']]=c['authority']
        for j,projection in enumerate(record['survivors']):expected[c['index'],j]=projection
    assert len(source['records'])==len(expected) and {(r['index'],r['projection_index']) for r in source['records']}==set(expected)
    results=[]
    for record in source['records']:
        key=record['index'],record['projection_index'];projection=expected[key];detail=read_certificate(b,record['proof'])
        assert (detail['index'],detail['projection_index'])==key and detail['projection']==projection and detail['catalog']==catalogs[key[0]]
        assert detail['parent']==source['parent'] and detail['geometry']==source['geometry'] and detail['input_domains']==parent['domains'] and detail['core_mask']==3
        spectrum=sorted([[q,1] for q in projection['positive']]+[[q,-1] for q in projection['linear']]+[[q,-2] for q in projection['negative']]);assert detail['spectrum']==spectrum
        assert detail['proof']['status']==record['status'] and len(detail['proof']['steps'])==record['steps']
        verified=reader.replay(parent['domains'],spectrum,3,detail['proof'])
        result=dict(index=key[0],projection_index=key[1],proof=record['proof'],excluded=verified['excluded'])
        if not verified['excluded']:
            result['domain_sizes']=[len(d['rows']) for d in verified['domains']];assert result['domain_sizes']==record['domain_sizes']
        results.append(result)
    summaries=[]
    for index in sorted(catalogs):
        subset=[r for r in results if r['index']==index]
        summary=dict(index=index,projections=len(subset),excluded=sum(r['excluded'] for r in subset),remaining=sum(not r['excluded'] for r in subset))
        summary['negative_position_excluded']=not summary['remaining'];summaries.append(summary);print(json.dumps(summary),flush=True)
    for name in ('verify_fixed_projection_domains.py','test_verify_fixed_projection_domains.py','verify_core_fourier_envelope_certificate.py','verify_four_cube_pair_domains.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_PARENT00_FIXED_PROJECTION_PROPAGATION',global_status='UNRESOLVED',source=b.bind(source_path),frontier=source['frontier'],geometry=source['geometry'],parent=source['parent'],core_mask=3,
        records=results,summaries=summaries,whole_parent_excluded=False,boolean_function_on14_constructed=False,solver_imported=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
