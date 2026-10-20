"""Audit new Farkas transfers against an exact surviving pair/count cover."""
from argparse import ArgumentParser
from pathlib import Path
from math import comb
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from conditional_cubic_scalar import ConditionalCubicScalar
from verify_variable_cubic_certificate import rebuild,verify
from verify_variable_cubic_transfers import bound_rhs

H=Path(__file__).resolve().parent


def validate_input_cover(previous,detail):
    expected={r['pair_index']:r for r in previous['remaining']};assert len(expected)==len(previous['remaining'])==previous['remaining_pairs']
    assert len(detail['records'])==len(expected) and {r['pair_index'] for r in detail['records']}==set(expected)
    for r in detail['records']:
        old=expected[r['pair_index']]
        assert r['row_pair']==old['row_pair'] and [c['negative_count'] for c in r['counts']]==old['negative_counts']
    return expected


def run(source_path,output):
    b=Bindings();source=b.read(source_path);assert source['status']=='PARENT00_INCREMENTAL_CUBIC_COEFFICIENT_TRANSFERS'
    frontier=b.read(source['frontier']['path'],source['frontier']['sha256']);assert frontier['status']=='ACCEPTED_PARENT00_COUPLED_PROJECTION_FRONTIER' and source['previous_authority']==frontier['pair_authority']
    previous=b.read(source['previous_authority']['path'],source['previous_authority']['sha256'])
    assert previous['status'] in ('INDEPENDENTLY_VERIFIED_PARENT00_VARIABLE_CUBIC_CERTIFICATE_TRANSFERS','INDEPENDENTLY_VERIFIED_INCREMENTAL_CUBIC_COEFFICIENT_TRANSFERS')
    authority=b.read(source['certificate_authority']['path'],source['certificate_authority']['sha256']);assert authority['status']=='INDEPENDENTLY_VERIFIED_SAMPLED_VARIABLE_CUBIC_CERTIFICATES'
    assert authority['frontier']==source['frontier'] and authority['authority']==source['previous_authority']
    assert source['geometry']==frontier['geometry']==authority['geometry'] and source['parent']==frontier['parent']==authority['parent']
    accepted={r['proof']['path']:r['proof'] for r in authority['records'] if r['excluded'] and not r['energy']};certificates=[];points=set();offset=1+comb(10,3)
    for basis in source['basis']:
        assert basis['proof']==accepted[basis['proof']['path']];reference=read_certificate(b,basis['proof']);assert not reference['energy']
        variables,rows=rebuild(10,reference['negative_count'],reference['values'],False);assert variables==reference['variables'];certificate=reference['result']['certificate'];verify(variables,rows,certificate)
        assert bound_rhs(10,certificate,reference['values'],reference['negative_count'])==certificate['integer_rhs']
        certificates.append(certificate);points.update(i-offset for i,s,m in certificate['terms'] if i>=offset)
    assert certificates
    expected={(r['index'],r['projection_index']):r for r in previous['records'] if r['remaining_pairs']}
    assert len(source['records'])==len(expected) and {(r['index'],r['projection_index']) for r in source['records']}==set(expected)
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];scalar=ConditionalCubicScalar(rows,source['geometry']);results=[]
    for record in source['records']:
        key=record['index'],record['projection_index'];prior=expected[key];detail=read_certificate(b,record['proof']);assert detail['case_authority']==prior['proof']
        prior_detail=read_certificate(b,prior['proof']);assert detail['previous']==prior_detail['previous'];old=read_certificate(b,detail['previous'])
        assert detail['geometry']==source['geometry'] and detail['parent']==source['parent'] and (detail['index'],detail['projection_index'])==key
        validate_input_cover(prior,detail);assert len(detail['records'])==record['row_pairs']
        B={x:sum(k*(1-2*((q&x).bit_count()%2)) for q,k in old['spectrum']) for x in points};remaining=[];checked_counts=0;remaining_counts=0
        for attempt in detail['records']:
            j=attempt['pair_index'];assert attempt['row_pair']==old['proof']['surviving_pairs'][j];row_ids=[d['rows'][0] for d in old['input_domains']]
            for slot,row in zip(old['proof']['free_slots'],attempt['row_pair']):row_ids[slot]=row
            polynomials=[scalar.rows.polynomial_values(i) for i in row_ids]
            values={x:scalar.at_signature(x.bit_count(),1-(x&1)-((x>>1)&1),tuple(p[x] for p in polynomials),B[x]) for x in points};assert all(values.values());surviving=[]
            for count in attempt['counts']:
                N=count['negative_count'];rhs=[bound_rhs(10,c,values,N) for c in certificates];checked_counts+=1
                assert 0<=count['basis']<len(certificates) and rhs[count['basis']]==count['integer_rhs']==min(rhs) and count['excluded']==(count['integer_rhs']<0)
                if not count['excluded']:surviving.append(N)
            assert attempt['remaining_negative_counts']==surviving
            if surviving:remaining.append(dict(pair_index=j,row_pair=attempt['row_pair'],negative_counts=surviving));remaining_counts+=len(surviving)
        assert len(remaining)==record['remaining_pairs'] and checked_counts==record['count_cases'] and remaining_counts==record['remaining_count_cases']
        result=dict(index=key[0],projection_index=key[1],proof=record['proof'],row_pairs=len(detail['records']),remaining=remaining,remaining_pairs=len(remaining),remaining_count_cases=remaining_counts,projection_excluded=not remaining)
        results.append(result);print(json.dumps({k:v for k,v in result.items() if k not in ('proof','remaining')}),flush=True)
    for name in ('verify_incremental_cubic_transfers.py','test_verify_incremental_cubic_transfers.py','verify_variable_cubic_transfers.py','conditional_cubic_scalar.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_INCREMENTAL_CUBIC_COEFFICIENT_TRANSFERS',global_status='UNRESOLVED',source=b.bind(source_path),frontier=source['frontier'],geometry=source['geometry'],parent=source['parent'],
        records=results,independent_basis_cancellation_checks=len(certificates),whole_parent_excluded=False,solver_imported=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(remaining_pairs=sum(r['remaining_pairs'] for r in results),remaining_count_cases=sum(r['remaining_count_cases'] for r in results),closed_projections=sum(r['projection_excluded'] for r in results))),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.source,a.output)
