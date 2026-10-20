"""Add the proved singleton-core norm restriction as a finite count relation."""
from argparse import ArgumentParser
from itertools import product
from pathlib import Path
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate, write_certificate

H = Path(__file__).resolve().parent


def run(authority_path, output):
    b = Bindings(); authority = b.read(authority_path)
    assert authority['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and authority['complete_actual_cover'] is True
    instance = read_certificate(b, authority['instance']); geometry = authority['geometry']
    core = geometry['positive_doubles'][0] & geometry['positive_doubles'][1]
    vertices = [v for v in range(14) if core >> v & 1]
    negative_counts = [sum(n & core == 1 << v for n in geometry['negative_supports']) for v in vertices]
    caps = [16 if count == 0 else 20 for count in negative_counts]
    directory = output.with_suffix(''); assert not directory.exists() and not output.exists(); directory.mkdir()
    columns = []; reports = []; frequencies = []
    for j, component in enumerate(instance['components']):
        values = np.load(component['values']['path'], allow_pickle=False)
        if j == authority['component_index']: values = values[authority['selected_row_indices']]
        numerator = 16-values[:, [1 << i for i in range(10)]].sum(axis=1)
        assert np.all(numerator % 4 == 0)
        counts = numerator//4
        assert np.all((counts >= 0) & (counts <= 10) & (counts % 2 == 0))
        path = directory/f'counts-{j}.npy'; np.save(path, counts.astype(np.int8), allow_pickle=False)
        choices, multiplicities = np.unique(counts, return_counts=True)
        columns.append(tuple(map(int, choices))); frequencies.append(dict(zip(map(int, choices), map(int, multiplicities))))
        reports.append(dict(component_index=j, counts=b.bind(path), candidates=len(counts), values=list(columns[-1])))
    pairs = instance['core_pair_order']; all_tuples = list(product(*columns))
    allowed = [list(q) for q in all_tuples if all(sum(c for p, c in zip(pairs, q) if p >> i & 1) <= caps[i] for i in range(4))]
    def mass(tuples):
        total = 0
        for row in tuples:
            count = 1
            for j, v in enumerate(row): count *= frequencies[j][v]
            total += count
        return total
    proof = dict(base_authority=b.bind(authority_path), geometry_index=authority['geometry_index'],
                 core_pair_order=pairs, negative_singleton_core_counts=negative_counts,
                 incident_linear_count_caps=caps, columns=reports, allowed_count_tuples=allowed,
                 cartesian_count_tuples=len(all_tuples), cartesian_domain_mass=mass(all_tuples), retained_domain_mass=mass(allowed))
    path = directory/'refinement.json.gz'; write_certificate(path, proof)
    control_path = H/'matched-core-linear-count-lemma-controls-cycle283.json'; control = b.read(control_path)
    assert control['status'] == 'EXACT_MATCHED_CORE_LINEAR_COUNT_LEMMA_CONTROLS'
    for name in ('build_matched_count_refinement.py', 'matched_core_linear_count_bound_cycle283.md'): b.bind(H/name)
    result = dict(status='PROPOSED_MATCHED_COMPONENT_LINEAR_COUNT_REFINEMENT', global_status='UNRESOLVED',
                  base_authority=b.bind(authority_path), geometry_index=authority['geometry_index'], proof=b.bind(path),
                  lemma_controls=b.bind(control_path), allowed_count_tuples=len(allowed),
                  geometry_exclusions=0, files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(geometry=authority['geometry_index'], allowed_count_tuples=len(allowed),
                         cartesian_count_tuples=len(all_tuples), caps=caps,
                         retained_domain_mass=proof['retained_domain_mass'], cartesian_domain_mass=proof['cartesian_domain_mass'])), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--authority', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); run(a.authority, a.output)
