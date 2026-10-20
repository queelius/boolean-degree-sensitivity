"""Exact finite controls for the analytic matched-core linear-count bound."""
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from verify_core_fourier_envelope_certificate import literal_words

H = Path(__file__).resolve().parent; b = Bindings(); pairs = [3, 5, 6, 9, 10, 12]
counts = {}
for weight, delta in ((0, 1), (1, 1), (1, 0)):
    selected = 0
    for word, d, ts, empty in literal_words((3, 12), 0):
        if d != delta: continue
        if any((weight+x.bit_count() in (0, 12, 13) and (word >> x) & 1) or
               (weight+x.bit_count() in (1, 2, 14) and not ((word >> x) & 1)) for x in range(16)): continue
        coefficients = {q: sum((1-2*((word >> x) & 1))*(-1 if (q & x).bit_count() % 2 else 1) for x in range(16)) for q in range(16)}
        for i in range(4):
            assert coefficients[1 << i] in ({0} if weight == 0 else {0, -8})
            if weight == 1:
                assert coefficients[1 << i]+sum(coefficients[q] for q in pairs if q >> i & 1)+coefficients[15] == 0
        selected += 1
    counts[str((weight, delta))] = selected
assert list(counts.values()) == [1, 15, 7]
for value in (-16, -8, 0, 8, 16):
    assert value*value-8*value >= 0
    assert (value*value == 8*value) == (value in (0, 8))
for a in (1, 2):
    for ell in (0, 1):
        energy = a*a+3*a+4*ell
        assert energy < 8*a or (energy == 8*a and ell > 0)
spectral = {0: 2, 15: -2}
for i in range(4): spectral[(1 << i) | 16] = -1; spectral[(15 ^ (1 << i)) | 16] = 1
values = []
for x in range(32):
    z = [1-2*((x >> i) & 1) for i in range(5)]
    direct = (1-z[0]*z[1]*z[2]*z[3])*(2-z[4]*sum(z[:4]))
    expanded = sum(k*(-1 if (q & x).bit_count() % 2 else 1) for q, k in spectral.items())
    assert direct == expanded and direct in (0, 8); values.append(direct)
assert values[0] == 0 and all(values[1 << i] == 0 for i in range(5))
assert sum(values) == 64 and sum(v*v for v in values) == 512
for name in ('matched_core_linear_count_checks_cycle283.py', 'matched_core_linear_count_bound_cycle283.md',
             'matching_core_word_lemma_cycle224.md', 'matched_core_catalog_transfer_cycle229.md'): b.bind(H/name)
result = dict(status='EXACT_MATCHED_CORE_LINEAR_COUNT_LEMMA_CONTROLS', global_status='UNRESOLVED',
              guarded_core_word_counts=counts, negative_quartic_positive_control_inputs=32,
              no_negative_quartic_minimum_ell=2, geometry_exclusions=0,
              files=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
output = H/'matched-core-linear-count-lemma-controls-cycle283.json'; assert not output.exists(); output.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ('status', 'guarded_core_word_counts', 'negative_quartic_positive_control_inputs')}))
