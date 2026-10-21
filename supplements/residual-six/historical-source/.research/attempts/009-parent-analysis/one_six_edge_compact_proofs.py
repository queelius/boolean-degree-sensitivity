"""Discard unused deductions and export literal, constant-independent proofs."""
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

from exact_binary_row_propagation import interval, replay
from one_six_edge_interval_proofs import instance

HERE = Path(__file__).resolve().parent


def supporting_variables(row, values, override=None):
    low, high = interval(row, values, override)
    use_lower = low > row.upper
    assert use_lower or high < row.lower
    required = []
    for variable, coefficient in row.terms:
        if variable not in values or (override is not None and variable == override[0]):
            continue
        value = values[variable]
        # Retain only assignments that tighten the relevant interval end.
        needed = ((coefficient > 0 and value == 1) or (coefficient < 0 and value == 0))
        if needed == use_lower:
            required.append(variable)
    return required


def compact(rows, certificate):
    assert certificate['status'] == 'EXACT_INTERVAL_CONTRADICTION'
    values, indices, dependencies = {}, {}, []
    for index, step in enumerate(certificate['steps']):
        required = supporting_variables(rows[step['row']], values,
                                        (step['variable'], 1-step['value']))
        dependencies.append({indices[variable] for variable in required})
        indices[step['variable']] = index
        values[step['variable']] = step['value']
    required = supporting_variables(rows[certificate['contradiction_row']], values)
    selected = {indices[variable] for variable in required}
    stack = list(selected)
    while stack:
        index = stack.pop()
        for dependency in dependencies[index] - selected:
            selected.add(dependency)
            stack.append(dependency)
    retained = [certificate['steps'][index] for index in sorted(selected)]
    originals = sorted({step['row'] for step in retained} | {certificate['contradiction_row']})
    mapping = {old: new for new, old in enumerate(originals)}
    new_rows = [rows[index] for index in originals]
    proof = dict(status='EXACT_INTERVAL_CONTRADICTION',
                 steps=[dict(variable=step['variable'], value=step['value'], row=mapping[step['row']])
                        for step in retained],
                 contradiction_row=mapping[certificate['contradiction_row']],
                 original_row_indices=originals)
    replay(new_rows, proof)
    return new_rows, proof


def main():
    catalog_path = HERE / 'one-six-edge-vertex-links.json'
    source = HERE / 'one-six-edge-interval-proofs.json'
    catalog = json.loads(catalog_path.read_text())
    previous = json.loads(source.read_text())
    result = dict(status='THREE_EXACT_CONSTANT_INDEPENDENT_CONTRADICTIONS', global_status='UNRESOLVED',
                  scope='Only literal rows used by the proof are retained. No global f-vector row occurs; the same contradictions apply to all constants for which the structural reduction is valid (c<=3).',
                  sources=[dict(path=str(path), sha256=sha256(path.read_bytes()).hexdigest())
                           for path in (catalog_path, source, Path(__file__),
                                        HERE / 'exact_binary_row_propagation.py',
                                        HERE / 'one_six_edge_interval_proofs.py',
                                        HERE / 'one_six_edge_complex.py', HERE / 'negative_free_complex.py')], cases=[])
    for link in catalog['targets']:
        data = instance(link, 1)
        old = next(case for case in previous['cases'] if case['link_order'] == link['order'] and case['constant'] == 1)
        rows, proof = compact(data.rows, old)
        assert all(row.reason != 'face_count' for row in rows)
        proof.update(link_order=link['order'], link_index=link['index'],
                     endpoint_link=link, rows=[asdict(row) for row in rows])
        result['cases'].append(proof)
        print(json.dumps(dict(order=link['order'], deductions=len(proof['steps']), rows=len(rows),
                             reasons=sorted({row.reason for row in rows}))), flush=True)
    (HERE / 'one-six-edge-compact-proofs.json').write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    main()
