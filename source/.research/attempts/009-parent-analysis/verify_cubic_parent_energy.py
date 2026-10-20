"""Independent count certificates for partial-domain cubic parent diagnostics."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from cubic_partial_scalar import PartialScalarValues
from verify_cubic_energy_values import verify_energy
from verify_cubic_singleton_energy_batch import check_energy_coverage

H=Path(__file__).resolve().parent


def remaining_patterns(pending,selected,records):
    lookup={r['index']:r for r in pending};assert len(lookup)==len(pending)
    assert len({r['index'] for r in selected})==len(selected) and all(lookup[r['index']]==r for r in selected)
    check_energy_coverage([r['negative'] for r in selected],records)
    assert [r['index'] for r in records]==[r['index'] for r in selected for q in range(0,11,2)]
    closed={r['index'] for r in selected if all(c['excluded'] for c in records if c['index']==r['index'])}
    return [r for r in pending if r['index'] not in closed]


def run(output):
    b=Bindings();source_path=H/'cubic-parent-energy-pilot-cycle110.json';source=b.read(source_path)
    assert source['status']=='COMPLETE_TWO_FIXED_ROW_CUBIC_ENERGY_PILOT' and source['stop_reason'] is None
    authority=b.read(source['authority']['path'],source['authority']['sha256']);assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_TWO_FIXED_ROW_CUBIC_INTERVAL_COVERS'
    assert source['geometry']==authority['geometry'] and source['core_mask']==authority['core_mask']==3
    assert [(r['first_row'],r['second_row']) for r in source['cases']]==[(r['first_row'],r['second_row']) for r in authority['records']]
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];scalar=PartialScalarValues(rows,source['geometry']);results=[]
    for case,prior in zip(source['cases'],authority['records']):
        assert case['complete'] and case['parent']==prior['parent'];parent=read_certificate(b,case['parent']);values=scalar.allowed(parent['domains'],3);records=[]
        for record in case['records']:
            detail=read_certificate(b,record['proof']);assert detail['parent']==case['parent'] and detail['negative']==record['negative'] and detail['linear_count']==record['linear_count'] and detail['core_mask']==3 and detail['result']['status']==record['status']
            if record['status']=='EXACT_BOX_ROW_LP_CONTRADICTION':records.append({**record,'excluded':True,'verification':verify_energy(detail,values)})
            else:
                assert record['status'] in ('NUMERICALLY_FEASIBLE_BOX_RELAXATION','INCONCLUSIVE_BOX_ROW_LP');records.append({**record,'excluded':False})
        remaining=remaining_patterns(prior['remaining'],case['selected'],records)
        results.append(dict(first_row=case['first_row'],second_row=case['second_row'],parent=case['parent'],records=records,
            remaining=remaining,actual_parent_excluded=not remaining))
        print(json.dumps(dict(first=case['first_row'],second=case['second_row'],remaining=remaining,actual_parent_excluded=not remaining)),flush=True)
    for name in ('verify_cubic_parent_energy.py','test_verify_cubic_parent_energy.py','verify_cubic_energy_values.py','test_verify_cubic_energy_values.py','signed-divisibility-criterion-cycle107.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_TWO_FIXED_ROW_CUBIC_ENERGY_PILOT',global_status='UNRESOLVED',source=b.bind(source_path),
        interval_authority=source['authority'],geometry=source['geometry'],core_mask=3,records=results,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
