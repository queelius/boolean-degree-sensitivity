"""Independent literal finite-value/Parseval certificate reconstruction."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from verify_missing_diagonal_witnesses import ScalarValues

H=Path(__file__).resolve().parent


class EnergyChecker:
    def __init__(self,rows,g):self.g=g;self.scalar=ScalarValues(rows,g)

    def verify(self,domains,record):
        assert record['result']['status']=='EXACT_BOX_ROW_LP_CONTRADICTION' and record['core_mask']==3
        assert [d['pair'] for d in domains]==self.g['eligible_pairs'] and all(len(d['rows'])==1 for d in domains)
        negative=record['negative'];assert len(negative)==1 and type(negative[0]) is int and 0<negative[0]<1024 and negative[0].bit_count()==3
        Q=record['linear_count'];assert type(Q) is int and Q in range(0,11,2)
        metadata=record['variables'];assert len(metadata)>=129;local=[]
        for v in metadata[:129]:
            assert v['kind']=='coefficient' and type(v['support']) is int and v['support']&15==3
            q=v['support']>>4;sign=-1 if v['role']=='cubic_negative' else 1
            assert v['role'] in ('cubic_negative','quintic_positive');local.append((q,sign))
        expected={(q,-1) for q in range(1024) if q.bit_count()==1}|{(q,1) for q in range(1024) if q.bit_count()==3 and q not in negative}
        assert set(local)==expected and len(set(local))==129
        values=self.scalar.allowed(tuple(d['rows'][0] for d in domains),3)
        assert values[0]==[4] and all(values[x]==sorted(-v for v in values[x^1023]) for x in range(512))
        def polynomial(x):
            constant=-2*sum(-1 if (q&x).bit_count()%2 else 1 for q in negative)
            terms={i:sign*(-1 if (q&x).bit_count()%2 else 1) for i,(q,sign) in enumerate(local)}
            return constant,terms
        rows=[]
        for x in range(1024):
            constant,terms=polynomial(x);rows.append((values[x][0]-constant,values[x][-1]-constant,terms))
        expected_states=[];fixed=0;energy={i:-512 for i in range(129)}
        for point in range(512):
            squares={v*v for v in values[point]}
            if len(squares)==1:fixed+=next(iter(squares));continue
            columns=list(range(129+len(expected_states),129+len(expected_states)+len(values[point])))
            expected_states.extend(dict(kind='generic_fourier_value_state',core_mask=3,outside_point=point,value=v) for v in values[point])
            rows.append((1,1,{i:1 for i in columns}));constant,terms=polynomial(point)
            terms.update({i:-v for i,v in zip(columns,values[point]) if v});rows.append((-constant,-constant,terms))
            energy.update({i:v*v for i,v in zip(columns,values[point]) if v})
        assert metadata[129:]==expected_states
        target=512*4-fixed;rows.append((target,target,energy))
        rows.append((Q,Q,{i:1 for i,(q,sign) in enumerate(local) if sign==-1}))
        rows.append((Q+6,Q+6,{i:1 for i,(q,sign) in enumerate(local) if sign==1}))
        assert record['result']['variables']==len(metadata) and record['result']['rows']==len(rows)
        certificate=record['result']['certificate'];residual=[0]*len(metadata);rhs=0;used=set()
        for index,side,multiplier in certificate['terms']:
            assert type(index) is int and 0<=index<len(rows) and side in (-1,1) and type(multiplier) is int and multiplier>0
            low,high,terms=rows[index];rhs+=multiplier*(high if side==1 else -low);used.add(index)
            for i,k in terms.items():residual[i]+=side*multiplier*k
        for column,side,multiplier in certificate['box_terms']:
            assert type(column) is int and 0<=column<len(metadata) and side in (-1,1) and type(multiplier) is int and multiplier>0
            residual[column]+=side*multiplier
            if side==1:rhs+=multiplier
        assert not any(residual) and rhs<0 and rhs==certificate['integer_rhs']
        return dict(integer_rhs=rhs,variables=len(metadata),literal_rows=len(rows),used_rows=len(used),solver_imported=False)


def run(output):
    b=Bindings();path=H/'fixed-cubic-energy-pilot-cycle107.json';source=b.read(path)
    assert source['status']=='COMPLETE_SCOPED_FIXED_CUBIC_ENERGY_COUNT_PILOT'
    authority=b.read(source['authority']['path'],source['authority']['sha256']);assert authority['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_FIXED_CUBIC_ONE_NEGATIVE_PLACEMENT_SCREEN'
    assert source['geometry']==authority['geometry'] and source['parent']==authority['parent'] and source['core_mask']==authority['core_mask']==3
    expected=[([n],q) for n in authority['remaining_negative_supports'] for q in range(0,11,2)]
    assert [(r['negative'],r['linear_count']) for r in source['records']]==expected
    parent=read_certificate(b,source['parent']);rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];checker=EnergyChecker(rows,source['geometry']);results=[]
    for record in source['records']:
        detail=read_certificate(b,record['proof']);assert detail['parent']==source['parent'] and detail['core_mask']==3
        assert detail['negative']==record['negative'] and detail['linear_count']==record['linear_count']
        assert detail['result']['status']==record['status']=='EXACT_BOX_ROW_LP_CONTRADICTION';check=checker.verify(parent['domains'],detail)
        results.append({**record,'independently_excluded':True,'verification':check})
    for name in ('verify_fixed_cubic_energy.py','test_verify_fixed_cubic_energy.py','signed-divisibility-criterion-cycle107.md','test_signed_divisibility_criterion.py','fixed-cubic-energy-certificate-proof-cycle107.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_CONDITIONAL_CUBIC_ONE_NEGATIVE_EXCLUSION',global_status='UNRESOLVED',source=b.bind(path),
        placement_authority=source['authority'],geometry=source['geometry'],parent=source['parent'],core_mask=3,third_row=authority['third_row'],fourth_row=authority['fourth_row'],
        records=results,one_negative_projection_excluded=True,negative_minimum_in_actual_exact_cycle_scope=2,fixed_quartet_excluded=False,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(certificates=len(results),one_negative_projection_excluded=True,global_status='UNRESOLVED')),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
