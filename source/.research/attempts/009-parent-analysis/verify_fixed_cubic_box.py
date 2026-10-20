"""Independent scalar Farkas reader for fixed-negative cubic projections."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_missing_diagonal_witnesses import ScalarValues

H=Path(__file__).resolve().parent


class FixedCubicChecker:
    def __init__(self,rows,g):self.g=g;self.scalar=ScalarValues(rows,g)

    def verify(self,domains,record):
        assert record['result']['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
        assert [d['pair'] for d in domains]==self.g['eligible_pairs'] and all(len(d['rows'])==1 for d in domains)
        mask=record['core_mask'];assert mask.bit_count()==2 and mask not in self.scalar.pairs
        negative=record['negative'];assert negative==sorted(set(negative)) and len(negative)==1
        assert all(type(q) is int and 0<q<1024 and q.bit_count()==3 for q in negative)
        variables=[tuple(v) for v in record['variables']]
        expected={(q,-1) for q in range(1024) if q.bit_count()==1}|{(q,1) for q in range(1024) if q.bit_count()==3 and q not in negative}
        assert set(variables)==expected and len(variables)==len(expected)==129
        assert record['result']['variables']==129 and record['result']['rows']==1024
        values=self.scalar.allowed(tuple(d['rows'][0] for d in domains),mask)
        certificate=record['result']['certificate'];residual=[0]*len(variables);rhs=0;used=set()
        for point,side,multiplier in certificate['terms']:
            assert type(point) is int and 0<=point<1024 and side in (-1,1) and type(multiplier) is int and multiplier>0
            constant=-2*sum(-1 if (q&point).bit_count()%2 else 1 for q in negative);low=values[point][0]-constant;high=values[point][-1]-constant
            rhs+=multiplier*(high if side==1 else -low);used.add(point)
            for i,(q,sign) in enumerate(variables):residual[i]+=side*multiplier*sign*(-1 if (q&point).bit_count()%2 else 1)
        for column,side,multiplier in certificate['box_terms']:
            assert type(column) is int and 0<=column<len(variables) and side in (-1,1) and type(multiplier) is int and multiplier>0
            residual[column]+=side*multiplier
            if side==1:rhs+=multiplier
        assert not any(residual) and rhs<0 and rhs==certificate['integer_rhs']
        return dict(integer_rhs=rhs,variables=len(variables),used_scalar_envelopes=len(used),solver_imported=False)


def run(output):
    b=Bindings();path=H/'fixed-cubic-mask03-N1-batch-cycle107.json';source=b.read(path)
    assert source['status']=='COMPLETE_FIXED_CUBIC_ONE_NEGATIVE_PLACEMENT_SCREEN' and source['stop_reason'] is None
    authority=b.read(source['authority']['path'],source['authority']['sha256']);assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_SCOPED_FOUR_CYCLE_FIXED_FRONTIER'
    g=source['geometry'];assert g==authority['geometry'] and source['core_mask']==3 and source['negative_count']==1
    case=next(r for r in authority['records'] if (r['third_row'],r['fourth_row'])==(source['third_row'],source['fourth_row']));assert case['propagation']==source['parent']
    parent=read_certificate(b,source['parent']);rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];checker=FixedCubicChecker(rows,g)
    expected={q for q in range(1024) if q.bit_count()==3};actual=[r['negative'][0] for r in source['records']]
    assert set(actual)==expected and len(actual)==len(expected)==120
    results=[];remaining=[]
    for record in source['records']:
        detail=read_certificate(b,record['proof']);assert detail['parent']==source['parent'] and detail['core_mask']==record['core_mask']==source['core_mask']
        assert detail['negative']==record['negative'] and detail['result']['status']==record['status']
        excluded=record['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
        check=checker.verify(parent['domains'],detail) if excluded else None
        if not excluded:remaining.append(record['negative'][0])
        results.append({**record,'independently_excluded':excluded,'verification':check})
    pilot=b.read(source['pilot']['path'],source['pilot']['sha256']);assert pilot['parent']==source['parent'];pilot_checks=[]
    for record in pilot['records']:
        detail=read_certificate(b,record['proof']);assert detail['parent']==source['parent'] and detail['core_mask']==record['core_mask'] and detail['negative']==record['negative']
        assert detail['result']['status']==record['status']
        if record['status']=='EXACT_BOX_ROW_LP_CONTRADICTION':pilot_checks.append({**record,'verification':checker.verify(parent['domains'],detail)})
    for name in ('verify_fixed_cubic_box.py','test_verify_fixed_cubic_box.py','verify_missing_diagonal_witnesses.py','fixed-cubic-box-certificate-lemma-cycle107.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_COMPLETE_FIXED_CUBIC_ONE_NEGATIVE_PLACEMENT_SCREEN',global_status='UNRESOLVED',
        source=b.bind(path),authority=source['authority'],geometry=g,parent=source['parent'],third_row=source['third_row'],fourth_row=source['fourth_row'],core_mask=3,
        one_negative_projection_excluded=not remaining,remaining_negative_supports=remaining,records=results,pilot_checks=pilot_checks,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(excluded=120-len(remaining),remaining=len(remaining),one_negative_projection_excluded=not remaining)),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
