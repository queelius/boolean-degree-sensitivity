"""Update a first-row frontier from a complete independently certified case."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from first_case_spectrum_scope import input_scope,CaseScope
from first_case_spectrum_exclusion import validate
from merge_first_row_exclusions import merge_rows

H=Path(__file__).resolve().parent


def run(authority_path,previous_path,output,frontier_output):
    assert not output.exists() and not frontier_output.exists()
    b=Bindings(); authority=b.read(authority_path); previous=b.read(previous_path)
    first=validate(authority,previous); scope=CaseScope.from_data(authority['scope'])
    ref=authority['input_authority']; inputs=b.read(ref['path'],ref['sha256'])
    assert input_scope(inputs)==scope and inputs['source']==authority['input_source']
    ref=authority['model_source']; model=b.read(ref['path'],ref['sha256'])
    assert model['scope']==scope.to_data() and model['input_authority']==authority['input_authority']
    ref=authority['run_source']; executed=b.read(ref['path'],ref['sha256'])
    assert executed['scope']==scope.to_data() and executed['model_source']==authority['model_source']
    ref=previous['scope']['quotient_authority']; quota=b.read(ref['path'],ref['sha256'])
    assert quota['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    assert quota['geometry_index']==scope.geometry_index and quota['marked_pair']==previous['scope']['marked_pair']
    universe=quota['selected_row_indices']
    assert sorted(previous['excluded_first_rows']+previous['remaining_first_rows'])==sorted(universe)
    assert not set(previous['excluded_first_rows'])&set(previous['remaining_first_rows'])
    merged=merge_rows(universe,previous['excluded_first_rows'],[first])
    for name in ('compose_first_case_spectrum_exclusion.py','first_case_spectrum_exclusion.py',
                 'test_first_case_spectrum_exclusion.py','first_case_spectrum_scope.py','merge_first_row_exclusions.py'):
        b.bind(H/name)
    result=dict(schema_version=1,status='VERIFIED_ASSEMBLY_COMPLETE_FIRST_CASE_SPECTRUM_EXCLUSION',global_status='UNRESOLVED',
        scope=scope.to_data(),geometry_index=scope.geometry_index,first_row=first,
        quotient_authority=previous['scope']['quotient_authority'],exact_authority=b.bind(authority_path),
        exact_integer_rhs=authority['exact_integer_rhs'],whole_first_case_excluded=True,
        complete_first_case_necessary_cover=True,whole_geometry_excluded=False,actual_boolean_function=False,
        global_goal_complete=False,bookkeeping_replays_mathematics=False,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with output.open('x') as stream: json.dump(result,stream,indent=2); stream.write('\n')
    frontier=dict(schema_version=1,status='VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER',global_status='UNRESOLVED',
        scope=previous['scope'],previous_frontier=b.bind(previous_path),
        conditional_exclusion_authorities=[dict(first_row=first,authority=b.bind(output))],
        total_first_rows=len(universe),excluded_first_rows=merged['excluded'],remaining_first_rows=merged['remaining'],
        newly_excluded_first_rows=merged['newly_excluded'],whole_geometry_excluded=merged['whole_geometry_excluded'],
        global_goal_complete=False,bookkeeping_replays_mathematics=False,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    with frontier_output.open('x') as stream: json.dump(frontier,stream,indent=2); stream.write('\n')
    print(json.dumps(dict(geometry=scope.geometry_index,first_row=first,exact_integer_rhs=authority['exact_integer_rhs'],
        excluded=len(merged['excluded']),remaining=len(merged['remaining']),newly_excluded=merged['newly_excluded'])),flush=True)


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__); parser.add_argument('--authority',type=Path,required=True)
    parser.add_argument('--previous',type=Path,required=True); parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--frontier-output',type=Path,required=True); a=parser.parse_args()
    run(a.authority,a.previous,a.output,a.frontier_output)
