"""Solver-free reconstruction of variable-negative cubic coefficient certificates."""
from argparse import ArgumentParser
from itertools import combinations
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from conditional_cubic_scalar import ConditionalCubicScalar

H=Path(__file__).resolve().parent


def rebuild(n,N,values,energy):
    triples=[sum(1<<i for i in t) for t in combinations(range(n),3)];variables=[];coefficient_supports=[]
    for kind,supports,sign in [('negative_linear_flag',[1<<i for i in range(n)],-1),('positive_triangle_flag',triples,1),('negative_double_triangle_flag',triples,-2)]:
        for q in supports:
            variables.append(dict(kind=kind,support=q,point=-1,value=0));coefficient_supports.append((q,sign))
    t=len(triples);rows=[([(i,1) for i in range(n+t,n+2*t)],N,N)]
    rows.extend(([(n+j,1),(n+t+j,1)],0,1) for j in range(t));expressions=[]
    for x,allowed in enumerate(values):
        terms=[(i,sign*(1-2*((q&x).bit_count()%2))) for i,(q,sign) in enumerate(coefficient_supports)];expressions.append(terms)
        rows.append((terms,min(allowed),max(allowed)))
    if energy:
        energy_terms=[];fixed=0;half=1<<(n-1)
        for x,allowed in enumerate(values[:half]):
            squares={v*v for v in allowed}
            if len(squares)==1:fixed+=next(iter(squares));continue
            columns=[]
            for v in allowed:
                i=len(variables);columns.append(i);variables.append(dict(kind='finite_value_weight',support=0,point=x,value=v));energy_terms.append((i,v*v))
            rows.append(([(i,1) for i in columns],1,1));rows.append((expressions[x]+[(i,-v) for i,v in zip(columns,allowed)],0,0))
        energy_terms.extend((i,-half) for i in range(n+t));rhs=half*4*N-fixed;rows.append((energy_terms,rhs,rhs))
    return variables,rows


def verify(variables,rows,certificate):
    residual=[0]*len(variables);rhs=0
    for index,side,multiplier in certificate['terms']:
        assert type(index) is int and 0<=index<len(rows) and side in (-1,1) and type(multiplier) is int and multiplier>0
        terms,low,high=rows[index];rhs+=multiplier*(high if side==1 else -low)
        for i,k in terms:residual[i]+=multiplier*side*k
    for i,side,multiplier in certificate['box_terms']:
        assert type(i) is int and 0<=i<len(variables) and side in (-1,1) and type(multiplier) is int and multiplier>0
        residual[i]+=side*multiplier
        if side==1:rhs+=multiplier
    assert not any(residual) and rhs<0 and rhs==certificate['integer_rhs'];return rhs


def run(output):
    b=Bindings();source_path=H/'parent00-second-coefficient-pilot-cycle114.json';source=b.read(source_path)
    assert source['status']=='PARENT00_CONDITIONAL_SECOND_CUBIC_COEFFICIENT_PILOT'
    authority=b.read(source['authority']['path'],source['authority']['sha256']);assert authority['status']=='INDEPENDENTLY_VERIFIED_PARENT00_TWO_ROW_CATALOGS_AND_SYMMETRY'
    counts=b.read(source['actual_counts_authority']['path'],source['actual_counts_authority']['sha256']);assert counts['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_CUBIC_TWO_NEGATIVE_COVER_WITH_ACTUAL_FILTER'
    possible={tuple(r['counts']) for r in counts['actual_missing_diagonal_counts']};assert possible=={(1,1),(1,2)}
    selected=sorted((r for r in authority['records'] if r['surviving_pairs']),key=lambda r:(r['surviving_pairs'],r['index'],r['projection_index']))[:2]
    expected={(r['index'],r['projection_index'],j):r for r in selected for j in range(r['surviving_pairs'])}
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];scalar=ConditionalCubicScalar(rows,source['geometry']);results=[];seen=set()
    for record in source['records']:
        key=record['index'],record['projection_index'],record['pair_index'];assert key in expected;seen.add(key)
        detail=read_certificate(b,record['proof']);assert detail['previous']==expected[key]['proof'];old=read_certificate(b,detail['previous'])
        assert detail['geometry']==authority['geometry']==source['geometry'] and detail['parent']==authority['parent']==source['parent']
        assert detail['row_pair']==old['proof']['surviving_pairs'][key[2]] and len(old['projection']['negative'])==2 and detail['negative_count']==1
        assert detail['fixed_core_mask']==3 and detail['target_core_mask']==12
        row_ids=[d['rows'][0] for d in old['input_domains']]
        for slot,row in zip(old['proof']['free_slots'],detail['row_pair']):row_ids[slot]=row
        values=scalar.allowed(row_ids,old['spectrum']);assert detail['values']==values
        variables,inequalities=rebuild(10,1,values,detail['energy']);assert variables==detail['variables'] and detail['energy']==record['energy']
        result=detail['result'];assert result['status']==record['status'];assert result['variables']==len(variables) and result['rows']==len(inequalities)
        assert result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
        rhs=verify(variables,inequalities,result['certificate']);results.append(dict(index=key[0],projection_index=key[1],pair_index=key[2],proof=record['proof'],energy=detail['energy'],integer_rhs=rhs))
    assert seen==set(expected)
    for name in ('conditional_cubic_scalar.py','verify_variable_cubic_certificate.py','test_verify_variable_cubic_certificate.py'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_CONDITIONAL_SECOND_CUBIC_COEFFICIENT_EXCLUSIONS',global_status='UNRESOLVED',source=b.bind(source_path),authority=source['authority'],actual_counts_authority=source['actual_counts_authority'],
        geometry=source['geometry'],parent=source['parent'],records=results,closed_projection_representatives=[[r['index'],r['projection_index']] for r in selected],
        whole_parent_excluded=False,solver_imported=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(certificates=len(results),closed_projections=result['closed_projection_representatives'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
