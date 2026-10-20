"""Independent literal-word and butterfly-transform audit of the scalar screen."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate

H = Path(__file__).resolve().parent


def walsh(coefficients):
    values = np.array(coefficients, dtype=np.int64, copy=True)
    assert values.ndim == 2
    count, size = values.shape
    assert size > 0 and size & (size-1) == 0
    step = 1
    while step < size:
        blocks = values.reshape(count, size//(2*step), 2, step)
        left = blocks[:, :, 0, :].copy(); right = blocks[:, :, 1, :].copy()
        blocks[:, :, 0, :] = left+right; blocks[:, :, 1, :] = left-right
        step *= 2
    return values


def check_filter(values, allowed):
    assert values.ndim == 2 and values.shape[1] == len(allowed)
    good = np.ones(values.shape, dtype=bool)
    for x, options in enumerate(allowed): good[:, x] = np.isin(values[:, x], sorted(options))
    failures = []; retained = []
    for i, row in enumerate(good):
        bad = np.flatnonzero(~row)
        failures.append(int(bad[0]) if len(bad) else None)
        if not len(bad): retained.append(i)
    return failures, retained


def literal_sets():
    result = {(w, d): set() for w in range(11) for d in (-1, 0, 1)}; matched = 0
    for word in range(65536):
        signs = [1-2*((word >> x) & 1) for x in range(16)]
        def character(q): return sum(s*(-1 if (q & x).bit_count() % 2 else 1) for x, s in enumerate(signs))
        if any(character(q) for q in (7, 11, 13, 14)): continue
        fourth = character(15)
        if fourth not in (-4, 0, 4): continue
        matched += 1; value = character(3)
        for weight in range(11):
            if any((weight+x.bit_count() in (0, 12, 13) and (word >> x) & 1) or
                   (weight+x.bit_count() in (1, 2, 14) and not ((word >> x) & 1)) for x in range(16)): continue
            result[weight, fourth//4].add(value)
    assert matched == 526
    return result


def run(source_path, output):
    assert not output.exists(); start = monotonic(); b = Bindings()
    source = b.read(source_path)
    assert source['status'] == 'PROPOSED_MATCHED_CORE_CANONICAL_SCALAR_CATALOG_FILTER'
    assert source['actual_geometry_cover_supplied'] is False and source['geometry_exclusions'] == 0
    authority = b.read(source['authority']['path'], source['authority']['sha256'])
    assert authority['status'] == 'INDEPENDENTLY_VERIFIED_SINGLETON_STRATIFIED_CUBIC_CATALOGS'
    values = literal_sets()
    assert source['scalar_value_sets'] == [dict(weight=w, delta=d, values=sorted(v)) for (w, d), v in sorted(values.items())]
    allowed = [values[x.bit_count(), 1-(x & 1)-((x >> 1) & 1)] for x in range(1024)]
    catalog = {(r['low_count'], r['index']): r for r in authority['records']}
    assert len(catalog) == len(authority['records'])
    assert len(source['records']) == len(catalog) and {(r['low_count'], r['index']) for r in source['records']} == set(catalog)
    reports = []; evaluations = 0
    for report in source['records']:
        key = report['low_count'], report['index']; entry = catalog[key]
        proof = read_certificate(b, report['proof']); original = read_certificate(b, entry['proof'])
        assert proof['source'] == entry['proof'] and proof['negative'] == entry['negative'] == original['negative']
        assert (proof['low_count'], proof['index']) == key
        candidates = original['candidates']; failures = []; retained = []
        assert len(candidates) == proof['input_candidates'] == report['input_candidates'] == entry['candidates']
        for offset in range(0, len(candidates), 512):
            batch = candidates[offset:offset+512]; coefficients = np.zeros((len(batch), 1024), dtype=np.int64)
            coefficients[:, original['negative']] = -2
            for i, candidate in enumerate(batch):
                positive = candidate['positive']; linear = candidate['linear']
                assert len(set(positive)) == len(positive) and len(set(linear)) == len(linear)
                assert all(q.bit_count() == 3 for q in positive) and all(q.bit_count() == 1 for q in linear)
                assert not set(positive) & set(original['negative'])
                coefficients[i, positive] = 1; coefficients[i, linear] = -1
            rejected, live = check_filter(walsh(coefficients), allowed)
            failures.extend(rejected); retained.extend(offset+i for i in live); evaluations += len(batch)*1024
        assert failures == proof['rejected_at_point'] and retained == proof['retained_indices']
        assert len(retained) == report['retained']
        reports.append(dict(low_count=key[0], index=key[1], negative=entry['negative'], source=entry['proof'],
                            filter_proof=report['proof'], input_candidates=len(candidates), retained_indices=retained))
    assert sum(r['input_candidates'] for r in reports) == source['input_candidates']
    assert sum(len(r['retained_indices']) for r in reports) == source['retained_candidates']
    for name in ('verify_matched_core_scalar_filter.py', 'test_verify_matched_core_scalar_filter.py'): b.bind(H/name)
    result = dict(status='INDEPENDENTLY_VERIFIED_MATCHED_CORE_CANONICAL_SCALAR_CATALOG_FILTER', global_status='UNRESOLVED',
                  source=b.bind(source_path), catalog_authority=source['authority'], records=reports,
                  scalar_value_sets=source['scalar_value_sets'], input_candidates=source['input_candidates'],
                  retained_candidates=source['retained_candidates'], complete_evaluations=evaluations,
                  producer_imported=False, producer_sparse_evaluator_used=False,
                  actual_geometry_cover_supplied=False, geometry_exclusions=0, seconds=monotonic()-start,
                  files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('input_candidates', 'retained_candidates', 'complete_evaluations', 'seconds')}), flush=True)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__); p.add_argument('--source', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); run(a.source, a.output)
