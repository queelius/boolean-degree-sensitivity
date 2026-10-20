"""Translate a verified source functional into an audited target's exact rows.

No numerical optimization runs here. A separate literal target reader must
accept the resulting integer certificate before the frontier may change.
"""
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from time import monotonic
import gc
import json
import resource
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from first_case_spectrum_scope import CaseScope
from core_slice_degree_lp import PatternBlock
from selfdual_core_projection import ProjectedCoefficient
from bounded_core_spectrum_lp import CoefficientTotal,prepare
from primitive_box_rows import primitive_row
from probe_spectrum_functional_mixture import source_functional
from spectrum_dual_functional import compile_functional,simplex_bound
from simplex_row_reconstruction import reconstruct
from transfer_spectrum_row_weights import transfer


def rebuild_model(b,reference):
    source=b.read(reference['path'],reference['sha256']); proof=read_certificate(b,source['proof'])
    ref=source['input_source']; inputs=b.read(ref['path'],ref['sha256'])
    data=read_certificate(b,inputs['proof'])
    assert source['scope']==proof['scope']==data['scope']
    blocks=[]
    for record in data['blocks']:
        ref=record['values']; b.bind(ref['path'],ref['sha256'])
        values=np.load(ref['path'],allow_pickle=False)
        assert list(values.shape)==ref['shape'] and str(values.dtype)==ref['dtype']
        blocks.append(PatternBlock(tuple(record['features']),values))
    coefficients=[ProjectedCoefficient(c['feature'],c['character'],c['support'],tuple(c['values']))
                  for c in data['projected_coefficients']]
    totals=[CoefficientTotal(tuple(t['supports']),t['target']) for t in proof['totals']]
    assert proof['include_moments'] is True
    model=prepare(data['word_pools'],blocks,coefficients,totals=totals,include_moments=True)
    assert model.coefficient_records()==proof['coefficients']
    assert model.base.partition_records()==proof['partitions']
    return model,source,proof,data,coefficients


def run(source_path,target_path,transfer_path,output,memory_mib):
    assert not output.exists(); start=monotonic()
    resource.setrlimit(resource.RLIMIT_AS,(memory_mib<<20,memory_mib<<20)); b=Bindings()
    source_authority=b.read(source_path); target_authority=b.read(target_path)
    assert source_authority['status']==target_authority['status']=='INDEPENDENTLY_VERIFIED_FIRST_CASE_FULL_SPECTRUM_MODEL'
    assert source_authority['exact_certificate_verified'] and source_authority['whole_first_case_excluded']
    assert target_authority['all_original_rows_and_divisors_rebuilt']
    assert target_authority['saved_primitive_matrix_equal_literal_rows']
    source_scope=CaseScope.from_data(source_authority['scope'])
    target_scope=CaseScope.from_data(target_authority['scope'])
    assert source_scope.geometry_index==target_scope.geometry_index
    assert source_scope.to_data()['quotient_authority']==target_scope.to_data()['quotient_authority']
    assert source_scope.first_row!=target_scope.first_row
    proposal=b.read(transfer_path)
    assert proposal['status']=='PROPOSED_COMPLETE_FIRST_CASE_SPECTRUM_TRANSFER'
    assert proposal['exact_authority']==b.bind(source_path)
    transfer_proof=read_certificate(b,proposal['proof'])
    targets=[r for r in transfer_proof['records'] if r['first_row']==target_scope.first_row]
    assert len(targets)==1; proposed_target=targets[0]
    assert proposed_target['after']['bound']['gap']>0
    lifted=source_functional(b,source_path)
    assert lifted.report['scale']==transfer_proof['scale']
    assert lifted.report['row_weights']==transfer_proof['row_weights']
    source_model,_,_,_,_=rebuild_model(b,source_authority['model_source'])
    source_reasons=[row.reason for row in source_model.rows()]
    assert len(source_reasons)==len(lifted.report['row_weights'])
    del source_model; gc.collect()
    print(json.dumps(dict(stage='source_certificate_and_identities_rebuilt',seconds=monotonic()-start)),flush=True)
    model,model_source,proof,data,coefficients=rebuild_model(b,target_authority['model_source'])
    assert data['domain_proof']==proposed_target['domain_proof']
    assert data['geometry']==lifted.coordinates['geometry'] and data['outside']==lifted.coordinates['outside']
    assert sorted((c.feature,c.character,c.support,c.values) for c in coefficients)==lifted.coordinates['coefficient_domains']
    assert proof['totals']==lifted.coordinates['totals']
    rows=list(model.rows()); reasons=[r.reason for r in rows]
    moved=transfer(source_reasons,lifted.report['row_weights'],reasons,proof['partitions'])
    target_functional=compile_functional(rows,model.variable_count,moved)
    assert target_functional.rhs==lifted.functional.rhs
    base=model.base.basis.base; costs=[[] for _ in data['word_pools']]
    for j,variable in enumerate(model.variables[:base.word_variable_count]):
        cost=lifted.functional.word_score(variable['outside_point'],variable['features'])
        assert cost==target_functional.coefficients[j]
        costs[variable['outside_point']].append(cost)
    for block,(record,offset) in enumerate(zip(base.blocks,base.block_offsets)):
        values=lifted.functional.pattern_scores(block,record.values,record.features)
        assert list(map(int,values))==list(target_functional.coefficients[offset:offset+len(values)])
        costs.append(values)
    flag_lookup=dict(zip(lifted.flag_keys,lifted.flags)); flags=[]
    for j,variable in enumerate(model.variables):
        if variable['kind']!='full_spectral_flag': continue
        key=(variable['feature'],variable['character'],variable['support'],tuple(variable['values']))
        assert flag_lookup[key]==target_functional.coefficients[j]
        flags.append(target_functional.coefficients[j])
    assert len(flags)==len(flag_lookup)
    bound=simplex_bound(costs,flags,target_functional.rhs)
    assert bound['gap']==proposed_target['after']['bound']['gap'] and bound['contradiction']
    matrix=read_certificate(b,proof['primitive_matrix']); primitive=[]
    assert len(rows)==len(matrix)==len(proof['divisors'])
    for row,divisor,saved in zip(rows,proof['divisors'],matrix):
        normalized,actual=primitive_row(row)
        assert actual==divisor
        assert saved==[normalized.lower,normalized.upper,[[j,a] for j,a in sorted(normalized.terms)]]
        primitive.append(normalized)
    del matrix,rows; gc.collect()
    primitive_weights=[weight*divisor for weight,divisor in zip(moved,proof['divisors'])]
    groups=defaultdict(list)
    for j,variable in enumerate(model.variables):
        if variable['kind']=='joint_core_value_state':
            groups[(variable['kind'],variable['outside_point'])].append(j)
        elif variable['kind']=='slice_pattern_weight':
            groups[(variable['kind'],variable['block'])].append(j)
        else:
            assert variable['kind']=='full_spectral_flag'
    group_keys=sorted(groups)
    result=reconstruct(primitive,model.variable_count,primitive_weights,[groups[k] for k in group_keys])
    assert result['integer_rhs']==-bound['gap']
    assert result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
    certificate=result['certificate']
    result=dict(status=result['status'],proof_verified=True,certificate=certificate,
        reconstruction={k:v for k,v in result.items() if k!='certificate'},
        numerical_solver_run=False,method='exact_structural_row_transfer_and_simplex_reconstruction')
    proof_path=output.with_suffix('.json.gz')
    write_certificate(proof_path,dict(scope=target_scope.to_data(),model_authority=b.bind(target_path),
        model_source=target_authority['model_source'],primitive_matrix=proof['primitive_matrix'],result=result,
        candidate=None,dual_candidate=None,numerical_report=None,source_authority=b.bind(source_path),
        prior_transfer=b.bind(transfer_path),source_integer_lift_scale=lifted.report['scale'],
        original_target_row_weights=moved,normalization_group_keys=group_keys,
        all_target_columns_match_extended_source_functional=True,extended_bound=bound))
    here=Path(__file__).resolve().parent
    for name in ('certify_transferred_spectrum_functional.py','transfer_spectrum_row_weights.py',
                 'test_transfer_spectrum_row_weights.py','test_transferred_spectrum_certificate.py',
                 'simplex_row_reconstruction.py','test_simplex_row_reconstruction.py',
                 'probe_spectrum_functional_mixture.py','spectrum_dual_functional.py'):
        b.bind(here/name)
    produced=dict(schema_version=1,status='PROPOSED_FIRST_CASE_FULL_SPECTRUM_LP_RUN',
        execution_kind='exact_transfer_of_verified_source_functional',numerical_solver_reexecuted=False,
        global_status='UNRESOLVED',scope=target_scope.to_data(),model_authority=b.bind(target_path),
        model_source=target_authority['model_source'],source_authority=b.bind(source_path),
        prior_transfer=b.bind(transfer_path),proof=b.bind(proof_path),model_inventory=model_source['model_inventory'],
        result_status=result['status'],candidate=None,dual_candidate=None,numerical_report=None,
        whole_first_case_excluded_claim=True,independent_audit='PENDING',whole_geometry_excluded=False,
        actual_boolean_function=False,global_goal_complete=False,
        parameters=dict(memory_mib=memory_mib,source_integer_lift_scale=lifted.report['scale']),
        seconds=monotonic()-start,process_peak_resident_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream:
        json.dump(produced,stream,indent=2); stream.write('\n')
    print(json.dumps(dict(status=result['status'],scope=target_scope.to_data(),integer_rhs=certificate['integer_rhs'],
        row_terms=len(certificate['terms']),box_terms=len(certificate['box_terms']),
        seconds=produced['seconds'],peak_kib=produced['process_peak_resident_kib'])),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__)
    p.add_argument('--source-authority',type=Path,required=True)
    p.add_argument('--target-authority',type=Path,required=True)
    p.add_argument('--transfer',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--memory-mib',type=int,default=4096)
    a=p.parse_args(); run(a.source_authority,a.target_authority,a.transfer,a.output,a.memory_mib)
