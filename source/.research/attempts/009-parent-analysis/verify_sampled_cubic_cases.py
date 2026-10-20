"""Independent coefficient-certificate audit with explicit surviving-case coverage."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from conditional_cubic_scalar import ConditionalCubicScalar
from verify_variable_cubic_certificate import rebuild,verify

H=Path(__file__).resolve().parent


def run(source_path,output):
    b=Bindings();source=b.read(source_path);assert source['status']=='SAMPLED_VARIABLE_CUBIC_COEFFICIENT_CASES'
    frontier=b.read(source['frontier']['path'],source['frontier']['sha256']);authority=b.read(source['authority']['path'],source['authority']['sha256'])
    assert frontier['status']=='ACCEPTED_PARENT00_COUPLED_PROJECTION_FRONTIER' and source['authority']==frontier['pair_authority']
    assert authority['status'] in ('INDEPENDENTLY_VERIFIED_PARENT00_VARIABLE_CUBIC_CERTIFICATE_TRANSFERS','INDEPENDENTLY_VERIFIED_INCREMENTAL_CUBIC_COEFFICIENT_TRANSFERS')
    assert source['geometry']==frontier['geometry'] and source['parent']==frontier['parent']
    limit=source['parameters']['limit'];assert type(limit) is int and limit>0 and source['parameters']['seconds']>0
    selected=sorted((r for r in authority['records'] if r['remaining_pairs']),key=lambda r:(r['remaining_count_cases'],r['index'],r['projection_index']))[:limit];expected={}
    for r in selected:
        c=min(r['remaining'],key=lambda c:c['pair_index']);expected[r['index'],r['projection_index'],c['pair_index'],min(c['negative_counts'])]=(r,c)
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];scalar=ConditionalCubicScalar(rows,source['geometry']);results=[];seen={}
    for record in source['records']:
        key=record['index'],record['projection_index'],record['pair_index'],record['negative_count'];assert key in expected;seen.setdefault(key,[]).append(record);parent_case,chosen=expected[key]
        detail=read_certificate(b,record['proof']);assert detail['case_authority']==parent_case['proof'];previous=read_certificate(b,parent_case['proof']);assert detail['previous']==previous['previous'];old=read_certificate(b,detail['previous'])
        assert detail['geometry']==source['geometry'] and detail['parent']==source['parent'] and detail['row_pair']==chosen['row_pair']==old['proof']['surviving_pairs'][key[2]]
        assert detail['negative_count']==key[3] and detail['fixed_core_mask']==3 and detail['target_core_mask']==12 and detail['energy']==record['energy']
        row_ids=[d['rows'][0] for d in old['input_domains']]
        for slot,row in zip(old['proof']['free_slots'],detail['row_pair']):row_ids[slot]=row
        values=scalar.allowed(row_ids,old['spectrum']);assert detail['values']==values
        variables,inequalities=rebuild(10,key[3],values,detail['energy']);assert variables==detail['variables'];result=detail['result']
        assert result['status']==record['status'] and result['variables']==len(variables) and result['rows']==len(inequalities)
        checked=dict(index=key[0],projection_index=key[1],pair_index=key[2],negative_count=key[3],proof=record['proof'],energy=detail['energy'],excluded=False,status=result['status'])
        if result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION':checked.update(excluded=True,integer_rhs=verify(variables,inequalities,result['certificate']))
        else:assert result['status'] in ('NUMERICALLY_FEASIBLE_BOX_RELAXATION','INCONCLUSIVE_BOX_ROW_LP')
        results.append(checked)
    assert set(seen)==set(expected)
    for records in seen.values():
        if len(records)==1:assert not records[0]['energy'] and records[0]['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
        else:assert len(records)==2 and [r['energy'] for r in records]==[False,True] and records[0]['status']!='EXACT_BOX_ROW_LP_CONTRADICTION'
    for name in ('verify_sampled_cubic_cases.py','verify_variable_cubic_certificate.py','test_verify_variable_cubic_certificate.py','conditional_cubic_scalar.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_SAMPLED_VARIABLE_CUBIC_CERTIFICATES',global_status='UNRESOLVED',source=b.bind(source_path),frontier=source['frontier'],authority=source['authority'],
        geometry=source['geometry'],parent=source['parent'],records=results,whole_projection_exclusion_claimed=False,whole_parent_excluded=False,solver_imported=False,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(attempts=len(results),exact_certificates=sum(r['excluded'] for r in results))),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.source,a.output)
