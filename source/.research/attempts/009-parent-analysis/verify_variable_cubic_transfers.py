"""Independent raw-row evaluation of interval Farkas transfers."""
from argparse import ArgumentParser
from math import comb
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from conditional_cubic_scalar import ConditionalCubicScalar
from verify_variable_cubic_certificate import rebuild,verify

H=Path(__file__).resolve().parent


def bound_rhs(n,certificate,values,N):
    offset=1+comb(n,3);rhs=0
    for index,side,multiplier in certificate['terms']:
        if index==0:rhs+=side*multiplier*N
        elif index<offset:
            if side==1:rhs+=multiplier
        else:
            x=index-offset;assert 0<=x<1<<n
            rhs+=multiplier*(max(values[x]) if side==1 else -min(values[x]))
    for i,side,multiplier in certificate['box_terms']:
        if side==1:rhs+=multiplier
    return rhs


def run(output):
    b=Bindings();source_path=H/'parent00-coefficient-transfers-cycle115.json';source=b.read(source_path)
    assert source['status']=='PARENT00_SPARSE_COEFFICIENT_CERTIFICATE_TRANSFERS'
    frontier=b.read(source['frontier']['path'],source['frontier']['sha256']);assert frontier['status']=='ACCEPTED_PARENT00_COUPLED_PROJECTION_FRONTIER'
    assert source['geometry']==frontier['geometry'] and source['parent']==frontier['parent']
    accepted=b.read(frontier['coefficient_authority']['path'],frontier['coefficient_authority']['sha256']);allowed_refs={r['proof']['path']:r['proof'] for r in accepted['records']}
    joint=b.read(frontier['joint_authority']['path'],frontier['joint_authority']['sha256']);previous={(r['index'],r['projection_index']):r for r in joint['records']}
    counts=b.read(accepted['actual_counts_authority']['path'],accepted['actual_counts_authority']['sha256']);count_pairs=set()
    for r in counts['actual_missing_diagonal_counts']:
        a,c=r['counts'];count_pairs.update(((a,c),(c,a)))
    certificates=[];points=set()
    for basis in source['basis']:
        assert basis['proof']==allowed_refs[basis['proof']['path']];reference=read_certificate(b,basis['proof']);assert not reference['energy']
        variables,rows=rebuild(10,reference['negative_count'],reference['values'],False);assert variables==reference['variables']
        certificate=reference['result']['certificate'];verify(variables,rows,certificate)
        assert bound_rhs(10,certificate,reference['values'],reference['negative_count'])==certificate['integer_rhs']
        certificates.append(certificate);points.update(i-121 for i,s,m in certificate['terms'] if i>=121)
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];scalar=ConditionalCubicScalar(rows,source['geometry'])
    expected={(r['index'],j) for r in frontier['records'] for j in r['remaining_representatives']}
    assert len(source['records'])==len(expected) and {(r['index'],r['projection_index']) for r in source['records']}==expected
    results=[]
    for record in source['records']:
        key=record['index'],record['projection_index'];detail=read_certificate(b,record['proof']);assert detail['previous']==previous[key]['proof'];old=read_certificate(b,detail['previous'])
        assert detail['geometry']==source['geometry'] and detail['parent']==source['parent'] and (detail['index'],detail['projection_index'])==key
        allowed_counts=sorted(c for a,c in count_pairs if a==len(old['projection']['negative']));assert detail['allowed_negative_counts']==allowed_counts
        pairs=old['proof']['surviving_pairs'];assert len(detail['records'])==len(pairs)==record['row_pairs']
        assert [r['pair_index'] for r in detail['records']]==list(range(len(pairs)))
        B={x:sum(k*(1-2*((q&x).bit_count()%2)) for q,k in old['spectrum']) for x in points};remaining=[];counts_remaining=0
        for attempt in detail['records']:
            j=attempt['pair_index'];assert attempt['row_pair']==pairs[j]
            row_ids=[d['rows'][0] for d in old['input_domains']]
            for slot,row in zip(old['proof']['free_slots'],pairs[j]):row_ids[slot]=row
            polynomials=[scalar.rows.polynomial_values(i) for i in row_ids]
            values={x:scalar.at_signature(x.bit_count(),1-(x&1)-((x>>1)&1),tuple(p[x] for p in polynomials),B[x]) for x in points};assert all(values.values())
            assert [r['negative_count'] for r in attempt['counts']]==allowed_counts;surviving=[]
            for count in attempt['counts']:
                N=count['negative_count'];right_sides=[bound_rhs(10,c,values,N) for c in certificates]
                assert 0<=count['basis']<len(certificates) and right_sides[count['basis']]==count['integer_rhs']==min(right_sides)
                assert count['excluded']==(count['integer_rhs']<0)
                if not count['excluded']:surviving.append(N)
            assert attempt['remaining_negative_counts']==surviving
            if surviving:remaining.append(dict(pair_index=j,row_pair=pairs[j],negative_counts=surviving));counts_remaining+=len(surviving)
        assert len(remaining)==record['remaining_pairs'] and counts_remaining==record['remaining_count_cases'] and len(pairs)*len(allowed_counts)==record['count_cases']
        result=dict(index=key[0],projection_index=key[1],proof=record['proof'],row_pairs=len(pairs),remaining=remaining,remaining_pairs=len(remaining),remaining_count_cases=counts_remaining,projection_excluded=not remaining)
        results.append(result);print(json.dumps({k:v for k,v in result.items() if k not in ('proof','remaining')}),flush=True)
    for name in ('verify_variable_cubic_transfers.py','test_verify_variable_cubic_transfers.py','conditional_cubic_scalar.py','verify_variable_cubic_certificate.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_PARENT00_VARIABLE_CUBIC_CERTIFICATE_TRANSFERS',global_status='UNRESOLVED',source=b.bind(source_path),frontier=source['frontier'],geometry=source['geometry'],parent=source['parent'],records=results,
        independent_basis_cancellation_checks=len(certificates),whole_parent_excluded=False,solver_imported=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(remaining_pairs=sum(r['remaining_pairs'] for r in results),remaining_count_cases=sum(r['remaining_count_cases'] for r in results),closed_projections=sum(r['projection_excluded'] for r in results))),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
