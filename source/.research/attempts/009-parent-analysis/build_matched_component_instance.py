"""Assemble a proposed six-component finite instance from checked scalar catalogs."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate, write_certificate
from fixed_projection_cube_domains import projection_values
from vectorized_input_image import input_image
from core_fourier_envelope import core_words

H = Path(__file__).resolve().parent


def run(geometry_index, output):
    start = monotonic(); b = Bindings(); directory = output.with_suffix('')
    assert not output.exists() and not directory.exists(); directory.mkdir()
    plan_path = H/'matched-core-joint-probe-cycle264.json'; plan = b.read(plan_path)
    assert plan['status'] == 'EXACT_MATCHED_CORE_JOINT_IDENTITIES_AND_EXPLORATORY_COMPONENT_COUNTS'
    scope = next(r for r in plan['records'] if r['geometry'] == geometry_index)
    scalar = b.read(plan['scalar_authority']['path'], plan['scalar_authority']['sha256'])
    assert scalar['status'] == 'INDEPENDENTLY_VERIFIED_MATCHED_CORE_CANONICAL_SCALAR_CATALOG_FILTER'
    data = b.read(H/'two-positive-pair-embeddings.json', '0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')
    geometry = data['representatives'][geometry_index]; pair_order = plan['core_pair_order']
    catalog = {(r['low_count'], r['index']): r for r in scalar['records']}
    source_cache = {}; value_cache = {}; components = []; safe_values = None
    missing = {r['local_core_pair']: r for r in scope['components']}
    for pair in pair_order:
        if pair in missing:
            original = missing[pair]; blocks = []; branches = []; offset = 0
            for branch in original['branches']:
                key = len(branch['low_coordinates']), branch['degree_index']; entry = catalog[key]
                if key not in source_cache: source_cache[key] = read_certificate(b, entry['source'])
                if key not in value_cache:
                    src = source_cache[key]; values = []
                    for index in entry['retained_indices']:
                        c = src['candidates'][index]
                        spectrum = [(q, 1) for q in c['positive']]+[(q, -1) for q in c['linear']]+[(q, -2) for q in src['negative']]
                        values.append(projection_values(spectrum))
                    value_cache[key] = np.asarray(values, dtype=np.int8).reshape(len(values), 1024)
                canonical = value_cache[key]; assert len(canonical) == branch['candidates']
                image = input_image(branch['map'])
                blocks.append(canonical[:, image])
                branches.append(dict(low_coordinates=branch['low_coordinates'], degree_index=branch['degree_index'],
                                     map=branch['map'], source=entry['source'], canonical_indices=entry['retained_indices'],
                                     start=offset, stop=offset+len(canonical)))
                offset += len(canonical)
            values = np.concatenate(blocks, axis=0)
            assert len(values) == original['candidates']
            metadata = dict(kind='catalog_component', local_core_pair=pair, core_pair=original['core_pair'],
                            negative=original['negative'], branches=branches)
        else:
            if safe_values is None:
                all_values = []
                for row in data['domain']['rows']:
                    assert row['linear_numerators'][2:4] == [0, 0] and all(q & 12 == 0 for q in row['unit_faces'])
                    linear = row['linear_numerators'][:2]+row['linear_numerators'][4:]
                    spectrum = [(1 << i, k) for i, k in enumerate(linear) if k]
                    spectrum += [((q & 3) | ((q >> 4) << 2), 1) for q in row['unit_faces']]
                    all_values.append(projection_values(spectrum))
                safe_values = np.asarray(all_values, dtype=np.int8)
            values = safe_values
            metadata = dict(kind='safe_pair_row', local_core_pair=pair, row_count=len(values))
        assert values.shape[1] == 1024 and np.all((values >= -16) & (values <= 16))
        path = directory/f'pair-{pair:02d}.npy'; np.save(path, values, allow_pickle=False)
        components.append(dict(**metadata, candidates=len(values), values=b.bind(path)))
    words, truth, deltas, ts, sums = core_words((3, 12)); assert len(words) == 526
    relation_types = []
    for weight in range(11):
        for delta in (-1, 0, 1):
            keep = deltas == delta
            for x in range(16):
                if weight+x.bit_count() in (0, 12, 13): keep &= truth[:, x] == 0
                elif weight+x.bit_count() in (1, 2, 14): keep &= truth[:, x] == 1
            tuples = sorted(set(tuple(map(int, r)) for r in sums[keep][:, pair_order]))
            relation_types.append(dict(weight=weight, delta=delta, tuples=[list(r) for r in tuples]))
    detail = dict(geometry_index=geometry_index, geometry=geometry, outside=scope['outside'], core_pair_order=pair_order,
                  components=components, relation_types=relation_types)
    proof_path = directory/'instance.json.gz'; write_certificate(proof_path, detail)
    for name in ('build_matched_component_instance.py', 'fixed_projection_cube_domains.py', 'vectorized_input_image.py',
                 'test_vectorized_input_image.py', 'matched_core_catalog_transfer_cycle229.md',
                 'matched_core_joint_constraints_cycle264.md'): b.bind(H/name)
    result = dict(status='PROPOSED_COMPLETE_MATCHED_CORE_COMPONENT_INSTANCE', global_status='UNRESOLVED',
                  geometry_index=geometry_index, plan=b.bind(plan_path), scalar_authority=plan['scalar_authority'],
                  proof=b.bind(proof_path), domain_sizes=[r['candidates'] for r in components],
                  actual_boolean_function=False, necessary_components_only=True, seconds=monotonic()-start,
                  files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('geometry_index', 'domain_sizes', 'seconds')}), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--geometry', type=int, required=True); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); run(a.geometry, a.output)
