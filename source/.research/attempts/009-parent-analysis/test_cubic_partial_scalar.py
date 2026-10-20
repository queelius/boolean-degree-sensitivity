from pathlib import Path
import json,gzip
import pytest
from cubic_partial_scalar import PartialScalarValues
from verify_missing_diagonal_witnesses import ScalarValues


def fixture():
    h=Path(__file__).resolve().parent;f=json.loads((h/'four-cycle-a0056-b0056-fixed-frontier-independent-manifest.json').read_text())
    rows=json.loads((h/'two-positive-pair-embeddings.json').read_text())['domain']['rows']
    p=json.loads(gzip.decompress(Path(f['records'][0]['propagation']['path']).read_bytes()));return rows,f['geometry'],p['domains']


def test_fixed_domains_agree_and_union_domains_preserve_every_fixed_word():
    rows,g,domains=fixture();reader=PartialScalarValues(rows,g);fixed=reader.allowed(domains,3)
    assert fixed==ScalarValues(rows,g).allowed(tuple(d['rows'][0] for d in domains),3)
    enlarged=[{**d,'rows':sorted(set(d['rows']+[181]))} for d in domains]
    broad=reader.allowed(enlarged,3);assert all(set(v)<=set(w) for v,w in zip(fixed,broad))
    with pytest.raises(AssertionError):reader.allowed(list(reversed(domains)),3)
