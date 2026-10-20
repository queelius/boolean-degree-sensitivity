"""Exact scalar screen of the existing canonical catalogs under a safe matching."""
from collections import Counter
from pathlib import Path
from time import monotonic
import json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate, write_certificate

H = Path(__file__).resolve().parent
b = Bindings(); start = monotonic()
authority_path = H/'complete-singleton-stratified-cubic-catalogs-independent-manifest-cycle149.json'
authority = b.read(authority_path)
assert authority['status'] == 'INDEPENDENTLY_VERIFIED_SINGLETON_STRATIFIED_CUBIC_CATALOGS'
assert authority['low_counts'] == list(range(7))
words = np.arange(65536, dtype=np.int64)
truth = ((words[:, None] >> np.arange(16)) & 1).astype(np.int16)
chars4 = np.array([[(-1 if (x & q).bit_count() % 2 else 1) for q in range(16)] for x in range(16)], dtype=np.int16)
sums = (1-2*truth) @ chars4
matched = np.all(sums[:, [7, 11, 13, 14]] == 0, axis=1) & np.isin(sums[:, 15], [-4, 0, 4])
assert int(matched.sum()) == 526
weights4 = np.array([x.bit_count() for x in range(16)])
allowed = {}
pair_masks = [q for q in range(16) if q.bit_count() == 2]
for weight in range(11):
    for delta in (-1, 0, 1):
        valid = matched & (sums[:, 15] == 4*delta)
        total = weight + weights4
        zeros = np.isin(total, [0, 12, 13]); ones = np.isin(total, [1, 2, 14])
        valid &= np.all(truth[:, zeros] == 0, axis=1) & np.all(truth[:, ones] == 1, axis=1)
        sets = [sorted(set(map(int, sums[valid, q]))) for q in pair_masks]
        assert all(s == sets[0] for s in sets)
        allowed[weight, delta] = sets[0]
points = np.arange(1024)
characters = np.array([[(-1 if (q & x).bit_count() % 2 else 1) for x in range(1024)] for q in range(1024)], dtype=np.int16)
lookup = np.zeros((1024, 65), dtype=bool)
for x in range(1024):
    values = allowed[x.bit_count(), 1-(x & 1)-((x >> 1) & 1)]
    assert values
    lookup[x, np.array(values)+32] = True
output = H/'matched-core-scalar-catalog-probe-cycle262.json'
directory = output.with_suffix(''); assert not output.exists() and not directory.exists(); directory.mkdir()
reports = []; histogram = Counter()
for entry in authority['records']:
    source = read_certificate(b, entry['proof']); negative = source['negative']
    assert negative == entry['negative'] and len(source['candidates']) == entry['candidates']
    fixed = -2*characters[negative].sum(axis=0)
    failures = []; retained = []
    for i, candidate in enumerate(source['candidates']):
        values = fixed + characters[candidate['positive']].sum(axis=0) - characters[candidate['linear']].sum(axis=0)
        # Coefficient sums give this generous bound independently of the screen.
        good = (values >= -32) & (values <= 32)
        good &= lookup[points, np.clip(values+32, 0, 64)]
        bad = np.flatnonzero(~good)
        witness = int(bad[0]) if len(bad) else None
        failures.append(witness)
        if witness is None: retained.append(i); histogram[len(negative), entry['low_count']] += 1
    detail = dict(source=entry['proof'], low_count=entry['low_count'], index=entry['index'], negative=negative,
                  input_candidates=len(failures), rejected_at_point=failures, retained_indices=retained)
    path = directory/f"L{entry['low_count']}-r{entry['index']:03d}.json.gz"; write_certificate(path, detail)
    report = {k: detail[k] for k in ('low_count', 'index', 'negative', 'input_candidates')}
    report.update(retained=len(retained), proof=b.bind(path)); reports.append(report)
    print(json.dumps(report), flush=True)
for name in ('matched_core_scalar_catalog_probe_cycle262.py', 'matching_core_word_lemma_cycle224.md',
             'matched_core_catalog_transfer_cycle229.md'): b.bind(H/name)
result = dict(status='PROPOSED_MATCHED_CORE_CANONICAL_SCALAR_CATALOG_FILTER', global_status='UNRESOLVED',
              authority=b.bind(authority_path), words_checked=65536, matched_words=526,
              scalar_value_sets=[dict(weight=w, delta=d, values=v) for (w, d), v in sorted(allowed.items())],
              records=reports, input_candidates=sum(r['input_candidates'] for r in reports),
              retained_candidates=sum(r['retained'] for r in reports),
              retained_histogram=[dict(negative_count=n, low_count=l, count=c) for (n, l), c in sorted(histogram.items())],
              actual_geometry_cover_supplied=False, geometry_exclusions=0, seconds=monotonic()-start,
              files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
output.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ('input_candidates', 'retained_candidates', 'retained_histogram', 'seconds')}), flush=True)
