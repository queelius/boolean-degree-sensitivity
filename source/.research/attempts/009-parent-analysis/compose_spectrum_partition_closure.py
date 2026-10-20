"""Bind an exact group contradiction to its complete cover and update the frontier."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from merge_first_row_exclusions import merge_rows
from spectrum_partition_closure import validate

H = Path(__file__).resolve().parent


def run(spectrum_path, previous_path, output, frontier_output):
    assert not output.exists() and not frontier_output.exists()
    b = Bindings()
    docs, refs = {}, {}

    def read(name, reference):
        refs[name] = reference
        docs[name] = b.read(reference['path'], reference['sha256'])
        return docs[name]

    spectrum = read('spectrum', b.bind(spectrum_path))
    inputs = read('inputs', spectrum['input_authority'])
    base = read('base', inputs['base_authority'])
    read('zero', inputs['zero_product_authority'])
    read('support', base['support_sum_authority'])
    read('groups', base['product_group_authority'])
    summary = validate(docs, refs)
    previous = b.read(previous_path)
    assert previous['status'] == 'VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER'
    scope = previous['scope']
    assert summary['geometry_index'] == scope['geometry_index']
    assert summary['quotient_authority'] == scope['quotient_authority']
    q = b.read(scope['quotient_authority']['path'], scope['quotient_authority']['sha256'])
    assert q['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and q['complete_actual_cover'] is True
    assert q['geometry_index'] == scope['geometry_index'] and q['marked_pair'] == scope['marked_pair']
    universe = q['selected_row_indices']
    assert sorted(previous['excluded_first_rows'] + previous['remaining_first_rows']) == sorted(universe)
    assert not set(previous['excluded_first_rows']) & set(previous['remaining_first_rows'])
    merged = merge_rows(universe, previous['excluded_first_rows'], [summary['first_row']])
    for name in ('compose_spectrum_partition_closure.py', 'spectrum_partition_closure.py',
                 'test_spectrum_partition_closure.py', 'merge_first_row_exclusions.py'):
        b.bind(H / name)
    accepted = dict(schema_version=1, status='VERIFIED_ASSEMBLY_MATCHED_SPECTRUM_FIRST_CASE_EXCLUSION',
        global_status='UNRESOLVED', **summary, authorities=refs,
        complete_exact_group_cover=True, whole_first_case_excluded=True,
        whole_geometry_excluded=False, actual_boolean_function=False, global_goal_complete=False,
        bookkeeping_replays_mathematics=False,
        files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    with output.open('x') as stream:
        json.dump(accepted, stream, indent=2)
        stream.write('\n')
    frontier = dict(schema_version=1, status='VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER',
        global_status='UNRESOLVED', scope=scope, previous_frontier=b.bind(previous_path),
        conditional_exclusion_authorities=[dict(first_row=summary['first_row'], authority=b.bind(output))],
        total_first_rows=len(universe), excluded_first_rows=merged['excluded'], remaining_first_rows=merged['remaining'],
        newly_excluded_first_rows=merged['newly_excluded'], whole_geometry_excluded=merged['whole_geometry_excluded'],
        global_goal_complete=False, bookkeeping_replays_mathematics=False,
        files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    with frontier_output.open('x') as stream:
        json.dump(frontier, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(geometry=summary['geometry_index'], first_row=summary['first_row'],
        groups=summary['group_count'], exact_integer_rhs=summary['exact_integer_rhs'],
        excluded=len(merged['excluded']), remaining=len(merged['remaining']), newly_excluded=merged['newly_excluded'])), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__)
    p.add_argument('--spectrum', type=Path, required=True)
    p.add_argument('--previous', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--frontier-output', type=Path, required=True)
    a = p.parse_args()
    run(a.spectrum, a.previous, a.output, a.frontier_output)
